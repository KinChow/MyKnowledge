"""Fail-closed validator/writer for public-release-confirmation/v1 events."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from filelock import FileLock, Timeout

from .common import atomic_write, hash_canonical, safe_id, safe_operation_id
from .paths import RepoPaths

SCHEMA = "public-release-confirmation/v1"
REQUIRED = {
    "event_id",
    "operation_id",
    "target_ref",
    "target_vault",
    "actor_type",
    "actor_id",
    "decision",
    "release_input_sha256",
    "reviewed_content_sha256",
    "reviewed_evidence_sha256",
    "leak_gate_report_sha256",
    "leak_gate_report_scope",
    "reason",
    "confirmation_nonce",
}


def validate_event(event: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(event, dict) or event.get("schema_version") != SCHEMA:
        return {"valid": False, "error_code": "event_schema_invalid"}
    missing = sorted(REQUIRED - set(event))
    if missing:
        return {
            "valid": False,
            "error_code": "event_fields_missing",
            "missing": missing,
        }
    try:
        safe_id(str(event["event_id"]))
        safe_id(str(event["actor_id"]))
    except ValueError:
        return {"valid": False, "error_code": "event_id_invalid"}
    try:
        safe_operation_id(str(event["operation_id"]))
    except ValueError:
        return {"valid": False, "error_code": "operation_id_invalid"}
    ref = event["target_ref"]
    if (
        not isinstance(ref, dict)
        or ref.get("vault_id") != "public"
        or ref.get("object_type") != "wiki"
    ):
        return {"valid": False, "error_code": "target_not_public"}
    try:
        safe_id(str(ref["object_id"]))
    except (KeyError, ValueError):
        return {"valid": False, "error_code": "target_ref_invalid"}
    if (
        event["target_vault"] != "public"
        or event["actor_type"] != "human"
        or event["decision"] != "approve"
    ):
        return {"valid": False, "error_code": "event_authority_invalid"}
    reason = event["reason"]
    if (
        not isinstance(reason, str)
        or not reason.strip()
        or len(reason) > 240
        or re.search(r"(?:https?://|/|\\|private|internal)", reason, re.I)
    ):
        return {"valid": False, "error_code": "reason_not_public_safe"}
    if event["leak_gate_report_scope"] != "input-tree":
        return {"valid": False, "error_code": "leak_gate_scope_invalid"}
    expected = hash_canonical({k: v for k, v in event.items() if k != "event_sha256"})
    if event.get("event_sha256") and event["event_sha256"] != expected:
        return {"valid": False, "error_code": "event_hash_mismatch"}
    return {"valid": True, "event_sha256": expected}


def write_event(root: Path, event: dict[str, Any]) -> dict[str, Any]:
    result = validate_event(event)
    if not result["valid"]:
        return {"state": "blocked", **result}
    event = {**event, "event_sha256": result["event_sha256"]}
    paths = RepoPaths(root)
    path = paths.release_confirmations / f"{event['event_id']}.json"
    # 两侧都 resolve 再取相对路径：`--root .` 时 RepoPaths 给出的是相对路径，
    # 直接 relative_to(resolved_root) 会抛 ValueError——事件已落盘却以 traceback
    # 收尾，人只能看到"报错了"，无法判断确认到底有没有生效。
    reported = str(path.resolve().relative_to(Path(root).resolve()))
    # 检查与写入必须持同一把锁（check-then-act）：nonce 是一次性的，两个并发
    # confirm 若同时通过扫描，就会把同 nonce 写进两份不同事件，击穿防重放。
    # 锁文件放 state/locks/（git 忽略的临时运行态），与 VaultLock 同源 filelock。
    lock = FileLock(paths.state_locks / "release-confirmations.lock")
    try:
        lock.acquire(timeout=0)
    except Timeout:
        return {"state": "blocked", "error_code": "lock_busy"}
    try:
        if path.exists():
            # 重复执行同一条确认不是失败：append-only 记录已经在了，目标状态已达成。
            # 只有"同 event_id、不同内容"才是真冲突——那说明有人想覆盖一条已签的
            # 确认，必须 fail-closed。把两者都报成 event_exists 会诱导人删记录重跑。
            try:
                existing = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, ValueError, json.JSONDecodeError):
                return {"state": "blocked", "error_code": "event_unreadable"}
            if existing.get("event_sha256") != event["event_sha256"]:
                return {"state": "blocked", "error_code": "event_id_conflict"}
            return {
                "state": "already_applied",
                "event_sha256": event["event_sha256"],
                "path": reported,
            }
        # Nonces are one-shot across event IDs; otherwise an attacker could replay
        # a valid approval by changing only the event filename/operation metadata.
        for existing in path.parent.glob("*.json"):
            try:
                data = json.loads(existing.read_text(encoding="utf-8"))
            except (OSError, ValueError, json.JSONDecodeError):
                continue
            if data.get("confirmation_nonce") == event.get("confirmation_nonce"):
                return {"state": "blocked", "error_code": "confirmation_nonce_reused"}
        atomic_write(
            path, json.dumps(event, ensure_ascii=False, indent=2).encode("utf-8"), 0o600
        )
        return {
            "state": "created",
            "event_sha256": result["event_sha256"],
            "path": reported,
        }
    finally:
        lock.release()
