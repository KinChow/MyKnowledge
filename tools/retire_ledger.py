"""append-only 删除账本：`audit/retire/<object_type>.jsonl`。

两阶段删除（对齐 Azure Key Vault soft-delete→purge / IMAP \\Deleted→EXPUNGE /
git rm→gc-prune）都记在本 append-only 账本，用 ``event`` 区分：

- ``event=delete``：软删墓碑（可恢复期内逻辑删）。读取侧据此判定"已删除"，不物理删盘。
- ``event=purge``：硬删墓碑（过宽限期后物理回收，记录"曾存在且已永久删除"的审计）。

账本本身永不重写（append-only）；``at`` 记录事件时间，供 purge 的宽限期判定。
`SourceRepository`/`WikiRepository`/`QuestionStore` 共用本模块的单份实现。
"""

from __future__ import annotations

import json
import os
import time

from .common import canonical_json
from .paths import RepoPaths

RECORD_SCHEMA = "retire-record/v1"


def _ledger_path(paths: RepoPaths, object_type: str):
    return paths.audit_retire / f"{object_type}.jsonl"


def _records(paths: RepoPaths, object_type: str) -> list[dict]:
    """逐行解析账本记录（缺失/损坏行跳过）。"""
    ledger = _ledger_path(paths, object_type)
    out: list[dict] = []
    if not ledger.exists():
        return out
    for raw in ledger.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line:
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(record, dict) and isinstance(record.get("object_id"), str):
            out.append(record)
    return out


def retired_object_ids(paths: RepoPaths, object_type: str) -> set[str]:
    """已删除（软或硬）的 object_id 集合——读取侧据此判定"已删除"。"""
    return {r["object_id"] for r in _records(paths, object_type)}


def is_retired(paths: RepoPaths, object_type: str, object_id: str) -> bool:
    return object_id in retired_object_ids(paths, object_type)


def deleted_at(paths: RepoPaths, object_type: str, object_id: str) -> float | None:
    """该对象最早一条 ``delete`` 墓碑的时间戳（epoch 秒）；无可判定时间返回 None。

    供 purge 的宽限期判定；历史墓碑若无 ``at`` 字段则返回 None（无法确认删除时间，
    purge 侧 fail-closed 不放行）。
    """
    times = [
        float(r["at"])
        for r in _records(paths, object_type)
        if r.get("object_id") == object_id
        and r.get("event", "delete") == "delete"
        and isinstance(r.get("at"), int | float)
    ]
    return min(times) if times else None


def is_purged(paths: RepoPaths, object_type: str, object_id: str) -> bool:
    """是否已有 ``purge`` 硬删墓碑（物理回收已发生，幂等判据）。"""
    return any(
        r.get("object_id") == object_id and r.get("event") == "purge"
        for r in _records(paths, object_type)
    )


def append_retire(
    paths: RepoPaths,
    object_type: str,
    *,
    vault_id: str,
    object_id: str,
    reason: str,
    at: float | None = None,
) -> None:
    """追加一条软删（``event=delete``）墓碑（append-only + fsync，永不覆盖）。"""
    _append(
        paths,
        object_type,
        event="delete",
        vault_id=vault_id,
        object_id=object_id,
        reason=reason,
        at=at,
    )


def append_purge(
    paths: RepoPaths,
    object_type: str,
    *,
    vault_id: str,
    object_id: str,
    reason: str,
    at: float | None = None,
) -> None:
    """追加一条硬删（``event=purge``）墓碑：物理回收后记录"曾存在、已永久删除"。"""
    _append(
        paths,
        object_type,
        event="purge",
        vault_id=vault_id,
        object_id=object_id,
        reason=reason,
        at=at,
    )


def _append(
    paths: RepoPaths,
    object_type: str,
    *,
    event: str,
    vault_id: str,
    object_id: str,
    reason: str,
    at: float | None,
) -> None:
    ledger = _ledger_path(paths, object_type)
    ledger.parent.mkdir(parents=True, exist_ok=True)
    record = {
        "schema_version": RECORD_SCHEMA,
        "event": event,
        "vault_id": vault_id,
        "object_type": object_type,
        "object_id": object_id,
        "reason": reason,
        "at": time.time() if at is None else float(at),
    }
    with ledger.open("ab") as handle:
        handle.write(canonical_json(record) + b"\n")
        handle.flush()
        os.fsync(handle.fileno())
