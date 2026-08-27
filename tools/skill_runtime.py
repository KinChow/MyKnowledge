"""受控 Agent Skill 运行适配器（F009）。

只接受结构化 action 白名单，并把实际工作委托给现有领域服务；不执行
任意 shell，不接受物理路径写入，也不暴露 capability token。
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

from .backup import BackupManager
from .question import QuestionStore
from .vault_registry import VaultRegistry
from .write_operation import WriteOperation
from .indexing import Retriever
from .ingest.source_ingestor import SourceIngestor
from .validation.validator import WikiValidator
import json
from .common import safe_id

ALLOWED_ACTIONS = frozenset({"skill_status", "query", "retrieve", "read", "backlinks", "write_preview", "write_apply", "source_preview", "source_apply", "wiki_validate", "publish_preview", "vault_check", "backup_status", "backup_manifest", "question_create", "question_answer", "question_review"})
FORBIDDEN_KEYS = frozenset({"shell", "command", "exec", "git", "path", "absolute_path", "capability_token", "api_key"})
ACTION_FIELDS = {
    "skill_status": set(), "query": {"query", "scope", "top_k"}, "retrieve": {"query", "scope", "top_k"},
    "read": {"vault_id", "object_id"}, "backlinks": {"vault_id", "object_id"},
    "write_preview": {"files", "operation_type", "vault_id"},
    "write_apply": {"operation_id", "confirmed", "actor_id"},
    "source_preview": {"request"}, "source_apply": {"operation_id", "confirmed", "actor_id"},
    "wiki_validate": {"wiki_path"}, "publish_preview": {"wiki_path"},
    "vault_check": set(), "backup_status": set(), "backup_manifest": {"vault_id"},
    "question_create": {"spec", "wiki_path"}, "question_answer": {"question_id", "response", "scoring_mode"},
    "question_review": {"question_id", "rating"},
}


def _public_projection_items(root: Path) -> list[dict[str, Any]]:
    manifest_path = root / "queries" / "public" / "manifest.json"
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    if data.get("schema_version") != "public-projection/v1" or data.get("projection") != "public":
        raise ValueError("manifest_invalid")
    items: list[dict[str, Any]] = []
    for item in data.get("items", []):
        if item.get("vault_id") != "public" or item.get("public_publishable") is not True or item.get("public_release") is not True or item.get("status") != "published" or item.get("effective_confidentiality") != "public":
            continue
        rel = Path(str(item.get("body_path", "")))
        if rel.is_absolute() or ".." in rel.parts or not rel.parts or rel.parts[0] != "wiki":
            raise ValueError("projection_path_invalid")
        body_path = root / rel
        if not body_path.is_file() or body_path.is_symlink():
            raise ValueError("projection_body_unavailable")
        items.append({**item, "object_type": "wiki", "object_id": item["id"], "body": body_path.read_text(encoding="utf-8"), "availability": "available", "confidentiality": "public"})
    return items


def dispatch(action: str, payload: dict[str, Any] | None = None, *, root: Path) -> dict[str, Any]:
    payload = payload or {}
    if action not in ALLOWED_ACTIONS:
        return {"state": "blocked", "error_code": "skill_action_not_allowed", "action": action}
    if not isinstance(payload, dict) or any(key in FORBIDDEN_KEYS for key in payload):
        return {"state": "blocked", "error_code": "skill_payload_forbidden"}
    unknown = sorted(set(payload) - ACTION_FIELDS[action])
    if unknown:
        return {"state": "blocked", "error_code": "skill_payload_unknown_field", "fields": unknown}
    root = Path(root).resolve()
    try:
        if action == "skill_status":
            skill = root / "skills" / "myknowledge" / "SKILL.md"
            if not skill.is_file() or skill.is_symlink():
                return {"state": "unavailable", "error_code": "skill_unavailable", "reason": "canonical_skill_missing"}
            text = skill.read_text(encoding="utf-8")
            required = ("name: myknowledge", "tools.cli", "explicit human confirmation")
            if any(marker not in text for marker in required):
                return {"state": "unavailable", "error_code": "skill_unavailable", "reason": "canonical_skill_invalid"}
            return {"state": "available", "schema_version": "skill-status/v1", "skill": "myknowledge"}
        if action in {"query", "retrieve"}:
            if str(payload.get("scope", "public")) != "public" or not isinstance(payload.get("query"), str):
                return {"state": "blocked", "error_code": "skill_public_query_only"}
            items = _public_projection_items(root)
            return Retriever(items).search(payload["query"], "public", int(payload.get("top_k", 8)))
        if action == "read":
            if payload.get("vault_id", "public") != "public":
                return {"state": "blocked", "error_code": "skill_private_read_requires_api"}
            object_id = str(payload.get("object_id", ""))
            safe_id(object_id)
            item = next((x for x in _public_projection_items(root) if x["object_id"] == object_id), None)
            if item is None:
                return {"state": "blocked", "error_code": "object_not_found"}
            return {"schema_version": "read-result/v1", "object_ref": {"vault_id": "public", "object_type": "wiki", "object_id": object_id}, "path": item["body_path"], "body": item["body"]}
        if action == "backlinks":
            if payload.get("vault_id", "public") != "public":
                return {"state": "blocked", "error_code": "skill_private_read_requires_api"}
            object_id = str(payload.get("object_id", "")); safe_id(object_id)
            items = _public_projection_items(root)
            if not any(item["object_id"] == object_id for item in items):
                return {"state": "blocked", "error_code": "object_not_found"}
            needle = f"/wiki/{object_id}"
            results = [
                {"vault_id": "public", "object_type": "wiki", "object_id": item["object_id"]}
                for item in items if item["object_id"] != object_id and (needle in item["body"] or object_id in {str(link).strip("/").split("/")[-1] for link in item.get("links", [])})
            ]
            return {"schema_version": "backlinks-result/v1", "target": {"vault_id": "public", "object_type": "wiki", "object_id": object_id}, "items": results}
        if action == "write_preview":
            files = payload.get("files")
            if not isinstance(files, dict):
                return {"state": "blocked", "error_code": "files_required"}
            return WriteOperation(root).preview(files, operation_type=str(payload.get("operation_type", "write")), vault_id=str(payload.get("vault_id", "public")))
        if action == "write_apply":
            return WriteOperation(root).apply(str(payload.get("operation_id", "")), confirmed=payload.get("confirmed") is True, actor_id=str(payload.get("actor_id", "local-user")))
        if action == "source_preview":
            request = payload.get("request")
            if not isinstance(request, dict):
                return {"state": "blocked", "error_code": "source_request_required"}
            return SourceIngestor(root).preview(request)
        if action == "source_apply":
            return SourceIngestor(root).apply(str(payload.get("operation_id", "")), confirmed=payload.get("confirmed") is True, actor_id=str(payload.get("actor_id", "local-user")))
        if action in {"wiki_validate", "publish_preview"}:
            wiki_path = payload.get("wiki_path")
            if not isinstance(wiki_path, str) or not wiki_path:
                return {"state": "blocked", "error_code": "wiki_path_required"}
            candidate = (root / wiki_path).resolve()
            try:
                candidate.relative_to(root)
            except ValueError:
                return {"state": "blocked", "error_code": "path_invalid"}
            report = WikiValidator(root).validate(candidate)
            if action == "wiki_validate":
                return report
            derived = report.get("derived") or {}
            return {"state": "previewed" if report.get("valid") else "blocked", "wiki_report": report, "public_publishable": derived.get("public_publishable", False), "private_publishable": derived.get("private_publishable", False)}
        if action == "vault_check":
            return VaultRegistry(root).check()
        if action == "backup_status":
            return BackupManager(root).status()
        if action == "backup_manifest":
            return BackupManager(root).create_manifest(str(payload.get("vault_id", "public")))
        store = QuestionStore(root)
        if action == "question_create":
            spec = payload.get("spec")
            if not isinstance(spec, dict):
                return {"state": "blocked", "error_code": "spec_required"}
            wiki_path = payload.get("wiki_path")
            if not isinstance(wiki_path, str) or not wiki_path:
                return {"state": "blocked", "error_code": "wiki_path_required"}
            candidate = (root / wiki_path).resolve()
            try:
                candidate.relative_to(root)
            except ValueError:
                return {"state": "blocked", "error_code": "path_invalid"}
            if not candidate.is_file() or candidate.is_symlink():
                return {"state": "blocked", "error_code": "wiki_not_found"}
            report = WikiValidator(root).validate(candidate)
            return store.create(spec, wiki_path=candidate, wiki_report=report)
        if action == "question_answer":
            scoring_mode = payload.get("scoring_mode", "manual")
            if scoring_mode not in {"manual", "deterministic", "llm"}:
                return {"state": "blocked", "error_code": "scoring_mode_invalid"}
            return store.answer(
                str(payload.get("question_id", "")),
                payload.get("response"),
                scoring_mode=scoring_mode,
            )
        return store.review(str(payload.get("question_id", "")), payload.get("rating"))
    except (OSError, ValueError, TypeError) as exc:
        return {"state": "blocked", "error_code": str(exc)}
