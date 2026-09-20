"""统一 Source 创建契约（locator/kind/content）跨三入口的接入与安全门禁。

- 归一化：http/file/data/inline + kind → 内部 SourceIngestor 请求（形状不变）。
- 安全：非 file 白名单入口（skill/HTTP）拒 file:// 与 legacy 本地 input_path。
- 三入口：registry.create / skill source_ingest / backend POST /api/source / cli --from。
"""

from __future__ import annotations

from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from backend.app import create_app
from tools.content_registry import ContentRegistry
from tools.ingest.source_request import LocatorError, normalize_source_request
from tools.skill_runtime import dispatch


def test_normalize_maps_scheme_and_kind():
    note = normalize_source_request(
        {"content": "正文", "kind": "note", "domain": "tools", "source_id": "n1"}
    )
    assert note["source_type"] == "personal-note" and note["body"] == "正文"

    web = normalize_source_request(
        {"locator": "https://x/a", "kind": "doc", "domain": "computer-science"}
    )
    assert web["source_type"] == "doc" and web["url"] == "https://x/a"

    local = normalize_source_request(
        {"locator": "file:///tmp/a.md", "kind": "doc", "domain": "tools"}
    )
    assert local["source_type"] == "local-file" and local["input_path"].endswith("a.md")

    data = normalize_source_request(
        {"locator": "data:text/markdown,hi%20there", "domain": "tools"}
    )
    assert data["source_type"] == "personal-note" and data["body"] == "hi there"


def test_normalize_scheme_allowlist_blocks_local_reads():
    with pytest.raises(LocatorError) as e1:
        normalize_source_request(
            {"locator": "file:///etc/passwd", "kind": "doc", "domain": "tools"},
            allowed_schemes={"http", "https", "data"},
        )
    assert e1.value.code == "locator_scheme_not_allowed"

    # legacy 内部请求携带 input_path 也被拒（堵住绕过统一契约的本地读取）
    with pytest.raises(LocatorError) as e2:
        normalize_source_request(
            {
                "source_type": "local-file",
                "input_path": "/etc/passwd",
                "domain": "tools",
            },
            allowed_schemes={"http", "https", "data"},
        )
    assert e2.value.code == "locator_scheme_not_allowed"


def test_registry_create_accepts_unified_inline(tmp_path: Path):
    result = ContentRegistry(tmp_path).create(
        "source",
        request={
            "content": "# Note\n正文",
            "kind": "note",
            "domain": "tools",
            "source_id": "u-note",
        },
    )
    assert result["status"] == "ok"
    assert result["source_id"] == "u-note"


def test_skill_source_ingest_rejects_local_file(tmp_path: Path):
    blocked = dispatch(
        "source_ingest",
        {
            "request": {
                "locator": "file:///etc/passwd",
                "kind": "doc",
                "domain": "tools",
            }
        },
        root=tmp_path,
    )
    assert blocked["status"] == "blocked"
    assert blocked["error_code"] == "locator_scheme_not_allowed"


def test_skill_source_ingest_accepts_inline(tmp_path: Path):
    ok = dispatch(
        "source_ingest",
        {
            "request": {
                "content": "内联正文",
                "kind": "note",
                "domain": "tools",
                "source_id": "s-note",
            }
        },
        root=tmp_path,
    )
    assert ok["status"] == "ok"


def test_backend_create_source_endpoint(tmp_path: Path):
    client = TestClient(create_app(root=tmp_path, capability_token="token"))
    headers = {"X-MyKnowledge-Capability": "token"}
    body = {
        "content": "内联正文",
        "kind": "note",
        "domain": "tools",
        "source_id": "http-note",
    }
    assert client.post("/api/source", json=body).status_code == 401  # 需写能力
    ok = client.post("/api/source", headers=headers, json=body)
    assert ok.status_code == 200 and ok.json()["status"] == "ok"
    # file:// 经 HTTP 一律 403（不许网络侧读本地盘）
    forbidden = client.post(
        "/api/source",
        headers=headers,
        json={"locator": "file:///etc/passwd", "kind": "doc", "domain": "tools"},
    )
    assert forbidden.status_code == 403
    assert forbidden.json()["detail"]["code"] == "locator_scheme_not_allowed"


def test_cli_source_add_from_inline_content(tmp_path: Path):
    from tools.ingest.source_ingestor import main

    code = main(
        [
            "--root",
            str(tmp_path),
            "--content",
            "# CLI Note\n正文",
            "--kind",
            "note",
            "--domain",
            "tools",
            "--source-id",
            "cli-note",
        ]
    )
    assert code == 0
    assert (tmp_path / "content" / "sources" / "tools" / "cli-note").exists()


def _seed_inline_source(root: Path, source_id: str) -> None:
    ok = ContentRegistry(root).create(
        "source",
        request={
            "content": "初始正文",
            "kind": "note",
            "domain": "tools",
            "source_id": source_id,
        },
    )
    assert ok["status"] == "ok", ok


def test_skill_source_update_rejects_local_file(tmp_path: Path):
    """回归：update 面此前漏了 scheme 门禁，可经 file:// 读本地盘写入 source 正文。"""
    _seed_inline_source(tmp_path, "upd-note")
    blocked = dispatch(
        "source_update",
        {
            "request": {
                "source_id": "upd-note",
                "domain": "tools",
                "locator": "file:///etc/passwd",
                "kind": "doc",
            }
        },
        root=tmp_path,
    )
    assert blocked["status"] == "blocked"
    assert blocked["error_code"] == "locator_scheme_not_allowed"


def test_backend_update_source_rejects_local_file(tmp_path: Path):
    _seed_inline_source(tmp_path, "http-upd")
    client = TestClient(create_app(root=tmp_path, capability_token="token"))
    headers = {"X-MyKnowledge-Capability": "token"}
    forbidden = client.post(
        "/api/source/update",
        headers=headers,
        json={
            "source_id": "http-upd",
            "domain": "tools",
            "locator": "file:///etc/passwd",
            "kind": "doc",
        },
    )
    assert forbidden.status_code == 403
    assert forbidden.json()["detail"]["code"] == "locator_scheme_not_allowed"


def test_cli_source_update_allows_local_file(tmp_path: Path):
    """受信人用 CLI（SourceRepository 直调）仍可用 file:// 重导入本地文件。"""
    from tools.cli import source_update_main

    _seed_inline_source(tmp_path, "cli-upd")
    local = tmp_path / "note.md"
    local.write_text("本地重导入的正文", encoding="utf-8")
    request_file = tmp_path / "req.json"
    request_file.write_text(
        '{"source_id":"cli-upd","domain":"tools","locator":"file://'
        + str(local)
        + '","kind":"doc"}',
        encoding="utf-8",
    )
    assert source_update_main([str(request_file), "--root", str(tmp_path)]) == 0
    body = ContentRegistry(tmp_path).read(
        "source", vault_id="public", object_id="cli-upd"
    )
    assert "本地重导入的正文" in (body.get("body") or "")
