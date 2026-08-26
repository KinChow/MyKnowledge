"""Official MCP stdio transport for the canonical MyKnowledge Skill (F009)."""
from __future__ import annotations

import argparse
import asyncio
from pathlib import Path
from typing import Any

from .skill_runtime import ALLOWED_ACTIONS, dispatch


def create_server(root: Path):
    """Build an MCP server bound to one explicit checkout."""
    try:
        from mcp.server.fastmcp import FastMCP
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError("mcp_unavailable") from exc
    checkout = Path(root).resolve()
    server = FastMCP("myknowledge", instructions="Controlled MyKnowledge actions; writes require preview and human confirmation.")

    @server.tool(name="myknowledge_dispatch", description="Dispatch one allowlisted MyKnowledge action through the existing domain runtime.")
    def myknowledge_dispatch(action: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        if action not in ALLOWED_ACTIONS:
            return {"state": "blocked", "error_code": "skill_action_not_allowed", "action": action}
        return dispatch(action, payload or {}, root=checkout)

    return server


async def _run(root: Path) -> None:
    await create_server(root).run_stdio_async()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="MyKnowledge MCP stdio server")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args(argv)
    asyncio.run(_run(args.root))
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
