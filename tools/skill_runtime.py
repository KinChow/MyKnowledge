"""受控 Agent Skill 运行适配器（F009）。

只接受结构化 action 白名单，并把实际工作委托给现有领域服务；不执行
任意 shell，不接受物理路径写入，也不暴露 capability token。

结构：``dispatch`` 只做通道级门禁（白名单 / 禁用键 / 未知字段），每个 action
一个 ``_handle_*`` 函数，映射表 ``_HANDLERS`` 是唯一的 action 事实来源
（``ALLOWED_ACTIONS`` 由它派生）。字段级非法一律 ``raise ValueError("<error_code>")``，
由 ``dispatch`` 统一收敛成 ``{"state": "blocked", "error_code": ...}``。
"""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path
from typing import Any

from .backup import BackupManager
from .common import safe_id
from .indexing import Retriever
from .ingest.source_ingestor import SourceIngestor
from .projection import PublicProjectionStore
from .question import QuestionStore
from .release_confirmation import write_event
from .validation.validator import WikiValidator
from .vault_registry import VaultRegistry
from .write_operation import WriteOperation

FORBIDDEN_KEYS = frozenset(
    {
        "shell",
        "command",
        "exec",
        "git",
        "path",
        "absolute_path",
        "capability_token",
        "api_key",
    }
)
ACTION_FIELDS = {
    "skill_status": set(),
    "query": {"query", "scope", "top_k"},
    "retrieve": {"query", "scope", "top_k"},
    "ask": {"query", "scope", "top_k"},
    "read": {"vault_id", "object_id"},
    "backlinks": {"vault_id", "object_id"},
    "write_preview": {"files", "operation_type", "vault_id"},
    "write_apply": {"operation_id", "confirmed", "actor_id", "confirmation"},
    "source_preview": {"request"},
    "source_apply": {"operation_id", "confirmed", "actor_id", "confirmation"},
    "wiki_validate": {"wiki_path"},
    "publish_preview": {"wiki_path"},
    "publish_confirm": {"event"},
    "vault_check": set(),
    "backup_status": set(),
    "backup_manifest": {"vault_id"},
    "question_create": {"spec", "wiki_path"},
    "question_answer": {"question_id", "response", "scoring_mode"},
    "question_review": {"question_id", "rating"},
}
CONFIRM_NEXT_ACTION = (
    "python -m tools.cli confirm-apply <operation_id> --actor-id <you> "
    "and pass the event as confirmation"
)


def _public_projection_items(root: Path) -> list[dict[str, Any]]:
    """严格版 public projection 加载，单实现见 projection.PublicProjectionStore。"""
    return PublicProjectionStore(root).public_items(with_body=True)


def _public_object_ref(object_id: str) -> dict[str, str]:
    return {"vault_id": "public", "object_type": "wiki", "object_id": object_id}


def _public_object_id(payload: dict[str, Any]) -> str:
    """Agent 通道只读 public vault；private/local 必须走带 capability 的 API。"""
    if payload.get("vault_id", "public") != "public":
        raise ValueError("skill_private_read_requires_api")
    return safe_id(str(payload.get("object_id", "")))


def _repo_relative_path(root: Path, payload: dict[str, Any]) -> Path:
    """把 payload 里的 wiki_path 解析成仓库内路径；越界或缺失都是结构化错误。"""
    wiki_path = payload.get("wiki_path")
    if not isinstance(wiki_path, str) or not wiki_path:
        raise ValueError("wiki_path_required")
    candidate = (root / wiki_path).resolve()
    try:
        candidate.relative_to(root)
    except ValueError:
        raise ValueError("path_invalid") from None
    return candidate


def _require_mapping(
    payload: dict[str, Any], key: str, error_code: str
) -> dict[str, Any]:
    value = payload.get(key)
    if not isinstance(value, dict):
        raise ValueError(error_code)
    return value


def _handle_skill_status(root: Path, _payload: dict[str, Any]) -> dict[str, Any]:
    skill = root / "skills" / "myknowledge" / "SKILL.md"
    if not skill.is_file() or skill.is_symlink():
        return {
            "state": "unavailable",
            "error_code": "skill_unavailable",
            "reason": "canonical_skill_missing",
        }
    text = skill.read_text(encoding="utf-8")
    required = ("name: myknowledge", "tools.cli", "explicit human confirmation")
    if any(marker not in text for marker in required):
        return {
            "state": "unavailable",
            "error_code": "skill_unavailable",
            "reason": "canonical_skill_invalid",
        }
    return {
        "state": "available",
        "schema_version": "skill-status/v1",
        "skill": "myknowledge",
    }


