"""三入口（skill dispatch / backend HTTP / CLI）经 ContentRegistry 接入统一 CRUD。

验证 source/wiki/question 的 list/retire/(source)update 动词在三个物理入口都可达，
且失败语义一致（未知类型→object_type_not_found，动词不支持→capability_not_supported，
缺写能力→401）。领域正确性（RESTRICT/CASCADE/幂等）在 repository 单测里，此处只测接入。
"""

from __future__ import annotations

import io
import json
from contextlib import redirect_stdout
from pathlib import Path

from fastapi.testclient import TestClient

from backend.app import create_app
from tools.skill_runtime import dispatch
from tools.source_repository import SourceRepository


def _note_request(source_id: str, body: str) -> dict:
    return {
        "source_type": "personal-note",
        "domain": "tools",
        "origin": "personal",
        "body": body,
        "source_id": source_id,
    }


def _seed_source(root: Path, source_id: str, body: str = "正文一。") -> None:
    result = SourceRepository(root).create(_note_request(source_id, body))
    assert result["status"] == "ok", result


def test_skill_list_retire_source_update_route_through_registry(tmp_path: Path):
    _seed_source(tmp_path, "src-a")
    listed = dispatch(
        "list", {"object_type": "source", "vault_id": "public"}, root=tmp_path
    )
    assert listed["status"] == "ok"
    ids = {item["object_ref"]["object_id"] for item in listed["items"]}
    assert "src-a" in ids

    updated = dispatch(
        "source_update",
        {"request": _note_request("src-a", "改写后的正文。")},
        root=tmp_path,
    )
    assert updated["status"] == "ok"
    assert updated["changed"] is True

    retired = dispatch(
        "retire",
        {"object_type": "source", "vault_id": "public", "object_id": "src-a"},
        root=tmp_path,
    )
    assert retired["status"] == "ok"
    assert retired["retired"] is True


def test_skill_list_unknown_type_and_source_update_requires_request(tmp_path: Path):
    miss = dispatch("list", {"object_type": "nope"}, root=tmp_path)
    assert miss["status"] == "blocked"
    assert miss["error_code"] == "object_type_not_found"
    bad = dispatch("source_update", {}, root=tmp_path)
    assert bad["error_code"] == "source_request_required"


def test_backend_list_source_is_anonymous_for_public(tmp_path: Path):
    _seed_source(tmp_path, "src-http")
    client = TestClient(create_app(root=tmp_path, capability_token="token"))
    resp = client.get("/api/list/public/source")
    assert resp.status_code == 200
    ids = {item["object_ref"]["object_id"] for item in resp.json()["items"]}
    assert "src-http" in ids


def test_backend_delete_and_update_require_write_capability(tmp_path: Path):
    _seed_source(tmp_path, "src-del")
    client = TestClient(create_app(root=tmp_path, capability_token="token"))
    assert client.delete("/api/object/public/source/src-del").status_code == 401
    anon_update = client.post("/api/source/update", json=_note_request("src-del", "x"))
    assert anon_update.status_code == 401

    headers = {"X-MyKnowledge-Capability": "token"}
    updated = client.post(
        "/api/source/update", headers=headers, json=_note_request("src-del", "新正文。")
    )
    assert updated.status_code == 200
    assert updated.json()["status"] == "ok"

    deleted = client.delete("/api/object/public/source/src-del", headers=headers)
    assert deleted.status_code == 200
    assert deleted.json()["retired"] is True


def test_backend_delete_unknown_type_is_structured_404(tmp_path: Path):
    client = TestClient(create_app(root=tmp_path, capability_token="token"))
    headers = {"X-MyKnowledge-Capability": "token"}
    unknown = client.delete("/api/object/public/nope/x", headers=headers)
    assert unknown.status_code == 404
    assert unknown.json()["detail"]["code"] == "object_type_not_found"


def test_cli_list_and_retire_route_through_registry(tmp_path: Path):
    from tools.cli import content_list_main, content_retire_main

    _seed_source(tmp_path, "src-cli")
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        code = content_list_main(["source", "--root", str(tmp_path)])
    assert code == 0
    payload = json.loads(buffer.getvalue())
    assert "src-cli" in {i["object_ref"]["object_id"] for i in payload["items"]}

    buffer = io.StringIO()
    with redirect_stdout(buffer):
        code = content_retire_main(["source", "src-cli", "--root", str(tmp_path)])
    assert code == 0
    assert json.loads(buffer.getvalue())["retired"] is True
