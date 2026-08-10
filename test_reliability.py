#!/usr/bin/env python3
"""
Deterministic unit tests for the reliability layer (no API calls).

The end-to-end examples in examples/ demonstrate real behavior against the
live model, but LLM output isn't fully reproducible run-to-run -- a bug
observed once (e.g. an orphaned heading) isn't guaranteed to reproduce on
the next call, especially after a prompt fix nudges the distribution. These
tests instead exercise the safety mechanisms directly with synthetic inputs,
so their correctness doesn't depend on coaxing the model into misbehaving.

Run: python test_reliability.py
"""

import unittest
from unittest.mock import patch

import doc_updater as du


class TestOrphanHeadingDetection(unittest.TestCase):
    def test_flags_newly_orphaned_heading(self):
        before = [
            {"id": "P1", "text": "## Legacy API"},
            {"id": "P2", "text": "The legacy API is deprecated."},
            {"id": "P3", "text": "## Support"},
        ]
        after = [
            {"id": "P1", "text": "## Legacy API"},
            {"id": "P3", "text": "## Support"},
        ]
        orphans = du.detect_new_orphan_headings(before, after)
        self.assertEqual([o["paragraph_id"] for o in orphans], ["P1"])

    def test_does_not_flag_preexisting_structure(self):
        # Title directly above the first section, in both before and after --
        # this is normal structure, not a defect introduced by editing.
        before = [
            {"id": "P1", "text": "# Title"},
            {"id": "P2", "text": "## Pricing"},
            {"id": "P3", "text": "Some pricing text."},
        ]
        after = [
            {"id": "P1", "text": "# Title"},
            {"id": "P2", "text": "## Pricing"},
            {"id": "P3", "text": "Updated pricing text."},
        ]
        self.assertEqual(du.detect_new_orphan_headings(before, after), [])

    def test_flags_heading_at_end_of_document(self):
        before = [{"id": "P1", "text": "## Support"}, {"id": "P2", "text": "Call us."}]
        after = [{"id": "P1", "text": "## Support"}]
        orphans = du.detect_new_orphan_headings(before, after)
        self.assertEqual([o["paragraph_id"] for o in orphans], ["P1"])


class TestEditValidation(unittest.TestCase):
    def setUp(self):
        self.paragraphs = [
            {"id": "P1", "text": "Intro paragraph."},
            {"id": "P2", "text": "Second paragraph."},
        ]
        self.changes = ["change zero", "change one"]

    def test_valid_edit_is_accepted(self):
        parsed = {"edits": [
            {"change_index": 0, "paragraph_id": "P1", "action": "replace",
             "new_text": "New intro.", "reasoning": "r"},
        ], "unresolved_changes": []}
        accepted, rejected = du.validate_and_partition(parsed, self.paragraphs, self.changes)
        self.assertEqual(len(accepted), 1)
        self.assertEqual(rejected, [])

    def test_unknown_paragraph_id_is_rejected_not_crashed(self):
        parsed = {"edits": [
            {"change_index": 0, "paragraph_id": "P99", "action": "replace",
             "new_text": "New text.", "reasoning": "r"},
        ], "unresolved_changes": []}
        accepted, rejected = du.validate_and_partition(parsed, self.paragraphs, self.changes)
        self.assertEqual(accepted, [])
        self.assertEqual(len(rejected), 1)
        self.assertIn("unknown paragraph_id", rejected[0]["problems"][0])

    def test_conflicting_edits_on_same_paragraph_both_dropped(self):
        # Two different changes both try to rewrite P1 -- neither should be
        # silently preferred over the other.
        parsed = {"edits": [
            {"change_index": 0, "paragraph_id": "P1", "action": "replace",
             "new_text": "Version A.", "reasoning": "r"},
            {"change_index": 1, "paragraph_id": "P1", "action": "replace",
             "new_text": "Version B.", "reasoning": "r"},
        ], "unresolved_changes": []}
        accepted, rejected = du.validate_and_partition(parsed, self.paragraphs, self.changes)
        self.assertEqual(accepted, [])
        self.assertEqual(len(rejected), 2)

    def test_placeholder_text_is_rejected(self):
        parsed = {"edits": [
            {"change_index": 0, "paragraph_id": "P1", "action": "replace",
             "new_text": "TODO: finish this section", "reasoning": "r"},
        ], "unresolved_changes": []}
        accepted, rejected = du.validate_and_partition(parsed, self.paragraphs, self.changes)
        self.assertEqual(accepted, [])
        self.assertEqual(len(rejected), 1)

    def test_out_of_range_change_index_is_rejected(self):
        parsed = {"edits": [
            {"change_index": 7, "paragraph_id": "P1", "action": "replace",
             "new_text": "New text.", "reasoning": "r"},
        ], "unresolved_changes": []}
        accepted, rejected = du.validate_and_partition(parsed, self.paragraphs, self.changes)
        self.assertEqual(accepted, [])
        self.assertEqual(len(rejected), 1)


