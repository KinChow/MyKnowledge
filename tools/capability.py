"""Capability token 校验单实现（结构收敛 Step0-2）。

此前 token 的恒定时间比较、TTL、audience、scope 检查存在三份平行实现：
``backend.app.require_capability``、``backend.app.require_write_capability``
与 ``tools.mcp_server`` 内联闭包。ADR 的 capability-token/v1 契约
（恒定时间比较、启动轮换、TTL、audience/scope、错误行为）没有单点实现。

本模块只提供**纯函数核**（不抛 HTTP 异常、不读时钟以外的状态），
HTTP/MCP adapter 各自把返回的错误码翻译为自己的失败形态。
来源说明：借鉴 itsdangerous 的 "签名核 + 比较器" 分层
（https://itsdangerous.palletsprojects.com/），不引入第三方依赖。
"""

from __future__ import annotations

import secrets
import time

CAPABILITY_AUDIENCE = "myknowledge-local-api"

# (error_code, retryable, next_action) —— 与既有 HTTP detail 结构逐字段一致
_CAPABILITY_TOKEN_REQUIRED = (
    "capability_token_required",
    False,
    "provide capability token",
)
_CAPABILITY_TOKEN_INVALID = (
    "capability_token_invalid",
    False,
    "request a fresh local token",
)
_CAPABILITY_TOKEN_EXPIRED = (
    "capability_token_expired",
    True,
    "restart the local API for a fresh token",
)
_CAPABILITY_AUDIENCE_INVALID = (
    "capability_audience_invalid",
    False,
    f"use the {CAPABILITY_AUDIENCE} audience",
)
_CAPABILITY_SCOPE_INVALID = (
    "capability_scope_invalid",
    False,
    "request capability scope {scope}",
)


def required_scope_for(scope: str, *, force: bool = False) -> str | None:
    """Map a query scope to the capability scope it demands (None = 无需 scope)."""
    if scope != "public":
        return {"private": "private-read", "local": "local-read"}.get(scope)
    return "local-read" if force else None


def check_capability(
    provided: str | None,
    expected: str | None,
    *,
    created_at: float,
    ttl_seconds: float,
    scopes: set[str],
    required_scope: str | None = None,
    audience: str | None = None,
    skip: bool = False,
) -> tuple[str, bool, str] | None:
    """Validate one capability token; return None on success, error tuple on failure.

    ``skip`` 对应"public 且非强制"的免 token 路径（语义与原
    ``require_capability`` 的 ``scope == "public" and not force`` 一致）。
    恒定时间比较经 :func:`secrets.compare_digest`；TTL 由调用方注入的
    ``created_at`` 与当前时钟比较。
    """
    if skip:
        return None
    if not provided:
        return _CAPABILITY_TOKEN_REQUIRED
    if not expected or not secrets.compare_digest(provided, expected):
        return _CAPABILITY_TOKEN_INVALID
    if time.time() - created_at > ttl_seconds:
        return _CAPABILITY_TOKEN_EXPIRED
    if audience is not None and audience != CAPABILITY_AUDIENCE:
        return _CAPABILITY_AUDIENCE_INVALID
    if required_scope is not None and required_scope not in scopes:
        return (
            _CAPABILITY_SCOPE_INVALID[0],
            _CAPABILITY_SCOPE_INVALID[1],
            _CAPABILITY_SCOPE_INVALID[2].format(scope=required_scope),
        )
    return None
