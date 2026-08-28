"""本地回环防护与 capability 门禁（F006）。

两层职责：
1. ``local_origin_guard`` 中间件——请求体上限 + 只接受回环 host/origin；
2. ``require_capability`` / ``require_write_capability``——``tools.capability``
   的 HTTP 适配层（核心判定只有一份，这里只负责映射到 401/403）。
"""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import Any

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.responses import Response

from tools.capability import check_capability, required_scope_for

from .errors import api_error, json_error

LOOPBACK_HOSTS = frozenset({"127.0.0.1", "localhost", "testserver"})
LOOPBACK_ORIGINS = ("http://127.0.0.1", "http://localhost", "http://testserver")
BODY_METHODS = frozenset({"POST", "PUT", "PATCH", "DELETE"})


def _too_large() -> JSONResponse:
    return json_error(413, "request_too_large", "request", "reduce request body")


def _declared_oversize(content_length: str, limit: int) -> bool:
    try:
        return int(content_length) > limit
    except ValueError:
        # 不可解析的 Content-Length 一律当超限拒绝，不猜真实体积
        return True


def _reject_non_loopback(request: Request) -> JSONResponse | None:
    host = (request.headers.get("host") or "").split(":", 1)[0].lower()
    if host and host not in LOOPBACK_HOSTS:
        return json_error(403, "host_not_allowed", "auth", "use loopback host")
    origin = request.headers.get("origin")
    if origin and not origin.startswith(LOOPBACK_ORIGINS):
        return json_error(403, "origin_not_allowed", "auth", "use loopback origin")
    return None


async def local_origin_guard(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    limit = request.app.state.max_request_body_bytes
    content_length = request.headers.get("content-length")
    if content_length and _declared_oversize(content_length, limit):
        return _too_large()
    if request.method in BODY_METHODS:
        if not content_length:
            # chunked 请求没有 Content-Length：只缓冲到上限，再把校验过的 body
            # 交给下游处理器（否则下游会二次读取空流）。
            body = bytearray()
            async for chunk in request.stream():
                body += chunk
                if len(body) > limit:
                    return _too_large()
            request._body = bytes(body)
        rejection = _reject_non_loopback(request)
        if rejection is not None:
            return rejection
    return await call_next(request)


def require_capability(
    state: Any,
    token: str | None,
    scope: str,
    audience: str | None = None,
    *,
    force: bool = False,
    required_scope: str | None = None,
) -> None:
    """HTTP adapter over tools.capability.check_capability (single core)."""
    result = check_capability(
        token,
        state.capability_token,
        created_at=state.capability_token_created_at,
        ttl_seconds=state.capability_token_ttl_seconds,
        scopes=state.capability_scopes,
        required_scope=required_scope
        if required_scope is not None
        else required_scope_for(scope, force=force),
        audience=audience,
        skip=scope == "public" and not force,
    )
    if result is None:
        return
    code, retryable, next_action = result
    # token 缺失是 401，其余校验失败是 403
    raise api_error(
        401 if code == "capability_token_required" else 403,
        code,
        "auth",
        next_action,
        retryable=retryable,
    )


def require_write_capability(
    state: Any,
    token: str | None,
    audience: str | None = None,
    *,
    required_scope: str = "write",
) -> None:
    require_capability(
        state, token, "write", audience, force=True, required_scope=required_scope
    )
