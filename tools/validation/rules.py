"""Wiki domain rule 层：状态组合、kind 分支、证据结构、来源矩阵（§6.7/§6.8）。

纯函数式规则：输入 metadata/body，输出 (errors, warnings, resolution)。
不持有实例状态；引用解析委托 resolution 模块（结果沿调用链返回）。
"""

from __future__ import annotations

import re
from pathlib import Path

from ..common import canonical_body, glob_without_symlinks
from . import resolution

PLANNED_ONLY_FIELDS = {"id", "title", "domain", "kind", "status"}

REQUIRED_SECTIONS = [
    "一句话结论",
    "核心概念",
    "工作机制",
    "示例或代码",
    "常见误区",
    "证据映射",
    "待验证项",
    "关联知识",
]

def check_index_links(body: str, paths) -> list[dict]:
    """index 页：正文中的 markdown 链接必须可解析到库内对象（§6.7 硬性要求）。

    支持两种链接形式：相对仓库根的 ``.md`` 路径（如 ``wiki/tools/foo.md``）
    与裸 wiki ID（如 ``foo``，按 owner Vault 内唯一解析）。
    """
    errors: list[dict] = []
    for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", body):
        cleaned = target.split("#")[0].split("?")[0]
        if not cleaned:
            continue
        if cleaned.endswith(".md"):
            # 相对仓库根路径（布局基准：root，非 wiki_root）
            candidate = paths.root / cleaned
            if not candidate.exists():
                errors.append(
                    {"code": "link_unresolved", "path": "body",
                     "reason": f"链接目标不存在: {cleaned}"}
                )
        else:
            hits = glob_without_symlinks(paths.wiki_root, f"*/{cleaned}.md")
            if len(hits) != 1:
                errors.append(
                    {"code": "link_unresolved", "path": "body",
                     "reason": f"链接目标无法唯一解析: {cleaned}"}
                )
    return errors


def domain_rules(
    metadata: dict, body: str, paths, quote_min_chars: int,
    owner_vault_id: str = "public",
) -> tuple[list[dict], list[dict], dict]:
    """跨字段规则：状态组合、planned 约束、kind 分支、证据结构与引文校验。

    返回 (errors, warnings, resolution)——resolution 沿调用链传递，
    不存实例状态（validator 实例可安全并发/复用）。
    """
    errors: list[dict] = []
    warnings: list[dict] = []
    kind = metadata.get("kind")
    status = metadata.get("status")
    scope = metadata.get("publication_scope")

    # planned 只允许五个字段、无正文、无 sources/evidence（§6.2/6.7）
    if status == "planned":
        extra = sorted(set(metadata.keys()) - PLANNED_ONLY_FIELDS)
        if extra:
            errors.append(
                {
                    "code": "planned_with_content",
                    "path": "status",
                    "reason": f"planned 只允许五字段，发现额外字段: {', '.join(extra)}",
                }
            )
        if canonical_body(body).strip("\n").strip():
            errors.append(
                {"code": "planned_with_content", "path": "body",
                 "reason": "planned 不允许正文"}
            )

    # published 组合约束（§6.8 互斥与前置约束）
    if status == "published":
        if scope == "none":
            errors.append(
                {"code": "published_scope_none", "path": "publication_scope",
                 "reason": "status: published 不能与 publication_scope: none 组合"}
            )
        if not metadata.get("sources"):
            errors.append(
                {"code": "source_missing", "path": "sources",
                 "reason": "published 必须有 source"}
            )

    # knowledge 必须：sources、evidence、正文模板、引文（planned 免除，§6.7）
    if kind == "knowledge" and status != "planned":
        if not metadata.get("sources"):
            errors.append({"code": "source_missing", "path": "sources"})
        if not metadata.get("evidence"):
            errors.append({"code": "evidence_missing", "path": "evidence"})
        missing_sections = [
            section for section in REQUIRED_SECTIONS if f"## {section}" not in body
        ]
        if missing_sections:
            errors.append(
                {
                    "code": "body_template_incomplete",
                    "path": "body",
                    "reason": f"缺少小节: {', '.join(missing_sections)}",
                }
            )

    # reference 必须引用 source（§6.7）；index 的替代检查是硬性要求（F009）
    if kind == "reference":
        if not metadata.get("sources"):
            errors.append({"code": "source_missing", "path": "sources",
                           "reason": "kind: reference 必须有 metadata-only 以上 source"})
        elif not metadata.get("evidence"):
            # C003：reference 无 claim 级 evidence 时不走 resolution，sources
            # 仍需可解析（幽灵 source 不得通过校验）
            for source_id in metadata.get("sources") or []:
                _, resolve_errors = resolution.resolve_source(source_id, paths)
                errors.extend(resolve_errors)
    if kind == "index":
        errors.extend(check_index_links(body, paths))

    # evidence 结构：claim_id 唯一、targets 非空、quote 与 targets 交叉一致
    evidence = metadata.get("evidence") or []
    seen_claim_ids: set[str] = set()
    for claim in evidence:
        claim_id = claim.get("claim_id")
        if claim_id in seen_claim_ids:
            errors.append(
                {"code": "claim_id_duplicate", "path": f"evidence.{claim_id}"}
            )
        seen_claim_ids.add(claim_id)
        targets = claim.get("targets") or []
        if not targets:
            errors.append(
                {"code": "claim_incomplete", "path": f"evidence.{claim_id}",
                 "reason": "claim 必须有 targets"}
            )
        quote_ids = {
            q.get("evidence_id")
            for q in (claim.get("supporting_quotes") or [])
            if q.get("evidence_id") is not None
        }
        target_ids = {
            t.get("evidence_id")
            for t in targets
            if t.get("evidence_id") is not None
        }
        undeclared_quotes = sorted(quote_ids - target_ids)
        if undeclared_quotes:
            errors.append(
                {
                    "code": "quote_target_mismatch",
                    "path": f"evidence.{claim_id}",
                    "reason": f"supporting_quotes 引用了未声明的 evidence_id: {', '.join(undeclared_quotes)}",
                }
            )

    # 引用解析 + supporting_quotes 逐字校验（§6.9）；resolution 沿调用链传递
    resolution_result = resolution.resolve_and_verify(
        metadata, evidence, paths, quote_min_chars, owner_vault_id
    )
    errors.extend(resolution_result["errors"])
    warnings.extend(resolution_result["warnings"])
    return errors, warnings, resolution_result
