"""Wiki 契约校验器：schema 层 + domain rule 层 + 派生字段与 hash 计算。

对应 F002 验收标准（docs/acceptance/F002-wiki-contract.md）：
- AC-F002-003/006：手写派生字段与发布组合一律拒绝（derived_field_mismatch）
- AC-F002-004：状态轴合法组合确定性校验（planned 只允许五字段、published 需审计确认、
  availability: unavailable 不写成 evidence_state: missing、public_release 默认 false）
- AC-F002-005：owner Vault 内引用解析，显式跨 Vault target 返回 cross_vault_reference
- AC-F002-007：版本化可执行 JSON Schema（config/json-schema/wiki-v1.json）与
  config/schemas.yaml registry 分离，validator 输出字段级错误与 schema 版本
- §6.6 内容 hash：content_sha256 = sha256(canonical_body)、
  evidence_sha256 = sha256(canonical_json(解析后 evidence，含 resolved_object_ref))
- §6.8 派生字段：evidence_state / validation_state / strength / availability /
  effective_confidentiality / private_publishable / public_publishable / publication_warning
- §6.9 引文逐字校验：canonical_quote 单一实现 + TextPositionSelector 限定范围 + 子串包含

validator 是只读确定性校验：不写 canonical 文件、不创建 operation。
"""

from __future__ import annotations

import difflib
import json
import re
from pathlib import Path

from .common import canonical_json, canonical_quote, hash_canonical, sha256_text
from .front_matter import FrontMatter
from .paths import RepoPaths

WIKI_SCHEMA_VERSION = "wiki/v1"
OWNER_VAULT_ID = "public"

# 派生/运行字段：作者手写一律拒绝（§6.8 声明/派生/operation-controlled 分组）
FORBIDDEN_DERIVED_FIELDS = frozenset(
    {
        "vault_id",
        "evidence_state",
        "validation_state",
        "effective_confidentiality",
        "strength",
        "private_publishable",
        "public_publishable",
        "public_release",
        "public_confirmation_sha256",
        "publication_warning",
        "validation_attestation_ref",
        "content_sha256",
        "evidence_sha256",
        "availability",
        "availability_reason",
    }
)

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

SUPPORT_ORIGIN_MATRIX = {
    "direct": {"external"},
    "synthesis": {"external"},
    "inferred": {"external", "personal"},
    "personal": {"personal"},
}


def canonical_body(body: str) -> str:
    """规范化正文（§6.6）：LF 统一、去行尾空白、折叠文件末尾空行为单个换行。

    只做这四步，不做其他改写（不动大小写、标点、列表重排）。
    """
    lines = [
        line.rstrip()
        for line in body.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    ]
    while lines and lines[-1] == "":
        lines.pop()
    lines.append("")
    return "\n".join(lines)