class TestApplyEdits(unittest.TestCase):
    def setUp(self):
        self.paragraphs = [
            {"id": "P1", "text": "First."},
            {"id": "P2", "text": "Second."},
            {"id": "P3", "text": "Third."},
        ]

    def test_replace(self):
        edits = [{"change_index": 0, "paragraph_id": "P2", "action": "replace",
                   "new_text": "Second (updated).", "reasoning": "r"}]
        result = du.apply_edits(self.paragraphs, edits)
        self.assertEqual([p["text"] for p in result], ["First.", "Second (updated).", "Third."])

    def test_delete(self):
        edits = [{"change_index": 0, "paragraph_id": "P2", "action": "delete",
                   "new_text": "", "reasoning": "r"}]
        result = du.apply_edits(self.paragraphs, edits)
        self.assertEqual([p["text"] for p in result], ["First.", "Third."])

    def test_insert_after(self):
        edits = [{"change_index": 0, "paragraph_id": "P1", "action": "insert_after",
                   "new_text": "Inserted.", "reasoning": "r"}]
        result = du.apply_edits(self.paragraphs, edits)
        self.assertEqual([p["text"] for p in result], ["First.", "Inserted.", "Second.", "Third."])

    def test_insert_before_first_paragraph(self):
        edits = [{"change_index": 0, "paragraph_id": "P0", "action": "insert_after",
                   "new_text": "New opener.", "reasoning": "r"}]
        result = du.apply_edits(self.paragraphs, edits)
        self.assertEqual(result[0]["text"], "New opener.")


class TestTruncationFallback(unittest.TestCase):
    """Simulates the model hitting the completion-token ceiling, without
    making a real API call, to prove the degrade-gracefully path works."""

    def test_single_change_truncation_reports_unresolved_not_crash(self):
        with patch.object(du, "call_openai", side_effect=du.TruncatedResponseError("boom")):
            parsed, usage = du._call_with_truncation_fallback("key", "model", [], ["one broad change"])
        self.assertEqual(parsed["edits"], [])
        self.assertEqual(len(parsed["unresolved_changes"]), 1)
        self.assertEqual(parsed["unresolved_changes"][0]["change_index"], 0)

    def test_multi_change_truncation_splits_and_remaps_indices(self):
        def fake_call(api_key, model, paragraphs, changes):
            # Succeed only once the batch has been split down to size 1.
            if len(changes) > 1:
                raise du.TruncatedResponseError("still too big")
            return (
                {"edits": [{"change_index": 0, "paragraph_id": "P1", "action": "replace",
                             "new_text": f"edit for {changes[0]}", "reasoning": "r"}],
                 "unresolved_changes": []},
                {"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15},
            )

        with patch.object(du, "call_openai", side_effect=fake_call):
            parsed, usage = du._call_with_truncation_fallback(
                "key", "model", [], ["change A", "change B", "change C", "change D"]
            )
        self.assertEqual(len(parsed["edits"]), 4)
        # Indices must be remapped back to the ORIGINAL 4-item change list,
        # not left as 0 for every split sub-batch.
        self.assertEqual(sorted(e["change_index"] for e in parsed["edits"]), [0, 1, 2, 3])
        self.assertEqual(usage["total_tokens"], 60)


if __name__ == "__main__":
    unittest.main(verbosity=2)
