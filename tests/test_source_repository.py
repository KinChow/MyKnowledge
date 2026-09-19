"""SourceRepository（CRUD 能力层，Repository 模式）的 TDD 契约测试。

覆盖 create 委派采集、read/list 复用定位、update 幂等且保留 evidence_items
（真实缺陷回归）、delete=RESTRICT（被活跃 wiki 引用则阻断）、软删 retire 幂等，
以及被 retire 的 wiki 不再阻断。返回一律走 tools.contract 统一信封。
"""

from __future__ import annotations

from pathlib import Path

from tools.content_repository import locate_managed_object
from tools.front_matter import FrontMatter
from tools.source_repository import SourceRepository
from tools.wiki_repository import WikiRepository


def _note_request(source_id: str, body: str) -> dict:
    return {
        "source_type": "personal-note",
        "domain": "tools",
        "origin": "personal",
        "body": body,
        "source_id": source_id,
    }


def _write_wiki(root: Path, wiki_id: str, sources: list[str], *, status: str) -> Path:
    metadata = {
        "schema_version": "wiki/v1",
        "id": wiki_id,
        "title": wiki_id,
        "domain": "tools",
        "kind": "knowledge",
        "status": status,
        "sources": sources,
        "evidence": [
            {
                "claim_id": "c1",
                "targets": [{"source_id": sid, "evidence_id": "e1"} for sid in sources],
            }
        ],
    }
    path = root / "content" / "wiki" / "tools" / f"{wiki_id}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(FrontMatter.render(metadata, "# body\n"), encoding="utf-8")
    return path


def _anchor_evidence(root: Path, source_id: str) -> list[dict]:
    """手工向已导入 source 追加 evidence_items（模拟锚定），返回写入的证据。"""
    path = locate_managed_object(root, "source", source_id)
    metadata, body = FrontMatter.parse(path.read_text(encoding="utf-8"))
    items = [
        {
            "id": "e1",
            "snapshot_sha256": metadata["snapshot_sha256"],
            "selector": {"type": "TextQuoteSelector", "exact": "锚定片段"},
        }
    ]
    metadata["evidence_items"] = items
    path.write_text(FrontMatter.render(metadata, body), encoding="utf-8")
    return items


def test_create_delegates_to_ingestor_and_returns_ok(tmp_path: Path):
    repo = SourceRepository(tmp_path)
    result = repo.create(_note_request("src-alpha", "第一份笔记正文，足够长。"))
    assert result["status"] == "ok"
    assert result["changed"] is True
    assert result["source_id"] == "src-alpha"
    assert locate_managed_object(tmp_path, "source", "src-alpha").exists()


def test_create_blocked_maps_ingest_failure(tmp_path: Path):
    repo = SourceRepository(tmp_path)
    result = repo.create(_note_request("src-empty", "   "))
    assert result["status"] == "blocked"
    assert result["error_code"] == "source_ingest_failed"
    assert result["errors"]


def test_read_returns_metadata_and_body(tmp_path: Path):
    repo = SourceRepository(tmp_path)
    repo.create(_note_request("src-read", "可读取的正文内容。"))
    result = repo.read("public", "src-read")
    assert result["status"] == "ok"
    assert result["metadata"]["id"] == "src-read"
    assert "可读取的正文内容。" in result["body"]
    assert result["object_ref"] == {
        "vault_id": "public",
        "object_type": "source",
        "object_id": "src-read",
    }


def test_read_missing_is_object_not_found(tmp_path: Path):
    repo = SourceRepository(tmp_path)
    result = repo.read("public", "nope")
    assert result["status"] == "blocked"
    assert result["error_code"] == "object_not_found"


def test_list_enumerates_sources(tmp_path: Path):
    repo = SourceRepository(tmp_path)
    repo.create(_note_request("src-one", "正文一。"))
    repo.create(_note_request("src-two", "正文二。"))
    result = repo.list("public")
    assert result["status"] == "ok"
    ids = sorted(item["object_ref"]["object_id"] for item in result["items"])
    assert ids == ["src-one", "src-two"]


def test_update_same_body_is_noop_and_preserves_evidence(tmp_path: Path):
    repo = SourceRepository(tmp_path)
    body = "稳定不变的正文内容。"
    repo.create(_note_request("src-idem", body))
    anchored = _anchor_evidence(tmp_path, "src-idem")

    result = repo.update(_note_request("src-idem", body))
    assert result["status"] == "ok"
    assert result["changed"] is False

    metadata, _ = FrontMatter.parse(
        locate_managed_object(tmp_path, "source", "src-idem").read_text("utf-8")
    )
    assert metadata.get("evidence_items") == anchored


def test_update_changed_body_still_preserves_evidence(tmp_path: Path):
    repo = SourceRepository(tmp_path)
    repo.create(_note_request("src-mut", "旧的正文内容。"))
    anchored = _anchor_evidence(tmp_path, "src-mut")

    result = repo.update(_note_request("src-mut", "全新的正文内容，明显不同。"))
    assert result["status"] == "ok"
    assert result["changed"] is True

    metadata, body = FrontMatter.parse(
        locate_managed_object(tmp_path, "source", "src-mut").read_text("utf-8")
    )
    assert "全新的正文内容" in body
    assert metadata.get("evidence_items") == anchored


def test_update_missing_source_is_object_not_found(tmp_path: Path):
    repo = SourceRepository(tmp_path)
    result = repo.update(_note_request("ghost", "正文。"))
    assert result["status"] == "blocked"
    assert result["error_code"] == "object_not_found"


def test_delete_restrict_blocks_when_active_wiki_references(tmp_path: Path):
    repo = SourceRepository(tmp_path)
    repo.create(_note_request("src-ref", "被引用的正文。"))
    _write_wiki(tmp_path, "wiki-live", ["src-ref"], status="draft")

    result = repo.delete("public", "src-ref")
    assert result["status"] == "blocked"
    assert result["error_code"] == "object_referenced"
    assert "wiki-live" in result["referenced_by"]
    assert not (tmp_path / "audit" / "retire" / "source.jsonl").exists()


def test_delete_retires_when_unreferenced_and_is_idempotent(tmp_path: Path):
    repo = SourceRepository(tmp_path)
    repo.create(_note_request("src-free", "无人引用的正文。"))

    first = repo.delete("public", "src-free")
    assert first["status"] == "ok"
    assert first["changed"] is True
    assert first["retired"] is True
    ledger = tmp_path / "audit" / "retire" / "source.jsonl"
    assert ledger.exists()
    assert (tmp_path / "archive" / "manifest.jsonl").exists()
    assert locate_managed_object(tmp_path, "source", "src-free").exists()

    second = repo.delete("public", "src-free")
    assert second["status"] == "ok"
    assert second["changed"] is False
    assert ledger.read_text("utf-8").strip().count("\n") == 0


def test_delete_ignores_retired_wiki_reference(tmp_path: Path):
    repo = SourceRepository(tmp_path)
    repo.create(_note_request("src-dead-ref", "曾被引用的正文。"))
    _write_wiki(tmp_path, "wiki-dead", ["src-dead-ref"], status="draft")
    WikiRepository(tmp_path).delete("public", "wiki-dead")

    result = repo.delete("public", "src-dead-ref")
    assert result["status"] == "ok"
    assert result["retired"] is True