def _handle_query(root: Path, payload: dict[str, Any]) -> dict[str, Any]:
    if str(payload.get("scope", "public")) != "public" or not isinstance(
        payload.get("query"), str
    ):
        raise ValueError("skill_public_query_only")
    from .indexing import default_public_index_path

    index_path = default_public_index_path(root)
    return Retriever(
        _public_projection_items(root),
        index_path=index_path if index_path.exists() else None,
    ).search(payload["query"], "public", int(payload.get("top_k", 8)))


def _handle_ask(root: Path, payload: dict[str, Any]) -> dict[str, Any]:
    """Agent 通道没有 LLM provider，只回检索结果 + 不可用理由，绝不编造答案。"""
    retrieval = _handle_query(root, payload)
    return {
        "schema_version": "ask-result/v1",
        "answer": None,
        "citations": [],
        "retrieval": retrieval,
        "availability": "unavailable",
        "availability_reason": "provider_unavailable",
        "confidentiality": retrieval.get("confidentiality_max", "public"),
        "limits": ["llm_unavailable"],
        "warnings": ["No LLM provider configured"],
    }


def _handle_read(root: Path, payload: dict[str, Any]) -> dict[str, Any]:
    object_id = _public_object_id(payload)
    item = next(
        (x for x in _public_projection_items(root) if x["object_id"] == object_id),
        None,
    )
    if item is None:
        raise ValueError("object_not_found")
    return {
        "schema_version": "read-result/v1",
        "object_ref": _public_object_ref(object_id),
        "path": item["body_path"],
        "body": item["body"],
    }


def _handle_backlinks(root: Path, payload: dict[str, Any]) -> dict[str, Any]:
    object_id = _public_object_id(payload)
    items = _public_projection_items(root)
    if not any(item["object_id"] == object_id for item in items):
        raise ValueError("object_not_found")
    needle = f"/wiki/{object_id}"
    results = [
        _public_object_ref(item["object_id"])
        for item in items
        if item["object_id"] != object_id
        and (
            needle in item["body"]
            or object_id
            in {str(link).strip("/").split("/")[-1] for link in item.get("links", [])}
        )
    ]
    return {
        "schema_version": "backlinks-result/v1",
        "target": _public_object_ref(object_id),
        "items": results,
    }


def _handle_write_preview(root: Path, payload: dict[str, Any]) -> dict[str, Any]:
    files = _require_mapping(payload, "files", "files_required")
    return WriteOperation(root).preview(
        files,
        operation_type=str(payload.get("operation_type", "write")),
        vault_id=str(payload.get("vault_id", "public")),
    )


def _handle_write_apply(root: Path, payload: dict[str, Any]) -> dict[str, Any]:
    confirmation = payload.get("confirmation")
    if not isinstance(confirmation, dict):
        # F009 收紧：Agent 通道不得自证确认。人工凭据只能来自
        # confirm-apply CLI 生成的事件（hash 与 durable record 绑定）。
        return {
            "state": "blocked",
            "error_code": "skill_confirmation_required",
            "next_action": CONFIRM_NEXT_ACTION,
        }
    return WriteOperation(root).apply(
        str(payload.get("operation_id", "")),
        confirmed=True,
        actor_id=str(payload.get("actor_id", "local-user")),
        confirmation=confirmation,
    )


def _handle_source_preview(root: Path, payload: dict[str, Any]) -> dict[str, Any]:
    request = _require_mapping(payload, "request", "source_request_required")
    return SourceIngestor(root).preview(request)


def _handle_source_apply(root: Path, payload: dict[str, Any]) -> dict[str, Any]:
    confirmation = payload.get("confirmation")
    # source op record 尚无 diff_hash（Source writer 未统一迁移，F004 遗留），
    # 此处做轻校验（human actor + operation 绑定 + 自哈希）；完整 hash 绑定
    # 随 writer 统一迁移后切 validate_apply_confirmation。
    if (
        not isinstance(confirmation, dict)
        or confirmation.get("actor_type") != "human"
        or confirmation.get("operation_id") != payload.get("operation_id")
        or not confirmation.get("event_sha256")
    ):
        return {
            "state": "blocked",
            "error_code": "skill_confirmation_required",
            "next_action": CONFIRM_NEXT_ACTION,
        }
    return SourceIngestor(root).apply(
        str(payload.get("operation_id", "")),
        confirmed=True,
        actor_id=str(payload.get("actor_id", "local-user")),
    )


