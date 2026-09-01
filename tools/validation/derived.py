"""Wiki 派生字段计算（§6.8）：evidence_state/strength/availability/publishable。

纯函数式：输入 metadata/resolution/report/hashes，输出派生字段 dict。
确认与验证报告读取统一经 ``read_json_dict``（fail-closed 类型契约）。
"""

from __future__ import annotations

import json
from pathlib import Path

from ..common import hash_canonical, sha256_text
from .schema import OWNER_VAULT_ID

BLOCKED_EVIDENCE_STATES = {"missing", "partial", "conflicting", "unresolved", "stale"}

# 审计记录 schema 版本（audit.py 与 derived.py 共用，避免循环导入）
SCHEMA_VERSION = "validation-report/v1"
NOT_RUN_SCHEMA_VERSION = "validation-notrun/v1"


def read_json_dict(path: Path) -> dict | None:
    """读取 JSON 文件；不可读/损坏/非 dict 形状一律返回 None（fail-closed）。

    统一外部输入（validation report / operation / confirmation event）的
    读取与类型契约校验（F006/R001/R002），消费点不再逐处防御。
    """
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        return None
    return value if isinstance(value, dict) else None


def load_validation_report(object_id: str, hashes: dict | None, paths) -> dict | None:
    """读取 owner Vault 内最近一次 LLM 验证记录（audit/validation/wiki/<id>/）。

    F003（hash 绑定）：报告必须绑定当前 (content, evidence) hash，否则视为
    过期无效（旧报告不得驱动 validation_state/verified）。F002 只消费
    verdict/claim_verdicts/corroborated；报告缺失或非法视为未运行。

    优先级：绑定当前 hash 的 ``validation-report/v1``（verdict 类）优先
    ——pass/fail 是已验证的客观证据；``validation-notrun/v1`` 是环境事实，
    只在没有 verdict 报告时用于展示 not_run_reason，不覆盖 pass/fail。
    多份 verdict 报告分歧时取 **fail**（更保守一侧），见函数内说明。
    """
    base = paths.audit_validation("wiki", object_id)
    if not base.exists():
        return None
    try:
        candidates = sorted(base.glob("*.json"))
    except OSError:
        return None
    verdict_records: list[tuple[float, dict, Path]] = []
    notrun_latest: dict | None = None
    notrun_mtime = 0.0
    for path in candidates:
        try:
            mtime = path.stat().st_mtime
        except OSError:
            continue
        record = read_json_dict(path)
        if record is None:
            continue
        version = record.get("schema_version")
        if version not in (SCHEMA_VERSION, NOT_RUN_SCHEMA_VERSION):
            continue
        if hashes is not None:
            rec_content = record.get("wiki_content_sha256") or record.get(
                "content_sha256"
            )
            rec_evidence = record.get("wiki_evidence_sha256") or record.get(
                "evidence_sha256"
            )
            if (
                rec_content != hashes["content_sha256"]
                or rec_evidence != hashes["evidence_sha256"]
            ):
                continue  # 绑定的是旧内容，视为过期
        if version == SCHEMA_VERSION:
            verdict_records.append((mtime, record, path))
        elif version == NOT_RUN_SCHEMA_VERSION and mtime > notrun_mtime:
            notrun_latest, notrun_mtime = record, mtime
    if verdict_records:
        # fail 优先（更保守一侧）：绑定同一 hash 的报告出现分歧时取 fail。
        # 实测（2026-09-01）：两个 provider 对同一页给出 fail/pass 相反结论，
        # 按 mtime 取最新等于"最后跑的模型说了算"——反复换 provider 重跑直到
        # 出现一次 pass 就能过门禁（审计洗牌）。要过门禁只能改内容，不能换模型。
        # 唯一例外是 owner 显式签过复议记录的 fail 报告（VAL-003），它带
        # actor_id/理由/逐条 claim 且绑定当前 hash——误判可被推翻，但推翻本身留痕。
        from .override import overridden_report_ids

        overridden = overridden_report_ids(object_id, hashes, paths)
        usable = [
            item
            for item in verdict_records
            if f"sha256:{item[2].stem}" not in overridden
        ]
        if not usable:
            # 全部 verdict 报告都被复议掉：没有可用的模型判定，回落"未运行"
            # （仍是 fail-closed：not_run 同样不满足发布门禁），而不是返回一份
            # owner 已声明误判的报告。
            return notrun_latest
        failed = [item for item in usable if item[1].get("verdict") == "fail"]
        return max(failed or usable, key=lambda item: item[0])[1]
    return notrun_latest


