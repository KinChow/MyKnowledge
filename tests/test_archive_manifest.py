"""archive/manifest.jsonl 唯一读写入口（§5.6 owner records）。

fixture 用真实产物：条目由 SourceIngestor 的 preview+apply 生成（conftest 的
real_import），不手写字典——手写的 entry 一旦与生产结构漂移，测试仍会通过。
"""

from __future__ import annotations

import json
from pathlib import Path

from tools.archive_manifest import ArchiveManifest
from tools.common import canonical_json


def test_missing_manifest_reads_as_empty(tmp_path: Path):
    manifest = ArchiveManifest(tmp_path)
    assert not manifest.path.exists()
    assert list(manifest.entries()) == []
    assert manifest.record_ids() == set() and manifest.snapshot_hashes() == set()


def test_entries_expose_record_ids_and_snapshot_hashes(tmp_path: Path, real_import):
    entry = real_import(tmp_path, "真实导入产生的正文内容", "manifest-one")
    manifest = ArchiveManifest(tmp_path)
    assert list(manifest.entries()) == [entry]
    assert manifest.record_ids() == {entry["record_id"]}
    assert manifest.snapshot_hashes() == {entry["snapshot_sha256"]}


def test_append_is_idempotent_by_record_id(tmp_path: Path, real_import):
    entry = real_import(tmp_path, "幂等追加验证正文内容", "manifest-idem")
    manifest = ArchiveManifest(tmp_path)
    manifest.append(entry)  # 同一 record_id 重复入账应无副作用
    assert manifest.path.read_bytes() == canonical_json(entry) + b"\n"

    other = {**entry, "record_id": entry["record_id"][::-1]}
    manifest.append(other)  # record_id 不同即视为新条目
    assert len(list(manifest.entries())) == 2
    assert manifest.record_ids() == {entry["record_id"], other["record_id"]}


def test_broken_lines_do_not_hide_the_rest(tmp_path: Path, real_import):
    """append-only 文件不能因一行损坏整体不可读——否则截断即等于账目消失。"""
    entry = real_import(tmp_path, "坏行容错验证正文内容", "manifest-broken")
    manifest = ArchiveManifest(tmp_path)
    with manifest.path.open("a", encoding="utf-8") as handle:
        handle.write("\n")  # 空行
        handle.write('{"record_id": "truncated"\n')  # 断行（崩溃在写一半）
        handle.write(json.dumps([entry]) + "\n")  # 合法 JSON 但不是对象
    assert list(manifest.entries()) == [entry]
    assert manifest.snapshot_hashes() == {entry["snapshot_sha256"]}
