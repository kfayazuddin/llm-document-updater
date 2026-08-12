# LLM-Driven Document Updates

A CLI that takes `{ sourceDocument, changes[] }` and produces a correctly updated
document using an LLM, designed to run unattended in batch over many ~10k-word
documents.

```
python doc_updater.py --input input.json --out-doc updated.md --out-report report.json
```

Requires `OPENAI_API_KEY`, set either as a real environment variable, via
`--api-key`, or in a local `.env` file (copy `.env.example` to `.env` and
fill in your key — `.env` is git-ignored and never committed). Pure Python 3
standard library — no dependencies to install (built under real time pressure;
`pip install` wasn't worth the risk of a flaky network delay mid-assessment,
and it kept a `.env` loader to a few lines of stdlib code rather than a
`python-dotenv` dependency).

Model defaults to `gpt-4o`, overridable with `--model` / `MODEL` env var.

Deterministic unit tests for the validation/reliability layer (no API key
needed): `python test_reliability.py`.

**Architecture diagram:** [`docs/architecture-diagram.html`](docs/architecture-diagram.html)
walks through the pipeline and the validator gate visually. GitHub shows raw
HTML as source rather than rendering it, so view it either by downloading
the file and opening it in a browser, or via
[htmlpreview.github.io](https://htmlpreview.github.io/?https://raw.githubusercontent.com/kfayazuddin/llm-document-updater/main/docs/architecture-diagram.html).

## Architecture, and why

**The core decision: don't ask the LLM to rewrite the whole document. Ask it to
propose a list of paragraph-level edit operations, then apply those
deterministically in code.**

1. The source document is split into paragraphs (blank-line-delimited), each
   assigned a stable id: `P1`, `P2`, ... This is the unit of addressing.
2. One LLM call gets the *entire numbered document* plus the full list of
   changes, and returns structured JSON (via `response_format: json_schema`,
   strict mode): a list of edits, each `{ change_index, paragraph_id, action:
   replace|delete|insert_after, new_text, reasoning }`, plus an
   `unresolved_changes` list for anything it can't safely do.
3. Every edit is validated in Python — does `paragraph_id` exist, is
   `new_text` non-empty where required, do two edits collide on the same
   paragraph — **before** anything is applied.
4. Accepted edits are applied with plain string operations (dict lookup +
   list rebuild + `"\n\n".join`). The LLM never touches the actual text
   splicing; it only decides *what* the new paragraph text should be.

### Why this addresses token/latency scaling

The naive approach — send the whole document, get the whole document back,
for every run — makes both input *and output* tokens scale with document
size regardless of how small the actual change is. Removing one paragraph
from a 10k-word document under that model still costs ~10k output tokens.

With paragraph-level edits, output tokens scale with **how much content
actually changed**, not with document size. Deleting one paragraph costs one
short edit object. Adding a GDPR sentence to the Security section costs one
paragraph's worth of text. Input tokens still scale with document size
(the model needs to see the whole document to locate things and use
correct context) — that's unavoidable and appropriate; it's the output
side, and the multiplicative blow-up from doing multiple full-document
passes, that this design avoids.

The one case where output cost approaches a full rewrite is a change that
touches nearly every paragraph (e.g. "make the tone more formal
throughout") — there, replace edits for most paragraphs are inherently
necessary. That's a property of the change, not the architecture; even a
human editor making that change touches every paragraph.

This also directly serves reliability: a full-document rewrite gives the
model far more surface area to accidentally paraphrase, drop, or reformat
content that no change asked it to touch. Constraining edits to named
paragraphs means untouched paragraphs are provably untouched — they're
never in the LLM's output at all.

### Alternative I considered and rejected

The first real alternative was **verbatim find/replace over the raw text**:
have the model return `{ find: "<exact substring>", replace: "<new
text>" }` pairs, and apply them by exact string match, rejecting any `find`
that doesn't match exactly once.

I rejected it because LLMs are unreliable at reproducing long spans of
source text byte-for-byte — a single mismatched space, smart quote, or
line wrap makes `find` fail to match, and the failure mode is silent
(rejected edit) rather than a clean success. Paragraph IDs sidestep this
entirely: the model only has to get a short id like `P7` right, not
reproduce potentially hundreds of characters verbatim. It also made
validation trivial (`pid in valid_ids`) instead of requiring fuzzy/substring
matching heuristics, which is exactly the kind of "formatting mistake"
category the assignment calls out as something to expect and handle.

A second alternative — full-document rewrite per change, applied N times
for N changes — was rejected outright for the reason above: cost scales
with `document_size × num_changes` instead of `document_size +
total_edit_size`, and it multiplies the number of opportunities for drift.

### Where I changed approach mid-build

Two things, both triggered by evidence rather than guessing upfront:

**1. Prompt fix.** Initial testing (`examples/sample1.json`, change 3, "make
the tone throughout more formal") showed the model being *too*
conservative: it put the entire change into `unresolved_changes` with the
reason "too broad, affects multiple paragraphs," rather than doing what the
architecture actually supports — emitting one replace edit per paragraph
that needs it. I hadn't told it that was expected. I added an explicit rule
to the system prompt permitting/requiring broad changes to be decomposed
into multiple paragraph edits, and re-ran: the same change went from 0
applied edits to 6.

**2. Testing methodology.** After that fix, I re-ran the same input a few
times and noticed the model didn't *reliably* follow the new "don't leave
an orphaned heading behind" instruction — it complied on some runs and not
on others, at the same temperature, on the same input (see Reliability
below). That was the moment I realized live end-to-end testing against a
non-deterministic model can't be my only evidence that the *validation
code itself* is correct — a bug in my Python could just as easily hide
behind "the model happened to behave" on any given run. So I added
`test_reliability.py`, a deterministic unit-test suite that exercises the
validator, the conflict-detector, and the orphan-heading check directly
with synthetic inputs, independent of any live API call. That suite
immediately caught a real bug (below) that every live test run up to that
point had missed by luck.

## Reliability approach

The brief: don't silently apply a bad change, and don't hard-fail on the
first bad output. Concretely, this system layers several independent
mechanisms rather than trusting the model's own claims about what it did:

1. **Structural validation of every edit, before applying anything.**
   Unknown `paragraph_id`, out-of-range `change_index`, empty `new_text` on
   a replace/insert, and text that looks like a truncated/placeholder
   generation (`TODO`, `[insert ...]`, trailing `...`, etc.) are all
   rejected individually — not the whole batch. A bad edit for change #2
   doesn't block change #1 or #3 from applying. Rejected edits are recorded
   with their reason in `rejected_edits_detail`, not dropped silently.

2. **Conflict detection — and a real bug in it that testing caught.** If
   two edits target the same paragraph (e.g. the model tries to both
   delete and replace `P5`, or two different changes both rewrite the same
   paragraph), the intent is that *both* are skipped rather than one being
   picked arbitrarily — silently guessing which one is "right" is exactly
   the kind of silent-bad-apply the brief warns against. My first
   implementation didn't actually do this: it accepted whichever
   conflicting edit was scanned *first* and only rejected the second one it
   saw — so a genuine conflict would have resulted in exactly the silent,
   arbitrary pick I was trying to prevent. `test_reliability.py::
   test_conflicting_edits_on_same_paragraph_both_dropped` caught this
   immediately (it failed on the first run); no live LLM test had exposed
   it, because getting a real model to produce two conflicting edits on
   demand isn't reliable to provoke. Fixed by separating structural
   validation from conflict detection into two explicit passes, so
   "how many edits target this paragraph" is computed from the *whole*
   accepted set before anything is kept, not decided incrementally while
   scanning.

3. **A deterministic post-hoc check independent of the model's own
   self-report**: `detect_new_orphan_headings` scans the paragraph list
   after edits are applied for a heading immediately followed by another
   heading (or end of document) — a section whose body was removed but
   whose heading wasn't. It compares against the *pre-edit* document so a
   document that legitimately has no intro paragraph before its first
   section (title directly above `## Pricing`, say) isn't a false positive
   — only headings newly orphaned by this run's edits are flagged. This
   caught a real, *recurring* bug: across three separate runs (small doc,
   twice; large ~8.5k-word doc, once — see Test cases below), the model
   deleted the "Legacy API" section's body per the instruction but left
   the `## Legacy API (v1)` heading behind on 2 of those 3 runs, despite
   the system prompt explicitly saying not to. Its own report claimed the
   change was fully "applied" every time. The heuristic caught it every
   time regardless. This is the clearest evidence in this whole project for
   why prompt instructions alone aren't reliability: the same prompt,
   against the same model, at the same low temperature, was inconsistent
   run to run — a code-level check that doesn't depend on the model
   remembering an instruction is what actually closed the gap.

4. **Output-size safety net.** A large document plus a broad change can in
   principle push the edit list's output size toward the model's
   completion-token ceiling, producing a response that's cut off
   mid-JSON — silently truncated output is exactly the kind of "formatting
   mistake" the brief says to expect. `call_openai` checks the API
   response's `finish_reason` and raises a distinct `TruncatedResponseError`
   (rather than letting it fail json parsing and look like a generic
   transport error). `_call_with_truncation_fallback` catches that and, if
   more than one change was requested in the batch, retries by splitting
   the change list in half and issuing two calls instead of one
   (remapping `change_index` back to the original list); if a single
   change alone still can't fit, it's reported as `unresolved` rather than
   applying partial/invalid output. In practice, the real ~8.5k-word test
   (below) never got close to the ceiling — 811 completion tokens against
   a 16,000-token budget — so I couldn't provoke this live without an
   artificial worst-case document (e.g. one where literally every
   paragraph needs rewriting). Instead it's covered by two unit tests in
   `test_reliability.py` that simulate the truncation via a mocked
   `call_openai`, which is the more honest way to test a failure mode that
   a realistic input doesn't naturally trigger.

5. **Per-change status, not a single pass/fail.** Every output change is
   classified as `applied`, `partially_applied`, `failed_validation`,
   `unresolved_by_model` (the model explicitly declined and said why), or
   `not_addressed` (the model silently produced zero edits for it and
   didn't explain — this is deliberately *not* the same bucket as
   `unresolved_by_model`, because a silent no-op is a worse failure mode
   than an explained one, and both need to be visible). `needs_human_review`
   is `true` if any change isn't cleanly `applied`, or if any orphan heading
   was introduced. Since this runs unattended, the report is the audit
   trail a batch pipeline would page on or route to a review queue —
   "no HITL in the loop" doesn't mean no visibility into what happened.

6. **Retries only where they're cheap and meaningful.** Transient API
   failures (429s, 5xx, timeouts) get up to 3 attempts with backoff — that's
   a full-price retry, so it's reserved for genuine transport failures, not
   for "the model gave an answer I didn't like." A single bad edit doesn't
   trigger a full-document re-generation; it's dropped and reported, which
   is both cheaper and avoids the failure mode of asking the model to "try
   again" and getting a different but equally-plausible-looking mistake.

7. **A last-resort safety net at the process boundary.** If a run fails
   for a reason none of the above handles (API outage that outlasts the
   retries, malformed input JSON), `main()` catches it, writes the
   *original* document through unchanged, writes a report with
   `fatal_error` set and `needs_human_review: true`, and exits non-zero —
   instead of an unhandled traceback. In an unattended batch pipeline
   calling this script per document, a crash and a "needs review" outcome
   should not look different to whatever's orchestrating the batch; both
   need to be visible in the same place (the report file), and one bad
   document failing shouldn't take down monitoring for the rest of the
   batch.

### A constructed example that would pass every check and still be wrong

Take the pricing bullet from `examples/sample1.json`:

```
- Enterprise: $2,000/month, billed monthly at $2,000/month, or $20,000/year if billed annually.
```

Change: *"Update the pricing section to reflect a 10% increase across all
tiers."* Suppose the model returns this replace edit:

```
- Enterprise: $2,200/month, billed monthly at $2,200/month, or $24,000/year if billed annually.
```

The monthly figure is correct ($2,000 × 1.1 = $2,200). The annual figure is
not — a consistent 10% increase gives $22,000, not $24,000 (which looks
like it was computed some other way, e.g. accidentally reapplying the
increase or multiplying the *new* monthly by 12 instead of scaling the
original 10x annual multiplier). This edit:

- targets a real, existing `paragraph_id`
- has non-empty, well-formatted `new_text`
- matches no placeholder pattern
- doesn't conflict with any other edit
- applies cleanly and leaves the document structurally intact

It passes every check this system runs, and the resulting document is
wrong. **My system validates the *mechanics* of an edit (does it target a
real location, is it well-formed, does it collide with another edit) — it
never validates the *arithmetic or factual content* of `new_text` against
the source.** Doing that in general would require the system to
independently re-derive what "correct" means for arbitrary natural-language
instructions (a calculator for numeric changes, a fact-checker for
factual ones, a consistency checker across the whole document for
referential ones) — which is a fundamentally harder, open-ended problem,
not a bounded validation rule, and it's out of scope for what a 1-2 hour
system reasonably attempts. A production version of this would want a
narrow, targeted check for exactly this class of error (e.g., extract all
dollar/percentage figures from a changed paragraph and verify they're
mutually consistent under the stated transformation) rather than a general
correctness oracle.

## Test cases run

Two layers, deliberately: live end-to-end runs against the real API (for
accuracy/latency/token evidence, and to see how the model actually
behaves), plus a deterministic unit suite (for proving the *validation
code* is correct independent of model behavior — see the pivot described
above). All live runs used the real key against `gpt-4o`; all inputs/
outputs/reports are committed in `examples/`.

**`python test_reliability.py`** — 14 unit tests, no API calls, run in
~2ms. Covers: orphan-heading detection (flags a newly-introduced orphan,
does *not* flag pre-existing title-above-heading structure, flags a
heading at document end); edit validation (valid edit accepted; unknown
`paragraph_id` rejected; out-of-range `change_index` rejected; placeholder
text rejected; **conflicting edits on the same paragraph — both dropped**,
which is the test that caught the real bug described above); `apply_edits`
correctness for replace/delete/insert_after including insert-before-first-
paragraph; and the truncation fallback's index-remapping logic under a
mocked `call_openai`. All 14 pass after the conflict-detection fix.

Live runs:

- **`sample1.json`** (~320 words) — the three example changes from the
  brief plus a fourth (add a GDPR sentence). Exercises replace (pricing
  math, tone), delete (legacy section), and insert-via-replace (GDPR
  append) in one call. This is where the tone-change over-caution and the
  orphan-heading issues were originally found (see above). Re-running it
  multiple times after the prompt fix shows all 4 changes consistently
  landing as `applied`, but the orphan heading reappeared on 2 of 3 later
  runs despite the prompt explicitly telling the model not to do that —
  concrete evidence that a prompt instruction is not a reliability
  mechanism by itself.
- **`sample2_crossref.json`** (~80 words) — the same pricing-increase
  change, with the same dollar figure deliberately repeated across three
  unrelated sections (pricing table, prose, FAQ), to probe whether a
  paragraph-scoped edit model would miss references outside the "obvious"
  pricing paragraph. The model located and updated all three consistently.
  This run also caught a false positive in my own orphan-heading heuristic
  (a title directly above the first `##` section isn't a defect) — fixed
  by diffing against the pre-edit document.
- **`sample3_unresolvable.json`** (~25 words) — a change referencing
  content that doesn't exist ("remove the paragraph about our mobile
  app"). Confirms the model reports it via `unresolved_changes` with a
  reason instead of fabricating an edit; the document is returned
  byte-for-byte unchanged; `needs_human_review` is correctly `true`.
- **`sample4_large.json`** (generated by `examples/generate_large_doc.py`,
  **8,509 words** — the scale the brief specifies) — a 39-section, 223-
  paragraph synthetic SaaS product doc (pricing, a legacy-API section, 40+
  integrations, security/compliance, casual onboarding prose, FAQ,
  glossary), run with the same style of changes as `sample1`: a pricing
  increase, a section deletion, a broad tone change, and a targeted
  addition. Real numbers from this run (`sample4_report.json`):
  **11,615 prompt tokens, 811 completion tokens, ~24 seconds latency.**
  Completion tokens are ~7% of prompt tokens — direct evidence for the
  core architectural claim that output cost tracks *what changed* (here,
  only 6 of 223 paragraphs needed a tone edit — most of the synthetic doc
  was already written in a neutral documentation register) rather than
  document size. All 4 changes applied correctly (pricing math consistent
  across monthly/annual figures, tone shifted in the casual sections,
  targeted note inserted in the right place) and the orphan-heading check
  again correctly flagged the same recurring Legacy API issue — the third
  time across three independent documents that this exact failure mode
  showed up, and the third time the deterministic check caught it.

## What I'd do differently with more time

- **Actually provoke the output-truncation path against a live model.** The
  8.5k-word test never got within an order of magnitude of the completion
  ceiling (811 of 16,000 tokens), because a realistic broad change only
  touches the paragraphs that genuinely need it. Proving the fallback
  works end-to-end (not just via a mocked unit test) would need a
  deliberately adversarial document where nearly every one of ~250
  paragraphs is individually miswritten and needs a full rewrite — worth
  building specifically to validate the safety net fires correctly under
  real API conditions, not just simulated ones.
- **The numeric/factual consistency check described above** — at minimum,
  extract numbers from a changed paragraph and flag (not block) when a
  stated percentage/delta doesn't reconcile across all figures in that
  paragraph.
- **Cross-paragraph consistency scanning** — sample2 showed the model can
  often get this right zero-shot, but "often" isn't a guarantee; a cheap
  second pass that greps the *unedited* paragraphs for now-stale figures
  related to an applied change would close that gap deterministically
  rather than relying on model diligence.
- **Batch/concurrency**: the CLI processes one document per invocation;
  for real batch volume I'd add a driver that fans out across documents
  concurrently (the per-document work is already a single LLM call, so
  this is mostly bounded by API rate limits, not redesign).
- **A second, cheap verification call** for `applied` changes only,
  asking a smaller/cheaper model "does this edit satisfy this instruction,
  yes/no" — traded off against the "order of magnitude" cost target in
  the brief, so I left it out, but it's a natural next layer if per-change
  accuracy needs to go up.
- **Real diff output** in the report (unified-diff style) instead of only
  full before/after documents, to make human review faster when
  `needs_human_review` is true.