def evidence_sha256(
    metadata: dict, resolution: dict, owner_vault_id: str = OWNER_VAULT_ID
) -> str:
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
                "vault_id": owner_vault_id,
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
                "vault_id": owner_vault_id,  # F015：owner 归属入证据摘要（§hash_inputs）
                "claim_id": claim.get("claim_id"),
                "claim": claim.get("claim"),
                "support": claim.get("support"),
                "targets": targets,
                "supporting_quotes": claim.get("supporting_quotes", []),
            }
        )
    return hash_canonical(resolved)


def fail_history(object_id: str, paths) -> dict:
    """扫描 append-only 审计报告，统计历史 fail 次数与最近一次 fail 的规则条目。

    AC-F003-016：历史 fail 可见（不锁定、可重跑）；人工审计界面必须展示。
    报告文件名是内容标识（与时间无关），"最近一次"按 st_mtime 取（㉒），
    不按文件名排序。报告缺失/目录不存在返回零值，不抛异常。
    """
    base = paths.audit_validation("wiki", object_id)
    fail_count = 0
    last_fail_rule_refs: list = []
    last_mtime = 0.0
    if base.exists():
        for path in sorted(base.glob("*.json")):
            try:
                mtime = path.stat().st_mtime
            except OSError:
                continue
            record = read_json_dict(path)
            if record is None:
                continue
            if record.get("schema_version") != SCHEMA_VERSION:
                continue
            if record.get("verdict") != "fail":
                continue
            fail_count += 1
            if mtime > last_mtime:
                last_mtime = mtime
                last_fail_rule_refs = sorted(
                    {
                        ref
                        for claim in record.get("claims", [])
                        if isinstance(claim, dict)
                        for ref in claim.get("applied_rule_refs", [])
                    }
                )
    return {"fail_count": fail_count, "last_fail_rule_refs": last_fail_rule_refs}


def _latest_evidence_state(object_id: str, paths) -> str | None:
    """取最近一次审计报告中的 corroboration evidence_state（不要求 hash 绑定）。

    AC-F003-010：availability unavailable 时保留最近可计算的 evidence_state，
    首次计算才为 unresolved。
    """
    base = paths.audit_validation("wiki", object_id)
    if not base.exists():
        return None
    latest: dict | None = None
    latest_mtime = 0.0
    for path in sorted(base.glob("*.json")):
        try:
            mtime = path.stat().st_mtime
        except OSError:
            continue
        record = read_json_dict(path)
        if record is None or record.get("schema_version") != SCHEMA_VERSION:
            continue
        if mtime > latest_mtime:
            latest, latest_mtime = record, mtime
    if latest is None:
        return None
    corroboration = latest.get("corroboration")
    if isinstance(corroboration, dict):
        state = corroboration.get("evidence_state")
        if isinstance(state, str):
            return state
    return None


def _ruleset_stale(report: dict, paths) -> bool:
    """报告 ruleset_sha256 与当前规则集不一致 → stale_ruleset（AC-F003-015）。

    规则措辞/章节重排改变 extract_sha256 → ruleset_sha256 变化 → 标记
    stale_ruleset（可见、不阻断、可重跑）；人工确认只绑定 (content, evidence)
    hash，**仍然有效**。当前规则集无法计算（规范文档缺失）时保守按 stale。
    """
    from .ruleset import load_ruleset

    rec_ruleset = report.get("ruleset_sha256")
    if not isinstance(rec_ruleset, str):
        return True  # 报告缺 ruleset 绑定：无法确认一致，保守 stale
    current = load_ruleset(paths.root)
    if current["errors"]:
        return True
    return current["ruleset_sha256"] != rec_ruleset


