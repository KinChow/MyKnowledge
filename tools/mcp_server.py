"""Official MCP stdio transport for the canonical MyKnowledge Skill (F009)."""
from __future__ import annotations

import argparse
import asyncio
import os
import secrets
import time
from pathlib import Path
from typing import Any, Literal

from .capability import check_capability
from .skill_runtime import ALLOWED_ACTIONS, dispatch


def create_server(root: Path, capability_token: str | None = None, capability_token_ttl_seconds: float = 3600.0):
    """Build an MCP server bound to one explicit checkout."""
    try:
        from mcp.server.fastmcp import FastMCP
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError("mcp_unavailable") from exc
    checkout = Path(root).resolve()
    expected_token = capability_token or os.environ.get("MYKNOWLEDGE_MCP_CAPABILITY_TOKEN")
    issued_at = time.time()
    protected_actions = {"ask", "write_preview", "write_apply", "source_preview", "source_apply", "wiki_validate", "publish_preview", "publish_confirm", "vault_check", "backup_manifest", "question_create", "question_answer", "question_review"}
    server = FastMCP("myknowledge", instructions="Controlled MyKnowledge actions; writes require preview and human confirmation.")

    @server.tool(name="myknowledge_dispatch", description="Dispatch one allowlisted MyKnowledge action through the existing domain runtime.")
    def myknowledge_dispatch(action: Literal["skill_status", "query", "retrieve", "ask", "read", "backlinks", "write_preview", "write_apply", "source_preview", "source_apply", "wiki_validate", "publish_preview", "publish_confirm", "vault_check", "backup_status", "backup_manifest", "question_create", "question_answer", "question_review"], payload: dict[str, Any] | None = None, capability_token: str | None = None) -> dict[str, Any]:
        if action not in ALLOWED_ACTIONS:
            return {"state": "blocked", "error_code": "skill_action_not_allowed", "action": action}
        if expected_token and action in protected_actions:
            # 单实现校验核（tools.capability）；MCP 侧将错误元组翻译为 blocked 结果
            result = check_capability(
                capability_token, expected_token,
                created_at=issued_at, ttl_seconds=capability_token_ttl_seconds,
                scopes={"write"},  # MCP 侧无 scope 分级，token 有效即视为 write 级
            )
            if result is not None:
                code, _retryable, _next = result
                return {"state": "blocked", "error_code": code, "next_action": "provide the configured MCP capability token"}
        return dispatch(action, payload or {}, root=checkout)

    return server


async def _run(root: Path, capability_token: str | None = None) -> None:
    await create_server(root, capability_token).run_stdio_async()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="MyKnowledge MCP stdio server")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--capability-token", default=os.environ.get("MYKNOWLEDGE_MCP_CAPABILITY_TOKEN"))
    args = parser.parse_args(argv)
    asyncio.run(_run(args.root, args.capability_token))
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
