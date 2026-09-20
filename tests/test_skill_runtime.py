import asyncio
import json
import sys
from pathlib import Path

from tools.mcp_server import create_server
from tools.skill_runtime import ACTION_FIELDS, ALLOWED_ACTIONS, dispatch


def test_action_table_and_field_contract_stay_in_sync():
    """白名单由 handler 表派生；字段契约漏一条 action 就会放过未知字段。"""
    assert set(ACTION_FIELDS) == set(ALLOWED_ACTIONS)


def test_skill_runtime_rejects_unknown_and_dangerous_actions(tmp_path: Path):
    assert (
        dispatch("shell", {}, root=tmp_path)["error_code"] == "skill_action_not_allowed"
    )
    assert (
        dispatch("vault_check", {"command": "git status"}, root=tmp_path)["error_code"]
        == "skill_payload_forbidden"
    )
    assert (
        dispatch(
            "query",
            {"query": "x", "provider_url": "https://example.invalid"},
            root=tmp_path,
        )["error_code"]
        == "skill_payload_unknown_field"
    )


def test_skill_runtime_write_is_direct_and_lands_content(tmp_path: Path):
    """写入是直接落盘（ADR-0019）：无 operation_id、无 preview 态、无确认事件。

    直写路径只保留一条写前约束：越界路径（越界写不可逆）。`content/working/` 的出处
    门已删除（A1-深，2026-09-15）——无回指的草稿现在直接落盘，出处校验归晋升关口。
    """
    result = dispatch(
        "write", {"files": {"content/wiki/item.md": "# Item\n"}}, root=tmp_path
    )
    assert result["status"] == "ok"
    assert result["changed"] is True
    assert result["applied_files"] == ["content/wiki/item.md"]
    assert "operation_id" not in result
    assert (tmp_path / "content" / "wiki" / "item.md").read_text(
        encoding="utf-8"
    ) == "# Item\n"

    assert (
        dispatch("write", {"files": {"../escape.md": "x"}}, root=tmp_path)["error_code"]
        == "path_outside_repo"
    )
    assert not (tmp_path / "escape.md").exists()

    # A1-深：working 层无回指约束，草稿直接落盘（低摩擦，出处门在晋升）
    working = dispatch(
        "write", {"files": {"content/working/draft.md": "草稿\n"}}, root=tmp_path
    )
    assert working["status"] == "ok"
    assert working["changed"] is True
    assert (tmp_path / "content" / "working" / "draft.md").read_text(
        encoding="utf-8"
    ) == "草稿\n"


def test_mcp_server_exposes_one_controlled_tool_bound_to_checkout(tmp_path: Path):
    async def exercise():
        server = create_server(tmp_path)
        tools = await server.list_tools()
        assert len(tools) == 1
        assert tools[0].name == "myknowledge_dispatch"
        assert "ask" in tools[0].input_schema["properties"]["action"]["enum"]
        assert "shell" not in tools[0].input_schema["properties"]["action"]["enum"]
        import pytest

        with pytest.raises(Exception, match="Input should be"):
            await server.call_tool(
                "myknowledge_dispatch", {"action": "shell", "payload": {}}
            )
        result = await server.call_tool(
            "myknowledge_dispatch",
            {"action": "vault_check", "payload": {}},
        )
        assert result.structured_content["schema_version"] == "vault-check/v1"

    asyncio.run(exercise())


def test_mcp_server_enforces_configured_capability_for_sensitive_actions(
    tmp_path: Path,
):
    """能力令牌门禁只认 token：缺失阻断、正确 token 才到领域服务。

    受测 action 只能是 MCP tool schema 声明过的那个集合（`tools/mcp_server.py`
    的 Literal 与 `protected_actions`）；ADR-0019 之后该文件尚未把写入 action
    同步为 `write`，故这里用同属受保护集合的 `vault_check` 承载该边界。
    """

    async def exercise():
        server = create_server(tmp_path, capability_token="mcp-secret")
        denied = await server.call_tool(
            "myknowledge_dispatch",
            {"action": "vault_check", "payload": {}},
        )
        assert denied.structured_content["error_code"] == "capability_token_required"
        allowed = await server.call_tool(
            "myknowledge_dispatch",
            {"action": "vault_check", "payload": {}, "capability_token": "mcp-secret"},
        )
        assert allowed.structured_content["schema_version"] == "vault-check/v1"

    asyncio.run(exercise())


