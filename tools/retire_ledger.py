"""append-only 删除账本：`audit/retire/<object_type>.jsonl`。

两阶段删除（对齐 Azure Key Vault soft-delete→purge / IMAP \\Deleted→EXPUNGE /
git rm→gc-prune）都记在本 append-only 账本，用 ``event`` 区分：

- ``event=delete``：软删墓碑（可恢复期内逻辑删）。读取侧据此判定"已删除"，不物理删盘。
- ``event=restore``：恢复为 active，取消旧删除周期的 purge 资格。
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


def _current_events(paths: RepoPaths, object_type: str) -> dict[str, dict]:
    """Latest event by append order, not by caller-provided timestamps.

    Malformed nonempty lines make destructive decisions fail closed. Historical
    records without an event are deletes, but missing timestamps never allow purge.
    """
    ledger = _ledger_path(paths, object_type)
    if not ledger.exists():
        return {}
    events: dict[str, dict] = {}
    for raw in ledger.read_text(encoding="utf-8").splitlines():
        if not raw.strip():
            continue
        try:
            record = json.loads(raw)
        except ValueError as exc:
            raise ValueError("lifecycle_ledger_invalid") from exc
        if (
            not isinstance(record, dict)
            or not isinstance(record.get("object_id"), str)
            or not isinstance(record.get("event", "delete"), str)
            or record.get("event", "delete") not in {"delete", "restore", "purge"}
            or record.get("schema_version", RECORD_SCHEMA) != RECORD_SCHEMA
            or record.get("object_type", object_type) != object_type
        ):
            raise ValueError("lifecycle_ledger_invalid")
        events[record["object_id"]] = record
    return events


def current_lifecycle_state(paths: RepoPaths, object_type: str, object_id: str) -> str:
    record = _current_events(paths, object_type).get(object_id)
    if record is None:
        return "active"
    return {"delete": "deleted", "restore": "active", "purge": "purged"}[
        record.get("event", "delete")
    ]


def retired_object_ids(paths: RepoPaths, object_type: str) -> set[str]:
    return {
        oid
        for oid, event in _current_events(paths, object_type).items()
        if event.get("event", "delete") != "restore"
    }


def is_retired(paths: RepoPaths, object_type: str, object_id: str) -> bool:
    return current_lifecycle_state(paths, object_type, object_id) != "active"


def deleted_at(paths: RepoPaths, object_type: str, object_id: str) -> float | None:
    """Timestamp of the current delete episode, never an earlier deleted lifetime."""
    import math

    record = _current_events(paths, object_type).get(object_id, {})
    value = record.get("at")
    if (
        record.get("event", "delete") == "delete"
        and isinstance(value, (int, float))
        and not isinstance(value, bool)
        and math.isfinite(value)
    ):
        return float(value)
    return None


def is_purged(paths: RepoPaths, object_type: str, object_id: str) -> bool:
    return current_lifecycle_state(paths, object_type, object_id) == "purged"


def append_restore(
    paths: RepoPaths,
    object_type: str,
    *,
    vault_id: str,
    object_id: str,
    reason: str,
    at: float | None = None,
) -> None:
    _append(
        paths,
        object_type,
        event="restore",
        vault_id=vault_id,
        object_id=object_id,
        reason=reason,
        at=at,
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
