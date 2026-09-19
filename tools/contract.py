"""全项目结果信封的单一事实源（Technical Design §14，激进版归一 · 尽量简单）。

设计对齐 gRPC status codes / Kubernetes ``metav1.Status`` / Rust ``Result``：**只有一根
``status`` 轴（ok/blocked/unavailable）+ 细分 ``error_code`` + 结果全进 payload**，不设
独立 effect 轴。领域函数返回的 dict 必带 ``schema_version`` + ``status``；``status != ok``
必带取自 ``ERROR_CODES`` 单一词表的 ``error_code``。构造器 fail-closed 校验，杜绝手写
字面量漂移。迁移以 TDD 逐模块推进：每纳入一个模块就在 ``ERROR_CODES`` 登记其码。
"""

from __future__ import annotations

import re
from typing import Any

# 唯一状态轴（TD §14.2）。写效果/判分/校验结论等一律进 payload 领域字段，不进 status。
STATUSES = frozenset({"ok", "blocked", "unavailable"})

# 单一 error_code 词表（TD §14.3）。迁移中每纳入一个模块就在此登记其码——
# 未登记的码在构造 blocked/unavailable 时 fail-closed，强制显式治理。
#
# 按域拆成命名子集再 union：多 agent 并行迁移时各改各的子集块（不同代码行），
# 避免同一 set 字面量的合并冲突。每个 agent 只往自己那块追加，不动别人的块。
_LOCATE_CODES = frozenset(
    {
        # 内容对象定位（已接入：content_repository / backend.services / validation.resolution）
        "invalid_object_ref",
        "object_type_not_found",
        "object_not_found",
        "object_id_ambiguous",
        "object_referenced",
        "vault_unavailable",
        # wiki 校验历史码（resolution 报告沿用，语义不变，纳入统一词表）
        "source_not_found",
        "source_ambiguous",
        "source_unreadable",
    }
)
# 以下子集由各迁移 agent 按自己模块填充（先空，TDD 首步登记本模块用到的码）。
_QUESTION_CODES: frozenset[str] = frozenset(
    {
        # question_quality（练习题质量校验入口）
        "quality_mode_invalid",
        "question_not_found",
    }
)  # agent-A1: question.py/question_quality
_SOURCE_CODES: frozenset[str] = frozenset()  # agent-A1: ingest/source_ingestor
_ENTRY_CODES: frozenset[str] = frozenset()  # agent-A2: backend/* / skill_runtime
_MISC_CODES: frozenset[str] = frozenset(
    {
        # release_confirmation（public-release-confirmation 写入门禁）
        "event_schema_invalid",
        "event_fields_missing",
        "event_id_invalid",
        "operation_id_invalid",
        "target_not_public",
        "target_ref_invalid",
        "event_authority_invalid",
        "reason_not_public_safe",
        "leak_gate_scope_invalid",
        "event_hash_mismatch",
        "lock_busy",
        "event_unreadable",
        "event_id_conflict",
        "confirmation_nonce_reused",
        # vault_registry（vault-check 顶层失败，CLI 入口）
        "manifest_invalid",
        "layout_invalid",
        # indexing（索引恢复失败）
        "index_recovery_failed",
    }
)  # agent-A2: validation/indexing/vault/backup/release/doctor
_CRUD_CODES: frozenset[str] = frozenset(
    {
        # source/wiki CRUD 能力层：采集委派失败的统一伞码（底层字段级错误进 payload.errors）。
        # RESTRICT/CASCADE/定位/vault 相关码复用 _LOCATE_CODES（object_referenced/
        # object_not_found/invalid_object_ref/source_unreadable/vault_unavailable 等）。
        "source_ingest_failed",
    }
)  # agent-B: source/wiki repository（CRUD 能力层）

ERROR_CODES = (
    _LOCATE_CODES
    | _QUESTION_CODES
    | _SOURCE_CODES
    | _ENTRY_CODES
    | _MISC_CODES
    | _CRUD_CODES
)

# 可重试是 status 的派生属性（gRPC 模型：仅 unavailable 可重试），供 HTTP 边界层使用。
RETRYABLE_STATUSES = frozenset({"unavailable"})


def is_retryable(status: str) -> bool:
    """由 status 派生 retryable（HTTP 边界用）；不把该布尔冗余进信封。"""
    return status in RETRYABLE_STATUSES


_SCHEMA_VERSION = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*/v\d+")


def require_error_code(code: str) -> str:
    """校验 error_code 已在单一词表登记；未登记 fail-closed。"""
    if code not in ERROR_CODES:
        raise ValueError(f"error_code_not_registered:{code}")
    return code


def result(schema_version: str, status: str, **fields: Any) -> dict[str, Any]:
    """构造统一结果信封（TD §14.1/§14.2）。

    强制：``schema_version`` 形如 ``name/vN``；``status`` ∈ :data:`STATUSES`；
    ``status != ok`` 必带且仅接受已登记的 ``error_code``。
    """
    if not isinstance(schema_version, str) or not _SCHEMA_VERSION.fullmatch(
        schema_version
    ):
        raise ValueError("schema_version_invalid")
    if status not in STATUSES:
        raise ValueError(f"status_not_controlled:{status}")
    if status != "ok":
        if "error_code" not in fields:
            raise ValueError("error_code_required")
        require_error_code(str(fields["error_code"]))
    return {"schema_version": schema_version, "status": status, **fields}


def ok(schema_version: str, **fields: Any) -> dict[str, Any]:
    return result(schema_version, "ok", **fields)


def blocked(schema_version: str, error_code: str, **fields: Any) -> dict[str, Any]:
    return result(schema_version, "blocked", error_code=error_code, **fields)


def unavailable(schema_version: str, error_code: str, **fields: Any) -> dict[str, Any]:
    return result(schema_version, "unavailable", error_code=error_code, **fields)
