from __future__ import annotations
import tempfile
import unittest
from pathlib import Path
from tools.question import QuestionStore

REPORT = {"valid": True, "object_ref": {"object_type": "wiki", "object_id": "wiki-one"}, "metadata": {"evidence": [{"claim_id": "claim-one"}]}, "derived": {"evidence_state": "supported"}, "hashes": {"content_sha256": "sha256:content", "evidence_sha256": "sha256:evidence"}}

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

    def test_create_rejects_wiki_or_claim_identity_mismatch(self):
        with tempfile.TemporaryDirectory() as d:
            store = QuestionStore(Path(d))
            wrong_wiki = store.create({**self.base(), "wiki_id": "other-wiki"}, wiki_report=REPORT)
            self.assertIn("wiki_id_mismatch", {e["code"] for e in wrong_wiki["errors"]})
            wrong_claim = store.create({**self.base(), "claim_id": "other-claim"}, wiki_report=REPORT)
            self.assertIn("claim_not_found", {e["code"] for e in wrong_claim["errors"]})

    def test_single_and_multi_choice_scoring(self):
        with tempfile.TemporaryDirectory() as d:
            store = QuestionStore(Path(d))
            one = store.create(self.base(), wiki_report=REPORT)["question"]["id"]
            self.assertTrue(store.answer(one, "a")["correct"])
            self.assertTrue((Path(d) / "practice" / "reviews" / "q-one.jsonl").exists())
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

    def test_short_answer_deterministic_rubric_and_provider_boundaries(self):
        with tempfile.TemporaryDirectory() as d:
            store = QuestionStore(Path(d)); short = self.base("short_answer")
            short["rubric"] = ["核心概念", {"label": "因果关系", "keywords": ["因为", "所以"]}]
            store.create(short, wiki_report=REPORT)
            result = store.answer("q-one", "包含核心概念，因为输入变化所以输出变化", scoring_mode="deterministic")
            self.assertEqual(result["state"], "graded")
            self.assertEqual(result["score"], 1.0)
            self.assertEqual(result["scoring_provider"], "deterministic_rubric")
            self.assertEqual(store.answer("q-one", "x", scoring_mode="llm")["reason"], "provider_unavailable")
            observed = store.answer("q-one", "x", scoring_mode="llm", scorer=lambda _: {"score": 0.5, "rationale": "部分覆盖"})
            self.assertEqual(observed["score"], 0.5)
            self.assertEqual(observed["scoring_provider"], "llm")
            self.assertEqual(store.answer("q-one", "x", scoring_mode="other")["error_code"], "scoring_mode_invalid")

    def test_fsrs_unavailable_is_explicit(self):
        with tempfile.TemporaryDirectory() as d:
            store = QuestionStore(Path(d)); store.create(self.base(), wiki_report=REPORT)
            result = store.review("q-one", 3)
            self.assertEqual(result["state"], "scheduled")
            self.assertEqual(result["review_state_schema"], "fsrs-card/v1")
            self.assertRegex(result["scheduler_version"], r"^\d+\.\d+")
            self.assertEqual(store.load("q-one")["review_state"]["state"], 1)

    def test_fsrs_persisted_card_can_be_reviewed_again(self):
        """真实 FSRS adapter 从持久化 Card 继续调度，不重置为新卡。"""
        with tempfile.TemporaryDirectory() as d:
            store = QuestionStore(Path(d)); store.create(self.base(), wiki_report=REPORT)
            first = store.review("q-one", 3)
            self.assertEqual(first["state"], "scheduled")
            first_card_id = store.load("q-one")["review_state"]["card_id"]
            second = store.review("q-one", 4)
            self.assertEqual(second["state"], "scheduled")
            persisted = store.load("q-one")["review_state"]
            self.assertEqual(persisted["card_id"], first_card_id)
            self.assertEqual(persisted["state"], 2)

    def test_fsrs_rejects_invalid_rating_before_adapter(self):
        with tempfile.TemporaryDirectory() as d:
            store = QuestionStore(Path(d)); store.create(self.base(), wiki_report=REPORT)
            result = store.review("q-one", 0)
            self.assertEqual(result, {"state": "blocked", "error_code": "rating_invalid"})

    def test_claim_hash_change_disables_question(self):
        with tempfile.TemporaryDirectory() as d:
            store = QuestionStore(Path(d)); store.create(self.base(), wiki_report=REPORT)
            stale = {**REPORT, "hashes": {"content_sha256": "sha256:changed", "evidence_sha256": "sha256:evidence"}}
            result = store.refresh_status("q-one", stale)
            self.assertEqual(result["state"], "disabled")
            self.assertEqual(store.answer("q-one", "a")["error_code"], "question_disabled")

    def test_refresh_rejects_wrong_wiki_claim_report_even_when_hashes_match(self):
        with tempfile.TemporaryDirectory() as d:
            store = QuestionStore(Path(d)); store.create(self.base(), wiki_report=REPORT)
            wrong = {**REPORT, "object_ref": {"object_type": "wiki", "object_id": "other-wiki"}}
            result = store.refresh_status("q-one", wrong)
            self.assertEqual(result["state"], "disabled")
            self.assertEqual(result["reason"], "claim_binding_stale")

    def test_refresh_all_disables_missing_or_stale_wiki_reports(self):
        with tempfile.TemporaryDirectory() as d:
            store = QuestionStore(Path(d))
            store.create(self.base(), wiki_report=REPORT)
            second = self.base(); second["id"] = "q-two"; second["wiki_id"] = "wiki-missing"
            missing_report = {**REPORT, "object_ref": {"object_type": "wiki", "object_id": "wiki-missing"}}
            store.create(second, wiki_report=missing_report)
            result = store.refresh_all({"wiki-one": REPORT})
            self.assertEqual(result["total"], 2)
            self.assertEqual(result["disabled"], 1)
            self.assertEqual(store.load("q-one")["status"], "enabled")
            self.assertEqual(store.load("q-two")["status"], "disabled")

    def test_choice_schema_rejects_duplicate_and_unknown_option_ids(self):
        with tempfile.TemporaryDirectory() as d:
            store = QuestionStore(Path(d))
            duplicate = self.base("single_choice")
            duplicate["options"] = [{"id": "a", "text": "4"}, {"id": "a", "text": "also 4"}]
            result = store.create(duplicate, wiki_report=REPORT)
            self.assertIn("option_ids_invalid", {item["code"] for item in result["errors"]})
            unknown = self.base("single_choice"); unknown["correct_option_ids"] = ["missing"]
            result = store.create(unknown, wiki_report=REPORT)
            self.assertIn("correct_option_id_unknown", {item["code"] for item in result["errors"]})

    def test_question_schema_rejects_unknown_and_type_specific_fields(self):
        with tempfile.TemporaryDirectory() as d:
            store = QuestionStore(Path(d))
            unknown = {**self.base(), "provider_url": "https://example.invalid"}
            result = store.create(unknown, wiki_report=REPORT)
            self.assertIn("unknown_field", {item["code"] for item in result["errors"]})
            short = self.base("short_answer")
            short["options"] = [{"id": "a", "text": "wrong"}]
            result = store.create(short, wiki_report=REPORT)
            self.assertIn("field_not_allowed", {item["code"] for item in result["errors"]})

    def test_tampered_question_content_is_fail_closed(self):
        with tempfile.TemporaryDirectory() as d:
            store = QuestionStore(Path(d)); store.create(self.base(), wiki_report=REPORT)
            path = store._file("q-one")
            value = __import__("json").loads(path.read_text(encoding="utf-8"))
            value["prompt"] = "tampered"
            path.write_text(__import__("json").dumps(value), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "question_hash_mismatch"):
                store.answer("q-one", "a")
            with self.assertRaisesRegex(ValueError, "question_hash_mismatch"):
                store.review("q-one", 3)

    def test_multi_choice_response_rejects_duplicate_ids(self):
        with tempfile.TemporaryDirectory() as d:
            store = QuestionStore(Path(d)); spec = self.base("multi_choice"); spec["correct_option_ids"] = ["a", "b"]
            store.create(spec, wiki_report=REPORT)
            result = store.answer("q-one", ["a", "a"])
            self.assertEqual(result["error_code"], "response_options_duplicate")

    def test_choice_response_rejects_unknown_option_ids(self):
        with tempfile.TemporaryDirectory() as d:
            store = QuestionStore(Path(d)); store.create(self.base(), wiki_report=REPORT)
            self.assertEqual(store.answer("q-one", "missing")["error_code"], "response_option_unknown")
            multi = self.base("multi_choice"); multi["id"] = "q-two"; store.create(multi, wiki_report=REPORT)
            self.assertEqual(store.answer("q-two", ["a", "missing"])["error_code"], "response_option_unknown")

if __name__ == "__main__": unittest.main()
