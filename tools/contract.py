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
ERROR_CODES = frozenset(
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
