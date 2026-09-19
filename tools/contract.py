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
        "object_unreadable",
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
        # question.py（authoring / import / lifecycle / grading / scheduling）
        "question_spec_invalid",
        "question_id_conflict",
        "existing_question_invalid",
        "question_json_invalid",
        "question_import_source_empty",
        "question_status_invalid",
        "session_size_invalid",
        "question_catalog_invalid",
        "error_queue_limit_invalid",
        "queue_size_invalid",
        "question_disabled",
        "response_option_unknown",
        "response_options_duplicate",
        "scoring_mode_invalid",
        "rating_invalid",
        "grading_provider_unavailable",
        "scheduler_unavailable",
    }
)  # agent-A1: question.py/question_quality
_SOURCE_CODES: frozenset[str] = frozenset(
    {
        # ingest/source_ingestor（source 采集入口）：仅登记少数“伞码”作为顶层
        # error_code。底层动态/明细码（fetch_blocked:*、injected_io_error:*、
        # transcript_format_unsupported、异常类名……）不进词表，放 errors[]。
        # 输入/校验类失败用这两个 blocked 伞码；网络/IO/解码类失败复用
        # _CRUD_CODES 的 source_ingest_failed（unavailable）。
        "schema_invalid",
        "source_empty",
    }
)  # agent-A1: ingest/source_ingestor
_ENTRY_CODES: frozenset[str] = frozenset(
    {
        # skill_runtime.dispatch 通道门禁与 catch-all
        "skill_action_not_allowed",
        "skill_payload_forbidden",
        "skill_payload_unknown_field",
        "skill_action_failed",
        # skill_runtime handler 抛出的结构化字段级错误码
        "skill_private_read_requires_api",
        "skill_public_query_only",
        "skill_unavailable",
        "wiki_path_required",
        "path_invalid",
        "files_required",
        "content_not_string",
        "empty_write",
        "path_symlink",
        "path_outside_repo",
        "invalid_target",
        "path_hardlink",
        "apply_failed",
        "source_request_required",
        "publish_event_required",
        "spec_required",
        "wiki_not_found",
        # mcp_server / backend capability 门禁（tools.capability 的码，语义不变）
        "capability_token_required",
        "capability_token_invalid",
        "capability_token_expired",
        "capability_audience_invalid",
        "capability_scope_invalid",
    }
)  # agent-A2: backend/* / skill_runtime / mcp_server
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