def compute_derived(
    metadata: dict,
    resolution: dict,
    report: dict | None,
    hashes: dict,
    paths,
    owner_vault_id: str = OWNER_VAULT_ID,
) -> dict:
    """按 §6.8 计算全部派生字段（不入 canonical、不写回文件）。

    正文不作为入参：派生只依赖 metadata/resolution/report 与调用方算好的
    hashes（content_sha256 已由 validator 用 canonical_body 计算）。
    """
    status = metadata.get("status")
    kind = metadata.get("kind")
    scope = metadata.get("publication_scope")
    confidentiality = metadata.get("confidentiality", "public")

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

    # validation_state（§6.8：只表达 LLM 规范审计运行结果）
    # F003：unavailable 优先（AC-F003-010）；stale_ruleset 由报告 ruleset_sha256
    # 与当前规则集不一致产生（AC-F003-015，可见、不阻断）；not_run 记录只提供
    # not_run_reason，不覆盖 pass/fail 报告。
    if availability == "unavailable":
        validation_state = "unavailable"
    elif report and report.get("verdict") == "pass":
        validation_state = "stale_ruleset" if _ruleset_stale(report, paths) else "pass"
    elif report and report.get("verdict") == "fail":
        validation_state = "fail"
    else:
        validation_state = "not_run"

    # evidence_state（§6.8 优先级表，阻断级命中第一条）
    evidence_state = compute_evidence_state(
        metadata, resolution, report, availability, paths
    )

    # effective_confidentiality = max(自身, 全部上游 source)
    levels = {"public": 0, "internal": 1}
    effective = levels.get(confidentiality, 0)
    for source in resolution.get("sources", {}).values():
        if source is not None:
            effective = max(
                effective,
                levels.get(source["metadata"].get("confidentiality", "public"), 0),
            )
    effective_confidentiality = "public" if effective == 0 else "internal"

    # strength（§6.8 映射表，按顺序命中第一条）
    strength = compute_strength(
        kind, evidence_state, resolution, report, validation_state
    )

    # publishable 派生（审计确认检查）
    content_sha256 = hashes["content_sha256"]
    evidence_sha256_value = hashes["evidence_sha256"]
    object_id = str(metadata.get("id", ""))
    has_audit = has_private_confirmation(
        object_id,
        content_sha256,
        evidence_sha256_value,
        effective_confidentiality,
        paths,
    )
    evidence_ok = evidence_state not in BLOCKED_EVIDENCE_STATES
    validation_ok = validation_state in {"not_run", "pass", "stale_ruleset"}
    base_publishable = (
        status == "published"
        and evidence_ok
        and validation_ok
        and has_audit
        and availability == "available"
    )
    private_publishable = base_publishable and scope == "private"
    # public 门禁分两段：前段（内容、证据、审计确认、保密等级、scope）与后段
    # （public 发布确认事件）。分开是必需的——`release input` 要先把待审材料算
    # 出来给人看，人才可能签发布确认；如果把发布确认也算进"能不能算材料"的前
    # 提，链路自锁：没有确认算不出材料，算不出材料签不了确认（实测 2026-09-01，
    # aar 之所以有确认事件是因为那份文件是手工编造的）。
    public_release_ready = (
        base_publishable and scope == "public" and effective_confidentiality == "public"
    )
    # F011：public confirmation 须为人类 approve 事件（F007 阶段仍恒 false）
    public_publishable = public_release_ready and has_public_confirmation(
        object_id, paths
    )

    # publication_warning（§6.8）
    publication_warning = (
        "internal"
        if effective_confidentiality == "internal" and private_publishable
        else "none"
    )

    return {
        "vault_id": owner_vault_id,
        "evidence_state": evidence_state,
        "validation_state": validation_state,
        "not_run_reason": (
            report.get("not_run_reason")
            if report is not None and validation_state == "not_run"
            else None
        ),
        "availability": availability,
        "availability_reason": availability_reason,
        "effective_confidentiality": effective_confidentiality,
        "strength": strength,
        "private_publishable": private_publishable,
        "public_release_ready": public_release_ready,
        "public_publishable": public_publishable,
        "public_release": False,  # F002 阶段恒 false；真实派生由 F007 发布 authority 完成
        "publication_warning": publication_warning,
        "fail_history": fail_history(object_id, paths),
    }


def _single_source_only(corroboration: dict, report: dict) -> bool:
    """corroboration 的 unresolved 是否只因「单一来源」而非证据缺陷。

    判据全部取自报告的确定性字段：无冲突对、无同组冲突、且全部独立性告警都是
    ``independence_unknown``（"独立性判定无 basis 举证，按单一 source 处理"）。
    出现任何其他告警码或冲突时不适用，仍按 unresolved 阻断。
    """
    if corroboration.get("conflict_pairs") or corroboration.get("same_group_conflicts"):
        return False
    warnings = report.get("independence_warnings") or []
    if not isinstance(warnings, list) or not warnings:
        return False
    return all(
        isinstance(w, dict) and w.get("code") == "independence_unknown"
        for w in warnings
    )


