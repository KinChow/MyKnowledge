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

ALLOWED_ACTIONS = frozenset({"write_preview", "write_apply", "vault_check", "backup_status", "backup_manifest", "question_create", "question_answer", "question_review"})
FORBIDDEN_KEYS = frozenset({"shell", "command", "exec", "git", "path", "absolute_path", "capability_token", "api_key"})


def dispatch(action: str, payload: dict[str, Any] | None = None, *, root: Path) -> dict[str, Any]:
    payload = payload or {}
    if action not in ALLOWED_ACTIONS:
        return {"state": "blocked", "error_code": "skill_action_not_allowed", "action": action}
    if not isinstance(payload, dict) or any(key in FORBIDDEN_KEYS for key in payload):
        return {"state": "blocked", "error_code": "skill_payload_forbidden"}
    root = Path(root).resolve()
    try:
        if action == "write_preview":
            files = payload.get("files")
            if not isinstance(files, dict):
                return {"state": "blocked", "error_code": "files_required"}
            return WriteOperation(root).preview(files, operation_type=str(payload.get("operation_type", "write")), vault_id=str(payload.get("vault_id", "public")))
        if action == "write_apply":
            return WriteOperation(root).apply(str(payload.get("operation_id", "")), confirmed=payload.get("confirmed") is True, actor_id=str(payload.get("actor_id", "local-user")))
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
            return store.create(spec)
        if action == "question_answer":
            return store.answer(str(payload.get("question_id", "")), payload.get("response"))
        return store.review(str(payload.get("question_id", "")), payload.get("rating"))
    except (OSError, ValueError, TypeError) as exc:
        return {"state": "blocked", "error_code": str(exc)}

