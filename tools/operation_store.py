"""Operation 记录仓库：两阶段写操作（preview→apply）的持久化与审计。

Operation 文件写入 ``state/operations/``（0600），审计快照写入 ``audit/operations/``。
"""

from __future__ import annotations

import json
import time
import uuid
from pathlib import Path

from .common import atomic_write, canonical_json, hash_canonical, redact, safe_id
from .paths import RepoPaths

OPERATION_TTL_SECONDS = 1800


class OperationStore:
    """Operation 两阶段写操作仓库：创建、读取、更新与审计。

    更新采用"审计先行（预提交）、state 最后写入（提交点）"顺序，
    audit 写失败时 state 保持原值，避免状态与审计不一致。
    """

    def __init__(self, root: Path) -> None:
        self.root = root
        self.paths = RepoPaths(root)

    def new(self, payload: dict) -> dict:
        """创建 previewed 状态的 operation 记录并持久化，返回完整记录。

        与 update 同一提交协议：audit 先行（预提交）、state 最后写入（提交点），
        保证创建的 operation 也有审计证据（R008）。
        """
        operation_id = "op_" + uuid.uuid4().hex
        record = {
            "schema_version": "operation/v1",
            "operation_id": operation_id,
            "created_at": time.time(),
            "state": "previewed",
            **payload,
        }
        audit = self._audit_snapshot(record)
        audit_path = (
            self.paths.operation_file(operation_id)
        )
        atomic_write(audit_path, canonical_json(redact(audit)) + b"\n", 0o600)
        path = self.paths.state_operation_file(operation_id)
        atomic_write(path, canonical_json(redact(record)) + b"\n", 0o600)
        return record

    def is_expired(self, record: dict) -> bool:
        """判断 operation 是否超过 TTL；损坏的时间戳按过期处理。

        source_ingestor 与 evidence_anchor 共用，避免 TTL 判定逻辑漂移。
        """
        try:
            return (
                time.time() - float(record.get("created_at", 0))
                > OPERATION_TTL_SECONDS
            )
        except (TypeError, ValueError):
            return True

    def load(self, operation_id: str) -> dict:
        """按 operation_id 读取 operation 记录；文件缺失或损坏时抛异常由调用方处理。"""
        safe_id(operation_id.removeprefix("op_"))
        path = self.paths.state_operation_file(operation_id)
        with path.open(encoding="utf-8") as handle:
            return json.load(handle)

    def update(self, record: dict, state: str, **fields: object) -> dict:
        """更新 operation 状态与字段：先写审计（预提交），state 最后写入作为提交点。"""
        updated = {**record, "state": state, **fields, "updated_at": time.time()}
        audit = self._audit_snapshot(updated)
        audit_path = (
            self.paths.operation_file(record["operation_id"])
        )
        atomic_write(audit_path, canonical_json(redact(audit)) + b"\n", 0o600)
        state_path = self.paths.state_operation_file(record["operation_id"])
        atomic_write(state_path, canonical_json(redact(updated)) + b"\n", 0o600)
        return updated

    def _audit_snapshot(self, updated: dict) -> dict:
        """从完整记录中提取审计安全字段，并附 evidence 绑定与记录 hash。"""
        safe_fields = {
            "schema_version",
            "operation_id",
            "operation_type",
            "created_at",
            "updated_at",
            "state",
            "target_vault",
            "source_id",
            "domain",
            "source_type",
            "input_hash",
            "target_hash",
            "source_hash",
            "snapshot_sha256",
            "extractor",
            "media_type",
            "network_required",
            "error_code",
            "applied_files",
            "confirmation",
        }
        audit = {k: v for k, v in updated.items() if k in safe_fields}
        evidence = updated.get("evidence")
        if isinstance(evidence, dict):
            audit["evidence_binding"] = {
                key: evidence[key]
                for key in (
                    "evidence_id",
                    "snapshot_sha256",
                    "selector_sha256",
                    "quote_sha256",
                    "position",
                )
                if key in evidence
            }
        audit["record_sha256"] = hash_canonical(audit)
        return audit
