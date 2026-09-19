"""Official MCP stdio transport for the canonical MyKnowledge Skill (F009)."""

from __future__ import annotations

import argparse
import asyncio
import os
import time
from pathlib import Path
from typing import Any, Literal

from . import contract
from .capability import check_capability
from .skill_runtime import ALLOWED_ACTIONS, dispatch

# action 签名从 skill_runtime 派生，不手抄：此前这里硬编码了一份 Literal 副本，
# 与 ALLOWED_ACTIONS 各自演化，删掉两阶段写入后它仍列着 write_preview/write_apply/
# source_preview/source_apply 四个已不存在的 action，而真正的 write/source_ingest
# 反而不在——漂移的静默代价是 MCP 面没有可调用的写入能力。
_ACTIONS = tuple(sorted(ALLOWED_ACTIONS))
Action = Literal[*_ACTIONS]


def create_server(
    root: Path,
    capability_token: str | None = None,
    capability_token_ttl_seconds: float = 3600.0,
):
    """Build an MCP server bound to one explicit checkout."""
    try:
        from mcp.server.fastmcp import FastMCP
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError("mcp_unavailable") from exc
    checkout = Path(root).resolve()
    expected_token = capability_token or os.environ.get(
        "MYKNOWLEDGE_MCP_CAPABILITY_TOKEN"
    )
    issued_at = time.time()
    protected_actions = {
        "ask",
        "write",
        "source_ingest",
        "wiki_validate",
        "publish_preview",
        "publish_confirm",
        "vault_check",
        "backup_manifest",
        "question_create",
        "question_list",
        "question_session",
        "question_errors",
        "question_queue",
        "question_disable",
        "question_enable",
        "question_delete",
        "question_answer",
        "question_review",
    }
    server = FastMCP(
        "myknowledge",
        instructions=(
            "Controlled MyKnowledge actions. Writes (write/source_ingest) land "
            "directly in the checkout; approval is the human's git commit, so a "
            "capability token still gates every mutating action."
        ),
    )

    @server.tool(
        name="myknowledge_dispatch",
        description="Dispatch one allowlisted MyKnowledge action through the existing domain runtime.",
    )
    def myknowledge_dispatch(
        action: Action,
        payload: dict[str, Any] | None = None,
        capability_token: str | None = None,
    ) -> dict[str, Any]:
        if action not in ALLOWED_ACTIONS:
            return contract.blocked(
                "skill-dispatch/v1", "skill_action_not_allowed", action=action
            )
        if expected_token and action in protected_actions:
            # 单实现校验核（tools.capability）；MCP 侧将错误元组翻译为 blocked 结果
            result = check_capability(
                capability_token,
                expected_token,
                created_at=issued_at,
                ttl_seconds=capability_token_ttl_seconds,
                scopes={"write"},  # MCP 侧无 scope 分级，token 有效即视为 write 级
            )
            if result is not None:
                code, _retryable, _next = result
                return contract.blocked(
                    "skill-dispatch/v1",
                    code,
                    next_action="provide the configured MCP capability token",
                )
        return dispatch(action, payload or {}, root=checkout)

    return server


async def _run(root: Path, capability_token: str | None = None) -> None:
    await create_server(root, capability_token).run_stdio_async()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="MyKnowledge MCP stdio server")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument(
        "--capability-token", default=os.environ.get("MYKNOWLEDGE_MCP_CAPABILITY_TOKEN")
    )
    args = parser.parse_args(argv)
    asyncio.run(_run(args.root, args.capability_token))
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
