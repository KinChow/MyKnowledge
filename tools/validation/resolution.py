"""Wiki 引用解析与引文校验（§6.9）。

owner Vault 内解析 source/evidence target、supporting_quotes 逐字校验
（canonical_quote 单一实现 + TextPositionSelector 限定范围 + 子串包含 +
LCS 诊断）。纯函数式：输入路径/参数，输出 resolution 数据对象，无实例状态。
"""

from __future__ import annotations

import difflib

from ..common import canonical_quote, glob_without_symlinks
from ..front_matter import FrontMatter
from .schema import OWNER_VAULT_ID

# §6.5 来源类型与论断语气兼容矩阵：support → 允许的 source origin
SUPPORT_ORIGIN_MATRIX = {
    "direct": {"external"},
    "synthesis": {"external"},
    "inferred": {"external", "personal"},
    "personal": {"personal"},
}


def resolve_source(source_id: str, paths) -> tuple[dict | None, list[dict]]:
    """owner Vault 内解析 source：sources/<domain>/<source_id>.md 唯一匹配。"""
    errors: list[dict] = []
    hits = glob_without_symlinks(paths.sources_root, f"*/{source_id}.md")
    if not hits:
        errors.append(
            {"code": "source_not_found", "path": f"sources.{source_id}"}
        )
        return None, errors
    if len(hits) > 1:
        errors.append(
            {"code": "source_ambiguous", "path": f"sources.{source_id}",
             "reason": f"多个 source 匹配: {', '.join(str(h) for h in hits)}"}
        )
        return None, errors
    try:
        text = hits[0].read_text(encoding="utf-8")
        metadata, _ = FrontMatter.parse(text)
    except (OSError, UnicodeError, ValueError, TypeError) as exc:
        errors.append(
            {"code": "source_unreadable", "path": f"sources.{source_id}",
             "reason": str(exc)}
        )
        return None, errors
    # evidence item 键名兼容（F001）：F001 evidence_anchor 产物键为
    # evidence_id（契约 evidence-item/v1 用 id）——两种都接受；
    # 字段类型校验（R003）：snapshot_sha256/position 违规 fail-closed
    items: dict[str, dict] = {}
    for item in metadata.get("evidence_items") or []:
        if not isinstance(item, dict):
            errors.append(
                {"code": "source_unreadable", "path": f"sources.{source_id}",
                 "reason": "evidence_items 含非对象条目"}
            )
            continue
        item_id = item.get("evidence_id") or item.get("id")
        if item_id is None or not isinstance(item_id, str):
            continue
        if not isinstance(item.get("snapshot_sha256"), str):
            errors.append(
                {"code": "source_unreadable", "path": f"sources.{source_id}",
                 "reason": f"evidence item {item_id} 的 snapshot_sha256 非字符串"}
            )
            continue
        position = item.get("position")
        if position is not None and not (
            isinstance(position, dict)
            and isinstance(position.get("start"), int)
            and isinstance(position.get("end"), int)
        ):
            errors.append(
                {"code": "source_unreadable", "path": f"sources.{source_id}",
                 "reason": f"evidence item {item_id} 的 position 非法"}
            )
            continue
        if item_id in items:
            errors.append({"code": "duplicate_evidence_id", "path": f"sources.{source_id}.evidence_items.{item_id}", "reason": "同一 Source 内 evidence_id 必须唯一"})
            continue
        items[item_id] = item
    return {"metadata": metadata, "evidence_items": items, "path": hits[0]}, errors