def test_mcp_server_expires_capability_token(tmp_path: Path):
    async def exercise():
        server = create_server(
            tmp_path, capability_token="short-lived", capability_token_ttl_seconds=-1
        )
        expired = await server.call_tool(
            "myknowledge_dispatch",
            {
                "action": "vault_check",
                "payload": {},
                "capability_token": "short-lived",
            },
        )
        assert expired.structured_content["error_code"] == "capability_token_expired"

    asyncio.run(exercise())


def test_mcp_stdio_transport_lists_and_calls_controlled_tool(tmp_path: Path):
    async def exercise():
        from mcp import ClientSession, StdioServerParameters
        from mcp.client.stdio import stdio_client

        parameters = StdioServerParameters(
            command=sys.executable,
            args=[
                "-m",
                "tools.mcp_server",
                "--root",
                str(tmp_path),
                "--capability-token",
                "stdio-secret",
            ],
            env=None,
        )
        async with stdio_client(parameters) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                listed = await session.list_tools()
                assert [tool.name for tool in listed.tools] == ["myknowledge_dispatch"]
                denied = await session.call_tool(
                    "myknowledge_dispatch",
                    {
                        "action": "vault_check",
                        "payload": {},
                    },
                )
                denied_value = json.loads(denied.content[0].text)
                assert denied_value["error_code"] == "capability_token_required"
                allowed = await session.call_tool(
                    "myknowledge_dispatch",
                    {
                        "action": "vault_check",
                        "payload": {},
                        "capability_token": "stdio-secret",
                    },
                )
                allowed_value = json.loads(allowed.content[0].text)
                assert allowed_value["schema_version"] == "vault-check/v1"

    asyncio.run(exercise())


def test_skill_public_query_and_read_use_projection_allowlist(tmp_path: Path):
    body = tmp_path / "content" / "wiki" / "one.md"
    body.parent.mkdir(parents=True)
    body.write_text("中文 projection", encoding="utf-8")
    manifest = {
        "schema_version": "public-projection/v1",
        "projection": "public",
        "items": [
            {
                "id": "one",
                "vault_id": "public",
                "public_publishable": True,
                "public_release": True,
                "status": "published",
                "effective_confidentiality": "public",
                "body_path": "content/wiki/one.md",
                "title": "One",
            }
        ],
    }
    (tmp_path / "var" / "queries" / "public").mkdir(parents=True)
    (tmp_path / "var" / "queries" / "public" / "manifest.json").write_text(
        json.dumps(manifest), encoding="utf-8"
    )
    query = dispatch("query", {"query": "projection", "scope": "public"}, root=tmp_path)
    assert (
        query["schema_version"] == "query-result/v1"
        and query["items"][0]["object_ref"]["object_id"] == "one"
    )
    read = dispatch("read", {"vault_id": "public", "object_id": "one"}, root=tmp_path)
    assert read["body"] == "中文 projection"
    assert (
        dispatch("query", {"query": "projection", "scope": "private"}, root=tmp_path)[
            "error_code"
        ]
        == "skill_public_query_only"
    )


