from __future__ import annotations
import tempfile
import unittest
from pathlib import Path
from tools.question import QuestionStore

REPORT = {"valid": True, "object_ref": {"object_type": "wiki"}, "derived": {"evidence_state": "supported"}, "hashes": {"content_sha256": "sha256:content", "evidence_sha256": "sha256:evidence"}}

class QuestionTests(unittest.TestCase):
    def base(self, kind="single_choice"):
        value = {"id": "q-one", "type": kind, "wiki_id": "wiki-one", "claim_id": "claim-one", "prompt": "2+2?", "confidentiality": "internal"}
        if kind in {"single_choice", "multi_choice"}:
            value.update(options=[{"id": "a", "text": "4"}, {"id": "b", "text": "5"}], correct_option_ids=["a"])
        else:
            value["rubric"] = ["包含核心概念"]
        return value

    def test_create_requires_verified_claim(self):
        with tempfile.TemporaryDirectory() as d:
            store = QuestionStore(Path(d))
            result = store.create(self.base(), wiki_report={"valid": False})
            self.assertEqual(result["state"], "blocked")
            self.assertIn("wiki_unverified", {e["code"] for e in result["errors"]})

    def test_single_and_multi_choice_scoring(self):
        with tempfile.TemporaryDirectory() as d:
            store = QuestionStore(Path(d))
            one = store.create(self.base(), wiki_report=REPORT)["question"]["id"]
            self.assertTrue(store.answer(one, "a")["correct"])
            multi = self.base("multi_choice"); multi["id"] = "q-two"; multi["correct_option_ids"] = ["a", "b"]
            store.create(multi, wiki_report=REPORT)
            self.assertFalse(store.answer("q-two", ["a"])["correct"])

    def test_short_answer_is_manual_and_disabled_is_blocked(self):
        with tempfile.TemporaryDirectory() as d:
            store = QuestionStore(Path(d)); short = self.base("short_answer")
            store.create(short, wiki_report=REPORT)
            self.assertEqual(store.answer("q-one", "answer")["state"], "manual_review")
            q = store.load("q-one"); q["status"] = "disabled"
            store._file("q-one").write_text(__import__("json").dumps(q), encoding="utf-8")
            self.assertEqual(store.answer("q-one", "answer")["error_code"], "question_disabled")

    def test_fsrs_unavailable_is_explicit(self):
        with tempfile.TemporaryDirectory() as d:
            store = QuestionStore(Path(d)); store.create(self.base(), wiki_report=REPORT)
            result = store.review("q-one", 3)
            self.assertIn(result["state"], {"unavailable", "scheduled"})

if __name__ == "__main__": unittest.main()
