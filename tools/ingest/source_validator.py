"""Source 请求与已发布 Source 文件的 schema 校验器。

校验规则对应 F001 验收标准的字段级约束（AC-F001-009）与发布后快照一致性。
"""

from __future__ import annotations

from pathlib import Path

from ..common import (
    ACQUISITIONS,
    DOMAINS,
    SOURCE_TYPES,
    canonical_quote,
    safe_id,
    sha256_text,
)
from ..front_matter import FrontMatter


class SourceValidator:
    """Source 请求与已发布文件的校验器（无状态，方法可静态调用）。"""

    def validate_request(self, request: dict) -> list[dict]:
        """校验导入请求的交叉字段约束，返回字段级错误列表（空列表表示通过）。

        校验 source_type/domain 枚举、local-file 与 input_path 的绑定、
        personal-note 的 origin、非本地来源的 url 必填与 acquisition 一致性。
        """
        errors: list[dict] = []
        source_type = request.get("source_type")
        if source_type not in SOURCE_TYPES:
            errors.append({"code": "schema_invalid", "path": "source_type"})
        if request.get("domain") not in DOMAINS:
            errors.append({"code": "schema_invalid", "path": "domain"})
        if request.get("input_path") and source_type != "local-file":
            errors.append(
                {
                    "code": "schema_invalid",
                    "path": "source_type",
                    "reason": "input_path_requires_local_file",
                }
            )
        if source_type == "local-file" and not request.get("input_path"):
            errors.append({"code": "schema_invalid", "path": "input_path"})
        if (
            source_type == "personal-note"
            and request.get("origin", "personal") != "personal"
        ):
            errors.append(
                {
                    "code": "schema_invalid",
                    "path": "origin",
                    "reason": "personal_note_requires_personal_origin",
                }
            )
        if source_type not in {"local-file", "personal-note"} and not request.get("url"):
            errors.append(
                {"code": "schema_invalid", "path": "url", "reason": "fetch_requires_url"}
            )
        acquisition = request.get("acquisition") or {
            "local-file": "local-file",
            "personal-note": "personal-note",
        }.get(source_type, "fetch")
        if acquisition not in ACQUISITIONS:
            errors.append({"code": "schema_invalid", "path": "retrieval.acquisition"})
        if request.get("source_id"):
            try:
                safe_id(request["source_id"])
            except ValueError:
                errors.append({"code": "schema_invalid", "path": "source_id"})
        return errors

    @staticmethod
    def quote_sha256(quote: str) -> str:
        """独立于锚定工具调用路径的引文摘要重算（AC-F001-013）。

        与 evidence_anchor 共用 canonical_quote 单一实现，但走独立调用路径；
        一致性测试常驻断言 anchor 生成值 == 本方法重算值。
        """
        return sha256_text(canonical_quote(quote))

    def validate_source_file(self, path: Path) -> list[dict]:
        """校验已发布 Source 文件的 front matter 与正文快照一致性，返回错误列表。"""
        try:
            metadata, body = FrontMatter.parse(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, TypeError, ValueError) as exc:
            return [{"code": "schema_invalid", "path": str(path), "reason": str(exc)}]
        errors = []
        if metadata.get("schema_version") != "source/v1":
            errors.append({"code": "schema_invalid", "path": "schema_version"})
        if metadata.get("source_type") not in SOURCE_TYPES:
            errors.append({"code": "schema_invalid", "path": "source_type"})
        if metadata.get("domain") not in DOMAINS:
            errors.append({"code": "schema_invalid", "path": "domain"})
        if metadata.get("source_type") == "local-file":
            local = metadata.get("local") or {}
            if not local.get("file_sha256"):
                errors.append({"code": "schema_invalid", "path": "local.file_sha256"})
            if not str(local.get("path_ref", "")).startswith("local-sidecar:"):
                errors.append({"code": "schema_invalid", "path": "local.path_ref"})
            if (metadata.get("retrieval") or {}).get("acquisition") != "local-file":
                errors.append({"code": "schema_invalid", "path": "retrieval.acquisition"})
            if not metadata.get("snapshot_sha256"):
                errors.append({"code": "schema_invalid", "path": "snapshot_sha256"})
        elif metadata.get("source_type") == "personal-note":
            if (metadata.get("retrieval") or {}).get("acquisition") != "personal-note":
                errors.append({"code": "schema_invalid", "path": "retrieval.acquisition"})
        if not body.strip():
            errors.append({"code": "source_empty", "path": "body"})
        if metadata.get("snapshot_sha256") and metadata.get(
            "snapshot_sha256"
        ) != sha256_text(body):
            errors.append({"code": "snapshot_hash_mismatch", "path": "snapshot_sha256"})
        return errors