def test_skill_retrieve_and_backlinks_are_projection_only(tmp_path: Path):
    wiki = tmp_path / "content" / "wiki"
    wiki.mkdir(parents=True, exist_ok=True)
    (wiki / "one.md").write_text("one", encoding="utf-8")
    (wiki / "two.md").write_text("See [one](/wiki/one).", encoding="utf-8")
    manifest = {
        "schema_version": "public-projection/v1",
        "projection": "public",
        "items": [
            {
                "id": "one",
                "vault_id": "public",
                "public_publishable": True,
                "public_release": True,
                "status": "published",
                "effective_confidentiality": "public",
                "body_path": "content/wiki/one.md",
                "title": "One",
            },
            {
                "id": "two",
                "vault_id": "public",
                "public_publishable": True,
                "public_release": True,
                "status": "published",
                "effective_confidentiality": "public",
                "body_path": "content/wiki/two.md",
                "title": "Two",
            },
        ],
    }
    path = tmp_path / "var" / "queries" / "public"
    path.mkdir(parents=True)
    (path / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    retrieve = dispatch("retrieve", {"query": "one"}, root=tmp_path)
    assert retrieve["schema_version"] == "query-result/v1"
    backlinks = dispatch(
        "backlinks", {"vault_id": "public", "object_id": "one"}, root=tmp_path
    )
    assert backlinks["items"] == [
        {"vault_id": "public", "object_type": "wiki", "object_id": "two"}
    ]
    assert (
        dispatch(
            "backlinks", {"vault_id": "private", "object_id": "one"}, root=tmp_path
        )["error_code"]
        == "skill_private_read_requires_api"
    )


def test_skill_ask_reuses_public_retrieval_and_offline_boundary(tmp_path: Path):
    wiki = tmp_path / "content" / "wiki"
    wiki.mkdir(parents=True, exist_ok=True)
    (wiki / "one.md").write_text("中文 projection", encoding="utf-8")
    (tmp_path / "content" / "practice" / "questions").mkdir(parents=True)
    (tmp_path / "content" / "practice" / "questions" / "q.json").write_text(
        '{"answer":"secret"}', encoding="utf-8"
    )
    manifest_dir = tmp_path / "var" / "queries" / "public"
    manifest_dir.mkdir(parents=True)
    manifest_dir.joinpath("manifest.json").write_text(
        json.dumps(
            {
                "schema_version": "public-projection/v1",
                "projection": "public",
                "items": [
                    {
                        "id": "one",
                        "vault_id": "public",
                        "public_publishable": True,
                        "public_release": True,
                        "status": "published",
                        "effective_confidentiality": "public",
                        "body_path": "content/wiki/one.md",
                        "title": "One",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    result = dispatch("ask", {"query": "projection", "scope": "public"}, root=tmp_path)
    assert result["schema_version"] == "ask-result/v1"
    assert result["answer"] is None and result["availability"] == "unavailable"
    assert result["retrieval"]["items"][0]["object_ref"]["object_id"] == "one"
    assert (
        dispatch("ask", {"query": "secret", "scope": "private"}, root=tmp_path)[
            "error_code"
        ]
        == "skill_public_query_only"
    )


def test_skill_status_is_fail_closed_for_canonical_skill(tmp_path: Path):
    assert (
        dispatch("skill_status", {}, root=tmp_path)["error_code"] == "skill_unavailable"
    )
    skill = tmp_path / "skills" / "myknowledge" / "SKILL.md"
    skill.parent.mkdir(parents=True)
    skill.write_text(
        "name: myknowledge\nUse tools.cli with explicit human confirmation.\n",
        encoding="utf-8",
    )
    assert dispatch("skill_status", {}, root=tmp_path)["status"] == "ok"


def test_skill_source_ingest_delegates_to_source_service(tmp_path: Path):
    """source_ingest 是直接写：单次调用完成采集，无 operation 记录与确认事件（ADR-0019）。"""
    request = {
        "source_type": "personal-note",
        "domain": "tools",
        "source_id": "skill-source",
        "body": "A source body",
    }
    applied = dispatch("source_ingest", {"request": request}, root=tmp_path)
    assert applied["status"] == "ok", applied
    assert applied["source_id"] == "skill-source"
    assert (
        tmp_path / "content" / "sources" / "tools" / "skill-source" / "skill-source.md"
    ).is_file()


def test_skill_wiki_validate_and_publish_preview_are_domain_only(tmp_path: Path):
    wiki = tmp_path / "content" / "wiki" / "skill.md"
    wiki.parent.mkdir(parents=True)
    wiki.write_text(
        "---\nschema_version: wiki/v1\nid: skill\nkind: knowledge\ntitle: Skill\nstatus: draft\npublication_scope: none\nconfidentiality: public\nsources: []\nevidence: []\n---\n\n# Skill\n",
        encoding="utf-8",
    )
    result = dispatch(
        "wiki_validate", {"wiki_path": "content/wiki/skill.md"}, root=tmp_path
    )
    assert result["object_ref"]["object_id"] == "skill"
    preview = dispatch(
        "publish_preview", {"wiki_path": "content/wiki/skill.md"}, root=tmp_path
    )
    assert preview["status"] == "ok"
    assert preview["public_publishable"] is False
    assert "wiki_report" in preview
    assert (
        dispatch("wiki_validate", {"wiki_path": "../secret.md"}, root=tmp_path)[
            "error_code"
        ]
        == "path_invalid"
    )


def test_skill_publish_confirm_delegates_event_validation(tmp_path: Path):
    event = {
        "schema_version": "public-release-confirmation/v1",
        "event_id": "event-skill",
        "operation_id": "op-skill",
        "target_ref": {
            "vault_id": "public",
            "object_type": "wiki",
            "object_id": "skill",
        },
        "target_vault": "public",
        "actor_type": "human",
        "actor_id": "alice",
        "decision": "approve",
        "release_input_sha256": "sha256:input",
        "reviewed_content_sha256": "sha256:content",
        "reviewed_evidence_sha256": "sha256:evidence",
        "leak_gate_report_sha256": "sha256:leak",
        "leak_gate_report_scope": "input-tree",
        "reason": "Reviewed public knowledge release",
        "confirmation_nonce": "nonce-skill",
    }
    result = dispatch("publish_confirm", {"event": event}, root=tmp_path)
    assert result["status"] == "ok"
    assert result["changed"] is True
    assert (tmp_path / "release" / "public-confirmations" / "event-skill.json").exists()
    invalid = dispatch(
        "publish_confirm",
        {"event": {**event, "event_id": "event-bad", "reason": "https://private"}},
        root=tmp_path,
    )
    assert invalid["error_code"] == "reason_not_public_safe"


def test_skill_question_answer_preserves_scoring_mode_boundary(tmp_path: Path):
    from tools.question import QuestionStore

    report = {
        "valid": True,
        "object_ref": {"object_type": "wiki", "object_id": "wiki-one"},
        "metadata": {"evidence": [{"claim_id": "claim-one"}]},
        "derived": {"evidence_state": "supported"},
        "hashes": {"content_sha256": "sha256:c", "evidence_sha256": "sha256:e"},
    }
    spec = {
        "id": "q-one",
        "type": "short_answer",
        "wiki_id": "wiki-one",
        "claim_id": "claim-one",
        "prompt": "Explain",
        "rubric": ["核心"],
    }
    QuestionStore(tmp_path).create(spec, wiki_report=report)
    deterministic = dispatch(
        "question_answer",
        {"question_id": "q-one", "response": "核心", "scoring_mode": "deterministic"},
        root=tmp_path,
    )
    assert deterministic["grading"]["state"] == "graded"
    assert deterministic["grading"]["scoring_provider"] == "deterministic_rubric"
    invalid = dispatch(
        "question_answer",
        {"question_id": "q-one", "response": "x", "scoring_mode": "other"},
        root=tmp_path,
    )
    assert invalid["error_code"] == "scoring_mode_invalid"


def test_skill_question_create_requires_validator_backed_wiki_path(tmp_path: Path):
    spec = {
        "id": "q-one",
        "type": "short_answer",
        "wiki_id": "wiki-one",
        "claim_id": "claim-one",
        "prompt": "Explain",
        "rubric": ["核心"],
    }
    missing = dispatch("question_create", {"spec": spec}, root=tmp_path)
    assert missing["error_code"] == "wiki_path_required"
    traversal = dispatch(
        "question_create", {"spec": spec, "wiki_path": "../wiki.md"}, root=tmp_path
    )
    assert traversal["error_code"] == "path_invalid"


def test_skill_question_create_delegates_validated_report(tmp_path: Path):
    from unittest import mock

    wiki = tmp_path / "content" / "wiki" / "one.md"
    wiki.parent.mkdir(parents=True)
    wiki.write_text("# one\n", encoding="utf-8")
    spec = {
        "id": "q-one",
        "type": "short_answer",
        "wiki_id": "wiki-one",
        "claim_id": "claim-one",
        "prompt": "Explain",
        "rubric": ["核心"],
    }
    report = {
        "valid": True,
        "object_ref": {"object_type": "wiki", "object_id": "wiki-one"},
        "metadata": {"evidence": [{"claim_id": "claim-one"}]},
        "derived": {"evidence_state": "supported"},
        "hashes": {"content_sha256": "sha256:c", "evidence_sha256": "sha256:e"},
    }
    with (
        mock.patch(
            "tools.skill_runtime.WikiValidator.validate", return_value=report
        ) as validate,
        mock.patch(
            "tools.skill_runtime.QuestionStore.create",
            return_value={"state": "created"},
        ) as create,
    ):
        result = dispatch(
            "question_create",
            {"spec": spec, "wiki_path": "content/wiki/one.md"},
            root=tmp_path,
        )
    assert result["state"] == "created"
    validate.assert_called_once_with(wiki)
    create.assert_called_once_with(spec, wiki_path=wiki, wiki_report=report)
