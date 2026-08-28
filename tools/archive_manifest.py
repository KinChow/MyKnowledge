"""archive/manifest.jsonl 的唯一读写入口（§5.6 append-only owner records）。

高内聚：文件格式、幂等去重与持久化（fsync 文件 + 目录）都只在这里；坏行容错
策略也只有一份。低耦合：不知道 entry 是怎么算出来的——条目构造属于导入语义，
留在 SourceIngestor；本类只负责"存进去、读出来、不重复"。

互斥：manifest 是跨 vault 的全局单文件，追加依赖调用方持有的 per-vault 锁
（R009）。target_vault 目前硬编码 "public" 无实际竞争；引入多 vault 写入时需要
全局锁或按 vault 分片。
"""

from __future__ import annotations

import json
import os
from collections.abc import Iterator
from pathlib import Path

from .common import canonical_json
from .paths import RepoPaths


class ArchiveManifest:
    def __init__(self, root: Path) -> None:
        self.path = RepoPaths(Path(root)).manifest

    def entries(self) -> Iterator[dict]:
        """逐行解析条目；坏行跳过（append-only 文件不因一行损坏而整体不可读）。"""
        if not self.path.exists():
            return
        with self.path.open(encoding="utf-8", errors="replace") as handle:
            for raw_line in handle:
                line = raw_line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if isinstance(entry, dict):
                    yield entry

    def record_ids(self) -> set[str]:
        """已登记的 record_id 集合（幂等追加的判据）。"""
        return {
            entry["record_id"] for entry in self.entries() if entry.get("record_id")
        }

    def snapshot_hashes(self) -> set[str]:
        """已入账的 snapshot_sha256 集合（证据账目完整性的判据）。"""
        return {
            entry["snapshot_sha256"]
            for entry in self.entries()
            if entry.get("snapshot_sha256")
        }

    def append(self, entry: dict) -> None:
        """幂等追加：record_id 已存在则跳过；写入后 fsync 文件与父目录。"""
        if entry["record_id"] in self.record_ids():
            return
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("ab") as handle:
            handle.write(canonical_json(entry) + b"\n")
            handle.flush()
            os.fsync(handle.fileno())
        directory_fd = os.open(self.path.parent, os.O_RDONLY)
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)
