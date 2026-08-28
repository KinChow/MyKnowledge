"""HTTP 错误响应的单一构造点（F006）。

对外契约固定为 ``{"detail": {code, stage, retryable, next_action}}``——错误码与
stage 是契约的一部分，散落的字面量 dict 让同一语义容易出现两种拼写。
"""

from __future__ import annotations

from fastapi import HTTPException
from fastapi.responses import JSONResponse


def error_detail(
    code: str, stage: str, next_action: str, *, retryable: bool = False
) -> dict[str, object]:
    return {
        "code": code,
        "stage": stage,
        "retryable": retryable,
        "next_action": next_action,
    }


def api_error(
    status_code: int,
    code: str,
    stage: str,
    next_action: str,
    *,
    retryable: bool = False,
) -> HTTPException:
    """端点内抛出的错误（走 FastAPI 异常处理）。"""
    return HTTPException(
        status_code=status_code,
        detail=error_detail(code, stage, next_action, retryable=retryable),
    )


def json_error(
    status_code: int,
    code: str,
    stage: str,
    next_action: str,
    *,
    retryable: bool = False,
) -> JSONResponse:
    """中间件内直接返回的错误（此时还没有异常处理链）。"""
    return JSONResponse(
        status_code=status_code,
        content={"detail": error_detail(code, stage, next_action, retryable=retryable)},
    )