# A 线剩余迁移的按域子集（各 agent 只填自己那块，避免同一字面量并行冲突）。
_BACKUP_CODES: frozenset[str] = frozenset(
    {
        # backup.py status/manifest/verify/restore 状态机的顶层伞码/明细码
        # （测试断言的具体码语义保持；动态/未预期异常归 backup_operation_failed）。
        "manifest_schema_invalid",
        "hash_mismatch",
        "vault_not_found",
        "manifest_owner_mismatch",
        "entry_path_invalid",
        "entry_path_symlink",
        "entry_missing",
        "entry_hardlink",
        "entry_invalid",
        "entries_invalid",
        "durable_record_hash_mismatch",
        "confirmation_record_invalid",
        "manifest_unverified",
        "backup_target_invalid",
        "backup_target_not_empty",
        "vault_id_invalid",
        "bundle_unverified",
        "bundle_unreadable",
        "cross_vault_restore",
        "restored_entry_path_invalid",
        "restored_entry_missing",
        "restored_hash_mismatch",
        "restore_marker_missing",
        "restore_extra_entry",
        "restore_target_invalid",
        "restore_target_not_empty",
        "restore_verification_failed",
        "backup_operation_failed",
    }
)  # agent-backup: backup.py
_VALIDATION_CODES: frozenset[str] = frozenset(
    {
        # WikiValidator.validate 无法跑通（可执行 JSON Schema 缺失）时的顶层伞码；
        # 字段级校验码（source_missing/unknown_field 等）留在 errors[]，不登记。
        "validator_unavailable",
    }
)  # agent-valing: validation/*
_INGEST_CODES: frozenset[str] = frozenset(
    {
        # video_frames：帧抽取 blocked 的明细码（动态/未预期异常归 video_frame_failed）。
        "source_not_video",
        "frame_media_missing",
        "frame_timestamps_missing",
        "frame_timestamp_invalid",
        "frame_extraction_timeout",
        "frame_extraction_failed",
        "frame_staging_missing",
        "frame_apply_failed",
        "video_frame_failed",
        # video_inventory：采集失败的顶层伞码（明细码进 errors[]）。
        "video_inventory_failed",
    }
)  # agent-valing: ingest/*（不含 source_ingestor）
_DOCTOR_CODES: frozenset[str] = frozenset()  # agent-valing: doctor.py（顶层恒 ok）
# A 线闭环：剩余遗留生产者归一（各 agent 只填自己那块）。
_ANCHOR_CODES: frozenset[str] = frozenset(
    {
        # evidence_anchor.main（CLI 定位/落盘入口）的 blocked 顶层码：
        # anchor() 的引文/选择子校验码与 anchor_evidence() 的漂移码，语义不变。
        "quote_too_short",
        "selector_unresolved",
        "ambiguous_selector",
        "media_fragment_invalid",
        "stale",
        "path_unresolved",
        # --from-jsonl 批量：存在未解析行时的顶层伞码
        # （每行的动态/明细码留在 payload.unresolved[].error_code，不进词表）。
        "anchor_batch_unresolved",
    }
)  # agent: evidence_anchor.py
_AUDIT_CODES: frozenset[str] = frozenset(
    {
        # validation/audit.py（LLM 证据审计编排）。审计判定（not_run/pass/fail、
        # 覆盖义务、引文二次校验等）是领域结果，进 payload，不登记为 error_code。
        # 这里只登记「操作层」status != ok 的顶层码：
        # provider 不可用/超时 → unavailable
        "provider_unavailable",
        "context_exceeded",
        # 前置门禁（AuditBlocked，CLI 边界归一为 blocked）
        "deterministic_blocked",
        "ruleset_unavailable",
        "evidence_missing",
        "policy_invalid",
        "wiki_unreadable",
    }
)  # agent: validation/audit.py
_CONFIRM_CODES: frozenset[str] = frozenset(
    {
        # validation/confirm.py（人工审计确认 CLI 前置门禁 → blocked）
        "invalid_decision",
        "invalid_actor_id",
        "deterministic_blocked",
        "llm_state_blocks_confirmation",
        "confirmation_write_failed",
        "operation_write_failed",
    }
)  # validation/confirm.py
_MATRIX_CODES: frozenset[str] = frozenset(
    {
        # matrix_sync.py（追踪矩阵/feature-list/文档索引一致性检查——发现不一致=blocked）
        "matrix_inconsistent",
        "feature_list_invalid",
        "doc_index_inconsistent",
        "matrix_unreadable",
        "feature_list_unreadable",
        "matrix_check_failed",
    }
)  # matrix_sync.py
_CLI_CODES: frozenset[str] = frozenset(
    {
        # cli.py 内联生产者：override（人工复议）+ release（发布输入）
        "actor_invalid",
        "object_invalid",
        "reason_required",
        "report_not_failed",
        "report_not_found",
        "report_schema_invalid",
        "write_failed",
        "not_public_publishable",
    }
)  # cli.py（override_main / release_main）

ERROR_CODES = (
    _LOCATE_CODES
    | _QUESTION_CODES
    | _SOURCE_CODES
    | _ENTRY_CODES
    | _MISC_CODES
    | _CRUD_CODES
    | _BACKUP_CODES
    | _VALIDATION_CODES
    | _INGEST_CODES
    | _DOCTOR_CODES
    | _ANCHOR_CODES
    | _AUDIT_CODES
    | _CONFIRM_CODES
    | _MATRIX_CODES
    | _CLI_CODES
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
