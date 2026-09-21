"""F008 question authoring, scoring and local review state.

Question facts are derived from a validated Wiki claim.  Answers and review
state live under ``practice/`` and are never consumed by public projection.
FSRS is an optional runtime adapter: absence is reported explicitly.
"""

from __future__ import annotations

import contextlib
import hashlib
import importlib.metadata
import json
import os
import random
import time
import unicodedata
import uuid
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from . import contract, retire_ledger
from .common import atomic_write, canonical_json, safe_id, sha256_bytes
from .content_repository import purge_precondition
from .paths import RepoPaths
from .validation.validator import WikiValidator

QUESTION_SCHEMA = "question/v1"
# 领域结果一律走 tools.contract 统一信封（TD §14）：唯一 status 轴（ok/blocked/
# unavailable），写效果放 ``changed``/``lifecycle``，判分下沉 ``grading``，调度结果
# 作为领域字段。每个操作一份 name/vN 信封 schema（与 CRUD 能力层同构）。
CREATE_SCHEMA = "question-create/v1"
IMPORT_SCHEMA = "question-import/v1"
IMPORT_BATCH_SCHEMA = "question-import-batch/v1"
LIST_SCHEMA = "question-list/v1"
SESSION_SCHEMA = "question-session/v1"
SESSION_PROGRESS_SCHEMA = "question-session-progress/v1"
ERROR_QUEUE_SCHEMA = "question-error-queue/v1"
REVIEW_QUEUE_SCHEMA = "question-review-queue/v1"
LIFECYCLE_SCHEMA = "question-lifecycle/v1"
REFRESH_SCHEMA = "question-refresh/v1"
REFRESH_BATCH_SCHEMA = "question-refresh-batch/v1"
ANSWER_SCHEMA = "question-answer/v1"
REVIEW_SCHEMA = "question-review/v1"
READ_SCHEMA = "question-read/v1"

# 个人库无需长期保留历史 practice 会话；新建会话时把会话文件数收敛到该上限。
SESSION_RETENTION = 100


def _is_imported(result: dict) -> bool:
    """批量导入：单条“新写入”= ok 信封且 ``changed`` 为真。"""
    return result.get("status") == "ok" and result.get("changed") is True


def _is_noop(result: dict) -> bool:
    """批量导入：单条“幂等命中”= ok 信封且 ``changed`` 为假。"""
    return result.get("status") == "ok" and result.get("changed") is False


QUESTION_TYPES = {"single_choice", "multi_choice", "short_answer", "cloze"}
QUESTION_FIELDS = {
    "id",
    "type",
    "vault_id",
    "wiki_id",
    "claim_id",
    "prompt",
    "confidentiality",
    "options",
    "correct_option_ids",
    "answer",
    "explanation",
    "rubric",
    "company_tags",
    "source_refs",
}
IMPORT_FIELDS = {
    "schema_version",
    "id",
    "type",
    "domain",
    "topic",
    "concept_id",
    "skill",
    "prompt",
    "options",
    "correct_option_ids",
    "answer",
    "explanation",
    "rubric",
    "wiki_refs",
    "company_tags",
    "source_refs",
    "status",
}


class FSRSAdapter:
    def __init__(self) -> None:
        self.version = "unavailable"
        try:
            from fsrs import Card, Rating, Scheduler  # type: ignore

            self._Scheduler, self._Card, self._Rating = Scheduler, Card, Rating
            try:
                self.version = importlib.metadata.version("fsrs")
            except importlib.metadata.PackageNotFoundError:
                self.version = "unknown"
        except ImportError:
            self._Scheduler = self._Card = self._Rating = None

    @property
    def available(self) -> bool:
        return self._Scheduler is not None

    def review(self, state: dict | None, rating: int) -> dict:
        if not self.available:
            return {
                "state": "unavailable",
                "reason": "provider_unavailable",
                "scheduler": "fsrs",
                "scheduler_version": self.version,
            }
        try:
            scheduler = self._Scheduler()
            card_state = (
                state.get("card")
                if isinstance(state, dict) and isinstance(state.get("card"), dict)
                else state
            )
            card = self._Card.from_dict(card_state) if card_state else self._Card()
            result = scheduler.review_card(card, self._Rating(rating))
            next_card = result.card if hasattr(result, "card") else result[0]
            card_dict = next_card.to_dict()
            return {
                **card_dict,
                "state": "scheduled",
                "scheduler": "fsrs",
                "scheduler_version": self.version,
                "review_state_schema": "fsrs-card/v1",
                "rating": rating,
                "card": card_dict,
            }
        except Exception as exc:  # noqa: BLE001 - 三方 fsrs 适配边界：异常面未知，归一为 unavailable，绝不伪造调度
            return {
                "state": "unavailable",
                "reason": "scheduler_error",
                "detail": type(exc).__name__,
                "scheduler": "fsrs",
                "scheduler_version": self.version,
            }


