"""检索与对象定位的 HTTP 侧编排（F006）。

只做「领域调用 ↔ HTTP 错误码」的映射：检索核心在 ``tools.indexing``，vault 解析
在 ``tools.vault_registry``，这里不复制任何领域判断。
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from tools.common import safe_id
from tools.front_matter import FrontMatter
from tools.vault_registry import VaultRegistry

from .errors import api_error
from .schemas import RetrieveRequest
from .security import require_capability

SCOPES = frozenset({"public", "local", "private"})
MAX_VAULT_IDS = 16
OBJECT_TYPES = frozenset({"wiki", "source"})


def require_scope(scope: str) -> None:
    if scope not in SCOPES:
        raise api_error(400, "scope_invalid", "request", "use public/local/private")


def attach_sources(result: dict, items: list[dict]) -> dict:
    """为命中 wiki 附带其 front matter 中的 sources/related 引用。"""
    by_id = {}
    for item in items:
        body = item.get("body")
        if not body or not item.get("object_id"):
            continue
        try:
            meta, _ = (
                FrontMatter.parse(body) if body.startswith("---\n") else ({}, None)
            )
        except ValueError:
            meta = {}
        by_id[item["object_id"]] = {
            "sources": meta.get("sources", []),
            "related": meta.get("related", []),
        }
    for hit in result.get("items", []):
        oid = (hit.get("object_ref") or {}).get("object_id")
        if oid in by_id:
            hit["sources"] = by_id[oid]["sources"]
            hit["related"] = by_id[oid]["related"]
    return result


def run_retrieve(
    state: Any,
    req: RetrieveRequest,
    token: str | None = None,
    audience: str | None = None,
) -> dict:
    require_scope(req.scope)
    require_capability(state, token, req.scope, audience)
    if req.scope == "private" and not req.vault_ids:
        raise api_error(
            400,
            "vault_ids_required",
            "request",
            "select one or more internal vault_ids",
        )
    if len(req.vault_ids or []) > MAX_VAULT_IDS:
        raise api_error(400, "query_limit_exceeded", "request", "reduce vault_ids")
    result = state.retriever.search(req.query, req.scope, req.top_k, req.vault_ids)
    # §12/§1958：include_sources/include_archive 是已定义契约，不允许
    # "被接受但被忽略"的静默参数（F006 review 修复）
    if req.include_sources:
        result = attach_sources(result, state.retriever.items)
    if req.include_archive:
        result.setdefault("warnings", []).append("archive_recall_not_available")
    return result


def resolve_object_path(
    root: Path, vault_id: str, object_type: str, object_id: str
) -> Path:
    """把 object_ref 解析成 owner vault 内的唯一物理路径。"""
    try:
        safe_id(vault_id)
        safe_id(object_id)
    except ValueError as exc:
        raise api_error(
            422, "invalid_object_ref", "request", "use a safe vault_id/object_id"
        ) from exc
    if object_type not in OBJECT_TYPES:
        raise api_error(404, "object_type_not_found", "read", "use wiki or source")
    try:
        owner_root = VaultRegistry(root).resolve_vault_path(vault_id)
    except (OSError, ValueError) as exc:
        raise api_error(
            404, "vault_unavailable", "read", "check vault registry"
        ) from exc
    base = owner_root / ("wiki" if object_type == "wiki" else "sources")
    matches = [
        p for p in base.rglob(f"{object_id}.md") if p.is_file() and not p.is_symlink()
    ]
    if not matches:
        raise api_error(404, "object_not_found", "read", "check object_ref")
    # AC-F006-003：同名对象不得按目录顺序猜测 owner（多匹配一律结构化拒绝）
    if len(matches) > 1:
        raise api_error(
            409,
            "object_id_ambiguous",
            "read",
            "disambiguate the object id within this vault",
        )
    return matches[0]