def resolve_and_verify(
    metadata: dict, evidence: list[dict], paths, quote_min_chars: int
) -> dict:
    """解析全部 claim target 并校验 supporting_quotes；结果供派生字段计算。"""
    errors: list[dict] = []
    warnings: list[dict] = []
    sources: dict[str, dict] = {}
    declared_sources = set(metadata.get("sources") or [])
    verified_targets = 0
    total_targets = 0
    origins: list[str] = []
    evidence_statuses: list[str] = []
    claims_origin: dict[str, list[str]] = {}
    resolved_targets: list[dict] = []

    for claim in evidence:
        claim_id = claim.get("claim_id", "?")
        targets = claim.get("targets") or []
        claims_origin.setdefault(claim_id, [])
        quotes = {
            q.get("evidence_id"): q.get("exact", "")
            for q in (claim.get("supporting_quotes") or [])
            if q.get("evidence_id") is not None
        }
        for target in targets:
            total_targets += 1
            source_id = target.get("source_id")
            evidence_id = target.get("evidence_id")
            if source_id not in declared_sources:
                errors.append(
                    {"code": "source_not_declared", "path": f"evidence.{claim_id}",
                     "reason": f"target 引用了未在 sources 声明的 source: {source_id}"}
                )
            if target.get("vault_id") and target["vault_id"] != OWNER_VAULT_ID:
                errors.append(
                    {"code": "cross_vault_reference",
                     "path": f"evidence.{claim_id}.targets.{source_id}",
                     "reason": f"显式跨 Vault target 被拒绝: vault={target['vault_id']}"}
                )
            source = sources.get(source_id)
            if source is None:
                source, resolve_errors = resolve_source(source_id, paths)
                sources[source_id] = source
                errors.extend(resolve_errors)
            if source is None:
                continue
            item = source["evidence_items"].get(evidence_id)
            if item is None:
                errors.append(
                    {"code": "evidence_not_found",
                     "path": f"evidence.{claim_id}.targets.{source_id}",
                     "reason": f"source {source_id} 中没有 evidence item: {evidence_id}"}
                )
                continue
            resolved_targets.append(
                {
                    "source_id": source_id,
                    "evidence_id": evidence_id,
                    "resolved_object_ref": {
                        "vault_id": OWNER_VAULT_ID,
                        "object_type": "source",
                        "object_id": source_id,
                    },
                    "snapshot_sha256": item.get("snapshot_sha256"),
                    "selector": item.get("selector") or {},
                    "position": item.get("position") or {},
                    "supporting_quote": quotes.get(evidence_id, ""),
                }
            )
            source_origin = source["metadata"].get("origin", "external")
            origins.append(source_origin)
            claims_origin[claim_id].append(source_origin)
            evidence_statuses.append(
                source["metadata"].get("evidence_status") or "source-reported"
            )
            # §6.5 来源类型与论断语气矩阵（F005）：support 与 source origin 必须兼容
            support = claim.get("support")
            allowed_origins = SUPPORT_ORIGIN_MATRIX.get(support)
            if allowed_origins is not None and source_origin not in allowed_origins:
                errors.append(
                    {"code": "support_origin_mismatch",
                     "path": f"evidence.{claim_id}",
                     "reason": (
                         f"support: {support} 不允许 origin: {source_origin} "
                         f"的 source（§6.5 兼容矩阵）"
                     )}
                )
            # 引文逐字校验（§6.9）
            exact = quotes.get(evidence_id)
            if exact is None:
                errors.append(
                    {"code": "quote_missing",
                     "path": f"evidence.{claim_id}",
                     "reason": f"target {source_id}/{evidence_id} 缺少 supporting_quotes.exact"}
                )
                continue
            quote_error = verify_quote(item, exact, paths, quote_min_chars)
            if quote_error:
                errors.append(quote_error)
            else:
                verified_targets += 1

    return {
        "errors": errors,
        "warnings": warnings,
        "sources": sources,
        "resolved_targets": resolved_targets,
        "verified_targets": verified_targets,
        "total_targets": total_targets,
        "personal_only": bool(origins) and all(o == "personal" for o in origins),
        "any_personal": any(o == "personal" for o in origins),
        "claims_origin": claims_origin,
        "common_knowledge_only": bool(evidence_statuses)
        and all(e == "common-knowledge" for e in evidence_statuses),
    }


def read_snapshot_scope(
    evidence_item: dict, paths
) -> tuple[str | None, str | None]:
    """读取 evidence item 的 snapshot 并限定 TextPositionSelector 范围。

    §6.9：匹配目标必须是 selector 限定的 snapshot 范围；返回
    (scope_text, error_code|None)，error_code ∈ {snapshot_missing,
    selector_unresolved}。verify_quote 与 audit 的审计上下文共用
    （F003 review R002：钳制实现单份，边界规则变更只改一处）。
    """
    snapshot_sha256 = evidence_item.get("snapshot_sha256")
    if not snapshot_sha256:
        return None, "snapshot_missing"
    snapshot_path = paths.snapshot_file(snapshot_sha256)
    if not snapshot_path.exists():
        return None, "snapshot_missing"
    try:
        snapshot = snapshot_path.read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        return None, "snapshot_missing"
    position = evidence_item.get("position")
    if not isinstance(position, dict):
        return None, "selector_unresolved"
    start = position.get("start")
    end = position.get("end")
    if not isinstance(start, int) or not isinstance(end, int):
        return None, "selector_unresolved"
    # 钳制边界防越界（R003）
    start = max(0, min(start, len(snapshot)))
    end = max(0, min(end, len(snapshot)))
    return snapshot[start:end], None


def verify_quote(
    evidence_item: dict, exact: str, paths, quote_min_chars: int
) -> dict | None:
    """在 evidence item 的 TextPositionSelector 范围内逐字校验引文（§6.9）。"""
    scope, scope_error = read_snapshot_scope(evidence_item, paths)
    if scope_error == "snapshot_missing":
        return {
            "code": "snapshot_missing", "path": "evidence",
            "reason": f"snapshot 缺失或不可读: {evidence_item.get('snapshot_sha256')}",
        }
    if scope_error == "selector_unresolved":
        return {
            "code": "selector_unresolved", "path": "evidence",
            "reason": (
                "evidence item 缺少 TextPositionSelector，无法限定匹配范围"
            ),
        }
    canon_scope = canonical_quote(scope)
    canon_exact = canonical_quote(exact)
    if len(canon_exact) < quote_min_chars:
        return {
            "code": "quote_too_short", "path": "evidence",
            "reason": f"规范化引文长度 {len(canon_exact)} < quote_min_chars {quote_min_chars}",
        }
    if canon_exact not in canon_scope:
        matcher = difflib.SequenceMatcher(None, canon_scope, canon_exact)
        block = matcher.find_longest_match(0, len(canon_scope), 0, len(canon_exact))
        return {
            "code": "quote_mismatch", "path": "evidence",
            "reason": (
                f"引文未在 target 指向的 snapshot 范围内逐字命中。"
                f"snapshot_sha256={evidence_item.get('snapshot_sha256')} "
                f"evidence_id={evidence_item.get('id')} "
                f"scope_len={len(canon_scope)} quote_len={len(canon_exact)} "
                f"lcs_pos={block.a} lcs_len={block.size}"
            ),
        }
    return None
