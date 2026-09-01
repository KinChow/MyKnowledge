"""存量 source 的定位判定与改判（F013 / §6.4 F010 澄清）。

fixture 全部走生产导入路径产出，不手写 front matter——手写 fixture 一旦与生产结构
漂移，测试会继续通过（伪绿）。
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from tools.front_matter import FrontMatter
from tools.ingest.source_ingestor import SourceIngestor
from tools.reposition import PLAN_SCHEMA_VERSION, apply, classify

LONG_BODY = "# 标题\n\n" + "\n\n".join(
    f"## 第 {i} 节\n\n{'终版正文内容。' * 60}" for i in range(4)
)


def _ingest_local_file(root: Path, source_id: str, body: str) -> dict:
    """走 local-file 通道导入：复现存量 163 篇的形态（origin: external）。"""
    original = root / "incoming" / f"{source_id}.md"
    original.parent.mkdir(parents=True, exist_ok=True)
    original.write_text(body, encoding="utf-8")
    ingestor = SourceIngestor(root)
    preview = ingestor.preview(
        {
            "source_type": "local-file",
            "domain": "tools",
            "source_id": source_id,
            "input_path": str(original),
        }
    )
    assert preview["state"] == "previewed", preview
    applied = ingestor.apply(preview["operation_id"], confirmed=True)
    assert applied["state"] == "applied", applied
    return applied


def _front_matter(root: Path, source_id: str) -> dict:
    path = root / "content" / "sources" / "tools" / f"{source_id}.md"
    metadata, _ = FrontMatter.parse(path.read_text(encoding="utf-8"))
    return metadata


def test_legacy_local_file_sources_are_registered_as_external(tmp_path: Path):
    """基线事实：local-file 导入产出 origin: external——这正是需要改判的失真点。"""
    _ingest_local_file(tmp_path, "baseline-note", LONG_BODY)
    metadata = _front_matter(tmp_path, "baseline-note")
    assert metadata["origin"] == "external"
    assert metadata["source_type"] == "local-file"


@pytest.mark.parametrize(
    ("source_id", "body", "expected"),
    [
        (
            "with-link",
            "# 有外链\n\n参见 https://example.com/doc 的说明。\n",
            "external",
        ),
        ("structured", LONG_BODY, "final"),
        ("stub", "# 短笔记\n\n只有一句话。\n", "intermediate"),
        ("unfinished", LONG_BODY + "\n\n## 待补\n\nTODO 补充结论\n", "intermediate"),
    ],
)
def test_classify_assigns_categories_from_body_signals(
    tmp_path: Path, source_id: str, body: str, expected: str
):
    """三分类判据来自正文信号（外链/final 门槛/未完成标记），清单默认未确认。"""
    _ingest_local_file(tmp_path, source_id, body)
    plan = classify(tmp_path)
    assert plan["schema_version"] == PLAN_SCHEMA_VERSION
    assert plan["confirmed"] is False  # 清单默认未确认，apply 必须被拦
    item = next(i for i in plan["items"] if i["source_id"] == source_id)
    assert item["category"] == expected
    assert item["suggested_category"] == expected
    assert item["reasons"], "判定必须给出依据，供 owner 逐篇核对"


def test_apply_refuses_an_unconfirmed_plan(tmp_path: Path):
    """未确认的清单必须被 apply 拦下（plan_not_confirmed），source 不得被改判。"""
    _ingest_local_file(tmp_path, "unconfirmed-note", LONG_BODY)
    plan_path = tmp_path / "plan.json"
    plan_path.write_text(
        json.dumps(classify(tmp_path), ensure_ascii=False), encoding="utf-8"
    )
    result = apply(tmp_path, plan_path)
    assert result == {
        "state": "blocked",
        "error_code": "plan_not_confirmed",
        "next_action": "owner 逐篇核对 category 后把 confirmed 改为 true",
    }
    assert _front_matter(tmp_path, "unconfirmed-note")["origin"] == "external"


def _confirmed_plan(root: Path, plan_path: Path) -> dict:
    plan = {**classify(root), "confirmed": True}
    plan_path.write_text(json.dumps(plan, ensure_ascii=False), encoding="utf-8")
    return plan


def _working_front_matter(root: Path, source_id: str, domain: str = "tools") -> dict:
    path = root / "content" / "working" / domain / f"{source_id}.md"
    metadata, _ = FrontMatter.parse(path.read_text(encoding="utf-8"))
    return metadata


def test_apply_requires_the_public_vault_write_lock(tmp_path: Path):
    """落位是不可逆批量写：锁被占用时必须整批拒绝，不能写一半。"""
    from tools.common import new_operation_id
    from tools.vault_lock import VaultLock

    _ingest_local_file(tmp_path, "locked-note", LONG_BODY)
    plan_path = tmp_path / "plan.json"
    _confirmed_plan(tmp_path, plan_path)

    with VaultLock(tmp_path, "public", new_operation_id()):
        result = apply(tmp_path, plan_path)
    assert result["state"] == "blocked"
    assert result["error_code"] == "lock_busy"
    # 一篇都不能落位：source 仍在原处，working 层没有半成品
    assert (tmp_path / "content" / "sources" / "tools" / "locked-note.md").is_file()
    assert not (tmp_path / "content" / "working").exists()

    assert apply(tmp_path, plan_path)["relocated"] == 1


def test_relocation_carries_the_legacy_git_time_when_the_plan_has_it(tmp_path: Path):
    """时间事实由清单携带、apply 原样落位；缺失时不写空值。

    落位会重写文件，`mtime` 从此是落位时间——实测 161 篇存量的 mtime 已经全被
    迁移抹成同一天，Git 首次提交时间是仓库里仅剩的时间事实。
    """
    _ingest_local_file(tmp_path, "timed-note", LONG_BODY)
    plan_path = tmp_path / "plan.json"
    plan = {**classify(tmp_path), "confirmed": True}
    assert plan["legacy_time_unresolved"] == 1  # 非 Git 仓库：显式计数而非静默
    for item in plan["items"]:
        item["legacy_first_commit_at"] = "2025-07-06T20:30:14+08:00"
    plan_path.write_text(json.dumps(plan, ensure_ascii=False), encoding="utf-8")

    assert apply(tmp_path, plan_path)["relocated"] == 1
    metadata = _working_front_matter(tmp_path, "timed-note")
    assert metadata["legacy_first_commit_at"] == "2025-07-06T20:30:14+08:00"


def test_apply_relocates_every_category_into_the_working_layer(tmp_path: Path):
    """整批降级：三个类别一律落位 working/，落位文件不再有 object 身份。"""
    from tools.archive_manifest import ArchiveManifest

    _ingest_local_file(tmp_path, "final-note", LONG_BODY)
    _ingest_local_file(tmp_path, "stub-note", "# 短笔记\n\n一句话。\n")
    _ingest_local_file(tmp_path, "linked-note", "# 有外链\n\nhttps://example.com/a\n")
    manifest_before = ArchiveManifest(tmp_path).snapshot_hashes()
    plan_path = tmp_path / "plan.json"
    plan = _confirmed_plan(tmp_path, plan_path)

    result = apply(tmp_path, plan_path)
    assert result["relocated"] == 3, result
    assert result["blocked"] == 0
    assert result["retained"] == 0

    for source_id in ("final-note", "stub-note", "linked-note"):
        # source 层不再持有它：object 身份随降级消失
        assert not (
            tmp_path / "content" / "sources" / "tools" / f"{source_id}.md"
        ).exists()
        metadata = _working_front_matter(tmp_path, source_id)
        assert set(metadata) == {
            "title",
            "domain",
            "legacy_path",
            "snapshot_sha256",
        }, metadata  # tmp_path 不是 Git 仓库 → 无时间事实，不写空值
        assert "schema_version" not in metadata
        assert metadata["snapshot_sha256"] in manifest_before

    # append-only 归档不因降级而变动
    assert ArchiveManifest(tmp_path).snapshot_hashes() == manifest_before

    # 一次降级一条 CDR，绑清单 hash 与全部 source_id
    cdr_paths = list((tmp_path / "content" / "decisions").glob("CDR-*.md"))
    assert len(cdr_paths) == 1, cdr_paths
    cdr, _ = FrontMatter.parse(cdr_paths[0].read_text(encoding="utf-8"))
    assert cdr["content_verdict"] == "downgrade"
    assert cdr["relocated_count"] == 3
    assert sorted(cdr["relocated_source_ids"]) == [
        "final-note",
        "linked-note",
        "stub-note",
    ]
    assert cdr["plan_sha256"].startswith("sha256:")
    assert cdr["id"] == result["decision_id"]
    assert plan["counts"]["external"] == 1  # 类别只剩升级优先级标注，不再路由


def test_cdr_records_duplicate_legacy_imports_without_choosing_one(tmp_path: Path):
    """同一 legacy_path 被导入成两个 source：两份都落位，重复事实写进 CDR。"""
    _ingest_local_file(tmp_path, "first-copy", LONG_BODY)
    _ingest_local_file(tmp_path, "second-copy", LONG_BODY + "\n\n## 补充\n\n差异。\n")
    # legacy_path 来自 local-file sidecar（生产口径），把两篇指回同一原始文档
    for source_id in ("first-copy", "second-copy"):
        sidecar = tmp_path / "var" / "state" / "local-sources" / "public"
        sidecar = sidecar / f"{source_id}.json"
        payload = json.loads(sidecar.read_text(encoding="utf-8"))
        payload["path"] = str(tmp_path / "docs" / "tools" / "same-origin.md")
        sidecar.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")

    plan_path = tmp_path / "plan.json"
    _confirmed_plan(tmp_path, plan_path)
    result = apply(tmp_path, plan_path)
    assert result["relocated"] == 2

    cdr_path = next((tmp_path / "content" / "decisions").glob("CDR-*.md"))
    cdr, _ = FrontMatter.parse(cdr_path.read_text(encoding="utf-8"))
    assert cdr["duplicate_legacy_paths"] == [
        {
            "legacy_path": "docs/tools/same-origin.md",
            "source_ids": ["first-copy", "second-copy"],
        }
    ]
    assert _working_front_matter(tmp_path, "first-copy")["legacy_path"] == (
        "docs/tools/same-origin.md"
    )
    assert _working_front_matter(tmp_path, "second-copy")["legacy_path"] == (
        "docs/tools/same-origin.md"
    )


def test_apply_retains_wiki_referenced_sources_and_blocks_drifted(tmp_path: Path):
    """保护清单由实际引用推导：被 wiki 引用的 source 不搬；漂移的一律拒绝。"""
    _ingest_local_file(tmp_path, "cited-note", LONG_BODY)
    _ingest_local_file(tmp_path, "drifted-note", "# 短笔记\n\n一句话。\n")
    wiki = tmp_path / "content" / "wiki" / "tools" / "citing-page.md"
    wiki.parent.mkdir(parents=True, exist_ok=True)
    wiki.write_text(
        FrontMatter.render(
            {
                "id": "citing-page",
                "domain": "tools",
                "kind": "knowledge",
                "sources": ["cited-note"],
            },
            "# 引用页\n",
        ),
        encoding="utf-8",
    )
    plan_path = tmp_path / "plan.json"
    plan = _confirmed_plan(tmp_path, plan_path)
    assert plan["retained"] == ["cited-note"]
    assert plan["relocatable"] == 1

    target = tmp_path / "content" / "sources" / "tools" / "drifted-note.md"
    target.write_text(
        target.read_text(encoding="utf-8") + "\n清单产出之后的手工改动\n",
        encoding="utf-8",
    )

    result = apply(tmp_path, plan_path)
    states = {r["source_id"]: r for r in result["results"]}
    assert states["cited-note"] == {
        "source_id": "cited-note",
        "state": "retained",
        "retained_by": ["citing-page"],
    }
    assert states["drifted-note"] == {
        "source_id": "drifted-note",
        "state": "blocked",
        "error_code": "source_drifted",
    }
    # 两篇都没搬走 → 没有降级发生 → 不写 CDR
    assert result["relocated"] == 0
    assert result["decision_id"] is None
    assert (tmp_path / "content" / "sources" / "tools" / "cited-note.md").exists()
    assert not (tmp_path / "content" / "working").exists()
