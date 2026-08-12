#!/usr/bin/env python3
"""
LLM-Driven Document Updates

Architecture (see README.md for full rationale):
  1. Split the source document into paragraphs, each assigned a stable ID (P1, P2, ...).
  2. Ask the LLM (one call) to translate the natural-language changes into a list of
     structured, paragraph-level edit operations (replace / delete / insert_after),
     rather than asking it to rewrite the whole document.
  3. Deterministically validate every edit (does the paragraph_id exist? is the action
     well-formed? do two edits collide on the same paragraph?) BEFORE applying anything.
  4. Apply only the edits that pass validation, using plain string operations (no LLM
     involved in the actual text mutation). Reject/flag the rest instead of silently
     applying or hard-failing the whole batch.
  5. Emit the updated document AND a machine-readable report describing what was applied,
     what was rejected, and why -- so an unattended batch pipeline has an audit trail.
"""

import argparse
import json
import os
import re
import sys
import time
import urllib.request
import urllib.error

OPENAI_URL = "https://api.openai.com/v1/chat/completions"
DEFAULT_MODEL = "gpt-4o"

# ---------------------------------------------------------------------------
# Paragraph splitting / reassembly
# ---------------------------------------------------------------------------

def split_paragraphs(doc: str):
    doc = doc.replace("\r\n", "\n").strip("\n")
    raw_paragraphs = re.split(r"\n\s*\n", doc)
    paragraphs = []
    for i, text in enumerate(raw_paragraphs, start=1):
        text = text.strip("\n")
        if text.strip() == "":
            continue
        paragraphs.append({"id": f"P{i}", "text": text})
    return paragraphs


def render_numbered_document(paragraphs):
    lines = []
    for p in paragraphs:
        lines.append(f"[{p['id']}]\n{p['text']}")
    return "\n\n".join(lines)


def reassemble(paragraphs):
    return "\n\n".join(p["text"] for p in paragraphs if p.get("text", "").strip() != "")


# ---------------------------------------------------------------------------
# LLM call
# ---------------------------------------------------------------------------

EDIT_SCHEMA = {
    "name": "document_edits",
    "strict": True,
    "schema": {
        "type": "object",
        "properties": {
            "edits": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "change_index": {"type": "integer"},
                        "paragraph_id": {"type": "string"},
                        "action": {
                            "type": "string",
                            "enum": ["replace", "delete", "insert_after"],
                        },
                        "new_text": {"type": "string"},
                        "reasoning": {"type": "string"},
                    },
                    "required": [
                        "change_index",
                        "paragraph_id",
                        "action",
                        "new_text",
                        "reasoning",
                    ],
                    "additionalProperties": False,
                },
            },
            "unresolved_changes": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "change_index": {"type": "integer"},
                        "reason": {"type": "string"},
                    },
                    "required": ["change_index", "reason"],
                    "additionalProperties": False,
                },
            },
        },
        "required": ["edits", "unresolved_changes"],
        "additionalProperties": False,
    },
}

SYSTEM_PROMPT = """You are an expert document editor operating inside an automated pipeline. \
You will be given a document broken into numbered paragraphs, each tagged like [P3], and a \
numbered list of requested changes (0-indexed).

Your job is to translate the requested changes into a list of precise, paragraph-level edit \
operations. Do NOT rewrite the whole document. Only touch paragraphs that a change actually \
requires.

Rules:
- action "replace": paragraph_id is an existing paragraph id; new_text is the COMPLETE replacement \
text for that paragraph (preserve its formatting style: heading markers, bullet/number markers, \
table row syntax, etc., unless the change requires altering that formatting).
- action "delete": paragraph_id is an existing paragraph id to remove entirely; new_text must be "".
- action "insert_after": paragraph_id is the id AFTER which to insert a new paragraph (use "P0" to \
insert before the very first paragraph); new_text is the new paragraph's full text.
- Every edit must reference the change_index (0-based, matching the input changes list) it serves. \
One change may require multiple edits (e.g. a tone change across many paragraphs, or a pricing \
change touching several rows). One paragraph should not be targeted by more than one edit -- if a \
single paragraph needs multiple things done, combine them into one replace edit with the full \
final text.
- If a change cannot be located in the document, doesn't apply, or is too ambiguous to execute \
safely, do NOT invent an edit for it. Instead add it to unresolved_changes with a clear reason.
- Broad/global changes (e.g. "make the tone more formal throughout") are NOT too ambiguous -- they \
are expected. Execute them by enumerating one replace edit per paragraph that needs adjustment. Do \
not send a broad change to unresolved_changes just because it touches many paragraphs; only do so \
if you genuinely cannot determine what to change.
- If removing content leaves its section heading with no remaining body text before the next \
heading (or the end of the document), also delete that now-empty heading's paragraph as part of the \
same change, so no orphaned heading is left behind.
- Never fabricate facts, numbers, or claims that are not implied by the change instruction or the \
existing document text.
- Output ONLY the structured edits object. Do not include commentary outside the schema.
"""


