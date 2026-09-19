from __future__ import annotations

import json
import tempfile
import unittest
from datetime import UTC, datetime, timedelta
from pathlib import Path

from tools.question import QuestionStore

REPORT = {
    "valid": True,
    "object_ref": {"object_type": "wiki", "object_id": "wiki-one"},
    "metadata": {"evidence": [{"claim_id": "claim-one"}]},
    "derived": {"evidence_state": "supported"},
    "hashes": {
        "content_sha256": "sha256:content",
        "evidence_sha256": "sha256:evidence",
    },
}


class QuestionTests(unittest.TestCase):
    def base(self, kind="single_choice"):
        value = {
            "id": "q-one",
            "type": kind,
            "wiki_id": "wiki-one",
            "claim_id": "claim-one",
            "prompt": "2+2?",
            "confidentiality": "internal",
        }
        if kind in {"single_choice", "multi_choice"}:
            value.update(
                options=[{"id": "a", "text": "4"}, {"id": "b", "text": "5"}],
                correct_option_ids=["a"],
            )
        else:
            value["rubric"] = ["包含核心概念"]
        return value

    def test_create_requires_verified_claim(self):
        with tempfile.TemporaryDirectory() as d:
            store = QuestionStore(Path(d))
            result = store.create(self.base(), wiki_report={"valid": False})
            self.assertEqual(result["status"], "blocked")
            self.assertIn("wiki_unverified", {e["code"] for e in result["errors"]})

    def test_create_rejects_wiki_or_claim_identity_mismatch(self):
        with tempfile.TemporaryDirectory() as d:
            store = QuestionStore(Path(d))
            wrong_wiki = store.create(
                {**self.base(), "wiki_id": "other-wiki"}, wiki_report=REPORT
            )
            self.assertIn("wiki_id_mismatch", {e["code"] for e in wrong_wiki["errors"]})
            wrong_claim = store.create(
                {**self.base(), "claim_id": "other-claim"}, wiki_report=REPORT
            )
            self.assertIn("claim_not_found", {e["code"] for e in wrong_claim["errors"]})

    def test_single_and_multi_choice_scoring(self):
        with tempfile.TemporaryDirectory() as d:
            store = QuestionStore(Path(d))
            one = store.create(self.base(), wiki_report=REPORT)["question"]["id"]
            self.assertTrue(store.answer(one, "a")["grading"]["correct"])
            self.assertTrue(
                (Path(d) / "content" / "practice" / "reviews" / "q-one.jsonl").exists()
            )
            multi = self.base("multi_choice")
            multi["id"] = "q-two"
            multi["correct_option_ids"] = ["a", "b"]
            store.create(multi, wiki_report=REPORT)
            self.assertFalse(store.answer("q-two", ["a"])["grading"]["correct"])

    def test_short_answer_is_manual_and_disabled_is_blocked(self):
        with tempfile.TemporaryDirectory() as d:
            store = QuestionStore(Path(d))
            short = self.base("short_answer")
            store.create(short, wiki_report=REPORT)
            self.assertEqual(
                store.answer("q-one", "answer")["grading"]["state"], "manual_review"
            )
            q = store.load("q-one")
            q["status"] = "disabled"
            store._file("q-one").write_text(
                __import__("json").dumps(q), encoding="utf-8"
            )
            self.assertEqual(
                store.answer("q-one", "answer")["error_code"], "question_disabled"
            )

    def test_short_answer_deterministic_rubric_and_provider_boundaries(self):
        with tempfile.TemporaryDirectory() as d:
            store = QuestionStore(Path(d))
            short = self.base("short_answer")
            short["rubric"] = [
                "核心概念",
                {"label": "因果关系", "keywords": ["因为", "所以"]},
            ]
            store.create(short, wiki_report=REPORT)
            result = store.answer(
                "q-one",
                "包含核心概念，因为输入变化所以输出变化",
                scoring_mode="deterministic",
            )
            self.assertEqual(result["grading"]["state"], "graded")
            self.assertEqual(result["grading"]["score"], 1.0)
            self.assertEqual(
                result["grading"]["scoring_provider"], "deterministic_rubric"
            )
            self.assertEqual(
                store.answer("q-one", "x", scoring_mode="llm")["reason"],
                "provider_unavailable",
            )
            observed = store.answer(
                "q-one",
                "x",
                scoring_mode="llm",
                scorer=lambda _: {"score": 0.5, "rationale": "部分覆盖"},
            )
            self.assertEqual(observed["grading"]["score"], 0.5)
            self.assertEqual(observed["grading"]["scoring_provider"], "llm")
            self.assertEqual(
                store.answer("q-one", "x", scoring_mode="other")["error_code"],
                "scoring_mode_invalid",
            )

    def test_fsrs_unavailable_is_explicit(self):
        with tempfile.TemporaryDirectory() as d:
            store = QuestionStore(Path(d))
            store.create(self.base(), wiki_report=REPORT)
            result = store.review("q-one", 3)
            self.assertEqual(result["status"], "ok")
            self.assertEqual(result["schedule"]["state"], "scheduled")
            self.assertEqual(result["schedule"]["review_state_schema"], "fsrs-card/v1")
            self.assertRegex(result["schedule"]["scheduler_version"], r"^\d+\.\d+")
            self.assertEqual(store.load("q-one")["review_state"]["state"], 1)

    def test_fsrs_persisted_card_can_be_reviewed_again(self):
        """真实 FSRS adapter 从持久化 Card 继续调度，不重置为新卡。"""
        with tempfile.TemporaryDirectory() as d:
            store = QuestionStore(Path(d))
            store.create(self.base(), wiki_report=REPORT)
            first = store.review("q-one", 3)
            self.assertEqual(first["schedule"]["state"], "scheduled")
            first_card_id = store.load("q-one")["review_state"]["card_id"]
            second = store.review("q-one", 4)
            self.assertEqual(second["schedule"]["state"], "scheduled")
            persisted = store.load("q-one")["review_state"]
            self.assertEqual(persisted["card_id"], first_card_id)
            self.assertEqual(persisted["state"], 2)

    def test_fsrs_rejects_invalid_rating_before_adapter(self):
        with tempfile.TemporaryDirectory() as d:
            store = QuestionStore(Path(d))
            store.create(self.base(), wiki_report=REPORT)
            result = store.review("q-one", 0)
            self.assertEqual(result["status"], "blocked")
            self.assertEqual(result["error_code"], "rating_invalid")

    def test_claim_hash_change_disables_question(self):
        with tempfile.TemporaryDirectory() as d:
            store = QuestionStore(Path(d))
            store.create(self.base(), wiki_report=REPORT)
            stale = {
                **REPORT,
                "hashes": {
                    "content_sha256": "sha256:changed",
                    "evidence_sha256": "sha256:evidence",
                },
            }
            result = store.refresh_status("q-one", stale)
            self.assertEqual(result["lifecycle"], "disabled")
            self.assertEqual(
                store.answer("q-one", "a")["error_code"], "question_disabled"
            )

    def test_refresh_rejects_wrong_wiki_claim_report_even_when_hashes_match(self):
        with tempfile.TemporaryDirectory() as d:
            store = QuestionStore(Path(d))
            store.create(self.base(), wiki_report=REPORT)
            wrong = {
                **REPORT,
                "object_ref": {"object_type": "wiki", "object_id": "other-wiki"},
            }
            result = store.refresh_status("q-one", wrong)
            self.assertEqual(result["lifecycle"], "disabled")
            self.assertEqual(result["reason"], "claim_binding_stale")

    def test_refresh_all_disables_missing_or_stale_wiki_reports(self):
        with tempfile.TemporaryDirectory() as d:
            store = QuestionStore(Path(d))
            store.create(self.base(), wiki_report=REPORT)
            second = self.base()
            second["id"] = "q-two"
            second["wiki_id"] = "wiki-missing"
            missing_report = {
                **REPORT,
                "object_ref": {"object_type": "wiki", "object_id": "wiki-missing"},
            }
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
            duplicate["options"] = [
                {"id": "a", "text": "4"},
                {"id": "a", "text": "also 4"},
            ]
            result = store.create(duplicate, wiki_report=REPORT)
            self.assertIn(
                "option_ids_invalid", {item["code"] for item in result["errors"]}
            )
            unknown = self.base("single_choice")
            unknown["correct_option_ids"] = ["missing"]
            result = store.create(unknown, wiki_report=REPORT)
            self.assertIn(
                "correct_option_id_unknown", {item["code"] for item in result["errors"]}
            )

    def test_question_schema_rejects_unknown_and_type_specific_fields(self):
        with tempfile.TemporaryDirectory() as d:
            store = QuestionStore(Path(d))
            unknown = {**self.base(), "provider_url": "https://example.invalid"}
            result = store.create(unknown, wiki_report=REPORT)
            self.assertIn("unknown_field", {item["code"] for item in result["errors"]})
            short = self.base("short_answer")
            short["options"] = [{"id": "a", "text": "wrong"}]
            result = store.create(short, wiki_report=REPORT)
            self.assertIn(
                "field_not_allowed", {item["code"] for item in result["errors"]}
            )

    def test_import_preserves_company_and_source_metadata(self):
        with tempfile.TemporaryDirectory() as d:
            store = QuestionStore(Path(d))
            result = store.import_spec(
                {
                    "id": "q-meta",
                    "type": "single_choice",
                    "domain": "llm-inference",
                    "topic": "serving",
                    "concept_id": "batching",
                    "skill": "design",
                    "prompt": "哪项最适合降低排队延迟？",
                    "options": [
                        {"id": "a", "text": "连续批处理"},
                        {"id": "b", "text": "固定大 batch"},
                    ],
                    "correct_option_ids": ["a"],
                    "explanation": "连续批处理可让新请求加入运行中的批次。",
                    "company_tags": ["ByteDance", "NVIDIA"],
                    "source_refs": [
                        {
                            "title": "CUDA C Programming Guide",
                            "url": "https://docs.nvidia.com/cuda/cuda-c-programming-guide/",
                            "kind": "official_docs",
                        }
                    ],
                }
            )
            self.assertIs(result["changed"], True)
            question = store.load("q-meta")
            self.assertEqual(question["company_tags"], ["ByteDance", "NVIDIA"])
            self.assertEqual(question["source_refs"][0]["kind"], "official_docs")
            catalog = store.list()["items"][0]
            self.assertEqual(catalog["company_tags"], ["ByteDance", "NVIDIA"])
            self.assertNotIn("correct_option_ids", catalog)

    def test_import_rejects_malformed_source_metadata(self):
        with tempfile.TemporaryDirectory() as d:
            store = QuestionStore(Path(d))
            spec = {
                "id": "q-meta",
                "type": "single_choice",
                "domain": "llm-inference",
                "topic": "serving",
                "concept_id": "batching",
                "skill": "design",
                "prompt": "哪项最适合降低排队延迟？",
                "options": [
                    {"id": "a", "text": "连续批处理"},
                    {"id": "b", "text": "固定大 batch"},
                ],
                "correct_option_ids": ["a"],
                "company_tags": ["ByteDance", "ByteDance"],
                "source_refs": [{"title": "bad"}],
            }
            result = store.import_spec(spec)
            codes = {item["code"] for item in result["errors"]}
            self.assertIn("company_tags_duplicate", codes)
            self.assertIn("source_ref_required", codes)

    def test_tampered_question_content_is_fail_closed(self):
        with tempfile.TemporaryDirectory() as d:
            store = QuestionStore(Path(d))
            store.create(self.base(), wiki_report=REPORT)
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
            store = QuestionStore(Path(d))
            spec = self.base("multi_choice")
            spec["correct_option_ids"] = ["a", "b"]
            store.create(spec, wiki_report=REPORT)
            result = store.answer("q-one", ["a", "a"])
            self.assertEqual(result["error_code"], "response_options_duplicate")

    def test_choice_response_rejects_unknown_option_ids(self):
        with tempfile.TemporaryDirectory() as d:
            store = QuestionStore(Path(d))
            store.create(self.base(), wiki_report=REPORT)
            self.assertEqual(
                store.answer("q-one", "missing")["error_code"],
                "response_option_unknown",
            )
            multi = self.base("multi_choice")
            multi["id"] = "q-two"
            store.create(multi, wiki_report=REPORT)
            self.assertEqual(
                store.answer("q-two", ["a", "missing"])["error_code"],
                "response_option_unknown",
            )

    def test_import_personal_question_without_wiki_is_idempotent_and_conflict_safe(
        self,
    ):
        with tempfile.TemporaryDirectory() as d:
            source = Path(d) / "q.json"
            source.write_text(
                json.dumps(
                    {
                        "schema_version": "question/v1",
                        "id": "q-import",
                        "type": "single_choice",
                        "domain": "llm-inference",
                        "topic": "kv-cache",
                        "concept_id": "kv-cache-purpose",
                        "skill": "mechanism",
                        "prompt": "KV Cache 的主要作用是什么？",
                        "options": [
                            {"id": "a", "text": "复用 K/V"},
                            {"id": "b", "text": "减少参数"},
                        ],
                        "correct_option_ids": ["a"],
                        "explanation": "复用历史 K/V。",
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )
            store = QuestionStore(Path(d))
            first = store.import_file(source)
            self.assertIs(first["changed"], True)
            self.assertIs(store.import_file(source)["changed"], False)
            changed = json.loads(source.read_text(encoding="utf-8"))
            changed["prompt"] = "changed"
            source.write_text(json.dumps(changed), encoding="utf-8")
            conflict = store.import_file(source)
            self.assertEqual(conflict["errors"][0]["code"], "question_id_conflict")

    def test_import_rejects_external_content_hash_field(self):
        with tempfile.TemporaryDirectory() as d:
            source = Path(d) / "q.json"
            source.write_text(
                json.dumps(
                    {
                        "id": "q-hash",
                        "type": "single_choice",
                        "domain": "llm-inference",
                        "topic": "kv-cache",
                        "concept_id": "kv-cache-purpose",
                        "skill": "mechanism",
                        "prompt": "What does KV cache do?",
                        "options": [
                            {"id": "a", "text": "Reuse K/V"},
                            {"id": "b", "text": "Increase parameters"},
                        ],
                        "correct_option_ids": ["a"],
                        "content_sha256": "sha256:wrong",
                    }
                ),
                encoding="utf-8",
            )
            result = QuestionStore(Path(d)).import_file(source)
            self.assertEqual(result["status"], "blocked")
            self.assertEqual(result["errors"][0]["code"], "unknown_field")

    def test_import_and_score_cloze_with_alias_and_normalization(self):
        with tempfile.TemporaryDirectory() as d:
            source = Path(d) / "cloze.json"
            source.write_text(
                json.dumps(
                    {
                        "id": "q-cloze",
                        "type": "cloze",
                        "domain": "llm-inference",
                        "topic": "serving",
                        "concept_id": "continuous-batching",
                        "skill": "terminology",
                        "prompt": "多个请求动态共享 GPU 执行机会的技术叫什么？",
                        "answer": {
                            "accepted_answers": ["continuous batching"],
                            "aliases": ["连续批处理"],
                            "normalization": {
                                "casefold": True,
                                "trim": True,
                                "collapse_whitespace": True,
                            },
                        },
                        "explanation": "Continuous batching dynamically admits requests.",
                    }
                ),
                encoding="utf-8",
            )
            store = QuestionStore(Path(d))
            self.assertIs(store.import_file(source)["changed"], True)
            correct = store.answer("q-cloze", "  CONTINUOUS   BATCHING ")
            self.assertEqual(correct["grading"]["state"], "graded")
            self.assertEqual(
                correct["grading"]["scoring_provider"], "deterministic_cloze"
            )
            self.assertTrue(correct["grading"]["correct"])
            self.assertEqual(
                correct["grading"]["normalized_response"], "continuous batching"
            )
            wrong = store.answer("q-cloze", "dynamic batching")
            self.assertFalse(wrong["grading"]["correct"])

    def test_cloze_normalization_applies_unicode_nfkc(self):
        with tempfile.TemporaryDirectory() as d:
            source = Path(d) / "cloze.json"
            source.write_text(
                json.dumps(
                    {
                        "id": "q-cloze-nfkc",
                        "type": "cloze",
                        "domain": "llm-inference",
                        "topic": "serving",
                        "concept_id": "batching",
                        "skill": "terminology",
                        "prompt": "技术名称？",
                        "answer": {
                            "accepted_answers": ["continuous batching"],
                            "normalization": {
                                "casefold": True,
                                "trim": True,
                                "collapse_whitespace": True,
                            },
                        },
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )
            store = QuestionStore(Path(d))
            self.assertIs(store.import_file(source)["changed"], True)
            result = store.answer("q-cloze-nfkc", "  ｃｏｎｔｉｎｕｏｕｓ　 batching ")
            self.assertTrue(result["grading"]["correct"])

    def test_cloze_import_rejects_unknown_normalization_rule(self):
        with tempfile.TemporaryDirectory() as d:
            source = Path(d) / "cloze.json"
            source.write_text(
                json.dumps(
                    {
                        "id": "q-cloze-invalid",
                        "type": "cloze",
                        "domain": "llm-inference",
                        "topic": "serving",
                        "concept_id": "continuous-batching",
                        "skill": "terminology",
                        "prompt": "What is it called?",
                        "answer": {
                            "accepted_answers": ["continuous batching"],
                            "normalization": {"fuzzy": True},
                        },
                    }
                ),
                encoding="utf-8",
            )
            result = QuestionStore(Path(d)).import_file(source)
            self.assertEqual(result["status"], "blocked")
            self.assertEqual(
                result["errors"][0]["code"], "answer_normalization_rule_unknown"
            )

    def test_cloze_import_rejects_choice_fields(self):
        with tempfile.TemporaryDirectory() as d:
            source = Path(d) / "cloze.json"
            source.write_text(
                json.dumps(
                    {
                        "id": "q-cloze-choice-fields",
                        "type": "cloze",
                        "domain": "llm-inference",
                        "topic": "serving",
                        "concept_id": "continuous-batching",
                        "skill": "terminology",
                        "prompt": "What is it called?",
                        "options": [
                            {"id": "a", "text": "A"},
                            {"id": "b", "text": "B"},
                        ],
                        "correct_option_ids": ["a"],
                        "answer": {"accepted_answers": ["continuous batching"]},
                    }
                ),
                encoding="utf-8",
            )
            result = QuestionStore(Path(d)).import_file(source)
            self.assertEqual(result["status"], "blocked")
            self.assertEqual(
                {error["field"] for error in result["errors"] if "field" in error},
                {"options", "correct_option_ids"},
            )

    def test_list_filters_catalog_and_excludes_answers(self):
        with tempfile.TemporaryDirectory() as d:
            store = QuestionStore(Path(d))
            source_dir = Path(d) / "imports"
            source_dir.mkdir()
            for suffix, topic, status in (
                ("one", "kv-cache", "enabled"),
                ("two", "batching", "disabled"),
            ):
                (source_dir / f"{suffix}.json").write_text(
                    json.dumps(
                        {
                            "id": f"q-{suffix}",
                            "type": "single_choice",
                            "domain": "llm-inference",
                            "topic": topic,
                            "concept_id": topic,
                            "skill": "mechanism",
                            "prompt": f"Explain {topic}",
                            "options": [
                                {"id": "a", "text": "correct"},
                                {"id": "b", "text": "distractor"},
                            ],
                            "correct_option_ids": ["a"],
                            "answer": "private answer",
                            "explanation": "private explanation",
                            "status": status,
                        }
                    ),
                    encoding="utf-8",
                )
            self.assertEqual(store.import_path(source_dir)["imported"], 2)
            result = store.list(topic="kv-cache")
            self.assertEqual(result["total"], 1)
            self.assertEqual(result["items"][0]["id"], "q-one")
            self.assertNotIn("answer", result["items"][0])
            self.assertNotIn("explanation", result["items"][0])

    def test_get_session_returns_completed_state_and_safe_items(self):
        with tempfile.TemporaryDirectory() as d:
            store = QuestionStore(Path(d))
            source = Path(d) / "question.json"
            source.write_text(
                json.dumps(
                    {
                        "id": "q-session-get",
                        "type": "single_choice",
                        "domain": "llm-inference",
                        "topic": "serving",
                        "concept_id": "batching",
                        "skill": "recall",
                        "prompt": "What is batching?",
                        "options": [
                            {"id": "a", "text": "group requests"},
                            {"id": "b", "text": "change weights"},
                        ],
                        "correct_option_ids": ["a"],
                        "answer": "private",
                        "explanation": "private",
                    }
                ),
                encoding="utf-8",
            )
            store.import_file(source)
            created = store.create_session(size=3)
            session_id = created["session"]["id"]
            store.update_session(session_id, current_index=1, completed=True)
            result = store.get_session(session_id)
            self.assertEqual(result["session"]["status"], "completed")
            self.assertEqual(result["session"]["current_index"], 1)
            self.assertNotIn("answer", result["items"][0])
            self.assertNotIn("explanation", result["items"][0])

    def test_list_isolates_invalid_question_files(self):
        with tempfile.TemporaryDirectory() as d:
            question_dir = Path(d) / "content" / "practice" / "questions"
            question_dir.mkdir(parents=True)
            (question_dir / "broken.json").write_text("{", encoding="utf-8")
            result = QuestionStore(Path(d)).list()
            self.assertEqual(result["total"], 0)
            self.assertEqual(result["invalid"][0]["reason"], "question_invalid")

    def test_disable_and_delete_preserve_review_history(self):
        with tempfile.TemporaryDirectory() as d:
            store = QuestionStore(Path(d))
            source = Path(d) / "question.json"
            source.write_text(
                json.dumps(
                    {
                        "id": "q-lifecycle",
                        "type": "single_choice",
                        "domain": "llm-inference",
                        "topic": "kv-cache",
                        "concept_id": "kv-cache",
                        "skill": "mechanism",
                        "prompt": "Explain KV cache",
                        "options": [
                            {"id": "a", "text": "Reuse K/V"},
                            {"id": "b", "text": "Change tokenizer"},
                        ],
                        "correct_option_ids": ["a"],
                    }
                ),
                encoding="utf-8",
            )
            store.import_file(source)
            disabled = store.disable("q-lifecycle", reason="manual_cleanup")
            self.assertEqual(disabled["lifecycle"], "disabled")
            self.assertEqual(
                store.answer("q-lifecycle", "a")["error_code"], "question_disabled"
            )
            self.assertIs(store.delete("q-lifecycle")["deleted"], True)
            self.assertFalse(store._file("q-lifecycle").exists())

            store.import_file(source)
            store.answer("q-lifecycle", "a")
            preserved = store.delete("q-lifecycle")
            self.assertIs(preserved["deleted"], False)
            self.assertEqual(preserved["lifecycle"], "disabled")
            self.assertEqual(preserved["reason"], "review_history_preserved")
            self.assertTrue(store._file("q-lifecycle").exists())
            self.assertEqual(store.load("q-lifecycle")["status"], "disabled")

    def test_enable_restores_answering_and_import_idempotency(self):
        with tempfile.TemporaryDirectory() as d:
            store = QuestionStore(Path(d))
            source = Path(d) / "question.json"
            source.write_text(
                json.dumps(
                    {
                        "id": "q-enable",
                        "type": "single_choice",
                        "domain": "llm-inference",
                        "topic": "kv-cache",
                        "concept_id": "kv-cache",
                        "skill": "mechanism",
                        "prompt": "Explain KV cache",
                        "options": [
                            {"id": "a", "text": "Reuse K/V"},
                            {"id": "b", "text": "Change tokenizer"},
                        ],
                        "correct_option_ids": ["a"],
                    }
                ),
                encoding="utf-8",
            )
            store.import_file(source)
            store.disable("q-enable", reason="manual_cleanup")
            enabled = store.enable("q-enable")
            self.assertEqual(enabled["lifecycle"], "enabled")
            self.assertTrue(store.answer("q-enable", "a")["grading"]["correct"])
            self.assertIs(store.enable("q-enable")["changed"], False)
            self.assertIs(store.import_file(source)["changed"], False)

    def test_create_session_is_stable_bounded_and_answer_safe(self):
        with tempfile.TemporaryDirectory() as d:
            store = QuestionStore(Path(d))
            source_dir = Path(d) / "imports"
            source_dir.mkdir()
            for index in range(4):
                (source_dir / f"q-{index}.json").write_text(
                    json.dumps(
                        {
                            "id": f"q-session-{index}",
                            "type": "single_choice",
                            "domain": "llm-inference",
                            "topic": "serving",
                            "concept_id": f"concept-{index % 2}",
                            "skill": "recall",
                            "prompt": f"Question {index}",
                            "options": [
                                {"id": "a", "text": "yes"},
                                {"id": "b", "text": "no"},
                            ],
                            "correct_option_ids": ["a"],
                            "answer": "private answer",
                            "explanation": "private explanation",
                        }
                    ),
                    encoding="utf-8",
                )
            self.assertEqual(store.import_path(source_dir)["imported"], 4)
            first = store.create_session(size=3, domain="llm-inference")
            second = store.create_session(size=3, domain="llm-inference")
            self.assertEqual(first["status"], "ok")
            self.assertEqual(first["question_count"], 3)
            self.assertEqual(
                first["session"]["question_ids"], second["session"]["question_ids"]
            )
            self.assertLessEqual(
                max(
                    first["session"]["question_ids"].count(question_id)
                    for question_id in first["session"]["question_ids"]
                ),
                1,
            )
            self.assertNotIn("answer", first["items"][0])
            self.assertNotIn("explanation", first["items"][0])
            self.assertEqual(
                store.create_session(size=4)["error_code"], "session_size_invalid"
            )
            self.assertEqual(
                store.create_session(size=6, concept_id="missing")["question_count"], 0
            )

    def test_create_session_prioritizes_due_then_errors_then_new(self):
        with tempfile.TemporaryDirectory() as d:
            store = QuestionStore(Path(d))
            source_dir = Path(d) / "imports"
            source_dir.mkdir()
            for index in range(3):
                (source_dir / f"q-{index}.json").write_text(
                    json.dumps(
                        {
                            "id": f"q-priority-{index}",
                            "type": "single_choice",
                            "domain": "llm-inference",
                            "topic": "serving",
                            "concept_id": f"concept-{index}",
                            "skill": "recall",
                            "prompt": f"Question {index}",
                            "options": [
                                {"id": "a", "text": "correct"},
                                {"id": "b", "text": "wrong"},
                            ],
                            "correct_option_ids": ["a"],
                        }
                    ),
                    encoding="utf-8",
                )
            store.import_path(source_dir)
            store.review("q-priority-0", 3)
            question = store.load("q-priority-0")
            question["review_state"]["due"] = (
                datetime.now(UTC) - timedelta(minutes=1)
            ).isoformat()
            store._file("q-priority-0").write_text(
                json.dumps(question), encoding="utf-8"
            )
            store.answer("q-priority-1", "b")

            session = store.create_session(size=3)
            self.assertEqual(
                session["session"]["question_ids"],
                ["q-priority-0", "q-priority-1", "q-priority-2"],
            )

    def test_update_session_persists_progress_and_completion(self):
        with tempfile.TemporaryDirectory() as d:
            store = QuestionStore(Path(d))
            source = Path(d) / "question.json"
            source.write_text(
                json.dumps(
                    {
                        "id": "q-session-progress",
                        "type": "single_choice",
                        "domain": "llm-inference",
                        "topic": "serving",
                        "concept_id": "batching",
                        "skill": "recall",
                        "prompt": "What is batching?",
                        "options": [
                            {"id": "a", "text": "group requests"},
                            {"id": "b", "text": "change weights"},
                        ],
                        "correct_option_ids": ["a"],
                    }
                ),
                encoding="utf-8",
            )
            store.import_file(source)
            created = store.create_session(size=3)
            session_id = created["session"]["id"]
            updated = store.update_session(session_id, current_index=1, completed=False)
            self.assertEqual(updated["session"]["current_index"], 1)
            completed = store.update_session(
                session_id, current_index=1, completed=True
            )
            self.assertEqual(completed["session"]["status"], "completed")
            self.assertEqual(completed["session"]["current_index"], 1)

    def test_error_queue_tracks_latest_wrong_attempt_and_filters(self):
        with tempfile.TemporaryDirectory() as d:
            store = QuestionStore(Path(d))
            source_dir = Path(d) / "imports"
            source_dir.mkdir()
            for question_id, topic in (
                ("q-error", "kv-cache"),
                ("q-other", "batching"),
            ):
                (source_dir / f"{question_id}.json").write_text(
                    json.dumps(
                        {
                            "id": question_id,
                            "type": "single_choice",
                            "domain": "llm-inference",
                            "topic": topic,
                            "concept_id": topic,
                            "skill": "recall",
                            "prompt": f"Explain {topic}",
                            "options": [
                                {"id": "a", "text": "correct"},
                                {"id": "b", "text": "wrong"},
                            ],
                            "correct_option_ids": ["a"],
                            "answer": "private answer",
                            "explanation": "private explanation",
                        }
                    ),
                    encoding="utf-8",
                )
            store.import_path(source_dir)
            store.answer("q-error", "b")
            store.answer("q-other", "b")
            result = store.error_queue(topic="kv-cache", limit=1)
            self.assertEqual(result["total"], 1)
            self.assertEqual(result["items"][0]["question_id"], "q-error")
            self.assertNotIn("answer", result["items"][0]["question"])
            self.assertNotIn("explanation", result["items"][0]["question"])
            self.assertEqual(
                store.error_queue(limit=0)["error_code"], "error_queue_limit_invalid"
            )
            store.answer("q-error", "a")
            self.assertEqual(store.error_queue(topic="kv-cache")["total"], 0)

    def test_error_queue_reports_corrupt_review_log(self):
        with tempfile.TemporaryDirectory() as d:
            store = QuestionStore(Path(d))
            source = Path(d) / "question.json"
            source.write_text(
                json.dumps(
                    {
                        "id": "q-corrupt-review",
                        "type": "single_choice",
                        "domain": "llm-inference",
                        "topic": "serving",
                        "concept_id": "batching",
                        "skill": "recall",
                        "prompt": "What is batching?",
                        "options": [
                            {"id": "a", "text": "group requests"},
                            {"id": "b", "text": "change weights"},
                        ],
                        "correct_option_ids": ["a"],
                    }
                ),
                encoding="utf-8",
            )
            store.import_file(source)
            review_path = store.paths.practice_reviews("q-corrupt-review")
            review_path.parent.mkdir(parents=True, exist_ok=True)
            review_path.write_text("{broken\n", encoding="utf-8")
            result = store.error_queue()
            self.assertEqual(result["total"], 0)
            self.assertEqual(result["warnings"][0]["code"], "review_log_invalid")
            self.assertEqual(result["warnings"][0]["question_id"], "q-corrupt-review")

    def test_review_queue_prioritizes_due_and_can_exclude_new(self):
        with tempfile.TemporaryDirectory() as d:
            store = QuestionStore(Path(d))
            source_dir = Path(d) / "imports"
            source_dir.mkdir()
            for index in range(3):
                (source_dir / f"q-{index}.json").write_text(
                    json.dumps(
                        {
                            "id": f"q-queue-{index}",
                            "type": "single_choice",
                            "domain": "llm-inference",
                            "topic": "serving",
                            "concept_id": f"concept-{index}",
                            "skill": "recall",
                            "prompt": f"Question {index}",
                            "options": [
                                {"id": "a", "text": "correct"},
                                {"id": "b", "text": "wrong"},
                            ],
                            "correct_option_ids": ["a"],
                            "answer": "private answer",
                            "explanation": "private explanation",
                        }
                    ),
                    encoding="utf-8",
                )
            store.import_path(source_dir)
            store.review("q-queue-0", 3)
            store.review("q-queue-1", 3)
            now = datetime.now(UTC)
            for question_id, due in (
                ("q-queue-0", now - timedelta(minutes=1)),
                ("q-queue-1", now + timedelta(days=1)),
            ):
                question = store.load(question_id)
                question["review_state"]["due"] = due.isoformat()
                store._file(question_id).write_text(
                    json.dumps(question), encoding="utf-8"
                )
            due_only = store.review_queue(size=3, include_new=False)
            self.assertEqual(due_only["total"], 1)
            self.assertEqual(due_only["items"][0]["queue_kind"], "due")
            self.assertEqual(due_only["items"][0]["question"]["id"], "q-queue-0")
            full = store.review_queue(size=3)
            self.assertEqual(full["total"], 2)
            self.assertEqual(full["items"][0]["queue_kind"], "due")
            self.assertEqual(full["items"][1]["queue_kind"], "new")
            self.assertNotIn("answer", full["items"][0]["question"])
            self.assertEqual(
                store.review_queue(size=4)["error_code"], "queue_size_invalid"
            )

    def test_disabled_question_cannot_be_reviewed(self):
        with tempfile.TemporaryDirectory() as d:
            store = QuestionStore(Path(d))
            source = Path(d) / "question.json"
            source.write_text(
                json.dumps(
                    {
                        "id": "q-disabled-review",
                        "type": "single_choice",
                        "domain": "llm-inference",
                        "topic": "serving",
                        "concept_id": "batching",
                        "skill": "recall",
                        "prompt": "What is batching?",
                        "options": [
                            {"id": "a", "text": "group requests"},
                            {"id": "b", "text": "change weights"},
                        ],
                        "correct_option_ids": ["a"],
                    }
                ),
                encoding="utf-8",
            )
            store.import_file(source)
            store.disable("q-disabled-review")
            result = store.review("q-disabled-review", 3)
            self.assertEqual(result["error_code"], "question_disabled")
            self.assertIsNone(store.load("q-disabled-review")["review_state"])


if __name__ == "__main__":
    unittest.main()
