from pathlib import Path
import asyncio

from tools.skill_runtime import dispatch
from tools.mcp_server import create_server
import json


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


def test_skill_public_query_and_read_use_projection_allowlist(tmp_path: Path):
    body = tmp_path / "wiki" / "one.md"; body.parent.mkdir(parents=True); body.write_text("中文 projection", encoding="utf-8")
    manifest = {"schema_version": "public-projection/v1", "projection": "public", "items": [{"id": "one", "vault_id": "public", "public_publishable": True, "public_release": True, "status": "published", "effective_confidentiality": "public", "body_path": "wiki/one.md", "title": "One"}]}
    (tmp_path / "queries" / "public").mkdir(parents=True); (tmp_path / "queries" / "public" / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    query = dispatch("query", {"query": "projection", "scope": "public"}, root=tmp_path)
    assert query["schema_version"] == "query-result/v1" and query["items"][0]["object_ref"]["object_id"] == "one"
    read = dispatch("read", {"vault_id": "public", "object_id": "one"}, root=tmp_path)
    assert read["body"] == "中文 projection"
    assert dispatch("query", {"query": "projection", "scope": "private"}, root=tmp_path)["error_code"] == "skill_public_query_only"


def test_skill_source_preview_and_apply_delegate_to_source_service(tmp_path: Path):
    request = {"source_type": "personal-note", "domain": "tools", "source_id": "skill-source", "body": "A source body"}
    preview = dispatch("source_preview", {"request": request}, root=tmp_path)
    assert preview["state"] == "previewed"
    blocked = dispatch("source_apply", {"operation_id": preview["operation_id"]}, root=tmp_path)
    assert blocked["state"] == "awaiting_confirmation"
    applied = dispatch("source_apply", {"operation_id": preview["operation_id"], "confirmed": True}, root=tmp_path)
    assert applied["state"] == "applied"


def test_skill_wiki_validate_and_publish_preview_are_domain_only(tmp_path: Path):
    wiki = tmp_path / "wiki" / "skill.md"
    wiki.parent.mkdir(parents=True)
    wiki.write_text("---\nschema_version: wiki/v1\nid: skill\nkind: knowledge\ntitle: Skill\nstatus: draft\npublication_scope: none\nconfidentiality: public\nsources: []\nevidence: []\n---\n\n# Skill\n", encoding="utf-8")
    result = dispatch("wiki_validate", {"wiki_path": "wiki/skill.md"}, root=tmp_path)
    assert result["object_ref"]["object_id"] == "skill"
    preview = dispatch("publish_preview", {"wiki_path": "wiki/skill.md"}, root=tmp_path)
    assert preview["state"] == "blocked"
    assert "wiki_report" in preview
    assert dispatch("wiki_validate", {"wiki_path": "../secret.md"}, root=tmp_path)["error_code"] == "path_invalid"
