"""本地回环防护与 capability 门禁（F006）。

两层职责：
1. ``local_origin_guard`` 中间件——请求体上限 + 只接受回环 host/origin；
2. ``require_action``——共享 action policy 与 ``tools.capability``
   的 HTTP 适配层（核心判定只有一份，这里只负责映射到 401/403）。
"""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import Any
from urllib.parse import urlsplit

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.responses import Response

from tools.access_policy import capability_for
from tools.capability import check_capability

from .errors import api_error, json_error

LOOPBACK_HOSTS = frozenset({"127.0.0.1", "::1", "localhost", "testserver"})
BODY_METHODS = frozenset({"POST", "PUT", "PATCH", "DELETE"})


def _too_large() -> JSONResponse:
    return json_error("request_too_large", "request", "reduce request body")


def _declared_oversize(content_length: str, limit: int) -> bool:
    try:
        return int(content_length) > limit
    except ValueError:
        # 不可解析的 Content-Length 一律当超限拒绝，不猜真实体积
        return True


def _reject_non_loopback(request: Request) -> JSONResponse | None:
    try:
        target = urlsplit("http://" + request.headers.get("host", ""))
        valid_host = (
            target.hostname in LOOPBACK_HOSTS
            and not target.username
            and not target.password
            and not target.path
            and not target.query
            and not target.fragment
        )
        target_port = target.port or 80
    except ValueError:
        valid_host = False
    if not valid_host:
        return json_error("host_not_allowed", "auth", "use loopback host")
    origin = request.headers.get("origin")
    if origin and not _local_origin(origin, target_port):
        return json_error("origin_not_allowed", "auth", "use loopback origin")
    return None


def _local_origin(origin: str, target_port: int) -> bool:
    try:
        parsed = urlsplit(origin)
        return (
            parsed.scheme == "http"
            and parsed.hostname in LOOPBACK_HOSTS
            and (parsed.port or 80) in {4321, 8765, target_port}
            and not parsed.username
            and not parsed.password
            and not parsed.path
            and not parsed.query
            and not parsed.fragment
        )
    except ValueError:
        return False


async def local_origin_guard(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    limit = request.app.state.max_request_body_bytes
    content_length = request.headers.get("content-length")
    if content_length and _declared_oversize(content_length, limit):
        return _too_large()
    rejection = _reject_non_loopback(request)
    if rejection is not None:
        return rejection
    if request.method in BODY_METHODS and not content_length:
        # chunked 请求没有 Content-Length：只缓冲到上限，再把校验过的 body
        # 交给下游处理器（否则下游会二次读取空流）。
        body = bytearray()
        async for chunk in request.stream():
            body += chunk
            if len(body) > limit:
                return _too_large()
        request._body = bytes(body)
    return await call_next(request)


def require_action(
    state: Any,
    action: str,
    token: str | None,
    audience: str | None = None,
    **payload: Any,
) -> None:
    """Use the shared resource/action policy; scope never bypasses authorization."""
    scope = payload.get("scope")
    if scope is not None and scope not in {"public", "local", "private"}:
        raise api_error("scope_invalid", "request", "use public/local/private")
    needed = capability_for(action, payload)
    if needed is None:
        return
    result = check_capability(
        token,
        state.capability_token,
        created_at=state.capability_token_created_at,
        ttl_seconds=state.capability_token_ttl_seconds,
        scopes=state.capability_scopes,
        required_scope=needed,
        audience=audience,
    )
    if result is not None:
        code, _retryable, next_action = result
        raise api_error(code, "auth", next_action)
