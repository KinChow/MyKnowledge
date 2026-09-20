"""HTTP 错误响应的单一构造点（F006）。

对外契约固定为 ``{"detail": {code, stage, retryable, next_action}}``——错误码与
stage 是契约的一部分，散落的字面量 dict 让同一语义容易出现两种拼写。
"""

from __future__ import annotations

from fastapi import HTTPException
from fastapi.responses import JSONResponse

from tools import contract

# 单一事实源：error_code → (HTTP status, contract status)。
# HTTP status 是对外契约码（语义不变）；contract status 走 tools.contract 的
# 唯一状态轴（ok/blocked/unavailable），``detail.retryable`` 一律由
# ``contract.is_retryable`` 派生（仅 unavailable 可重试），不再各调用点手抄布尔。
_ERROR_TABLE: dict[str, tuple[int, str]] = {
    # request 层
    "request_too_large": (413, "blocked"),
    "schema_invalid": (400, "blocked"),
    "scope_invalid": (400, "blocked"),
    "vault_ids_required": (400, "blocked"),
    "query_limit_exceeded": (400, "blocked"),
    "invalid_object_ref": (422, "blocked"),
    "question_spec_invalid": (422, "blocked"),
    # auth 层（capability 门禁；token 过期是可恢复的 unavailable）
    "host_not_allowed": (403, "blocked"),
    "origin_not_allowed": (403, "blocked"),
    "capability_token_required": (401, "blocked"),
    "capability_token_invalid": (403, "blocked"),
    "capability_token_expired": (403, "unavailable"),
    "capability_audience_invalid": (403, "blocked"),
    "capability_scope_invalid": (403, "blocked"),
    # read / validate 层
    "object_type_not_found": (404, "blocked"),
    "object_type_not_supported": (404, "blocked"),
    # 内容注册表全动词路由：动词不支持=405（对齐 apiserver MethodNotAllowed）
    "capability_not_supported": (405, "blocked"),
    "vault_unavailable": (404, "blocked"),
    "object_not_found": (404, "blocked"),
    "object_id_ambiguous": (409, "blocked"),
    "object_unreadable": (422, "blocked"),
    # 删除引用完整性（RESTRICT）：被引用时 409 冲突
    "object_referenced": (409, "blocked"),
    # 两阶段硬删 purge 前置门禁：未先软删 / 未过宽限期 → 409；物理回收失败 → 422
    "not_deleted": (409, "blocked"),
    "retention_not_elapsed": (409, "blocked"),
    "purge_failed": (422, "blocked"),
    # source 增改（重导入委派 / 请求缺失）
    "source_ingest_failed": (422, "blocked"),
    "source_request_required": (422, "blocked"),
    # 统一创建契约 locator 归一化：非法 URI=422；scheme 越权（如 HTTP 侧 file://）=403
    "locator_invalid": (422, "blocked"),
    "locator_scheme_not_allowed": (403, "blocked"),
    # practice 层
    "question_not_found": (404, "blocked"),
    "session_not_found": (404, "blocked"),
    "session_index_invalid": (422, "blocked"),
    "session_completion_invalid": (422, "blocked"),
    "quality_mode_invalid": (422, "blocked"),
    # write 写入门（越界/非法写入统一 422；码来自 skill_runtime 直写校验）
    "files_required": (422, "blocked"),
    "content_not_string": (422, "blocked"),
    "empty_write": (422, "blocked"),
    "path_symlink": (422, "blocked"),
    "path_outside_repo": (422, "blocked"),
    "invalid_target": (422, "blocked"),
    "path_hardlink": (422, "blocked"),
    "apply_failed": (422, "blocked"),
}


def http_status_for(code: str) -> int:
    """error_code → HTTP status（未登记 fail-closed，杜绝静默漂移）。"""
    try:
        return _ERROR_TABLE[code][0]
    except KeyError:
        raise ValueError(f"http_status_not_registered:{code}") from None


def error_detail(code: str, stage: str, next_action: str) -> dict[str, object]:
    contract_status = _ERROR_TABLE.get(code, (422, "blocked"))[1]
    return {
        "code": code,
        "stage": stage,
        "retryable": contract.is_retryable(contract_status),
        "next_action": next_action,
    }


def api_error(code: str, stage: str, next_action: str) -> HTTPException:
    """端点内抛出的错误（走 FastAPI 异常处理）。"""
    return HTTPException(
        status_code=http_status_for(code),
        detail=error_detail(code, stage, next_action),
    )


def json_error(code: str, stage: str, next_action: str) -> JSONResponse:
    """中间件内直接返回的错误（此时还没有异常处理链）。"""
    return JSONResponse(
        status_code=http_status_for(code),
        content={"detail": error_detail(code, stage, next_action)},
    )