def build_user_prompt(paragraphs, changes):
    numbered_doc = render_numbered_document(paragraphs)
    changes_block = "\n".join(f"{i}: {c}" for i, c in enumerate(changes))
    return (
        f"DOCUMENT (paragraphs are independently addressable by their [Pn] id):\n\n"
        f"{numbered_doc}\n\n"
        f"---\n\n"
        f"REQUESTED CHANGES (0-indexed):\n{changes_block}\n"
    )


class TruncatedResponseError(Exception):
    """The model hit its output-token ceiling mid-response. For a large
    document + a broad change (e.g. a tone rewrite touching most paragraphs),
    the edit list itself can approach the model's completion-token limit.
    This is distinguished from a generic parse failure so callers can decide
    to degrade gracefully instead of endlessly retrying an unwinnable call."""


def call_openai(api_key, model, paragraphs, changes, timeout=180, max_output_tokens=16000):
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": build_user_prompt(paragraphs, changes)},
        ],
        "response_format": {"type": "json_schema", "json_schema": EDIT_SCHEMA},
        "temperature": 0.1,
        "max_tokens": max_output_tokens,
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        OPENAI_URL,
        data=data,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    last_err = None
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                body = json.loads(resp.read().decode("utf-8"))
            choice = body["choices"][0]
            content = choice["message"]["content"]
            usage = body.get("usage", {})
            if choice.get("finish_reason") == "length":
                # Response was cut off before completion -- content is very
                # likely invalid/partial JSON. Don't burn a retry attempt on
                # something structurally unwinnable; surface it distinctly.
                raise TruncatedResponseError(
                    f"model output hit the {max_output_tokens}-token completion "
                    f"ceiling before finishing (usage={usage})"
                )
            return json.loads(content), usage
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8", errors="replace")
            last_err = f"HTTP {e.code}: {err_body}"
            if e.code == 429 or e.code >= 500:
                time.sleep(2 ** attempt)
                continue
            raise RuntimeError(last_err)
        except (urllib.error.URLError, json.JSONDecodeError, KeyError, TimeoutError) as e:
            last_err = str(e)
            time.sleep(2 ** attempt)
            continue
    raise RuntimeError(f"OpenAI call failed after retries: {last_err}")


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

PLACEHOLDER_PATTERNS = [
    r"\bTODO\b", r"\bTBD\b", r"\[insert[^\]]*\]", r"\blorem ipsum\b",
    r"\bplaceholder\b", r"\.\.\.\s*$",
]


def validate_and_partition(parsed, paragraphs, changes):
    """Two phases, deliberately kept separate:

    1. Per-edit structural checks (unknown paragraph_id, out-of-range
       change_index, empty text, placeholder text) -- independent of any
       other edit.
    2. A conflict pass over every edit that passed phase 1: if more than one
       edit targets the same paragraph via replace/delete, ALL of them are
       dropped (not just the second one seen). Silently keeping "whichever
       one happened to be scanned first" would itself be exactly the kind
       of silent-bad-apply this system exists to prevent -- the first edit
       scanned is not more likely to be correct than the second.
    """
    valid_ids = {p["id"] for p in paragraphs}
    valid_ids.add("P0")
    n_changes = len(changes)

    structurally_valid = []
    rejected = []

    for edit in parsed.get("edits", []):
        problems = []
        ci = edit.get("change_index")
        pid = edit.get("paragraph_id")
        action = edit.get("action")
        new_text = edit.get("new_text", "")

        if not isinstance(ci, int) or not (0 <= ci < n_changes):
            problems.append(f"change_index {ci} out of range")
        if pid not in valid_ids:
            problems.append(f"unknown paragraph_id {pid!r}")
        if action in ("replace", "insert_after") and not new_text.strip():
            problems.append("empty new_text for replace/insert_after")
        for pat in PLACEHOLDER_PATTERNS:
            if re.search(pat, new_text, re.IGNORECASE):
                problems.append(f"new_text looks like an incomplete/placeholder generation ({pat})")
                break

        if problems:
            rejected.append({"edit": edit, "problems": problems})
        else:
            structurally_valid.append(edit)

    target_counts = {}
    for e in structurally_valid:
        if e["action"] in ("replace", "delete"):
            target_counts[e["paragraph_id"]] = target_counts.get(e["paragraph_id"], 0) + 1

    accepted = []
    for e in structurally_valid:
        pid = e["paragraph_id"]
        if e["action"] in ("replace", "delete") and target_counts.get(pid, 0) > 1:
            rejected.append({
                "edit": e,
                "problems": [f"paragraph {pid} targeted by {target_counts[pid]} edits -- "
                             f"conflicting edits, all skipped for safety"],
            })
        else:
            accepted.append(e)

    return accepted, rejected