class QuestionStore:
    def __init__(self, root: Path) -> None:
        self.root = Path(root).resolve()
        self.paths = RepoPaths(self.root)
        self.fsrs = FSRSAdapter()

    def _file(self, question_id: str) -> Path:
        safe_id(question_id)
        return self.paths.practice_questions / f"{question_id}.json"

    @staticmethod
    def _content_hash(question: dict, *, legacy: bool = False) -> str:
        excluded = {"created_at", "review_state", "content_sha256"}
        if not legacy:
            # Status is mutable lifecycle state; review_state is scheduler state.
            excluded.update({"status", "disabled_reason"})
        return (
            "sha256:"
            + hashlib.sha256(
                canonical_json({k: v for k, v in question.items() if k not in excluded})
            ).hexdigest()
        )

    def _record_answer(self, question_id: str, result: dict, response: Any) -> None:
        path = self.paths.practice_reviews(question_id)
        record = {
            "schema_version": "practice-review-record/v1",
            "question_id": question_id,
            "recorded_at": time.time(),
            "response": response,
            "result": result,
        }
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("ab") as handle:
            handle.write(canonical_json(record) + b"\n")
            handle.flush()
            os.fsync(handle.fileno())

    @staticmethod
    def _validate_spec(spec: dict) -> list[dict]:  # noqa: PLR0915 - explicit Wiki question contract validation
        errors: list[dict] = []
        if not isinstance(spec, dict):
            return [{"code": "question_spec_invalid"}]
        for field in sorted(set(spec) - QUESTION_FIELDS):
            errors.append({"code": "unknown_field", "field": field})
        question_type = spec.get("type")
        if question_type not in QUESTION_TYPES:
            errors.append({"code": "question_type_invalid"})
        try:
            safe_id(str(spec.get("id", "")))
        except ValueError:
            errors.append({"code": "question_id_invalid"})
        if not isinstance(spec.get("prompt"), str) or not spec["prompt"].strip():
            errors.append({"code": "prompt_required"})
        for field in ("wiki_id", "claim_id"):
            if not isinstance(spec.get(field), str) or not spec[field].strip():
                errors.append({"code": f"{field}_required"})
        if question_type in {"single_choice", "multi_choice"}:
            options = spec.get("options")
            correct = spec.get("correct_option_ids")
            if not isinstance(options, list) or len(options) < 2:
                errors.append({"code": "options_required"})
            option_ids = (
                [item.get("id") for item in options if isinstance(item, dict)]
                if isinstance(options, list)
                else []
            )
            if len(option_ids) != len(set(option_ids)) or any(
                not isinstance(value, str) or not value for value in option_ids
            ):
                errors.append({"code": "option_ids_invalid"})
            if not isinstance(correct, list) or not correct:
                errors.append({"code": "correct_options_required"})
            elif any(value not in option_ids for value in correct) or len(
                set(correct)
            ) != len(correct):
                errors.append({"code": "correct_option_id_unknown"})
            if (
                question_type == "single_choice"
                and isinstance(correct, list)
                and len(correct) != 1
            ):
                errors.append({"code": "single_choice_requires_one_answer"})
        if question_type == "short_answer":
            if not isinstance(spec.get("rubric"), list):
                errors.append({"code": "rubric_required"})
            for field in ("options", "correct_option_ids"):
                if field in spec and spec[field] is not None:
                    errors.append(
                        {
                            "code": "field_not_allowed",
                            "field": field,
                            "type": question_type,
                        }
                    )
        if question_type == "cloze":
            if "rubric" in spec or "options" in spec or "correct_option_ids" in spec:
                errors.append({"code": "field_not_allowed", "type": question_type})
            answer = spec.get("answer")
            if not isinstance(answer, dict):
                errors.append({"code": "answer_required"})
            else:
                accepted = answer.get("accepted_answers")
                aliases = answer.get("aliases", [])
                normalization = answer.get("normalization", {})
                if (
                    not isinstance(accepted, list)
                    or not accepted
                    or any(
                        not isinstance(value, str) or not value.strip()
                        for value in accepted
                    )
                ):
                    errors.append({"code": "accepted_answers_required"})
                if not isinstance(aliases, list) or any(
                    not isinstance(value, str) or not value.strip() for value in aliases
                ):
                    errors.append({"code": "answer_aliases_invalid"})
                if not isinstance(normalization, dict):
                    errors.append({"code": "answer_normalization_invalid"})
                elif set(normalization) - {"casefold", "trim", "collapse_whitespace"}:
                    errors.append({"code": "answer_normalization_rule_unknown"})
        company_tags = spec.get("company_tags", [])
        if not isinstance(company_tags, list) or any(
            not isinstance(value, str) or not value.strip() for value in company_tags
        ):
            errors.append({"code": "company_tags_invalid"})
        elif len(company_tags) != len(set(company_tags)):
            errors.append({"code": "company_tags_duplicate"})
        source_refs = spec.get("source_refs", [])
        if not isinstance(source_refs, list):
            errors.append({"code": "source_refs_invalid"})
        else:
            for source in source_refs:
                if not isinstance(source, dict):
                    errors.append({"code": "source_ref_invalid"})
                    continue
                if any(
                    not isinstance(source.get(field), str) or not source[field].strip()
                    for field in ("title", "url", "kind")
                ):
                    errors.append({"code": "source_ref_required"})
                if any(
                    secret in source.get("url", "").lower()
                    for secret in ("token", "api_key", "secret")
                ):
                    errors.append({"code": "source_ref_sensitive_url"})
        return errors

    def _wiki_report(self, wiki_path: Path) -> dict:
        return WikiValidator(self.root).validate(wiki_path)

    def create(
        self,
        spec: dict,
        *,
        wiki_path: Path | None = None,
        wiki_report: dict | None = None,
    ) -> dict:
        errors = self._validate_spec(spec)
        report = wiki_report or (self._wiki_report(wiki_path) if wiki_path else None)
        if not report or not report.get("valid"):
            errors.append({"code": "wiki_unverified"})
        else:
            derived = report.get("derived") or {}
            if report.get("object_ref", {}).get("object_type") != "wiki" or derived.get(
                "evidence_state"
            ) not in {"supported", "corroborated"}:
                errors.append({"code": "wiki_claim_unverified"})
            if report.get("object_ref", {}).get("object_id") != spec.get("wiki_id"):
                errors.append({"code": "wiki_id_mismatch"})
            claim_ids = {
                item.get("claim_id")
                for item in (report.get("metadata", {}).get("evidence") or [])
                if isinstance(item, dict)
            }
            if spec.get("claim_id") not in claim_ids:
                errors.append({"code": "claim_not_found"})
        if errors:
            return contract.blocked(
                CREATE_SCHEMA, "question_spec_invalid", errors=errors
            )
        claim_id = str(spec["claim_id"])
        claim = {
            "vault_id": spec.get("vault_id", "public"),
            "wiki_id": spec["wiki_id"],
            "claim_id": claim_id,
            "content_sha256": report.get("hashes", {}).get("content_sha256"),
            "evidence_sha256": report.get("hashes", {}).get("evidence_sha256"),
        }
        question = {
            "schema_version": QUESTION_SCHEMA,
            "id": spec["id"],
            "type": spec["type"],
            "confidentiality": spec.get("confidentiality", "public"),
            "wiki_claim": claim,
            "prompt": spec["prompt"],
            "options": spec.get("options"),
            "correct_option_ids": spec.get("correct_option_ids"),
            "answer": spec.get("answer"),
            "explanation": spec.get("explanation"),
            "rubric": spec.get("rubric"),
            "company_tags": spec.get("company_tags", []),
            "source_refs": spec.get("source_refs", []),
            "status": "enabled",
            "created_at": time.time(),
            "review_state": None,
        }
        question["content_sha256"] = self._content_hash(question)
        atomic_write(
            self._file(question["id"]), canonical_json(question) + b"\n", 0o600
        )
        return contract.ok(CREATE_SCHEMA, changed=True, question=question)

    @staticmethod
    def _validate_import_spec(spec: dict) -> list[dict]:  # noqa: PLR0915 - explicit import contract validation
        errors: list[dict] = []
        if not isinstance(spec, dict):
            return [{"code": "question_spec_invalid"}]
        for field in sorted(set(spec) - IMPORT_FIELDS):
            errors.append({"code": "unknown_field", "field": field})
        if spec.get("schema_version") not in {None, QUESTION_SCHEMA}:
            errors.append({"code": "question_schema_invalid"})
        try:
            safe_id(str(spec.get("id", "")))
        except ValueError:
            errors.append({"code": "question_id_invalid"})
        if spec.get("type") not in {
            "single_choice",
            "multi_choice",
            "cloze",
            "short_answer",
        }:
            errors.append({"code": "question_type_invalid"})
        for field in ("prompt", "domain", "topic", "concept_id", "skill"):
            if not isinstance(spec.get(field), str) or not spec[field].strip():
                errors.append({"code": f"{field}_required"})
        # rubric 仅 short_answer 使用；其余题型出现即非法（与 cloze 的 field_not_allowed 一致）。
        if spec.get("type") != "short_answer" and spec.get("rubric") is not None:
            errors.append(
                {
                    "code": "field_not_allowed",
                    "field": "rubric",
                    "type": spec.get("type"),
                }
            )
        options = spec.get("options")
        correct = spec.get("correct_option_ids")
        option_ids = []
        if spec.get("type") in {"single_choice", "multi_choice"}:
            if not isinstance(options, list) or len(options) < 2:
                errors.append({"code": "options_required"})
            if isinstance(options, list):
                for item in options:
                    if (
                        not isinstance(item, dict)
                        or not isinstance(item.get("id"), str)
                        or not isinstance(item.get("text"), str)
                    ):
                        errors.append({"code": "option_invalid"})
                        continue
                    option_ids.append(item["id"])
        if spec.get("type") == "cloze":
            answer = spec.get("answer")
            for field in ("options", "correct_option_ids"):
                if field in spec and spec[field] is not None:
                    errors.append(
                        {
                            "code": "field_not_allowed",
                            "field": field,
                            "type": "cloze",
                        }
                    )
            if not isinstance(answer, dict):
                errors.append({"code": "answer_required"})
            else:
                accepted = answer.get("accepted_answers")
                aliases = answer.get("aliases", [])
                normalization = answer.get("normalization", {})
                if (
                    not isinstance(accepted, list)
                    or not accepted
                    or any(
                        not isinstance(value, str) or not value.strip()
                        for value in accepted
                    )
                ):
                    errors.append({"code": "accepted_answers_required"})
                if not isinstance(aliases, list) or any(
                    not isinstance(value, str) or not value.strip() for value in aliases
                ):
                    errors.append({"code": "answer_aliases_invalid"})
                if not isinstance(normalization, dict):
                    errors.append({"code": "answer_normalization_invalid"})
                elif set(normalization) - {"casefold", "trim", "collapse_whitespace"}:
                    errors.append({"code": "answer_normalization_rule_unknown"})
        if spec.get("type") == "short_answer":
            for field in ("options", "correct_option_ids", "answer"):
                if field in spec and spec[field] is not None:
                    errors.append(
                        {
                            "code": "field_not_allowed",
                            "field": field,
                            "type": "short_answer",
                        }
                    )
            rubric = spec.get("rubric")
            # rubric = 评分要点列表；每项为字符串（既是准则也是关键词）或
            # {label?, keywords: [str]}，与 answer() 确定性/人工/LLM 判分口径一致。
            if not isinstance(rubric, list) or not rubric:
                errors.append({"code": "rubric_required"})
            else:
                for item in rubric:
                    valid = (isinstance(item, str) and item.strip()) or (
                        isinstance(item, dict)
                        and isinstance(item.get("keywords"), list)
                        and bool(item["keywords"])
                        and all(
                            isinstance(k, str) and k.strip() for k in item["keywords"]
                        )
                    )
                    if not valid:
                        errors.append({"code": "rubric_item_invalid"})
        if len(option_ids) != len(set(option_ids)):
            errors.append({"code": "option_ids_invalid"})
        if spec.get("type") in {"single_choice", "multi_choice"}:
            if not isinstance(correct, list) or not correct:
                errors.append({"code": "correct_options_required"})
            elif any(value not in option_ids for value in correct) or len(
                set(correct)
            ) != len(correct):
                errors.append({"code": "correct_option_id_unknown"})
            if (
                spec.get("type") == "single_choice"
                and isinstance(correct, list)
                and len(correct) != 1
            ):
                errors.append({"code": "single_choice_requires_one_answer"})
        if "wiki_refs" in spec and not isinstance(spec["wiki_refs"], list):
            errors.append({"code": "wiki_refs_invalid"})
        company_tags = spec.get("company_tags", [])
        if not isinstance(company_tags, list) or any(
            not isinstance(value, str) or not value.strip() for value in company_tags
        ):
            errors.append({"code": "company_tags_invalid"})
        elif len(company_tags) != len(set(company_tags)):
            errors.append({"code": "company_tags_duplicate"})
        source_refs = spec.get("source_refs", [])
        if not isinstance(source_refs, list):
            errors.append({"code": "source_refs_invalid"})
        else:
            for source in source_refs:
                if not isinstance(source, dict):
                    errors.append({"code": "source_ref_invalid"})
                    continue
                if any(
                    not isinstance(source.get(field), str) or not source[field].strip()
                    for field in ("title", "url", "kind")
                ):
                    errors.append({"code": "source_ref_required"})
                if any(
                    secret in source.get("url", "").lower()
                    for secret in ("token", "api_key", "secret")
                ):
                    errors.append({"code": "source_ref_sensitive_url"})
        if spec.get("status", "enabled") not in {"enabled", "disabled"}:
            errors.append({"code": "question_status_invalid"})
        return errors

    @staticmethod
    def _import_content_hash(question: dict) -> str:
        excluded = {
            "content_sha256",
            "status",
            "disabled_reason",
            "created_at",
            "review_state",
        }
        return sha256_bytes(
            canonical_json(
                {key: value for key, value in question.items() if key not in excluded}
            )
        )

    def import_file(self, source: Path) -> dict:
        """Import one standalone personal question without requiring a Wiki claim."""
        try:
            spec = json.loads(source.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            return contract.blocked(
                IMPORT_SCHEMA,
                "question_json_invalid",
                source=str(source),
                errors=[
                    {"code": "question_json_invalid", "detail": type(exc).__name__}
                ],
            )
        result = self.import_spec(spec)
        if result["status"] == "blocked":
            result["source"] = str(source)
        return result

    def import_spec(self, spec: dict) -> dict:
        """Import one standalone personal question from an already parsed object."""
        errors = self._validate_import_spec(spec)
        if errors:
            return contract.blocked(
                IMPORT_SCHEMA, "question_spec_invalid", errors=errors
            )
        question = {
            "schema_version": QUESTION_SCHEMA,
            "id": spec["id"],
            "type": spec["type"],
            "domain": spec["domain"],
            "topic": spec["topic"],
            "concept_id": spec["concept_id"],
            "skill": spec["skill"],
            "prompt": spec["prompt"],
            "options": spec.get("options"),
            "correct_option_ids": spec.get("correct_option_ids"),
            "answer": spec.get("answer"),
            "explanation": spec.get("explanation", ""),
            "rubric": spec.get("rubric"),
            "wiki_refs": spec.get("wiki_refs", []),
            "company_tags": spec.get("company_tags", []),
            "source_refs": spec.get("source_refs", []),
            "status": spec.get("status", "enabled"),
            "created_at": time.time(),
            "review_state": None,
        }
        question["content_sha256"] = self._import_content_hash(question)
        target = self._file(question["id"])
        if target.exists():
            try:
                existing = self.load(question["id"])
            except (OSError, ValueError, json.JSONDecodeError) as exc:
                return contract.blocked(
                    IMPORT_SCHEMA,
                    "existing_question_invalid",
                    errors=[
                        {
                            "code": "existing_question_invalid",
                            "detail": type(exc).__name__,
                        }
                    ],
                )
            if self._import_content_hash(existing) == self._import_content_hash(
                question
            ):
                return contract.ok(
                    IMPORT_SCHEMA,
                    changed=False,
                    question_id=question["id"],
                    content_sha256=question["content_sha256"],
                )
            return contract.blocked(
                IMPORT_SCHEMA,
                "question_id_conflict",
                question_id=question["id"],
                errors=[{"code": "question_id_conflict"}],
            )
        atomic_write(target, canonical_json(question) + b"\n", 0o600)
        return contract.ok(
            IMPORT_SCHEMA,
            changed=True,
            question_id=question["id"],
            content_sha256=question["content_sha256"],
            path=str(target),
        )

    def import_path(self, source: Path) -> dict:
        source = Path(source)
        files = (
            [source]
            if source.is_file()
            else sorted(source.glob("*.json"))
            if source.is_dir()
            else []
        )
        if not files:
            return contract.blocked(
                IMPORT_BATCH_SCHEMA,
                "question_import_source_empty",
                source=str(source),
                errors=[{"code": "question_import_source_empty"}],
            )
        results = [self.import_file(path) for path in files]
        imported = sum(_is_imported(item) for item in results)
        return contract.ok(
            IMPORT_BATCH_SCHEMA,
            changed=imported > 0,
            source=str(source),
            total=len(results),
            imported=imported,
            noop=sum(_is_noop(item) for item in results),
            blocked=sum(item["status"] == "blocked" for item in results),
            results=results,
        )

    @staticmethod
    def _catalog_item(question: dict) -> dict:
        """Return the prompt-side shape; answers and explanations stay private."""
        return {
            key: question.get(key)
            for key in (
                "id",
                "type",
                "domain",
                "topic",
                "concept_id",
                "skill",
                "prompt",
                "options",
                "wiki_refs",
                "company_tags",
                "source_refs",
                "status",
            )
            if key in question
        }

    def _scan_questions(
        self,
        *,
        domain: str | None = None,
        topic: str | None = None,
        skill: str | None = None,
        status: str = "enabled",
    ) -> tuple[list[dict], list[dict]]:
        """单次读盘扫描题库：每个题文件只 ``load`` 一次（读+schema+hash 校验）。

        返回 ``(questions, invalid)``——已按分类过滤的**完整**题对象（含
        ``review_state`` 等调度态）与损坏题清单。``list`` 与三个队列构造器共用它，
        消除"先 list 读一遍、再逐题 load 二次读盘"的 N+1（为题量增长做准备）。
        """
        questions: list[dict] = []
        invalid: list[dict] = []
        for path in sorted(self.paths.practice_questions.glob("*.json")):
            try:
                question = self.load(path.stem)
            except (OSError, ValueError, json.JSONDecodeError) as exc:
                invalid.append(
                    {
                        "question_id": path.stem,
                        "reason": "question_invalid",
                        "detail": type(exc).__name__,
                    }
                )
                continue
            if status != "all" and question.get("status", "enabled") != status:
                continue
            if domain is not None and question.get("domain") != domain:
                continue
            if topic is not None and question.get("topic") != topic:
                continue
            if skill is not None and question.get("skill") != skill:
                continue
            questions.append(question)
        return questions, invalid

    def _latest_review_record(self, question_id: str) -> tuple[dict | None, bool]:
        """复习日志（append-only JSONL）中最新一条属于该题的记录。

        返回 ``(record | None, read_failed)``：文件不存在 → ``(None, False)``；
        读取/解析失败 → ``(None, True)``（调用方据此决定告警或忽略）。
        """
        path = self.paths.practice_reviews(question_id)
        if not path.exists():
            return None, False
        latest: dict | None = None
        try:
            for line in path.read_text(encoding="utf-8").splitlines():
                record = json.loads(line)
                if (
                    isinstance(record, dict)
                    and record.get("question_id") == question_id
                    and isinstance(record.get("recorded_at"), (int, float))
                    and (
                        latest is None or record["recorded_at"] > latest["recorded_at"]
                    )
                ):
                    latest = record
        except (OSError, UnicodeError, json.JSONDecodeError):
            return None, True
        return latest, False

    @staticmethod
    def _is_error_result(result: Any) -> bool:
        """最近一次判分是否算"错题"：已判分且 correct=False 或 score<1。"""
        return (
            isinstance(result, dict)
            and result.get("state") == "graded"
            and (result.get("correct") is False or result.get("score", 1) < 1)
        )

    def list(
        self,
        *,
        domain: str | None = None,
        topic: str | None = None,
        skill: str | None = None,
        status: str = "enabled",
    ) -> dict:
        """List valid local questions with optional classification filters."""
        if status not in {"enabled", "disabled", "all"}:
            return contract.blocked(LIST_SCHEMA, "question_status_invalid")
        questions, invalid = self._scan_questions(
            domain=domain, topic=topic, skill=skill, status=status
        )
        items = [self._catalog_item(question) for question in questions]
        return contract.ok(LIST_SCHEMA, total=len(items), items=items, invalid=invalid)

    def create_session(
        self,
        *,
        size: int = 6,
        domain: str | None = None,
        topic: str | None = None,
        concept_id: str | None = None,
        skill: str | None = None,
        shuffle: bool = False,
        seed: int | None = None,
    ) -> dict:
        if size not in {3, 6, 10}:
            return contract.blocked(SESSION_SCHEMA, "session_size_invalid")
        questions, invalid = self._scan_questions(
            domain=domain, topic=topic, skill=skill, status="enabled"
        )
        if invalid:
            return contract.blocked(
                SESSION_SCHEMA, "question_catalog_invalid", invalid=invalid
            )
        candidates = [
            question
            for question in questions
            if concept_id is None or question.get("concept_id") == concept_id
        ]
        if not candidates:
            return contract.ok(
                SESSION_SCHEMA,
                changed=False,
                session=None,
                items=[],
                question_count=0,
                next_action="import_question",
            )
        # Build deterministic buckets: due reviews first, then active errors, then new
        # questions. Future reviews are eligible only as a final fallback.
        now = datetime.now(UTC)
        due_ids: set[str] = set()
        reviewed_ids: set[str] = set()
        error_ids: set[str] = set()
        for question in candidates:
            qid = question["id"]
            review_state = question.get("review_state")
            if isinstance(review_state, dict):
                reviewed_ids.add(qid)
                try:
                    due = datetime.fromisoformat(str(review_state.get("due")))
                    if due.tzinfo is None:
                        due = due.replace(tzinfo=UTC)
                    if due <= now:
                        due_ids.add(qid)
                except (TypeError, ValueError):
                    pass
            latest, _ = self._latest_review_record(qid)
            result = latest.get("result") if isinstance(latest, dict) else None
            if self._is_error_result(result):
                error_ids.add(qid)

        # 默认按 (concept_id, id) 稳定排序，重复调用顺序一致；shuffle=True 时在每个
        # 优先级桶内做可选随机（seed 可复现）。保留 due→errors→new 的桶优先级，
        # 只打乱桶内次序——既满足"乱序做题"，又不破坏 FSRS 到期题优先的调度语义。
        # S311: 顺序打乱与安全无关，用普通伪随机即可（可选 seed 复现）。
        rng = random.Random(seed) if shuffle else None  # noqa: S311

        def order(items: list[dict]) -> list[dict]:
            if rng is not None:
                shuffled = list(items)
                rng.shuffle(shuffled)
                return shuffled
            return sorted(items, key=lambda q: (str(q.get("concept_id", "")), q["id"]))

        due_items = order([q for q in candidates if q["id"] in due_ids])
        error_items = order(
            [q for q in candidates if q["id"] in error_ids and q["id"] not in due_ids]
        )
        new_items = order(
            [
                q
                for q in candidates
                if q["id"] not in reviewed_ids and q["id"] not in error_ids
            ]
        )
        fallback_items = order(
            [
                q
                for q in candidates
                if q["id"] not in due_ids
                and q["id"] not in error_ids
                and q["id"] in reviewed_ids
            ]
        )
        ordered = due_items + error_items + new_items + fallback_items
        selected: list[dict] = []
        concept_counts: dict[str, int] = {}
        for question in ordered:
            concept = str(question.get("concept_id", ""))
            if concept_counts.get(concept, 0) >= 2:
                continue
            selected.append(question)
            concept_counts[concept] = concept_counts.get(concept, 0) + 1
            if len(selected) == size:
                break
        session_id = f"session-{uuid.uuid4().hex[:16]}"
        session = {
            "schema_version": "practice-session/v1",
            "id": session_id,
            "created_at": time.time(),
            "status": "active",
            "filters": {
                "domain": domain,
                "topic": topic,
                "concept_id": concept_id,
                "skill": skill,
            },
            "question_ids": [item["id"] for item in selected],
            "current_index": 0,
            "completed": False,
            "order": "random" if shuffle else "smart",
        }
        atomic_write(
            self.paths.practice_session(session_id),
            canonical_json(session) + b"\n",
            0o600,
        )
        self._prune_sessions()
        return contract.ok(
            SESSION_SCHEMA,
            changed=True,
            session=session,
            items=[self._catalog_item(question) for question in selected],
            question_count=len(selected),
        )

    def _prune_sessions(self, *, keep: int = SESSION_RETENTION) -> None:
        """把 practice-session 文件收敛到最近 ``keep`` 个（按 mtime，新→旧保留）。

        纯卫生操作、尽力而为：目录不存在、stat/删除失败都静默跳过，绝不阻断会话创建。
        """
        directory = self.paths.practice_sessions_root
        try:
            files = list(directory.glob("session-*.json"))
        except OSError:
            return
        entries: list[tuple[float, Path]] = []
        for path in files:
            try:
                entries.append((path.stat().st_mtime, path))
            except OSError:
                continue
        if len(entries) <= keep:
            return
        entries.sort(key=lambda entry: entry[0], reverse=True)
        for _, path in entries[keep:]:
            with contextlib.suppress(OSError):
                path.unlink()

    def update_session(
        self,
        session_id: str,
        *,
        current_index: int,
        completed: bool = False,
    ) -> dict:
        safe_id(session_id)
        path = self.paths.practice_session(session_id)
        try:
            session = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            raise ValueError("session_not_found") from exc
        if (
            not isinstance(session, dict)
            or session.get("schema_version") != "practice-session/v1"
            or session.get("id") != session_id
        ):
            raise ValueError("session_invalid")
        question_ids = session.get("question_ids")
        if not isinstance(question_ids, list) or not all(
            isinstance(item, str) for item in question_ids
        ):
            raise ValueError("session_invalid")
        if not isinstance(current_index, int) or not 0 <= current_index <= len(
            question_ids
        ):
            raise ValueError("session_index_invalid")
        if completed and current_index != len(question_ids):
            raise ValueError("session_completion_invalid")
        session["current_index"] = current_index
        session["completed"] = completed
        session["status"] = "completed" if completed else "active"
        atomic_write(path, canonical_json(session) + b"\n", 0o600)
        return contract.ok(SESSION_PROGRESS_SCHEMA, changed=True, session=session)

    def get_session(self, session_id: str) -> dict:
        safe_id(session_id)
        path = self.paths.practice_session(session_id)
        try:
            session = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            raise ValueError("session_not_found") from exc
        if (
            not isinstance(session, dict)
            or session.get("schema_version") != "practice-session/v1"
            or session.get("id") != session_id
        ):
            raise ValueError("session_invalid")
        question_ids = session.get("question_ids")
        current_index = session.get("current_index")
        if (
            not isinstance(question_ids, list)
            or not all(isinstance(item, str) for item in question_ids)
            or not isinstance(current_index, int)
            or not 0 <= current_index <= len(question_ids)
        ):
            raise ValueError("session_invalid")
        items = []
        for question_id in question_ids:
            question = self.load(question_id)
            if question.get("status") == "enabled":
                items.append(self._catalog_item(question))
        return contract.ok(
            SESSION_SCHEMA,
            session=session,
            items=items,
            question_count=len(items),
        )

    def error_queue(
        self,
        *,
        domain: str | None = None,
        topic: str | None = None,
        concept_id: str | None = None,
        skill: str | None = None,
        limit: int = 10,
    ) -> dict:
        if not 1 <= limit <= 50:
            return contract.blocked(ERROR_QUEUE_SCHEMA, "error_queue_limit_invalid")
        questions, invalid = self._scan_questions(
            domain=domain, topic=topic, skill=skill, status="enabled"
        )
        if invalid:
            return contract.blocked(
                ERROR_QUEUE_SCHEMA, "question_catalog_invalid", invalid=invalid
            )
        errors: list[dict] = []
        warnings: list[dict] = []
        for question in questions:
            if concept_id is not None and question.get("concept_id") != concept_id:
                continue
            qid = question["id"]
            latest, read_failed = self._latest_review_record(qid)
            if read_failed:
                warnings.append(
                    {
                        "code": "review_log_invalid",
                        "question_id": qid,
                        "detail": "review_log_unreadable",
                    }
                )
                continue
            result = latest.get("result") if isinstance(latest, dict) else None
            if not self._is_error_result(result):
                continue
            errors.append(
                {
                    "question_id": qid,
                    "last_error_at": latest["recorded_at"],
                    "last_result": {
                        key: result[key]
                        for key in ("score", "correct", "scoring_provider")
                        if key in result
                    },
                    "question": self._catalog_item(question),
                }
            )
        errors.sort(key=lambda item: (-item["last_error_at"], item["question_id"]))
        return contract.ok(
            ERROR_QUEUE_SCHEMA,
            total=min(len(errors), limit),
            items=errors[:limit],
            warnings=warnings,
        )

    def review_queue(
        self,
        *,
        size: int = 6,
        domain: str | None = None,
        topic: str | None = None,
        concept_id: str | None = None,
        skill: str | None = None,
        include_new: bool = True,
    ) -> dict:
        if size not in {3, 6, 10}:
            return contract.blocked(REVIEW_QUEUE_SCHEMA, "queue_size_invalid")
        questions, invalid = self._scan_questions(
            domain=domain, topic=topic, skill=skill, status="enabled"
        )
        if invalid:
            return contract.blocked(
                REVIEW_QUEUE_SCHEMA, "question_catalog_invalid", invalid=invalid
            )
        candidates = [
            question
            for question in questions
            if concept_id is None or question.get("concept_id") == concept_id
        ]
        now = datetime.now(UTC)
        due: list[tuple[datetime, dict]] = []
        new: list[dict] = []
        for question in candidates:
            review_state = question.get("review_state")
            if not isinstance(review_state, dict):
                new.append(question)
                continue
            due_value = review_state.get("due")
            try:
                parsed_due = datetime.fromisoformat(str(due_value))
                if parsed_due.tzinfo is None:
                    parsed_due = parsed_due.replace(tzinfo=UTC)
            except (TypeError, ValueError):
                continue
            if parsed_due <= now:
                due.append((parsed_due, question))
        due.sort(key=lambda pair: (pair[0], pair[1]["id"]))
        new.sort(key=lambda q: (str(q.get("concept_id", "")), q["id"]))
        selected: list[dict] = [
            {
                "queue_kind": "due",
                "due": due_value.isoformat(),
                "question": self._catalog_item(question),
            }
            for due_value, question in due[:size]
        ]
        if include_new and len(selected) < size:
            selected.extend(
                {
                    "queue_kind": "new",
                    "due": None,
                    "question": self._catalog_item(question),
                }
                for question in new[: size - len(selected)]
            )
        return contract.ok(
            REVIEW_QUEUE_SCHEMA,
            total=len(selected),
            items=selected,
            next_action=None if selected else "import_question",
        )

    def disable(self, question_id: str, *, reason: str = "manual") -> dict:
        question = self.load(question_id)
        if question.get("status") == "disabled":
            return contract.ok(
                LIFECYCLE_SCHEMA,
                changed=False,
                question_id=question_id,
                lifecycle="disabled",
            )
        question["status"] = "disabled"
        question["disabled_reason"] = reason
        atomic_write(self._file(question_id), canonical_json(question) + b"\n", 0o600)
        return contract.ok(
            LIFECYCLE_SCHEMA,
            changed=True,
            question_id=question_id,
            lifecycle="disabled",
            reason=reason,
        )

    def enable(self, question_id: str) -> dict:
        question = self.load(question_id)
        if question.get("status", "enabled") == "enabled":
            return contract.ok(
                LIFECYCLE_SCHEMA,
                changed=False,
                question_id=question_id,
                lifecycle="enabled",
            )
        question["status"] = "enabled"
        question.pop("disabled_reason", None)
        atomic_write(self._file(question_id), canonical_json(question) + b"\n", 0o600)
        return contract.ok(
            LIFECYCLE_SCHEMA,
            changed=True,
            question_id=question_id,
            lifecycle="enabled",
        )

    def delete(self, question_id: str) -> dict:
        """软删（可恢复）：登记删除墓碑 + 置 disabled，**绝不物理删**（对齐 source/wiki）。

        物理回收由 `purge`（过宽限期）承担，形成两阶段删除。复习历史随文件一起保留，
        purge 时才一并回收。
        """
        self.load(question_id)  # 缺失/损坏 → raise，由边界归一
        already = retire_ledger.is_retired(self.paths, "question", question_id)
        self.disable(question_id, reason="deleted")
        if not already:
            retire_ledger.append_retire(
                self.paths,
                "question",
                vault_id="local",
                object_id=question_id,
                reason="delete_requested",
            )
        return contract.ok(
            LIFECYCLE_SCHEMA,
            changed=not already,
            deleted=False,
            question_id=question_id,
            lifecycle="disabled",
        )

    def purge(self, question_id: str, *, grace_days: int | None = None) -> dict:
        """硬删（永久）：须先 delete（软删）且过宽限期，再物理删 practice 文件 + 复习历史。"""
        schema = "question-purge/v1"
        cond = purge_precondition(
            self.paths, "question", question_id, self.root, grace_days=grace_days
        )
        if cond == "already":
            return contract.ok(
                schema, changed=False, purged=True, question_id=question_id
            )
        if cond is not None:
            return contract.blocked(schema, cond, question_id=question_id)
        try:
            file = self._file(question_id)
        except ValueError:
            return contract.blocked(
                schema, "question_not_found", question_id=question_id
            )
        existed = file.exists()
        try:
            file.unlink(missing_ok=True)
            review = self.paths.practice_reviews(question_id)
            if review.exists():
                review.unlink()
        except OSError as exc:
            return contract.blocked(schema, "purge_failed", reason=str(exc))
        retire_ledger.append_purge(
            self.paths,
            "question",
            vault_id="local",
            object_id=question_id,
            reason="purge_requested",
        )
        return contract.ok(
            schema, changed=existed, purged=True, question_id=question_id
        )

    def load(self, question_id: str) -> dict:
        question = json.loads(self._file(question_id).read_text(encoding="utf-8"))
        if (
            not isinstance(question, dict)
            or question.get("schema_version") != QUESTION_SCHEMA
        ):
            raise ValueError("question_schema_invalid")
        if question.get("id") != question_id:
            raise ValueError("question_id_mismatch")
        stored = question.get("content_sha256")
        expected = self._content_hash(question)
        legacy_expected = self._content_hash(question, legacy=True)
        if stored not in {expected, legacy_expected}:
            raise ValueError("question_hash_mismatch")
        return question

    # ---- ADR-0017 能力接口别名：与 source/wiki Repository 的动词对齐 ----
    # question 不是 vault 作用域的 managed 对象（单一 practice 根，无 object_ref），
    # 故不继承 ManagedObjectRepository；这里补齐 read/exists 两个能力层别名，
    # 使三类实体共享同一组读动词，行为不变（read 信封化 load）。delete 沿用既有方法。
    def exists(self, question_id: str) -> bool:
        """题目文件是否存在（能力探测用；不做 schema/hash 校验）。非法 id 视为不存在。"""
        try:
            return self._file(question_id).exists()
        except ValueError:
            return False

    def read(self, question_id: str) -> dict:
        """信封化的单题读入口（对齐 source/wiki repo 的 read 契约）。

        ``load`` 是内部严格加载（不合法即抛 ``ValueError``）；``read`` 是能力层入口：
        缺失/非法 id → ``blocked/question_not_found``，存量损坏（schema/hash/id 不符）
        → ``blocked/existing_question_invalid``，成功 → ``ok`` + ``question``。
        """
        if not self.exists(question_id):
            return contract.blocked(
                READ_SCHEMA, "question_not_found", question_id=question_id
            )
        try:
            question = self.load(question_id)
        except (OSError, ValueError) as exc:
            return contract.blocked(
                READ_SCHEMA,
                "existing_question_invalid",
                question_id=question_id,
                reason=str(exc),
            )
        return contract.ok(READ_SCHEMA, question_id=question_id, question=question)

    def _score_cloze(self, question: dict, response: Any) -> dict:
        answer = question.get("answer") or {}
        normalization = answer.get("normalization") or {}

        def normalize(value: Any) -> str:
            normalized = unicodedata.normalize("NFKC", str(value))
            if normalization.get("trim", True):
                normalized = normalized.strip()
            if normalization.get("collapse_whitespace", True):
                normalized = " ".join(normalized.split())
            if normalization.get("casefold", True):
                normalized = normalized.casefold()
            return normalized

        expected = [
            normalize(value)
            for value in (answer.get("accepted_answers") or [])
            + (answer.get("aliases") or [])
        ]
        observed = normalize(response)
        correct = bool(observed) and observed in expected
        result = {
            "state": "graded",
            "scoring_provider": "deterministic_cloze",
            "score": 1.0 if correct else 0.0,
            "correct": correct,
            "normalized_response": observed,
        }
        self._record_answer(question["id"], result, response)
        return result

    def refresh_status(self, question_id: str, wiki_report: dict) -> dict:
        """Revalidate the claim binding and disable stale questions atomically."""
        question = self.load(question_id)
        claim = question.get("wiki_claim", {})
        hashes = wiki_report.get("hashes", {}) if isinstance(wiki_report, dict) else {}
        valid = bool(wiki_report.get("valid")) and (
            wiki_report.get("derived") or {}
        ).get("evidence_state") in {"supported", "corroborated"}
        report_ref = (
            wiki_report.get("object_ref") or {} if isinstance(wiki_report, dict) else {}
        )
        report_claim_ids = (
            {
                item.get("claim_id")
                for item in ((wiki_report.get("metadata") or {}).get("evidence") or [])
                if isinstance(item, dict)
            }
            if isinstance(wiki_report, dict)
            else set()
        )
        valid = (
            valid
            and report_ref.get("object_id") == claim.get("wiki_id")
            and claim.get("claim_id") in report_claim_ids
        )
        valid = (
            valid
            and claim.get("content_sha256") == hashes.get("content_sha256")
            and claim.get("evidence_sha256") == hashes.get("evidence_sha256")
        )
        newly_disabled = not valid and question.get("status") != "disabled"
        if newly_disabled:
            question["status"] = "disabled"
            question["disabled_reason"] = "claim_binding_stale"
            atomic_write(
                self._file(question_id), canonical_json(question) + b"\n", 0o600
            )
        return contract.ok(
            REFRESH_SCHEMA,
            changed=newly_disabled,
            question_id=question_id,
            lifecycle="enabled" if valid else "disabled",
            reason=None if valid else "claim_binding_stale",
        )

    def refresh_all(self, wiki_reports: dict[str, dict]) -> dict:
        """Revalidate every local question against reports keyed by wiki_id."""
        results: list[dict] = []
        for path in sorted(self.paths.practice_questions.glob("*.json")):
            try:
                question_id = path.stem
                question = self.load(question_id)
                wiki_id = str((question.get("wiki_claim") or {}).get("wiki_id", ""))
                results.append(
                    self.refresh_status(
                        question_id, wiki_reports.get(wiki_id, {"valid": False})
                    )
                )
            except (OSError, ValueError, json.JSONDecodeError) as exc:
                results.append(
                    contract.ok(
                        REFRESH_SCHEMA,
                        changed=False,
                        question_id=path.stem,
                        lifecycle="disabled",
                        reason="question_invalid",
                        detail=type(exc).__name__,
                    )
                )
        return contract.ok(
            REFRESH_BATCH_SCHEMA,
            total=len(results),
            disabled=sum(x.get("lifecycle") == "disabled" for x in results),
            results=results,
        )

    def answer(
        self,
        question_id: str,
        response: Any,
        *,
        scoring_mode: str = "manual",
        scorer: Any = None,
    ) -> dict:
        question = self.load(question_id)
        if question.get("status") != "enabled":
            return contract.blocked(ANSWER_SCHEMA, "question_disabled")

        def graded_with_feedback(grading: dict) -> dict:
            # 判分结论下沉 grading 子字段（TD §14）；correct_option_ids/answer/
            # explanation/wiki_refs 是判分后才揭示的题目反馈，留在顶层领域字段。
            self._record_answer(question_id, grading, response)
            return contract.ok(
                ANSWER_SCHEMA,
                grading=grading,
                correct_option_ids=question.get("correct_option_ids"),
                answer=question.get("answer"),
                explanation=question.get("explanation", ""),
                wiki_refs=question.get("wiki_refs", []),
            )

        kind = question["type"]
        if kind == "single_choice":
            option_ids = {
                item.get("id")
                for item in (question.get("options") or [])
                if isinstance(item, dict)
            }
            if not isinstance(response, str) or response not in option_ids:
                return contract.blocked(ANSWER_SCHEMA, "response_option_unknown")
            score = (
                1.0
                if response == question.get("correct_option_ids", [None])[0]
                else 0.0
            )
            return graded_with_feedback(
                {"state": "graded", "score": score, "correct": score == 1.0}
            )
        if kind == "multi_choice":
            expected = set(question.get("correct_option_ids") or [])
            values = response if isinstance(response, list) else []
            if len(values) != len(set(values)):
                return contract.blocked(ANSWER_SCHEMA, "response_options_duplicate")
            option_ids = {
                item.get("id")
                for item in (question.get("options") or [])
                if isinstance(item, dict)
            }
            if any(
                not isinstance(value, str) or value not in option_ids
                for value in values
            ):
                return contract.blocked(ANSWER_SCHEMA, "response_option_unknown")
            actual = set(values)
            score = 1.0 if actual == expected else 0.0
            return graded_with_feedback(
                {"state": "graded", "score": score, "correct": score == 1.0}
            )
        if kind == "cloze":
            # _score_cloze 自行落库并返回 grading 子结果（避免重复记录）。
            return contract.ok(
                ANSWER_SCHEMA,
                grading=self._score_cloze(question, response),
                correct_option_ids=question.get("correct_option_ids"),
                answer=question.get("answer"),
                explanation=question.get("explanation", ""),
                wiki_refs=question.get("wiki_refs", []),
            )
        if scoring_mode not in {"manual", "deterministic", "llm"}:
            return contract.blocked(ANSWER_SCHEMA, "scoring_mode_invalid")
        if scoring_mode == "manual":
            grading = {
                "state": "manual_review",
                "rubric": question.get("rubric", []),
                "response": response,
            }
            self._record_answer(question_id, grading, response)
            return contract.ok(ANSWER_SCHEMA, grading=grading)
        if scoring_mode == "deterministic":
            rubric = question.get("rubric") or []
            matched = 0
            criteria = []
            normalized = str(response).casefold()
            for item in rubric:
                if isinstance(item, str):
                    criterion, keywords = item, [item]
                elif isinstance(item, dict) and isinstance(item.get("keywords"), list):
                    criterion, keywords = (
                        item.get("label", "criterion"),
                        item["keywords"],
                    )
                else:
                    continue
                ok = bool(keywords) and all(
                    str(word).casefold() in normalized for word in keywords
                )
                criteria.append({"criterion": criterion, "matched": ok})
                matched += int(ok)
            score = matched / len(criteria) if criteria else 0.0
            grading = {
                "state": "graded",
                "scoring_provider": "deterministic_rubric",
                "score": score,
                "correct": score == 1.0,
                "criteria": criteria,
            }
            self._record_answer(question_id, grading, response)
            return contract.ok(ANSWER_SCHEMA, grading=grading)
        if not callable(scorer):
            return contract.unavailable(
                ANSWER_SCHEMA,
                "grading_provider_unavailable",
                reason="provider_unavailable",
                scoring_provider="llm",
                grading={"state": "unavailable", "reason": "provider_unavailable"},
            )
        try:
            observed = scorer(
                {
                    "question": question,
                    "response": response,
                    "rubric": question.get("rubric", []),
                }
            )
        except Exception as exc:  # noqa: BLE001 - 调用方注入的打分器是外部实现，异常面未知
            return contract.unavailable(
                ANSWER_SCHEMA,
                "grading_provider_unavailable",
                reason="provider_error",
                detail=type(exc).__name__,
                scoring_provider="llm",
                grading={"state": "unavailable", "reason": "provider_error"},
            )
        if (
            not isinstance(observed, dict)
            or not isinstance(observed.get("score"), (int, float))
            or not 0 <= float(observed["score"]) <= 1
        ):
            return contract.unavailable(
                ANSWER_SCHEMA,
                "grading_provider_unavailable",
                reason="provider_malformed",
                scoring_provider="llm",
                grading={"state": "unavailable", "reason": "provider_malformed"},
            )
        grading = {
            "state": "graded",
            "scoring_provider": "llm",
            "score": float(observed["score"]),
            "correct": float(observed["score"]) == 1.0,
        }
        if isinstance(observed.get("rationale"), str):
            grading["rationale"] = observed["rationale"][:2000]
        self._record_answer(question_id, grading, response)
        return contract.ok(ANSWER_SCHEMA, grading=grading)

    def review(self, question_id: str, rating: int) -> dict:
        if rating not in {1, 2, 3, 4}:
            return contract.blocked(REVIEW_SCHEMA, "rating_invalid")
        question = self.load(question_id)
        if question.get("status") != "enabled":
            return contract.blocked(REVIEW_SCHEMA, "question_disabled")
        scheduling = self.fsrs.review(question.get("review_state"), rating)
        if scheduling.get("state") == "scheduled":
            question["review_state"] = {
                **scheduling["card"],
                "scheduler": scheduling["scheduler"],
                "scheduler_version": scheduling["scheduler_version"],
                "review_state_schema": scheduling["review_state_schema"],
                "rating": scheduling["rating"],
            }
            atomic_write(
                self._file(question_id), canonical_json(question) + b"\n", 0o600
            )
            # 调度结果是领域数据（不是 status 轴）：整块嵌到 ``schedule`` 子字段，
            # 避免与顶层 status 并列出第二根状态轴（正交，单 status 轴）。
            return contract.ok(REVIEW_SCHEMA, schedule=scheduling)
        # 调度器缺失/异常是 provider 不可用 → unavailable 信封；领域细节进 schedule。
        return contract.unavailable(
            REVIEW_SCHEMA, "scheduler_unavailable", schedule=scheduling
        )


def practice_integrity_check(target: Path) -> None:
    """恢复语义校验钩子（供 BackupManager 注入；F012 解耦：备份不依赖题库）。

    逐字节数据不足以判定 practice 数据可用：按 question/v1 与
    practice-review-record/v1 契约重放校验。任何失败抛 ValueError
    （practice_question_invalid / practice_question_schema_invalid /
    practice_review_invalid / practice_review_owner_mismatch）。
    """
    questions = RepoPaths(target).practice_questions
    if questions.is_dir():
        store = QuestionStore(target)
        for path in sorted(questions.glob("*.json")):
            try:
                question = store.load(path.stem)
            except (OSError, ValueError, json.JSONDecodeError) as exc:
                raise ValueError("practice_question_invalid") from exc
            if question.get("schema_version") != QUESTION_SCHEMA:
                raise ValueError("practice_question_schema_invalid")
    reviews = RepoPaths(target).practice_reviews_root
    if reviews.is_dir():
        for path in sorted(reviews.glob("*.jsonl")):
            question_id = path.stem
            for line in path.read_text(encoding="utf-8").splitlines():
                try:
                    record = json.loads(line)
                except json.JSONDecodeError as exc:
                    raise ValueError("practice_review_invalid") from exc
                if (
                    record.get("schema_version") != "practice-review-record/v1"
                    or record.get("question_id") != question_id
                ):
                    raise ValueError("practice_review_owner_mismatch")
