"""F008 question authoring, scoring and local review state.

Question facts are derived from a validated Wiki claim.  Answers and review
state live under ``practice/`` and are never consumed by public projection.
FSRS is an optional runtime adapter: absence is reported explicitly.
"""
from __future__ import annotations

import hashlib
import json
import os
import time
from pathlib import Path
from typing import Any

from .common import atomic_write, canonical_json, safe_id
from .front_matter import FrontMatter
from .paths import RepoPaths
from .validation.validator import WikiValidator

QUESTION_SCHEMA = "question/v1"
QUESTION_TYPES = {"single_choice", "multi_choice", "short_answer"}


class FSRSAdapter:
    def __init__(self) -> None:
        try:
            from fsrs import Scheduler, Card, Rating  # type: ignore
            self._Scheduler, self._Card, self._Rating = Scheduler, Card, Rating
        except ImportError:
            self._Scheduler = self._Card = self._Rating = None

    @property
    def available(self) -> bool:
        return self._Scheduler is not None

    def review(self, state: dict | None, rating: int) -> dict:
        if not self.available:
            return {"state": "unavailable", "reason": "provider_unavailable", "scheduler": "fsrs"}
        try:
            scheduler = self._Scheduler()
            card = self._Card.from_dict(state) if state else self._Card()
            result = scheduler.review_card(card, self._Rating(rating))
            next_card = result.card if hasattr(result, "card") else result[0]
            return {"state": "scheduled", "scheduler": "fsrs", "rating": rating, "card": next_card.to_dict()}
        except Exception as exc:  # adapter failures are explicit, never a fake schedule
            return {"state": "unavailable", "reason": "scheduler_error", "detail": type(exc).__name__, "scheduler": "fsrs"}