def apply_edits(paragraphs, accepted_edits):
    by_id = {p["id"]: dict(p) for p in paragraphs}
    order = [p["id"] for p in paragraphs]
    deleted = set()
    inserts_after = {}  # paragraph_id -> list of new paragraph dicts

    for i, edit in enumerate(accepted_edits):
        pid = edit["paragraph_id"]
        action = edit["action"]
        if action == "replace":
            by_id[pid]["text"] = edit["new_text"]
        elif action == "delete":
            deleted.add(pid)
        elif action == "insert_after":
            new_id = f"{pid}_ins{i}"
            inserts_after.setdefault(pid, []).append({"id": new_id, "text": edit["new_text"]})

    result = []
    if "P0" in inserts_after:
        result.extend(inserts_after["P0"])
    for pid in order:
        if pid not in deleted:
            result.append(by_id[pid])
        if pid in inserts_after:
            result.extend(inserts_after[pid])
    return result


HEADING_RE = re.compile(r"^#{1,6}\s")


def detect_orphan_headings(paragraphs):
    """A heading immediately followed by another heading (or the end of the
    document) has no body content left under it."""
    orphans = []
    for i, p in enumerate(paragraphs):
        if HEADING_RE.match(p["text"].strip()):
            is_last = i == len(paragraphs) - 1
            next_is_heading = (not is_last) and HEADING_RE.match(paragraphs[i + 1]["text"].strip())
            if is_last or next_is_heading:
                orphans.append({"paragraph_id": p["id"], "text": p["text"].strip()})
    return orphans


def detect_new_orphan_headings(paragraphs_before, paragraphs_after):
    """Deterministic safety net: flags orphan headings that were INTRODUCED by
    the edits (e.g. a section's body was deleted but its heading wasn't). A
    document that already had a heading-immediately-followed-by-heading
    structure before editing (e.g. a title directly above the first section)
    is not a mistake we caused, so it's excluded by comparing against the
    pre-edit paragraph ids."""
    pre_existing_ids = {o["paragraph_id"] for o in detect_orphan_headings(paragraphs_before)}
    return [
        o for o in detect_orphan_headings(paragraphs_after)
        if o["paragraph_id"] not in pre_existing_ids
    ]


# ---------------------------------------------------------------------------
# Change-level status reporting
# ---------------------------------------------------------------------------