class WikiValidator:
    """Wiki 契约校验器（owner Vault 上下文内只读校验）。"""

    def __init__(self, root: Path, *, quote_min_chars: int = 12) -> None:
        self.root = root
        self.paths = RepoPaths(root)
        # 钳制下限（R011）：负值/0 会静默禁用 §6.9 引文长度门槛（fail-open）
        self.quote_min_chars = max(1, quote_min_chars)
        self._schema = self._load_schema()

    @staticmethod
    def _load_schema() -> dict:
        # schema 是代码资源，随包路径解析（与 --root 数据根解耦）；
        # 数据布局统一走 RepoPaths，但 wiki-v1.json 不是数据
        path = (
            Path(__file__).resolve().parent.parent
            / "config"
            / "json-schema"
            / "wiki-v1.json"
        )
        return json.loads(path.read_text(encoding="utf-8"))

    # ---------------- 主入口 ----------------

    def validate(self, wiki_path: Path) -> dict:
        """校验单个 Wiki 文件，返回确定性校验报告（不修改任何文件）。"""
        try:
            text = wiki_path.read_text(encoding="utf-8")
            metadata, body = FrontMatter.parse(text)
        except (OSError, UnicodeError):
            return self._report(
                wiki_path,
                errors=[{"code": "path_unresolved", "path": str(wiki_path)}],
            )
        except (ValueError, TypeError) as exc:
            return self._report(
                wiki_path,
                errors=[{"code": "front_matter_invalid", "path": str(wiki_path),
                         "reason": str(exc)}],
            )
        errors: list[dict] = []
        warnings: list[dict] = []

        # 1. 手写派生字段（先于 schema，独立错误码，fail-closed）
        for field in sorted(FORBIDDEN_DERIVED_FIELDS & metadata.keys()):
            errors.append({"code": "derived_field_mismatch", "path": field})

        # 2. schema version（AC-F002-007：错误 version 拒绝）
        schema_version = metadata.get("schema_version")
        if schema_version is not None and schema_version != WIKI_SCHEMA_VERSION:
            errors.append(
                {
                    "code": "wrong_schema_version",
                    "path": "schema_version",
                    "reason": str(schema_version),
                }
            )

        # 3. 可执行 JSON Schema（未知字段/类型/枚举/必填）
        errors.extend(self._check_schema(metadata))

        # 4. domain rule layer（结构合法后才运行，避免下游 KeyError）；
        #    jsonschema 不可用同样阻断（R005：fail-closed）
        structural_blocked = any(
            e["code"]
            in {
                "schema_invalid",
                "unknown_field",
                "wrong_schema_version",
                "validator_unavailable",
            }
            for e in errors
        )
        resolution: dict = {}
        if not structural_blocked:
            domain_errors, domain_warnings, resolution = self._domain_rules(
                metadata, body
            )
            errors.extend(domain_errors)
            warnings.extend(domain_warnings)

        report = self._report(wiki_path, errors=errors, warnings=warnings)
        report["object_ref"]["object_id"] = metadata.get("id")
        if not report["valid"]:
            return report

        # 5. 派生字段与 hash（仅结构/规则全部通过时计算）
        hashes = {
            "content_sha256": sha256_text(canonical_body(body)),
            "evidence_sha256": self._evidence_sha256(metadata, resolution),
        }
        # 验证报告只读取一次（F016）：hash 绑定校验（F003）与派生计算共用同一份
        validation_report = self._load_validation_report(
            str(metadata.get("id", "")), hashes
        )
        report["derived"] = self._compute_derived(
            metadata, body, resolution, validation_report, hashes
        )
        report["hashes"] = hashes
        report["validation_report"] = validation_report
        return report

    # ---------------- schema 层 ----------------

    def _check_schema(self, metadata: dict) -> list[dict]:
        """用 wiki-v1.json 执行结构校验，映射 jsonschema 错误为字段级错误。"""
        try:
            from jsonschema import Draft202012Validator, exceptions
        except ImportError:
            return [{"code": "validator_unavailable", "path": "_schema"}]
        validator = Draft202012Validator(self._schema)
        errors: list[dict] = []
        for error in sorted(
            validator.iter_errors(metadata), key=lambda e: list(e.path)
        ):
            if error.validator == "additionalProperties":
                errors.append(
                    {
                        "code": "unknown_field",
                        "path": ".".join(str(p) for p in error.path)
                        or error.message,
                        "reason": error.message,
                    }
                )
            else:
                errors.append(
                    {
                        "code": "schema_invalid",
                        "path": ".".join(str(p) for p in error.path) or error.validator,
                        "keyword": error.validator,
                        "reason": error.message,
                    }
                )
        return errors

    # ---------------- domain rule layer ----------------

    def _domain_rules(
        self, metadata: dict, body: str
    ) -> tuple[list[dict], list[dict], dict]:
        """跨字段规则：状态组合、planned 约束、knowledge 证据、引用解析与引文校验。

        返回 (errors, warnings, resolution)——resolution 沿调用链传递，
        不存实例状态（R004：validator 实例可安全并发/复用）。
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
        if kind == "reference" and not metadata.get("sources"):
            errors.append({"code": "source_missing", "path": "sources",
                           "reason": "kind: reference 必须有 metadata-only 以上 source"})
        if kind == "index":
            # §6.7：index 导航页的全部链接必须可解析到库内对象——失败即阻断
            errors.extend(self._check_index_links(body))

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
        resolution = self._resolve_and_verify(metadata, evidence)
        errors.extend(resolution["errors"])
        warnings.extend(resolution["warnings"])
        return errors, warnings, resolution

    def _check_index_links(self, body: str) -> list[dict]:
        """index 页：正文中的 markdown 链接必须可解析到库内对象（§6.7）。

        支持两种链接形式：相对仓库根的 ``.md`` 路径（如 ``wiki/tools/foo.md``）
        与裸 wiki ID（如 ``foo``，按 owner Vault 内唯一解析）。
        """
        warnings: list[dict] = []
        for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", body):
            cleaned = target.split("#")[0].split("?")[0]
            if not cleaned:
                continue
            if cleaned.endswith(".md"):
                # 相对仓库根路径（布局基准：root，非 wiki_root）
                candidate = (self.root / cleaned)
                if not candidate.exists():
                    warnings.append(
                        {"code": "link_unresolved", "path": "body",
                         "reason": f"链接目标不存在: {cleaned}"}
                    )
            else:
                hits = list(self.paths.wiki_root.glob(f"*/{cleaned}.md"))
                if len(hits) != 1:
                    warnings.append(
                        {"code": "link_unresolved", "path": "body",
                         "reason": f"链接目标无法唯一解析: {cleaned}"}
                    )
        return warnings

    # ---------------- 引用解析与引文校验 ----------------

    def _resolve_source(self, source_id: str) -> tuple[dict | None, list[dict]]:
        """owner Vault 内解析 source：sources/<domain>/<source_id>.md 唯一匹配。"""
        errors: list[dict] = []
        hits = list(self.paths.sources_root.glob(f"*/{source_id}.md"))
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
            items[item_id] = item
        return {"metadata": metadata, "evidence_items": items, "path": hits[0]}, errors

    def _resolve_and_verify(self, metadata: dict, evidence: list[dict]) -> dict:
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
                    source, resolve_errors = self._resolve_source(source_id)
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
                origins.append(source["metadata"].get("origin", "external"))
                source_origin = source["metadata"].get("origin", "external")
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
                quote_error = self._verify_quote(item, exact)
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

    def _verify_quote(self, evidence_item: dict, exact: str) -> dict | None:
        """在 evidence item 的 TextPositionSelector 范围内逐字校验引文（§6.9）。"""
        snapshot_sha256 = evidence_item.get("snapshot_sha256")
        if not snapshot_sha256:
            return {"code": "snapshot_missing", "path": "evidence",
                    "reason": f"evidence item 缺少 snapshot_sha256"}
        snapshot_path = self.paths.snapshot_file(snapshot_sha256)
        if not snapshot_path.exists():
            return {
                "code": "snapshot_missing", "path": "evidence",
                "reason": f"snapshot 不存在: {snapshot_path}",
            }
        try:
            snapshot = snapshot_path.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            return {
                "code": "snapshot_missing", "path": "evidence",
                "reason": f"snapshot 不可读: {snapshot_path}",
            }
        # §6.9：匹配目标必须是 selector 限定的 snapshot 范围；position 缺失或
        # 非法时返回 selector_unresolved，不得静默回退全快照匹配（F008）
        position = evidence_item.get("position")
        if not isinstance(position, dict):
            return {
                "code": "selector_unresolved", "path": "evidence",
                "reason": (
                    "evidence item 缺少 TextPositionSelector，无法限定匹配范围"
                ),
            }
        start = position.get("start")
        end = position.get("end")
        if not isinstance(start, int) or not isinstance(end, int):
            return {
                "code": "selector_unresolved", "path": "evidence",
                "reason": "TextPositionSelector 的 start/end 必须为整数",
            }
        # 钳制边界防越界（R003）
        start = max(0, min(start, len(snapshot)))
        end = max(0, min(end, len(snapshot)))
        scope = snapshot[start:end]
        canon_scope = canonical_quote(scope)
        canon_exact = canonical_quote(exact)
        if len(canon_exact) < self.quote_min_chars:
            return {
                "code": "quote_too_short", "path": "evidence",
                "reason": f"规范化引文长度 {len(canon_exact)} < quote_min_chars {self.quote_min_chars}",
            }
        if canon_exact not in canon_scope:
            matcher = difflib.SequenceMatcher(None, canon_scope, canon_exact)
            block = matcher.find_longest_match(0, len(canon_scope), 0, len(canon_exact))
            return {
                "code": "quote_mismatch", "path": "evidence",
                "reason": (
                    f"引文未在 target 指向的 snapshot 范围内逐字命中。"
                    f"snapshot_sha256={snapshot_sha256} evidence_id={evidence_item.get('id')} "
                    f"selector=[{start},{end}) scope_len={len(canon_scope)} quote_len={len(canon_exact)} "
                    f"lcs_pos={block.a} lcs_len={block.size}"
                ),
            }
        return None

    # ---------------- 派生字段与 hash ----------------

    @staticmethod
    def _read_json_dict(path: Path) -> dict | None:
        """读取 JSON 文件；不可读/损坏/非 dict 形状一律返回 None（fail-closed）。

        统一外部输入（validation report / operation / confirmation event）的
        读取与类型契约校验（F006/R001/R002），消费点不再逐处防御。
        """
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError):
            return None
        return value if isinstance(value, dict) else None

    def _load_validation_report(
        self, object_id: str, hashes: dict | None = None
    ) -> dict | None:
        """读取 owner Vault 内最近一次 LLM 验证报告（audit/validation/wiki/<id>/）。

        F003（hash 绑定）：报告必须绑定当前 (content, evidence) hash，否则视为
        过期无效（旧报告不得驱动 validation_state/verified）。F002 只消费
        verdict/claim_verdicts/corroborated；报告缺失或非法视为未运行。
        """
        base = self.paths.audit_validation("wiki", object_id)
        if not base.exists():
            return None
        try:
            candidates = sorted(base.glob("*.json"))
            if not candidates:
                return None
            latest = max(candidates, key=lambda p: p.stat().st_mtime)
        except OSError:
            return None
        report = self._read_json_dict(latest)
        if report is None:
            return None
        if hashes is not None:
            rec_content = report.get("wiki_content_sha256") or report.get(
                "content_sha256"
            )
            rec_evidence = report.get("wiki_evidence_sha256") or report.get(
                "evidence_sha256"
            )
            if (
                rec_content != hashes["content_sha256"]
                or rec_evidence != hashes["evidence_sha256"]
            ):
                return None  # 报告绑定的是旧内容，视为未运行
        return report

    def _evidence_sha256(self, metadata: dict, resolution: dict) -> str:
        """evidence_sha256 = sha256(canonical_json(解析后 evidence 含 resolved ref))。"""
        # 预构建查找表（R009）：O(T²) → O(T)
        ref_index = {
            (r["source_id"], r["evidence_id"]): r["resolved_object_ref"]
            for r in resolution.get("resolved_targets", [])
        }
        resolved = []
        for claim in metadata.get("evidence") or []:
            targets = []
            for target in claim.get("targets") or []:
                source_id = target.get("source_id")
                evidence_id = target.get("evidence_id")
                ref = ref_index.get((source_id, evidence_id)) or {
                    "vault_id": OWNER_VAULT_ID,
                    "object_type": "source",
                    "object_id": source_id,
                }
                targets.append(
                    {
                        "source_id": source_id,
                        "evidence_id": evidence_id,
                        "resolved_object_ref": ref,
                    }
                )
            resolved.append(
                {
                    "vault_id": OWNER_VAULT_ID,  # F015：owner 归属入证据摘要（§hash_inputs）
                    "claim_id": claim.get("claim_id"),
                    "claim": claim.get("claim"),
                    "support": claim.get("support"),
                    "targets": targets,
                    "supporting_quotes": claim.get("supporting_quotes", []),
                }
            )
        return hash_canonical(resolved)

    def _compute_derived(
        self,
        metadata: dict,
        body: str,
        resolution: dict,
        report: dict | None,
        hashes: dict,
    ) -> dict:
        """按 §6.8 计算全部派生字段（不入 canonical、不写回文件）。"""
        status = metadata.get("status")
        kind = metadata.get("kind")
        scope = metadata.get("publication_scope")
        confidentiality = metadata.get("confidentiality", "public")

        # validation_state（§6.8：只表达 LLM 规范审计运行结果）
        if report and report.get("verdict") == "pass":
            validation_state = "pass"
        elif report and report.get("verdict") == "fail":
            validation_state = "fail"
        else:
            validation_state = "not_run"

        # availability（§6.8 运行时派生）
        availability = "available"
        availability_reason = "none"
        for target in resolution.get("resolved_targets", []):
            if target.get("snapshot_sha256") is None:
                availability = "unavailable"
                availability_reason = "snapshot_missing"
                break
        if resolution.get("total_targets") == 0:
            availability = "unavailable"
            availability_reason = "selector_unresolved"

        # evidence_state（§6.8 优先级表，阻断级命中第一条）
        evidence_state = self._compute_evidence_state(
            metadata, resolution, report, availability
        )

        # effective_confidentiality = max(自身, 全部上游 source)
        levels = {"public": 0, "internal": 1}
        effective = levels.get(confidentiality, 0)
        for source in resolution.get("sources", {}).values():
            if source is not None:
                effective = max(effective, levels.get(source["metadata"].get("confidentiality", "public"), 0))
        effective_confidentiality = "public" if effective == 0 else "internal"

        # strength（§6.8 映射表，按顺序命中第一条）
        strength = self._compute_strength(
            kind, evidence_state, resolution, report, validation_state
        )

        # publishable 派生（审计确认检查）
        content_sha256 = hashes["content_sha256"]
        evidence_sha256 = hashes["evidence_sha256"]
        object_id = str(metadata.get("id", ""))
        has_audit = self._has_private_confirmation(
            object_id,
            content_sha256,
            evidence_sha256,
            effective_confidentiality,
        )
        blocked_states = {"missing", "partial", "conflicting", "unresolved", "stale"}
        evidence_ok = evidence_state not in blocked_states
        validation_ok = validation_state in {"not_run", "pass", "stale_ruleset"}
        base_publishable = (
            status == "published"
            and evidence_ok
            and validation_ok
            and has_audit
            and availability == "available"
        )
        private_publishable = base_publishable and scope == "private"
        # F011：public confirmation 须为人类 approve 事件（F007 阶段仍恒 false）
        public_publishable = (
            base_publishable
            and scope == "public"
            and effective_confidentiality == "public"
            and self._has_public_confirmation(object_id)
        )

        # publication_warning（§6.8）
        publication_warning = (
            "internal"
            if effective_confidentiality == "internal" and private_publishable
            else "none"
        )

        return {
            "vault_id": OWNER_VAULT_ID,
            "evidence_state": evidence_state,
            "validation_state": validation_state,
            "availability": availability,
            "availability_reason": availability_reason,
            "effective_confidentiality": effective_confidentiality,
            "strength": strength,
            "private_publishable": private_publishable,
            "public_publishable": public_publishable,
            "public_release": False,  # F002 阶段恒 false；真实派生由 F007 发布 authority 完成
            "publication_warning": publication_warning,
        }

    def _compute_evidence_state(
        self,
        metadata: dict,
        resolution: dict,
        report: dict | None,
        availability: str,
    ) -> str:
        """evidence_state：按 §6.8 阻断优先级命中第一条。

        conflicting/partial/corroborated 由 LLM 验证报告（F003）驱动——确定性层
        不自行做语义冲突与独立性判定；报告缺失时按确定性可算的结果取值。
        """
        evidence = metadata.get("evidence") or []
        if not evidence or resolution.get("total_targets") == 0:
            return "missing"
        if availability == "unavailable":
            return "unresolved"
        # snapshot 漂移：evidence item 的 snapshot_sha256 与归档实际内容不符
        for target in resolution.get("resolved_targets", []):
            snapshot_path = self.paths.snapshot_file(target["snapshot_sha256"])
            if not snapshot_path.exists():
                return "unresolved"
            try:
                actual = sha256_text(snapshot_path.read_text(encoding="utf-8"))
            except (OSError, UnicodeError):
                return "unresolved"
            if actual != target["snapshot_sha256"]:
                return "stale"
        if report:
            # R001：claim_verdicts 仅接受 list/tuple 或 dict（values），其他形状视为无；
            # corroborated 严格 is True（字符串 "false" 不算）
            verdicts = report.get("claim_verdicts")
            if isinstance(verdicts, dict):
                verdicts = list(verdicts.values())
            if not isinstance(verdicts, (list, tuple)):
                verdicts = []
            if "contradicted" in verdicts:
                return "conflicting"
            if any(
                v in {"partially_supported", "unsupported", "unmapped"}
                for v in verdicts
            ):
                return "partial"
            if report.get("corroborated") is True:
                return "corroborated"
        # 全部 target 可定位且引文校验通过；独立性未由报告证明时保守按单一 source
        return "supported"

    def _compute_strength(
        self,
        kind: str,
        evidence_state: str,
        resolution: dict,
        report: dict | None,
        validation_state: str,
    ) -> str | None:
        """strength：按 §6.8 映射顺序命中第一条。"""
        if kind == "index":
            return "index"
        if kind == "reference":
            return "reference"
        if evidence_state == "conflicting":
            return "conflicted"
        if evidence_state == "partial":
            return "partial"
        if evidence_state in {"unresolved", "stale"}:
            return "unresolved"
        # F007（§6.8）：任一 claim 只由 personal source 支撑 → 整页降级 personal
        # （混合来源取更保守一侧，不允许"部分已验证"）
        claims_origin = resolution.get("claims_origin") or {}
        any_claim_personal_only = any(
            bool(origins) and all(o == "personal" for o in origins)
            for origins in claims_origin.values()
        )
        if resolution.get("personal_only") or any_claim_personal_only:
            return "personal"
        if resolution.get("common_knowledge_only") and evidence_state in {"supported", "corroborated"}:
            return "attested"
        if evidence_state == "corroborated":
            return "corroborated"
        if validation_state == "pass" and report:
            return "verified"
        return None  # 其他：不可发布，等待补证/人工决策

    def _has_private_confirmation(
        self,
        object_id: str,
        content_sha256: str,
        evidence_sha256: str,
        effective_confidentiality: str,
    ) -> bool:
        """查找绑定当前 (content, evidence) hash 的 operation-confirmation/v1 审计确认。

        F004：effective_confidentiality 为 internal 时，确认必须携带
        warning_code/warning_text_sha256（未确认告警不得发布，§6.8）；
        F010：确认必须绑定目标对象（target_ref 匹配），内容相同的两个 Wiki
        不得复用彼此的审计确认。
        """
        audit_dir = self.paths.audit_operations
        if not audit_dir.exists():
            return False
        for path in sorted(audit_dir.glob("op_*.json")):
            record = self._read_json_dict(path)
            if record is None:
                continue
            confirmation = record.get("confirmation")
            if not isinstance(confirmation, dict):
                continue
            if confirmation.get("scope") != "publish_private":
                continue
            if confirmation.get("decision") not in (None, "approve"):
                continue
            # F010：目标对象绑定
            target = confirmation.get("target_ref") or record.get("target_ref") or {}
            if not isinstance(target, dict):
                continue
            if (
                target.get("object_type") not in (None, "wiki")
                or target.get("object_id") not in (None, object_id)
            ):
                continue
            # F004：internal 必须已确认 internal 发布告警
            if effective_confidentiality == "internal" and not (
                confirmation.get("warning_code")
                and confirmation.get("warning_text_sha256")
            ):
                continue
            rec_content = confirmation.get("content_sha256") or confirmation.get(
                "wiki_content_sha256"
            )
            rec_evidence = confirmation.get("evidence_sha256") or confirmation.get(
                "wiki_evidence_sha256"
            )
            if rec_content == content_sha256 and rec_evidence == evidence_sha256:
                return True
        return False

    def _has_public_confirmation(self, object_id: str) -> bool:
        """public-release-confirmation/v1 事件存在性。

        F011：仅人类 approve 事件有效（F002 阶段 public_release 恒 false，
        F007 派生 true 时同样依赖该判定）。
        """
        release_dir = self.paths.release_confirmations
        if not release_dir.exists():
            return False
        for path in sorted(release_dir.glob("evt_*.json")):
            event = self._read_json_dict(path)
            if event is None:
                continue
            if event.get("decision") != "approve":
                continue
            if event.get("actor_type") != "human":
                continue
            target = event.get("target_ref") or {}
            if not isinstance(target, dict):
                continue
            if target.get("object_type") == "wiki" and target.get("object_id") == object_id:
                return True
        return False

    # ---------------- 报告 ----------------

    def _report(
        self,
        wiki_path: Path,
        *,
        errors: list[dict],
        warnings: list[dict] | None = None,
    ) -> dict:
        return {
            "schema_version": WIKI_SCHEMA_VERSION,
            "validator": "wiki-validator",
            "object_ref": {"vault_id": OWNER_VAULT_ID, "object_type": "wiki",
                           "object_id": None},
            "valid": not errors,
            "errors": errors,
            "warnings": warnings or [],
            "derived": None,
            "hashes": None,
            "validation_report": None,
        }


def main(argv: list[str] | None = None) -> int:
    """wiki validate CLI：对单个 Wiki 文件执行确定性校验并输出报告。"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Deterministic validation of a Wiki canonical file"
    )
    parser.add_argument("wiki", type=Path)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--min-chars", type=int, default=12)
    args = parser.parse_args(argv)
    report = WikiValidator(args.root, quote_min_chars=args.min_chars).validate(
        args.wiki
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["valid"] else 2
