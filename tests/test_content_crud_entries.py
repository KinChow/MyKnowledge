"""三入口（skill dispatch / backend HTTP / CLI）经 ContentRegistry 接入统一 CRUD。

验证 source/wiki/question 的 list/retire/(source)update 动词在三个物理入口都可达，
且失败语义一致（未知类型→object_type_not_found，动词不支持→capability_not_supported，
缺写能力→401）。领域正确性（RESTRICT/CASCADE/幂等）在 repository 单测里，此处只测接入。
"""

from __future__ import annotations

import io
import json
import time
from contextlib import redirect_stdout
from pathlib import Path

from fastapi.testclient import TestClient

from backend.app import create_app
from tools import retire_ledger
from tools.paths import RepoPaths
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

    deleted = dispatch(
        "delete",
        {"object_type": "source", "vault_id": "public", "object_id": "src-a"},
        root=tmp_path,
    )
    assert deleted["status"] == "ok"
    assert deleted["retired"] is True


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


def test_cli_list_and_delete_route_through_registry(tmp_path: Path):
    from tools.cli import content_delete_main, content_list_main

    _seed_source(tmp_path, "src-cli")
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        code = content_list_main(["source", "--root", str(tmp_path)])
    assert code == 0
    payload = json.loads(buffer.getvalue())
    assert "src-cli" in {i["object_ref"]["object_id"] for i in payload["items"]}

    buffer = io.StringIO()
    with redirect_stdout(buffer):
        code = content_delete_main(["source", "src-cli", "--root", str(tmp_path)])
    assert code == 0
    assert json.loads(buffer.getvalue())["retired"] is True


def _mark_deleted_long_ago(root: Path, object_type: str, object_id: str) -> None:
    """模拟"很久以前已软删"：直接写一条过期的 delete 墓碑（跳过宽限期等待）。"""
    retire_ledger.append_retire(
        RepoPaths(root),
        object_type,
        vault_id="public",
        object_id=object_id,
        reason="delete",
        at=time.time() - 100 * 86400,
    )


def test_skill_purge_is_two_phase_and_reclaims_source_dir(tmp_path: Path):
    _seed_source(tmp_path, "src-p")
    src_dir = tmp_path / "content" / "sources" / "tools" / "src-p"
    assert src_dir.exists()

    # 未先软删 → not_deleted
    blocked = dispatch(
        "purge",
        {"object_type": "source", "vault_id": "public", "object_id": "src-p"},
        root=tmp_path,
    )
    assert blocked["error_code"] == "not_deleted"

    # 软删但未过宽限期 → retention_not_elapsed
    dispatch(
        "delete",
        {"object_type": "source", "vault_id": "public", "object_id": "src-p"},
        root=tmp_path,
    )
    too_soon = dispatch(
        "purge",
        {"object_type": "source", "vault_id": "public", "object_id": "src-p"},
        root=tmp_path,
    )
    assert too_soon["error_code"] == "retention_not_elapsed"

    # 过宽限期 → 物理回收目录 + 幂等
    _mark_deleted_long_ago(tmp_path, "source", "src-p")
    purged = dispatch(
        "purge",
        {"object_type": "source", "vault_id": "public", "object_id": "src-p"},
        root=tmp_path,
    )
    assert purged["status"] == "ok"
    assert purged["purged"] is True
    assert not src_dir.exists()
    again = dispatch(
        "purge",
        {"object_type": "source", "vault_id": "public", "object_id": "src-p"},
        root=tmp_path,
    )
    assert again["status"] == "ok"
    assert again["changed"] is False


def test_question_purge_is_capability_not_supported(tmp_path: Path):
    result = dispatch(
        "purge",
        {"object_type": "question", "vault_id": "local", "object_id": "q-x"},
        root=tmp_path,
    )
    assert result["status"] == "blocked"
    assert result["error_code"] == "capability_not_supported"


def test_backend_purge_endpoint_two_phase(tmp_path: Path):
    _seed_source(tmp_path, "src-http-p")
    client = TestClient(create_app(root=tmp_path, capability_token="token"))
    headers = {"X-MyKnowledge-Capability": "token"}
    url = "/api/object/public/source/src-http-p/purge"
    assert client.post(url).status_code == 401  # 需写能力
    assert client.post(url, headers=headers).status_code == 409  # not_deleted

    client.delete("/api/object/public/source/src-http-p", headers=headers)
    _mark_deleted_long_ago(tmp_path, "source", "src-http-p")
    ok = client.post(url, headers=headers)
    assert ok.status_code == 200
    assert ok.json()["purged"] is True
