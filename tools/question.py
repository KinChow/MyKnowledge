"""F008 question authoring, scoring and local review state.

Question facts are derived from a validated Wiki claim.  Answers and review
state live under ``practice/`` and are never consumed by public projection.
FSRS is an optional runtime adapter: absence is reported explicitly.
"""

from __future__ import annotations

import hashlib
import importlib.metadata
import json
import os
import time
import unicodedata
import uuid
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from .common import atomic_write, canonical_json, safe_id, sha256_bytes
from .paths import RepoPaths
from .validation.validator import WikiValidator

QUESTION_SCHEMA = "question/v1"
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
    "wiki_refs",
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
    def _validate_spec(spec: dict) -> list[dict]:
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
                if not isinstance(accepted, list) or not accepted or any(
                    not isinstance(value, str) or not value.strip()
                    for value in accepted
                ):
                    errors.append({"code": "accepted_answers_required"})
                if not isinstance(aliases, list) or any(
                    not isinstance(value, str) or not value.strip()
                    for value in aliases
                ):
                    errors.append({"code": "answer_aliases_invalid"})
                if not isinstance(normalization, dict):
                    errors.append({"code": "answer_normalization_invalid"})
                elif set(normalization) - {"casefold", "trim", "collapse_whitespace"}:
                    errors.append({"code": "answer_normalization_rule_unknown"})
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
            return {"state": "blocked", "errors": errors}
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
            "status": "enabled",
            "created_at": time.time(),
            "review_state": None,
        }
        question["content_sha256"] = self._content_hash(question)
        atomic_write(
            self._file(question["id"]), canonical_json(question) + b"\n", 0o600
        )
        return {"state": "created", "question": question}

    @staticmethod
    def _validate_import_spec(spec: dict) -> list[dict]:
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
        if spec.get("type") not in {"single_choice", "multi_choice", "cloze"}:
            errors.append({"code": "question_type_invalid"})
        for field in ("prompt", "domain", "topic", "concept_id", "skill"):
            if not isinstance(spec.get(field), str) or not spec[field].strip():
                errors.append({"code": f"{field}_required"})
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
                if not isinstance(accepted, list) or not accepted or any(
                    not isinstance(value, str) or not value.strip()
                    for value in accepted
                ):
                    errors.append({"code": "accepted_answers_required"})
                if not isinstance(aliases, list) or any(
                    not isinstance(value, str) or not value.strip()
                    for value in aliases
                ):
                    errors.append({"code": "answer_aliases_invalid"})
                if not isinstance(normalization, dict):
                    errors.append({"code": "answer_normalization_invalid"})
                elif set(normalization) - {"casefold", "trim", "collapse_whitespace"}:
                    errors.append({"code": "answer_normalization_rule_unknown"})
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
            canonical_json({key: value for key, value in question.items() if key not in excluded})
        )

    def import_file(self, source: Path) -> dict:
        """Import one standalone personal question without requiring a Wiki claim."""
        try:
            spec = json.loads(source.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            return {"state": "blocked", "source": str(source), "errors": [{"code": "question_json_invalid", "detail": type(exc).__name__}]}
        result = self.import_spec(spec)
        if result["state"] == "blocked":
            result["source"] = str(source)
        return result

    def import_spec(self, spec: dict) -> dict:
        """Import one standalone personal question from an already parsed object."""
        errors = self._validate_import_spec(spec)
        if errors:
            return {"state": "blocked", "errors": errors}
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
            "wiki_refs": spec.get("wiki_refs", []),
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
                return {"state": "blocked", "errors": [{"code": "existing_question_invalid", "detail": type(exc).__name__}]}
            if self._import_content_hash(existing) == self._import_content_hash(question):
                return {"state": "noop", "question_id": question["id"], "content_sha256": question["content_sha256"]}
            return {"state": "blocked", "question_id": question["id"], "errors": [{"code": "question_id_conflict"}]}
        atomic_write(target, canonical_json(question) + b"\n", 0o600)
        return {"state": "imported", "question_id": question["id"], "content_sha256": question["content_sha256"], "path": str(target)}

    def import_path(self, source: Path) -> dict:
        source = Path(source)
        files = [source] if source.is_file() else sorted(source.glob("*.json")) if source.is_dir() else []
        if not files:
            return {"state": "blocked", "source": str(source), "errors": [{"code": "question_import_source_empty"}]}
        results = [self.import_file(path) for path in files]
        return {
            "state": "imported" if any(item["state"] == "imported" for item in results) else "noop" if all(item["state"] == "noop" for item in results) else "blocked",
            "source": str(source),
            "total": len(results),
            "imported": sum(item["state"] == "imported" for item in results),
            "noop": sum(item["state"] == "noop" for item in results),
            "blocked": sum(item["state"] == "blocked" for item in results),
            "results": results,
        }

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
                "status",
            )
            if key in question
        }

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
            return {"state": "blocked", "error_code": "question_status_invalid"}
        items: list[dict] = []
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
            items.append(self._catalog_item(question))
        return {
            "state": "listed",
            "total": len(items),
            "items": items,
            "invalid": invalid,
        }

    def create_session(
        self,
        *,
        size: int = 6,
        domain: str | None = None,
        topic: str | None = None,
        concept_id: str | None = None,
        skill: str | None = None,
    ) -> dict:
        if size not in {3, 6, 10}:
            return {"state": "blocked", "error_code": "session_size_invalid"}
        catalog = self.list(domain=domain, topic=topic, skill=skill)
        if catalog["invalid"]:
            return {
                "state": "blocked",
                "error_code": "question_catalog_invalid",
                "invalid": catalog["invalid"],
            }
        candidates = [
            item
            for item in catalog["items"]
            if concept_id is None or item.get("concept_id") == concept_id
        ]
        if not candidates:
            return {
                "state": "empty",
                "question_count": 0,
                "next_action": "import_question",
            }
        # Build deterministic buckets: due reviews first, then active errors, then new
        # questions. Future reviews are eligible only as a final fallback.
        now = datetime.now(UTC)
        due_ids: set[str] = set()
        reviewed_ids: set[str] = set()
        error_ids: set[str] = set()
        for item in candidates:
            question = self.load(item["id"])
            review_state = question.get("review_state")
            if isinstance(review_state, dict):
                reviewed_ids.add(item["id"])
                try:
                    due = datetime.fromisoformat(str(review_state.get("due")))
                    if due.tzinfo is None:
                        due = due.replace(tzinfo=UTC)
                    if due <= now:
                        due_ids.add(item["id"])
                except (TypeError, ValueError):
                    pass
            review_path = self.paths.practice_reviews(item["id"])
            latest = None
            if review_path.exists():
                try:
                    for line in review_path.read_text(encoding="utf-8").splitlines():
                        record = json.loads(line)
                        if (
                            isinstance(record, dict)
                            and record.get("question_id") == item["id"]
                            and isinstance(record.get("recorded_at"), (int, float))
                            and (
                                latest is None
                                or record["recorded_at"] > latest["recorded_at"]
                            )
                        ):
                            latest = record
                except (OSError, UnicodeError, json.JSONDecodeError):
                    latest = None
            result = latest.get("result") if isinstance(latest, dict) else None
            if (
                isinstance(result, dict)
                and result.get("state") == "graded"
                and (
                    result.get("correct") is False
                    or result.get("score", 1) < 1
                )
            ):
                error_ids.add(item["id"])

        def stable(items: list[dict]) -> list[dict]:
            return sorted(
                items, key=lambda item: (str(item.get("concept_id", "")), item["id"])
            )

        due_items = stable([item for item in candidates if item["id"] in due_ids])
        error_items = stable(
            [
                item
                for item in candidates
                if item["id"] in error_ids and item["id"] not in due_ids
            ]
        )
        new_items = stable(
            [
                item
                for item in candidates
                if item["id"] not in reviewed_ids and item["id"] not in error_ids
            ]
        )
        fallback_items = stable(
            [
                item
                for item in candidates
                if item["id"] not in due_ids
                and item["id"] not in error_ids
                and item["id"] in reviewed_ids
            ]
        )
        candidates = due_items + error_items + new_items + fallback_items
        selected: list[dict] = []
        concept_counts: dict[str, int] = {}
        for item in candidates:
            concept = str(item.get("concept_id", ""))
            if concept_counts.get(concept, 0) >= 2:
                continue
            selected.append(item)
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
        }
        atomic_write(
            self.paths.practice_session(session_id),
            canonical_json(session) + b"\n",
            0o600,
        )
        return {
            "state": "created",
            "session": session,
            "items": selected,
            "question_count": len(selected),
        }

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
        return {"state": "updated", "session": session}

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
        return {
            "state": "listed",
            "session": session,
            "items": items,
            "question_count": len(items),
        }

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
            return {"state": "blocked", "error_code": "error_queue_limit_invalid"}
        catalog = self.list(
            domain=domain,
            topic=topic,
            skill=skill,
            status="enabled",
        )
        if catalog["invalid"]:
            return {
                "state": "blocked",
                "error_code": "question_catalog_invalid",
                "invalid": catalog["invalid"],
            }
        candidates = {
            item["id"]
            for item in catalog["items"]
            if concept_id is None or item.get("concept_id") == concept_id
        }
        errors: list[dict] = []
        warnings: list[dict] = []
        for question_id in candidates:
            path = self.paths.practice_reviews(question_id)
            latest = None
            if not path.exists():
                continue
            try:
                for line in path.read_text(encoding="utf-8").splitlines():
                    record = json.loads(line)
                    if (
                        isinstance(record, dict)
                        and record.get("question_id") == question_id
                        and isinstance(record.get("recorded_at"), (int, float))
                        and (
                            latest is None
                            or record["recorded_at"] > latest["recorded_at"]
                            )
                        ):
                            latest = record
            except (OSError, UnicodeError, json.JSONDecodeError) as exc:
                warnings.append(
                    {
                        "code": "review_log_invalid",
                        "question_id": question_id,
                        "detail": type(exc).__name__,
                    }
                )
                continue
            result = latest.get("result") if isinstance(latest, dict) else None
            if not isinstance(result, dict) or result.get("state") != "graded":
                continue
            if result.get("correct") is not False and result.get("score", 1) >= 1:
                continue
            question = self.load(question_id)
            errors.append(
                {
                    "question_id": question_id,
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
        return {
            "state": "listed",
            "total": min(len(errors), limit),
            "items": errors[:limit],
            "warnings": warnings,
        }

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
            return {"state": "blocked", "error_code": "queue_size_invalid"}
        catalog = self.list(
            domain=domain,
            topic=topic,
            skill=skill,
            status="enabled",
        )
        if catalog["invalid"]:
            return {
                "state": "blocked",
                "error_code": "question_catalog_invalid",
                "invalid": catalog["invalid"],
            }
        candidates = [
            item
            for item in catalog["items"]
            if concept_id is None or item.get("concept_id") == concept_id
        ]
        now = datetime.now(UTC)
        due: list[tuple[datetime, dict]] = []
        new: list[dict] = []
        for item in candidates:
            question = self.load(item["id"])
            review_state = question.get("review_state")
            if not isinstance(review_state, dict):
                new.append(item)
                continue
            due_value = review_state.get("due")
            try:
                parsed_due = datetime.fromisoformat(str(due_value))
                if parsed_due.tzinfo is None:
                    parsed_due = parsed_due.replace(tzinfo=UTC)
            except (TypeError, ValueError):
                continue
            if parsed_due <= now:
                due.append((parsed_due, item))
        due.sort(key=lambda pair: (pair[0], pair[1]["id"]))
        new.sort(key=lambda item: (str(item.get("concept_id", "")), item["id"]))
        selected: list[dict] = [
            {"queue_kind": "due", "due": due_value.isoformat(), "question": item}
            for due_value, item in due[:size]
        ]
        if include_new and len(selected) < size:
            selected.extend(
                {"queue_kind": "new", "due": None, "question": item}
                for item in new[: size - len(selected)]
            )
        return {
            "state": "listed" if selected else "empty",
            "total": len(selected),
            "items": selected,
            "next_action": None if selected else "import_question",
        }

    def disable(self, question_id: str, *, reason: str = "manual") -> dict:
        question = self.load(question_id)
        if question.get("status") == "disabled":
            return {
                "state": "noop",
                "question_id": question_id,
                "status": "disabled",
            }
        question["status"] = "disabled"
        question["disabled_reason"] = reason
        atomic_write(self._file(question_id), canonical_json(question) + b"\n", 0o600)
        return {
            "state": "disabled",
            "question_id": question_id,
            "status": "disabled",
            "reason": reason,
        }

    def enable(self, question_id: str) -> dict:
        question = self.load(question_id)
        if question.get("status", "enabled") == "enabled":
            return {
                "state": "noop",
                "question_id": question_id,
                "status": "enabled",
            }
        question["status"] = "enabled"
        question.pop("disabled_reason", None)
        atomic_write(self._file(question_id), canonical_json(question) + b"\n", 0o600)
        return {
            "state": "enabled",
            "question_id": question_id,
            "status": "enabled",
        }

    def delete(self, question_id: str) -> dict:
        self.load(question_id)
        review_path = self.paths.practice_reviews(question_id)
        if review_path.exists() and review_path.stat().st_size > 0:
            result = self.disable(question_id, reason="delete_requested_with_history")
            return {
                **result,
                "state": "disabled",
                "reason": "review_history_preserved",
            }
        self._file(question_id).unlink()
        return {"state": "deleted", "question_id": question_id}

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
        if not valid and question.get("status") != "disabled":
            question["status"] = "disabled"
            question["disabled_reason"] = "claim_binding_stale"
            atomic_write(
                self._file(question_id), canonical_json(question) + b"\n", 0o600
            )
        return {
            "state": "enabled" if valid else "disabled",
            "question_id": question_id,
            "reason": None if valid else "claim_binding_stale",
        }

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
                    {
                        "state": "disabled",
                        "question_id": path.stem,
                        "reason": "question_invalid",
                        "detail": type(exc).__name__,
                    }
                )
        return {
            "state": "refreshed",
            "total": len(results),
            "disabled": sum(x.get("state") == "disabled" for x in results),
            "results": results,
        }

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
            return {"state": "blocked", "error_code": "question_disabled"}

        def feedback(result: dict) -> dict:
            return {
                **result,
                "correct_option_ids": question.get("correct_option_ids"),
                "answer": question.get("answer"),
                "explanation": question.get("explanation", ""),
                "wiki_refs": question.get("wiki_refs", []),
            }

        kind = question["type"]
        if kind == "single_choice":
            option_ids = {
                item.get("id")
                for item in (question.get("options") or [])
                if isinstance(item, dict)
            }
            if not isinstance(response, str) or response not in option_ids:
                return {"state": "blocked", "error_code": "response_option_unknown"}
            score = (
                1.0
                if response == question.get("correct_option_ids", [None])[0]
                else 0.0
            )
            result = {"state": "graded", "score": score, "correct": score == 1.0}
            self._record_answer(question_id, result, response)
            return feedback(result)
        if kind == "multi_choice":
            expected = set(question.get("correct_option_ids") or [])
            values = response if isinstance(response, list) else []
            if len(values) != len(set(values)):
                return {"state": "blocked", "error_code": "response_options_duplicate"}
            option_ids = {
                item.get("id")
                for item in (question.get("options") or [])
                if isinstance(item, dict)
            }
            if any(
                not isinstance(value, str) or value not in option_ids
                for value in values
            ):
                return {"state": "blocked", "error_code": "response_option_unknown"}
            actual = set(values)
            score = 1.0 if actual == expected else 0.0
            result = {"state": "graded", "score": score, "correct": score == 1.0}
            self._record_answer(question_id, result, response)
            return feedback(result)
        if kind == "cloze":
            return feedback(self._score_cloze(question, response))
        if scoring_mode not in {"manual", "deterministic", "llm"}:
            return {"state": "blocked", "error_code": "scoring_mode_invalid"}
        if scoring_mode == "manual":
            result = {
                "state": "manual_review",
                "rubric": question.get("rubric", []),
                "response": response,
            }
            self._record_answer(question_id, result, response)
            return result
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
            result = {
                "state": "graded",
                "scoring_provider": "deterministic_rubric",
                "score": score,
                "correct": score == 1.0,
                "criteria": criteria,
            }
            self._record_answer(question_id, result, response)
            return result
        if not callable(scorer):
            return {
                "state": "unavailable",
                "reason": "provider_unavailable",
                "scoring_provider": "llm",
            }
        try:
            observed = scorer(
                {
                    "question": question,
                    "response": response,
                    "rubric": question.get("rubric", []),
                }
            )
        except Exception as exc:  # noqa: BLE001 - 调用方注入的打分器是外部实现，异常面未知
            return {
                "state": "unavailable",
                "reason": "provider_error",
                "detail": type(exc).__name__,
                "scoring_provider": "llm",
            }
        if (
            not isinstance(observed, dict)
            or not isinstance(observed.get("score"), (int, float))
            or not 0 <= float(observed["score"]) <= 1
        ):
            return {
                "state": "unavailable",
                "reason": "provider_malformed",
                "scoring_provider": "llm",
            }
        result = {
            "state": "graded",
            "scoring_provider": "llm",
            "score": float(observed["score"]),
            "correct": float(observed["score"]) == 1.0,
        }
        if isinstance(observed.get("rationale"), str):
            result["rationale"] = observed["rationale"][:2000]
        self._record_answer(question_id, result, response)
        return result

    def review(self, question_id: str, rating: int) -> dict:
        if rating not in {1, 2, 3, 4}:
            return {"state": "blocked", "error_code": "rating_invalid"}
        question = self.load(question_id)
        if question.get("status") != "enabled":
            return {"state": "blocked", "error_code": "question_disabled"}
        result = self.fsrs.review(question.get("review_state"), rating)
        if result.get("state") == "scheduled":
            question["review_state"] = {
                **result["card"],
                "scheduler": result["scheduler"],
                "scheduler_version": result["scheduler_version"],
                "review_state_schema": result["review_state_schema"],
                "rating": result["rating"],
            }
            atomic_write(
                self._file(question_id), canonical_json(question) + b"\n", 0o600
            )
        return result


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