class QuestionStore:
    def __init__(self, root: Path) -> None:
        self.root = Path(root).resolve()
        self.paths = RepoPaths(self.root)
        self.fsrs = FSRSAdapter()

    def _file(self, question_id: str) -> Path:
        safe_id(question_id)
        return self.paths.practice_questions / f"{question_id}.json"

    def _record_answer(self, question_id: str, result: dict, response: Any) -> None:
        path = self.paths.practice_reviews(question_id)
        record = {"schema_version": "practice-review-record/v1", "question_id": question_id, "recorded_at": time.time(), "response": response, "result": result}
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("ab") as handle:
            handle.write(canonical_json(record) + b"\n")
            handle.flush(); os.fsync(handle.fileno())

    @staticmethod
    def _validate_spec(spec: dict) -> list[dict]:
        errors: list[dict] = []
        if spec.get("type") not in QUESTION_TYPES:
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
        if spec.get("type") in {"single_choice", "multi_choice"}:
            options = spec.get("options")
            correct = spec.get("correct_option_ids")
            if not isinstance(options, list) or len(options) < 2:
                errors.append({"code": "options_required"})
            if not isinstance(correct, list) or not correct:
                errors.append({"code": "correct_options_required"})
            if spec.get("type") == "single_choice" and isinstance(correct, list) and len(correct) != 1:
                errors.append({"code": "single_choice_requires_one_answer"})
        if spec.get("type") == "short_answer" and not isinstance(spec.get("rubric"), list):
            errors.append({"code": "rubric_required"})
        return errors

    def _wiki_report(self, wiki_path: Path) -> dict:
        return WikiValidator(self.root).validate(wiki_path)

    def create(self, spec: dict, *, wiki_path: Path | None = None, wiki_report: dict | None = None) -> dict:
        errors = self._validate_spec(spec)
        report = wiki_report or (self._wiki_report(wiki_path) if wiki_path else None)
        if not report or not report.get("valid"):
            errors.append({"code": "wiki_unverified"})
        else:
            derived = report.get("derived") or {}
            if report.get("object_ref", {}).get("object_type") != "wiki" or derived.get("evidence_state") not in {"supported", "corroborated"}:
                errors.append({"code": "wiki_claim_unverified"})
        if errors:
            return {"state": "blocked", "errors": errors}
        claim_id = str(spec["claim_id"])
        claim = {"vault_id": spec.get("vault_id", "public"), "wiki_id": spec["wiki_id"], "claim_id": claim_id, "content_sha256": report.get("hashes", {}).get("content_sha256"), "evidence_sha256": report.get("hashes", {}).get("evidence_sha256")}
        question = {"schema_version": QUESTION_SCHEMA, "id": spec["id"], "type": spec["type"], "confidentiality": spec.get("confidentiality", "public"), "wiki_claim": claim, "prompt": spec["prompt"], "options": spec.get("options"), "correct_option_ids": spec.get("correct_option_ids"), "answer": spec.get("answer"), "explanation": spec.get("explanation"), "rubric": spec.get("rubric"), "status": "enabled", "created_at": time.time(), "review_state": None}
        question["content_sha256"] = "sha256:" + hashlib.sha256(canonical_json({k: v for k, v in question.items() if k not in {"created_at", "review_state", "content_sha256"}})).hexdigest()
        atomic_write(self._file(question["id"]), canonical_json(question) + b"\n", 0o600)
        return {"state": "created", "question": question}

    def load(self, question_id: str) -> dict:
        return json.loads(self._file(question_id).read_text(encoding="utf-8"))

    def refresh_status(self, question_id: str, wiki_report: dict) -> dict:
        """Revalidate the claim binding and disable stale questions atomically."""
        question = self.load(question_id)
        claim = question.get("wiki_claim", {})
        hashes = wiki_report.get("hashes", {}) if isinstance(wiki_report, dict) else {}
        valid = bool(wiki_report.get("valid")) and (wiki_report.get("derived") or {}).get("evidence_state") in {"supported", "corroborated"}
        valid = valid and claim.get("content_sha256") == hashes.get("content_sha256") and claim.get("evidence_sha256") == hashes.get("evidence_sha256")
        if not valid and question.get("status") != "disabled":
            question["status"] = "disabled"
            question["disabled_reason"] = "claim_binding_stale"
            atomic_write(self._file(question_id), canonical_json(question) + b"\n", 0o600)
        return {"state": "enabled" if valid else "disabled", "question_id": question_id, "reason": None if valid else "claim_binding_stale"}

    def refresh_all(self, wiki_reports: dict[str, dict]) -> dict:
        """Revalidate every local question against reports keyed by wiki_id."""
        results: list[dict] = []
        for path in sorted(self.paths.practice_questions.glob("*.json")):
            try:
                question_id = path.stem
                question = self.load(question_id)
                wiki_id = str((question.get("wiki_claim") or {}).get("wiki_id", ""))
                results.append(self.refresh_status(question_id, wiki_reports.get(wiki_id, {"valid": False})))
            except (OSError, ValueError, json.JSONDecodeError) as exc:
                results.append({"state": "disabled", "question_id": path.stem, "reason": "question_invalid", "detail": type(exc).__name__})
        return {"state": "refreshed", "total": len(results), "disabled": sum(x.get("state") == "disabled" for x in results), "results": results}

    def answer(self, question_id: str, response: Any, *, scoring_mode: str = "manual", scorer: Any = None) -> dict:
        question = self.load(question_id)
        if question.get("status") != "enabled":
            return {"state": "blocked", "error_code": "question_disabled"}
        kind = question["type"]
        if kind == "single_choice":
            score = 1.0 if response == question.get("correct_option_ids", [None])[0] else 0.0
            result = {"state": "graded", "score": score, "correct": score == 1.0}; self._record_answer(question_id, result, response); return result
        if kind == "multi_choice":
            expected = set(question.get("correct_option_ids") or [])
            actual = set(response if isinstance(response, list) else [])
            score = 1.0 if actual == expected else 0.0
            result = {"state": "graded", "score": score, "correct": score == 1.0}; self._record_answer(question_id, result, response); return result
        if scoring_mode not in {"manual", "deterministic", "llm"}:
            return {"state": "blocked", "error_code": "scoring_mode_invalid"}
        if scoring_mode == "manual":
            result = {"state": "manual_review", "rubric": question.get("rubric", []), "response": response}
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
                    criterion, keywords = item.get("label", "criterion"), item["keywords"]
                else:
                    continue
                ok = bool(keywords) and all(str(word).casefold() in normalized for word in keywords)
                criteria.append({"criterion": criterion, "matched": ok})
                matched += int(ok)
            score = matched / len(criteria) if criteria else 0.0
            result = {"state": "graded", "scoring_provider": "deterministic_rubric", "score": score, "correct": score == 1.0, "criteria": criteria}
            self._record_answer(question_id, result, response)
            return result
        if not callable(scorer):
            return {"state": "unavailable", "reason": "provider_unavailable", "scoring_provider": "llm"}
        try:
            observed = scorer({"question": question, "response": response, "rubric": question.get("rubric", [])})
        except Exception as exc:
            return {"state": "unavailable", "reason": "provider_error", "detail": type(exc).__name__, "scoring_provider": "llm"}
        if not isinstance(observed, dict) or not isinstance(observed.get("score"), (int, float)) or not 0 <= float(observed["score"]) <= 1:
            return {"state": "unavailable", "reason": "provider_malformed", "scoring_provider": "llm"}
        result = {"state": "graded", "scoring_provider": "llm", "score": float(observed["score"]), "correct": float(observed["score"]) == 1.0}
        if isinstance(observed.get("rationale"), str):
            result["rationale"] = observed["rationale"][:2000]
        self._record_answer(question_id, result, response)
        return result

    def review(self, question_id: str, rating: int) -> dict:
        if rating not in {1, 2, 3, 4}:
            return {"state": "blocked", "error_code": "rating_invalid"}
        question = self.load(question_id)
        result = self.fsrs.review(question.get("review_state"), rating)
        if result.get("state") == "scheduled":
            question["review_state"] = result["card"]
            atomic_write(self._file(question_id), canonical_json(question) + b"\n", 0o600)
        return result
