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

# AC-F004-006/011：apply 侧确认事件契约。public release 故意不是合法 scope
# （它是独立事件类型 public-release-confirmation/v1，schema 层不可冒充）。
APPLY_CONFIRMATION_SCHEMA = "operation-confirmation/v1"
APPLY_CONFIRMATION_SCOPES = frozenset({"apply", "publish_private"})
APPLY_CONFIRMATION_REQUIRED = ("schema_version", "operation_id", "scope", "actor_type", "actor_id", "input_hash", "diff_hash", "event_sha256")


def validate_apply_confirmation(record: dict, event: object) -> str | None:
    """校验 apply 消费的 operation-confirmation/v1 事件；返回 error_code 或 None。

    只接受 ``actor_type: human``、scope ∈ {apply, publish_private}、
    input/diff hash 与当前 operation 完全绑定的事件（§1239：apply 的重放
    由 hash 绑定挡住，不需要 nonce）。任何字段缺失/不匹配 fail-closed。
    """
    if not isinstance(event, dict):
        return "confirmation_schema_invalid"
    if event.get("schema_version") != APPLY_CONFIRMATION_SCHEMA:
        return "confirmation_schema_invalid"
    missing = [key for key in APPLY_CONFIRMATION_REQUIRED if key not in event]
    if missing:
        return "confirmation_fields_missing"
    if event.get("scope") not in APPLY_CONFIRMATION_SCOPES:
        return "confirmation_scope_invalid"
    if event.get("actor_type") != "human":
        return "confirmation_actor_invalid"
    try:
        safe_id(str(event.get("actor_id", "")))
    except ValueError:
        return "confirmation_actor_invalid"
    if event.get("operation_id") != record.get("operation_id"):
        return "confirmation_operation_mismatch"
    if event.get("input_hash") != record.get("input_hash") or event.get("diff_hash") != record.get("diff_hash"):
        return "confirmation_hash_mismatch"
    if event.get("scope") == "publish_private":
        publish_missing = [key for key in ("content_sha256", "evidence_sha256", "target_vault") if not event.get(key)]
        if publish_missing or event.get("target_vault") != record.get("target_vault"):
            return "confirmation_fields_missing"
    # F-2：event_sha256 必填且必须匹配（审计完整性：durable audit 里的确认
    # 事件始终有自哈希，可独立复核）
    expected = hash_canonical({k: v for k, v in event.items() if k != "event_sha256"})
    if event["event_sha256"] != expected:
        return "confirmation_hash_mismatch"
    return None


def build_apply_confirmation(
    store: "OperationStore",
    operation_id: str,
    actor_id: str,
    *,
    scope: str = "apply",
    content_sha256: str | None = None,
    evidence_sha256: str | None = None,
) -> tuple[dict | None, str | None]:
    """从 durable record 派生确认事件；返回 (event, error_code)。

    生成与校验同文件（防契约漂移）：hash 一律取自 ``state/operations``
    记录而非调用方参数——人只能确认"当前记录的状态"，不可能确认错 hash。
    只读不写：本函数不落任何 durable 状态、不触发 apply；生成器运行在
    人的本地交互终端（与 ADR-0010 人工门禁同一信任模型，非密码学认证）。
    ``scope: publish_private`` 需显式给出 content/evidence hash
    （对内容的人工背书，不可从 record 代取）。
    """
    try:
        safe_id(actor_id)
    except ValueError:
        return None, "confirmation_actor_invalid"
    try:
        record = store.load(operation_id)
    except (OSError, ValueError):
        return None, "operation_not_found"
    if scope not in APPLY_CONFIRMATION_SCOPES:
        return None, "confirmation_scope_invalid"
    if record.get("state") != "previewed":
        return None, "operation_not_previewed"
    if store.is_expired(record):
        return None, "operation_expired"
    event: dict = {
        "schema_version": APPLY_CONFIRMATION_SCHEMA,
        "operation_id": operation_id,
        "scope": scope,
        "actor_type": "human",
        "actor_id": actor_id,
        "input_hash": record.get("input_hash"),
        "diff_hash": record.get("diff_hash"),
    }
    if scope == "publish_private":
        publish = {"content_sha256": content_sha256, "evidence_sha256": evidence_sha256, "target_vault": record.get("target_vault")}
        if not content_sha256 or not evidence_sha256:
            return None, "confirmation_fields_missing"
        event.update(publish)
    event["event_sha256"] = hash_canonical(event)
    # 自校验：生成的事件必须能通过本校验器（生成/校验同源）
    if validate_apply_confirmation(record, event) is not None:
        return None, "confirmation_generation_invalid"
    return event, None


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

    def apply_preflight(
        self, operation_id: str, expected_type: str | tuple[str, ...], confirmed: bool
    ) -> tuple[dict | None, dict | None]:
        """两阶段写 apply 的通用前置校验（source_ingestor 与 evidence_anchor 共用）。

        返回 (record, error_response)；error_response 为 None 表示可继续。
        覆盖：加载失败（operation_not_found）、非 previewed、未确认、
        operation_type 不匹配——与调用方锁内复查/TTL/业务逻辑解耦，
        避免两个 apply 的状态判定漂移。
        """
        try:
            record = self.load(operation_id)
        except (OSError, ValueError, json.JSONDecodeError, UnicodeDecodeError):
            return None, {
                "state": "blocked",
                "operation_id": operation_id,
                "error_code": "operation_not_found",
            }
        audit_error = self.verify_audit(operation_id)
        if audit_error is not None:
            return record, {"state": "blocked", "operation_id": operation_id, "error_code": audit_error}
        if record.get("state") != "previewed":
            error = {
                "state": record.get("state"),
                "operation_id": operation_id,
            }
            if record.get("applied_files"):
                error["applied_files"] = record["applied_files"]
            return record, error
        if not confirmed:
            return record, {
                "state": "awaiting_confirmation",
                "operation_id": operation_id,
            }
        allowed_types = (expected_type,) if isinstance(expected_type, str) else expected_type
        if record.get("operation_type") not in allowed_types:
            return record, {
                "state": "blocked",
                "operation_id": operation_id,
                "error_code": "operation_type_mismatch",
            }
        return record, None

    def load(self, operation_id: str) -> dict:
        """按 operation_id 读取 operation 记录；文件缺失或损坏时抛异常由调用方处理。"""
        safe_id(operation_id.removeprefix("op_"))
        path = self.paths.state_operation_file(operation_id)
        with path.open(encoding="utf-8") as handle:
            return json.load(handle)

    def verify_audit(self, operation_id: str) -> str | None:
        """Return an error code when the durable audit snapshot is missing/tampered."""
        try:
            safe_id(operation_id.removeprefix("op_"))
            data = json.loads(self.paths.operation_file(operation_id).read_text(encoding="utf-8"))
            stored = data.get("record_sha256")
            if not stored:
                return "hash_mismatch"
            actual = hash_canonical({k: v for k, v in data.items() if k != "record_sha256"})
            return None if stored == actual and data.get("operation_id") == operation_id else "hash_mismatch"
        except (OSError, ValueError, json.JSONDecodeError, UnicodeDecodeError):
            return "hash_mismatch"

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
