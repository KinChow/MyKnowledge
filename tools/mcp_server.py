"""Official MCP stdio transport for the canonical MyKnowledge Skill (F009)."""
from __future__ import annotations

import argparse
import asyncio
import os
import secrets
import time
from pathlib import Path
from typing import Any

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
    protected_actions = {"write_preview", "write_apply", "source_preview", "source_apply", "wiki_validate", "publish_preview", "vault_check", "backup_manifest", "question_create", "question_answer", "question_review"}
    server = FastMCP("myknowledge", instructions="Controlled MyKnowledge actions; writes require preview and human confirmation.")

    @server.tool(name="myknowledge_dispatch", description="Dispatch one allowlisted MyKnowledge action through the existing domain runtime.")
    def myknowledge_dispatch(action: str, payload: dict[str, Any] | None = None, capability_token: str | None = None) -> dict[str, Any]:
        if action not in ALLOWED_ACTIONS:
            return {"state": "blocked", "error_code": "skill_action_not_allowed", "action": action}
        if expected_token and action in protected_actions:
            if not capability_token or not secrets.compare_digest(capability_token, expected_token):
                return {"state": "blocked", "error_code": "capability_token_invalid", "next_action": "provide the configured MCP capability token"}
            if time.time() - issued_at > capability_token_ttl_seconds:
                return {"state": "blocked", "error_code": "capability_token_expired", "next_action": "restart the MCP server for a fresh token"}
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