def _handle_wiki_validate(root: Path, payload: dict[str, Any]) -> dict[str, Any]:
    return WikiValidator(root).validate(_repo_relative_path(root, payload))


def _handle_publish_preview(root: Path, payload: dict[str, Any]) -> dict[str, Any]:
    report = _handle_wiki_validate(root, payload)
    derived = report.get("derived") or {}
    return {
        "state": "previewed" if report.get("valid") else "blocked",
        "wiki_report": report,
        "public_publishable": derived.get("public_publishable", False),
        "private_publishable": derived.get("private_publishable", False),
    }


def _handle_publish_confirm(root: Path, payload: dict[str, Any]) -> dict[str, Any]:
    return write_event(
        root, _require_mapping(payload, "event", "publish_event_required")
    )


def _handle_vault_check(root: Path, _payload: dict[str, Any]) -> dict[str, Any]:
    return VaultRegistry(root).check()


def _handle_backup_status(root: Path, _payload: dict[str, Any]) -> dict[str, Any]:
    return BackupManager(root).status()


def _handle_backup_manifest(root: Path, payload: dict[str, Any]) -> dict[str, Any]:
    return BackupManager(root).create_manifest(str(payload.get("vault_id", "public")))


def _handle_question_create(root: Path, payload: dict[str, Any]) -> dict[str, Any]:
    spec = _require_mapping(payload, "spec", "spec_required")
    candidate = _repo_relative_path(root, payload)
    if not candidate.is_file() or candidate.is_symlink():
        raise ValueError("wiki_not_found")
    report = WikiValidator(root).validate(candidate)
    return QuestionStore(root).create(spec, wiki_path=candidate, wiki_report=report)


def _handle_question_answer(root: Path, payload: dict[str, Any]) -> dict[str, Any]:
    scoring_mode = payload.get("scoring_mode", "manual")
    if scoring_mode not in {"manual", "deterministic", "llm"}:
        raise ValueError("scoring_mode_invalid")
    return QuestionStore(root).answer(
        str(payload.get("question_id", "")),
        payload.get("response"),
        scoring_mode=scoring_mode,
    )


def _handle_question_review(root: Path, payload: dict[str, Any]) -> dict[str, Any]:
    return QuestionStore(root).review(
        str(payload.get("question_id", "")), payload.get("rating")
    )


# action → handler 是 action 的唯一事实来源；ALLOWED_ACTIONS 由它派生，
# ACTION_FIELDS 必须与它键一致（tests/test_skill_runtime.py 有对账断言）。
_HANDLERS: dict[str, Callable[[Path, dict[str, Any]], dict[str, Any]]] = {
    "skill_status": _handle_skill_status,
    "query": _handle_query,
    "retrieve": _handle_query,
    "ask": _handle_ask,
    "read": _handle_read,
    "backlinks": _handle_backlinks,
    "write_preview": _handle_write_preview,
    "write_apply": _handle_write_apply,
    "source_preview": _handle_source_preview,
    "source_apply": _handle_source_apply,
    "wiki_validate": _handle_wiki_validate,
    "publish_preview": _handle_publish_preview,
    "publish_confirm": _handle_publish_confirm,
    "vault_check": _handle_vault_check,
    "backup_status": _handle_backup_status,
    "backup_manifest": _handle_backup_manifest,
    "question_create": _handle_question_create,
    "question_answer": _handle_question_answer,
    "question_review": _handle_question_review,
}
ALLOWED_ACTIONS = frozenset(_HANDLERS)


def dispatch(
    action: str, payload: dict[str, Any] | None = None, *, root: Path
) -> dict[str, Any]:
    payload = payload or {}
    handler = _HANDLERS.get(action)
    if handler is None:
        return {
            "state": "blocked",
            "error_code": "skill_action_not_allowed",
            "action": action,
        }
    if not isinstance(payload, dict) or any(key in FORBIDDEN_KEYS for key in payload):
        return {"state": "blocked", "error_code": "skill_payload_forbidden"}
    unknown = sorted(set(payload) - ACTION_FIELDS[action])
    if unknown:
        return {
            "state": "blocked",
            "error_code": "skill_payload_unknown_field",
            "fields": unknown,
        }
    try:
        return handler(Path(root).resolve(), payload)
    except (OSError, ValueError, TypeError) as exc:
        return {"state": "blocked", "error_code": str(exc)}
