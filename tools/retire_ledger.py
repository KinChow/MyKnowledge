"""append-only 退休（软删）墓碑账本：`audit/retire/<object_type>.jsonl`。

内容对象删除采用逻辑删/墓碑（对齐数据库 logical delete）：不物理删
source/wiki/archive/manifest（内容寻址与账目不可变，见 `paths.py` 注释），只向本
账本 append 一条墓碑记录，读取侧据此判定"已退休"。`SourceRepository` 与
`WikiRepository` 共用本模块的**单份实现**——此前退休助手是 `source_repository` 的
下划线私有函数被 `wiki_repository` 跨模块借用（坏味道），现收敛为一个内聚模块。
"""

from __future__ import annotations

import json
import os

from .common import canonical_json
from .paths import RepoPaths

RECORD_SCHEMA = "retire-record/v1"


def _ledger_path(paths: RepoPaths, object_type: str):
    return paths.audit_retire / f"{object_type}.jsonl"


def retired_object_ids(paths: RepoPaths, object_type: str) -> set[str]:
    """读取账本，返回已墓碑化的 object_id 集合（缺失/损坏行跳过）。"""
    ledger = _ledger_path(paths, object_type)
    ids: set[str] = set()
    if not ledger.exists():
        return ids
    for raw in ledger.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line:
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            continue
        object_id = record.get("object_id")
        if isinstance(object_id, str):
            ids.add(object_id)
    return ids


def is_retired(paths: RepoPaths, object_type: str, object_id: str) -> bool:
    return object_id in retired_object_ids(paths, object_type)


def append_retire(
    paths: RepoPaths,
    object_type: str,
    *,
    vault_id: str,
    object_id: str,
    reason: str,
) -> None:
    """向账本追加一条墓碑记录（append-only + fsync，永不覆盖）。"""
    ledger = _ledger_path(paths, object_type)
    ledger.parent.mkdir(parents=True, exist_ok=True)
    record = {
        "schema_version": RECORD_SCHEMA,
        "vault_id": vault_id,
        "object_type": object_type,
        "object_id": object_id,
        "reason": reason,
    }
    with ledger.open("ab") as handle:
        handle.write(canonical_json(record) + b"\n")
        handle.flush()
        os.fsync(handle.fileno())