def build_report(changes, accepted, rejected, unresolved, usage, paragraphs_before, paragraphs_after):
    status = {}
    for i, c in enumerate(changes):
        status[i] = {"change": c, "applied_edits": 0, "rejected_edits": 0, "state": "not_addressed"}

    for e in accepted:
        status[e["change_index"]]["applied_edits"] += 1
    for r in rejected:
        ci = r["edit"].get("change_index")
        if ci in status:
            status[ci]["rejected_edits"] += 1

    for u in unresolved:
        ci = u.get("change_index")
        if ci in status:
            status[ci]["state"] = "unresolved_by_model"
            status[ci]["reason"] = u.get("reason")

    for i, s in status.items():
        if s["state"] == "unresolved_by_model":
            continue
        if s["applied_edits"] > 0:
            s["state"] = "applied" if s["rejected_edits"] == 0 else "partially_applied"
        elif s["rejected_edits"] > 0:
            s["state"] = "failed_validation"
        else:
            s["state"] = "not_addressed"  # model silently produced nothing -- flagged, not hidden

    words_before = sum(len(p["text"].split()) for p in paragraphs_before)
    words_after = sum(len(p["text"].split()) for p in paragraphs_after)
    orphan_headings = detect_new_orphan_headings(paragraphs_before, paragraphs_after)

    return {
        "changes": [status[i] for i in range(len(changes))],
        "rejected_edits_detail": rejected,
        "orphan_headings": orphan_headings,
        "token_usage": usage,
        "doc_stats": {
            "paragraphs_before": len(paragraphs_before),
            "paragraphs_after": len(paragraphs_after),
            "words_before": words_before,
            "words_after": words_after,
            "word_delta_pct": round(100 * (words_after - words_before) / max(words_before, 1), 1),
        },
        "needs_human_review": bool(orphan_headings) or any(
            s["state"] in ("failed_validation", "not_addressed", "unresolved_by_model", "partially_applied")
            for s in status.values()
        ),
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _call_with_truncation_fallback(api_key, model, paragraphs, changes):
    """Wraps call_openai with one level of graceful degradation: if the
    response was cut off at the completion-token ceiling (a real risk on a
    ~10k-word document when many/broad changes are requested in one call),
    split the change list in half and issue two calls instead of one, then
    merge the results (remapping change_index back to the original list).
    This keeps the common case -- several changes, only some of which are
    broad -- from failing outright just because the combined output was too
    large. If a single change alone still can't fit (nothing left to split),
    it's reported as unresolved rather than crashing or applying partial
    (likely-invalid) output."""
    try:
        return call_openai(api_key, model, paragraphs, changes)
    except TruncatedResponseError as e:
        if len(changes) <= 1:
            return (
                {
                    "edits": [],
                    "unresolved_changes": [{
                        "change_index": 0,
                        "reason": f"model output exceeded the completion-token limit "
                                  f"for this document/change combination ({e}); too broad "
                                  f"to execute in a single pass",
                    }],
                },
                {},
            )
        mid = len(changes) // 2
        combined = {"edits": [], "unresolved_changes": []}
        combined_usage = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
        for offset, subset in ((0, changes[:mid]), (mid, changes[mid:])):
            sub_parsed, sub_usage = _call_with_truncation_fallback(api_key, model, paragraphs, subset)
            for edit in sub_parsed.get("edits", []):
                e2 = dict(edit)
                e2["change_index"] = offset + e2["change_index"]
                combined["edits"].append(e2)
            for u in sub_parsed.get("unresolved_changes", []):
                u2 = dict(u)
                u2["change_index"] = offset + u2["change_index"]
                combined["unresolved_changes"].append(u2)
            for k in combined_usage:
                combined_usage[k] += sub_usage.get(k, 0)
        return combined, combined_usage


def run(source_document, changes, api_key, model=DEFAULT_MODEL):
    paragraphs = split_paragraphs(source_document)
    if not changes:
        return source_document, {"changes": [], "needs_human_review": False, "note": "no changes requested"}

    parsed, usage = _call_with_truncation_fallback(api_key, model, paragraphs, changes)
    accepted, rejected = validate_and_partition(parsed, paragraphs, changes)
    new_paragraphs = apply_edits(paragraphs, accepted)
    updated_doc = reassemble(new_paragraphs)
    report = build_report(
        changes, accepted, rejected, parsed.get("unresolved_changes", []),
        usage, paragraphs, new_paragraphs,
    )
    return updated_doc, report


def load_dotenv(path=".env"):
    """Minimal .env loader -- no python-dotenv dependency needed for a
    handful of KEY=value lines. Never overrides a variable already set in
    the real environment, so `$env:OPENAI_API_KEY = "..."` still wins if
    both are present."""
    if not os.path.exists(path):
        return
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def main():
    load_dotenv()

    ap = argparse.ArgumentParser(description="LLM-driven document updater")
    ap.add_argument("--input", required=True, help="Path to JSON file: {sourceDocument, changes}")
    ap.add_argument("--out-doc", required=True, help="Path to write updated document")
    ap.add_argument("--out-report", required=True, help="Path to write JSON report")
    ap.add_argument("--model", default=os.environ.get("MODEL", DEFAULT_MODEL))
    ap.add_argument("--api-key", default=os.environ.get("OPENAI_API_KEY"))
    args = ap.parse_args()

    if not args.api_key:
        print("Error: set OPENAI_API_KEY env var or pass --api-key", file=sys.stderr)
        sys.exit(1)

    with open(args.input, "r", encoding="utf-8") as f:
        payload = json.load(f)

    source_document = payload["sourceDocument"]
    try:
        updated_doc, report = run(
            source_document, payload["changes"], args.api_key, args.model
        )
        fatal = False
    except Exception as e:
        # Last-resort safety net for an unattended batch pipeline: a
        # genuinely unrecoverable failure (network exhausted, API outage)
        # still produces a valid, unchanged document and a report explaining
        # why, instead of a bare traceback that a batch driver can't act on
        # -- one bad document should not look different from "needs review"
        # to whatever is orchestrating the batch.
        updated_doc = source_document
        report = {
            "changes": [],
            "needs_human_review": True,
            "fatal_error": f"{type(e).__name__}: {e}",
        }
        fatal = True

    with open(args.out_doc, "w", encoding="utf-8") as f:
        f.write(updated_doc)
    with open(args.out_report, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    print(f"Wrote updated document to {args.out_doc}")
    print(f"Wrote report to {args.out_report}")
    if report.get("needs_human_review"):
        print("NOTE: report flags items needing human review (see out-report).")
    if fatal:
        print(f"NOTE: run failed ({report['fatal_error']}); original document passed through unchanged.", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
