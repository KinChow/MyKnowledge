from pathlib import Path
import asyncio

from tools.skill_runtime import dispatch
from tools.mcp_server import create_server


def test_skill_runtime_rejects_unknown_and_dangerous_actions(tmp_path: Path):
    assert dispatch("shell", {}, root=tmp_path)["error_code"] == "skill_action_not_allowed"
    assert dispatch("vault_check", {"command": "git status"}, root=tmp_path)["error_code"] == "skill_payload_forbidden"


def test_skill_runtime_write_preview_delegates_to_writer(tmp_path: Path):
    result = dispatch("write_preview", {"files": {"wiki/item.md": "# Item\n"}}, root=tmp_path)
    assert result["state"] == "previewed"
    assert not (tmp_path / "wiki" / "item.md").exists()


def test_skill_runtime_apply_requires_explicit_confirmation(tmp_path: Path):
    preview = dispatch("write_preview", {"files": {"wiki/item.md": "# Item\n"}}, root=tmp_path)
    blocked = dispatch("write_apply", {"operation_id": preview["operation_id"]}, root=tmp_path)
    assert blocked["state"] == "awaiting_confirmation"
    assert not (tmp_path / "wiki" / "item.md").exists()


def test_mcp_server_exposes_one_controlled_tool_bound_to_checkout(tmp_path: Path):
    async def exercise():
        server = create_server(tmp_path)
        tools = await server.list_tools()
        assert len(tools) == 1
        assert tools[0].name == "myknowledge_dispatch"
        _, result = await server.call_tool("myknowledge_dispatch", {"action": "shell", "payload": {}})
        assert result["error_code"] == "skill_action_not_allowed"
        _, result = await server.call_tool("myknowledge_dispatch", {"action": "write_preview", "payload": {"files": {"wiki/mcp.md": "# MCP\n"}}})
        assert result["state"] == "previewed"
    asyncio.run(exercise())
    assert not (tmp_path / "wiki" / "mcp.md").exists()
