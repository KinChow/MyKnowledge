"""Small shared access policy for HTTP and MCP, not a user/role system.

Only named read operations may be anonymous. Unknown/new operations default to
write capability, so adding a handler cannot accidentally create an open writer.
The transport owns credentials; caller-supplied query scope is never authority.
"""

from __future__ import annotations

from typing import Any

CAPABILITY_SCOPES = frozenset({"local-read", "private-read", "vault-check", "write"})
LOCAL_READ_ACTIONS = frozenset(
    {
        "question_list",
        "question_errors",
        "question_queue",
        "question_session_get",
        "backup_status",
    }
)


def capability_for(action: str, payload: dict[str, Any] | None = None) -> str | None:
    payload = payload or {}
    fixed = {
        "skill_status": None,
        "vault_check": "vault-check",
        **dict.fromkeys(LOCAL_READ_ACTIONS, "local-read"),
    }
    if action in fixed:
        return fixed[action]
    if action in {"query", "retrieve", "ask", "citation_replay"}:
        scope = payload.get("scope", "public")
        return (
            None
            if scope == "public" and action == "query"
            else "private-read"
            if scope == "private"
            else "local-read"
        )
    if action in {"read", "list", "backlinks"}:
        kind = payload.get("object_type", "wiki")
        vault = payload.get("vault_id", "public")
        if kind == "question":
            return "local-read"
        if vault != "public" or payload.get("scope") == "private":
            return "private-read"
        if kind == "wiki" and payload.get("scope", "public") == "public":
            return None
        return "local-read"
    return "write"
