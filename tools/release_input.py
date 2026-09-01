"""`release_input_sha256` 的唯一计算入口（§6.8）。

规范原文：`release_input_sha256` 覆盖 public copy 的正文、allowlisted attachments 的
相对路径与 hash、允许公开的 metadata、Wiki-to-Wiki links、route、
`public_lineage_commitment` 以及 policy/schema 版本；它不是单独的 `content_sha256`。

实测动机（2026-09-01）：这个 hash 此前从未被计算过——projection 把确认事件里的值
原样拷进 manifest，而现存那个事件里它与 `reviewed_content_sha256` 逐字相同。后果是
人工批准只绑定正文与证据，`route`/`body_path`/`attachments`/`links` 在批准之后改动，
页面仍以"已批准"状态发布。因此计算与比对必须共用同一份实现：projection 用它派生
`public_release`，签名命令用它给 owner 展示待签值，两处各算一份必然漂移。

正文以其 `content_sha256` 参与：正文的规范化口径已经由 content hash 定义，再写第二份
正文归一化实现就是第二个真相源。
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .common import hash_canonical, sha256_text
from .paths import RepoPaths
from .policy import policy_value
from .schemas import schemas_value

WIKI_SCHEMA_VERSION = "wiki/v1"


def public_metadata(item: dict[str, Any], root: Path) -> dict[str, Any]:
    """按 `public_projection.public_metadata_fields` 取允许公开的 metadata 子集。"""
    fields = (
        schemas_value(root, "public_projection", "public_metadata_fields", default=[])
        or []
    )
    return {field: item.get(field) for field in sorted(fields)}


def lineage_commitment(root: Path, operation_id: str) -> str:
    """§6.8：commitment 是 lineage 记录路径的 sha256，只用于本机回到审计记录。

    它不含 private Vault 名称或对象 ID，因此不需要额外的 HMAC 密钥体系。
    注意：路径参与 hash，所以 §4.6 的 ledger 迁移（批次 3）会改变它，从而使既有
    确认事件失配——这是设计要求的"输入变化即回落"，不是缺陷。
    """
    paths = RepoPaths(root)
    record = paths.operation_file(operation_id)
    try:
        relative = record.relative_to(paths.root)
    except ValueError:
        relative = record
    return sha256_text(str(relative))


def compute(
    root: Path,
    *,
    item: dict[str, Any],
    content_sha256: str,
    operation_id: str,
) -> tuple[str, dict[str, Any]]:
    """返回 (release_input_sha256, 参与计算的材料)。

    材料一并返回，供签名命令展示给人核对——只给一个 hash 让人签，人无法核对。
    """
    material = {
        "body": content_sha256,
        "body_path": item.get("body_path"),
        "attachments": item.get("attachments") or [],
        "public_metadata": public_metadata(item, root),
        "links": item.get("links") or [],
        "route": item.get("route"),
        "public_lineage_commitment": lineage_commitment(root, operation_id),
        "policy_version": policy_value(root, "policy_version", default=None),
        "schema_version": WIKI_SCHEMA_VERSION,
    }
    return hash_canonical(material), material