def compute_evidence_state(
    metadata: dict,
    resolution: dict,
    report: dict | None,
    availability: str,
    paths,
) -> str:
    """evidence_state：按 §6.8 阻断优先级命中第一条。

    conflicting/partial/corroborated 由 LLM 验证报告（F003）驱动——确定性层
    不自行做语义冲突与独立性判定；报告缺失时按确定性可算的结果取值。
    """
    evidence = metadata.get("evidence") or []
    if not evidence or resolution.get("total_targets") == 0:
        return "missing"
    if availability == "unavailable":
        # AC-F003-010：unavailable 保留最近可计算的 evidence_state，
        # 首次计算才为 unresolved；不伪装成 missing
        object_id = str(metadata.get("id", ""))
        return _latest_evidence_state(object_id, paths) or "unresolved"
    # snapshot 漂移：evidence item 的 snapshot_sha256 与归档实际内容不符
    for target in resolution.get("resolved_targets", []):
        snapshot_path = paths.snapshot_file(target["snapshot_sha256"])
        if not snapshot_path.exists():
            return "unresolved"
        try:
            actual = sha256_text(snapshot_path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError):
            return "unresolved"
        if actual != target["snapshot_sha256"]:
            return "stale"
    if report:
        # F003：per-claim verdict 优先（单 target 时 corroboration 聚合无信号，
        # contradicted/unsupported 必须反映到 evidence_state）；
        # 然后 corroboration.evidence_state（多 source 一致性聚合）；
        # 旧格式兼容 claim_verdicts。
        claim_verdicts = [
            c.get("verdict")
            for c in report.get("claims", [])
            if isinstance(c, dict) and isinstance(c.get("verdict"), str)
        ]
        if "contradicted" in claim_verdicts:
            return "conflicting"
        if any(
            v in {"partially_supported", "unsupported", "unmapped"}
            for v in claim_verdicts
        ):
            return "partial"
        corroboration = report.get("corroboration")
        if isinstance(corroboration, dict):
            state = corroboration.get("evidence_state")
            if state == "unresolved" and _single_source_only(corroboration, report):
                # 「只有一个来源」不等于「证据坏了」：unresolved 的本意是 target
                # 无法定位或 snapshot 漂移，而这里全部 target 定位良好、引文逐字
                # 匹配，缺的只是第二个独立来源。共用一个取值会让任何单一来源的
                # 页面（读书笔记天然如此）永远不可发布。强度层用 attested 表达
                # 「已核实但未交叉验证」（owner 2026-09-01 决策）。
                return "supported"
            if state in {"conflicting", "corroborated", "unresolved"}:
                return state
            if state == "supported":
                return "supported"
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
            v in {"partially_supported", "unsupported", "unmapped"} for v in verdicts
        ):
            return "partial"
        if report.get("corroborated") is True:
            return "corroborated"
    # 全部 target 可定位且引文校验通过；独立性未由报告证明时保守按单一 source
    return "supported"


def compute_strength(
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
    if resolution.get("common_knowledge_only") and evidence_state in {
        "supported",
        "corroborated",
    }:
        return "attested"
    if evidence_state == "corroborated":
        return "corroborated"
    if validation_state == "pass" and report:
        # owner 2026-09-01 决策：`verified` 保留给多来源互证；单一来源的审计通过
        # 落 `attested`（已核实的转述，未交叉验证）。读者据此区分"一本书说的"
        # 与"多个独立来源都说的"。
        sources = {
            target.get("source_id")
            for target in resolution.get("resolved_targets") or []
            if target.get("source_id")
        }
        return "attested" if len(sources) <= 1 else "verified"
    return None  # 其他：不可发布，等待补证/人工决策


def has_private_confirmation(
    object_id: str,
    content_sha256: str,
    evidence_sha256: str,
    effective_confidentiality: str,
    paths,
) -> bool:
    """查找绑定当前 (content, evidence) hash 的 operation-confirmation/v1 审计确认。

    F004：effective_confidentiality 为 internal 时，确认必须携带
    warning_code/warning_text_sha256（未确认告警不得发布，§6.8）；
    F010：确认必须绑定目标对象（target_ref 匹配），内容相同的两个 Wiki
    不得复用彼此的审计确认。
    """
    audit_dir = paths.audit_operations
    if not audit_dir.exists():
        return False
    for path in sorted(audit_dir.glob("op_*.json")):
        record = read_json_dict(path)
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
        if target.get("object_type") not in (None, "wiki") or target.get(
            "object_id"
        ) not in (None, object_id):
            continue
        # F004：internal 必须已确认 internal 发布告警
        if effective_confidentiality == "internal" and not (
            confirmation.get("warning_code") and confirmation.get("warning_text_sha256")
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


def has_public_confirmation(object_id: str, paths) -> bool:
    """public-release-confirmation/v1 事件存在性。

    F011：仅人类 approve 事件有效（F002 阶段 public_release 恒 false，
    F007 派生 true 时同样依赖该判定）。
    """
    release_dir = paths.release_confirmations
    if not release_dir.exists():
        return False
    # 与 PublicProjectionGenerator._confirmation / write_event 一致：safe_id 允许
    # 连字符（evt-xxx），不能只匹配 evt_* 下划线前缀（曾导致发布确认永不生效）
    for path in sorted(release_dir.glob("*.json"), reverse=True):
        event = read_json_dict(path)
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
