"""LLM 证据审计编排（F003）：确定性先行 → 规则集 → provider → 覆盖义务 → 报告。

对应 §8 / AC-F003-003/007/008/011/014/015/016 与 wiki-claim-validation.md：

- 确定性 validator 必须先于 provider 运行并输出 DeterministicReport；
- 单次调用、不做多次采样聚合；provider 不可用/超时/malformed/覆盖不全
  一律落 ``validation_state: not_run`` + 结构化 reason，**不是** fail；
- 模型引文按 §6.9 逐字二次校验，找不到即判 ``unsupported``（无论模型 verdict）；
- 模型自行声明的 ``not_run`` 被拒绝；操作者主动跳过不写任何审计记录；
- 审计报告 append-only 写入 ``audit/validation/wiki/<id>/``，内容 hash 命名。

本模块只做编排：规则集（ruleset）、provider（provider）、corroboration
（corroboration）各自独立，报告写入复用 common.atomic_write。
"""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

from ..common import atomic_write, canonical_quote, hash_canonical, sha256_text
from ..paths import RepoPaths
from . import corroboration, ruleset
from .corroboration import normalize_observation
from .derived import (
    NOT_RUN_SCHEMA_VERSION,
    SCHEMA_VERSION,
    fail_history,
)
from .provider import ProviderResult
from .resolution import read_snapshot_scope, verify_quote
from .schema import load_json_schema
from .validator import WikiValidator

# 报告 hash 输入中的运行时字段（每次运行必变，不参与内容标识）：
# 同名同内容重跑幂等覆盖，异内容并存（append-only 语义保持）
RUNTIME_REPORT_FIELDS = frozenset(
    {
        "audited_at",
        "call_id",
        "input_hash",
        "provider_duration_ms",
        "provider_meta",
        "fail_history",
    }
)


class AuditBlocked(Exception):
    """审计前置失败（确定性校验/ruleset 缺失）：不写任何审计记录。

    对应 §8.3"操作者主动跳过不写审计报告"——没跑就是没跑，不留"已审"痕迹。
    """

    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.message = message


def load_response_schema() -> dict:
    """加载 wiki-validation/v1 输出契约（跨 adapter 唯一，与 wiki-v1 同源加载）。"""
    return load_json_schema("validation-response-v1.json")


def _snapshot_excerpt(resolution: dict, source_id: str, evidence_id: str, paths) -> str:
    """取 evidence item selector 限定的 snapshot 片段（供 LLM 审计上下文）。

    复用 resolution.read_snapshot_scope（钳制/边界规则单份实现）；缺失时
    返回空串，由调用方决定是否阻断（fail-closed）。
    """
    source = resolution.get("sources", {}).get(source_id)
    if not source:
        return ""
    item = source["evidence_items"].get(evidence_id)
    if not item:
        return ""
    scope, _ = read_snapshot_scope(item, paths)
    return scope or ""


def build_validation_request(
    vreport: dict, ruleset_data: dict, paths
) -> dict:
    """构造 ValidationRequest：claim/target/quote 上下文 + ruleset + provenance。

    LLM 只能接收已通过确定性检查的 target 上下文（TD Validator 契约），
    不能新增 target 或放宽 quote 规则。
    """
    metadata = vreport["metadata"]
    resolution = vreport["resolution"]
    claims = []
    for claim in metadata.get("evidence") or []:
        targets = []
        for target in claim.get("targets") or []:
            source_id = target.get("source_id")
            evidence_id = target.get("evidence_id")
            source = resolution.get("sources", {}).get(source_id)
            source_meta = source.get("metadata", {}) if source else {}
            targets.append(
                {
                    "source_id": source_id,
                    "evidence_id": evidence_id,
                    "quote": _snapshot_excerpt(resolution, source_id, evidence_id, paths),
                    "origin": source_meta.get("origin", "external"),
                    "evidence_status": source_meta.get("evidence_status")
                    or "source-reported",
                    "provenance": (source_meta.get("provenance") or {}),
                    "confidentiality": source_meta.get("confidentiality", "public"),
                }
            )
        claims.append(
            {
                "claim_id": claim.get("claim_id"),
                "claim": claim.get("claim"),
                "support": claim.get("support"),
                "targets": targets,
            }
        )
    return {
        "wiki_id": metadata.get("id"),
        "wiki_content_sha256": vreport["hashes"]["content_sha256"],
        "wiki_evidence_sha256": vreport["hashes"]["evidence_sha256"],
        "ruleset": {
            "rule_refs": ruleset_data["rule_refs"],
            "ruleset_sha256": ruleset_data["ruleset_sha256"],
        },
        "claims": claims,
    }


def check_response_schema(payload: dict, response_schema: dict) -> list[str]:
    """provider 输出做 JSON Schema 校验；错误列表非空即协议不可用。"""
    try:
        from jsonschema import Draft202012Validator
    except ImportError:
        return ["jsonschema unavailable"]
    validator = Draft202012Validator(response_schema)
    return [f"{'.'.join(str(p) for p in e.path)}: {e.message}" for e in validator.iter_errors(payload)]


def model_declared_not_run(payload: dict) -> bool:
    """模型自声明 not_run 必须被拒绝（§8.3：not_run 只能由运行时观测事实产生）。"""
    return payload.get("not_run") not in (None, "", False)


def check_coverage(payload: dict, request: dict) -> list[str]:
    """覆盖义务校验（AC-F003-014）：全 claim × 全 target、逐条回引规则、advisory 不计覆盖。

    返回错误列表；任一错误 → 整次审计无效（incomplete_coverage，不保存部分结论）。
    """
    errors: list[str] = []
    request_claims = {c["claim_id"] for c in request["claims"]}
    payload_claims = {c["claim_id"] for c in payload.get("claims", [])}
    if payload_claims != request_claims:
        missing = sorted(request_claims - payload_claims)
        extra = sorted(payload_claims - request_claims)
        errors.append(
            f"claim 覆盖不全: 缺 {missing} 多 {extra}"
        )
        return errors
    spec_ids = {ref["spec_id"] for ref in request["ruleset"]["rule_refs"]}
    for claim in payload.get("claims", []):
        claim_id = claim["claim_id"]
        request_targets = {
            (t["source_id"], t["evidence_id"])
            for c in request["claims"]
            if c["claim_id"] == claim_id
            for t in c["targets"]
        }
        payload_targets = {
            (t["source_id"], t["evidence_id"]) for t in claim.get("targets", [])
        }
        if payload_targets != request_targets:
            errors.append(
                f"claim {claim_id} target 覆盖不全: "
                f"缺 {sorted(request_targets - payload_targets)} "
                f"多 {sorted(payload_targets - request_targets)}"
            )
        quote_ids = {
            q.get("evidence_id") for q in claim.get("supporting_quotes", [])
        }
        if quote_ids != {e for _, e in payload_targets}:
            errors.append(
                f"claim {claim_id} supporting_quotes 未覆盖全部 target"
            )
        refs = claim.get("applied_rule_refs") or []
        if not refs:
            errors.append(f"claim {claim_id} 缺少 applied_rule_refs（逐条回引义务）")
        elif not set(refs) <= spec_ids:
            errors.append(
                f"claim {claim_id} applied_rule_refs 引用未知规则: "
                f"{sorted(set(refs) - spec_ids)}"
            )
        offsets = claim.get("rationale_offsets") or []
        if not offsets:
            errors.append(f"claim {claim_id} rationale 无引用区间（举证义务）")
        else:
            # ⑯ 逐条校验：类型、0<=start<=end、指向本 claim 的 target
            for o in offsets:
                if not isinstance(o, dict):
                    errors.append(f"claim {claim_id} rationale 区间非对象: {o!r}")
                    continue
                start, end = o.get("start"), o.get("end")
                if not (
                    isinstance(start, int)
                    and isinstance(end, int)
                    and 0 <= start <= end
                ):
                    errors.append(f"claim {claim_id} rationale 区间非法: {o!r}")
                    continue
                if (o.get("source_id"), o.get("evidence_id")) not in payload_targets:
                    errors.append(
                        f"claim {claim_id} rationale 区间未指向任何 target: "
                        f"{(o.get('source_id'), o.get('evidence_id'))}"
                    )
    return errors


def verify_model_quotes(payload: dict, resolution: dict, paths, quote_min_chars: int) -> list[dict]:
    """模型引文逐字二次校验（§8.2）：每个 target 一条引文，须在 selector 范围内命中。

    找不到即该 claim 判 unsupported（无论模型 verdict）；校验错误记录
    evidence/snapshot/selector/LCS 诊断（§6.9 失败可诊断要求）。
    """
    errors: list[dict] = []
    for claim in payload.get("claims", []):
        for quote in claim.get("supporting_quotes", []):
            evidence_id = quote.get("evidence_id")
            exact = quote.get("exact", "")
            target = next(
                (
                    t
                    for t in claim.get("targets", [])
                    if t.get("evidence_id") == evidence_id
                ),
                None,
            )
            if target is None:
                errors.append(
                    {
                        "code": "quote_target_mismatch",
                        "claim_id": claim.get("claim_id"),
                        "evidence_id": evidence_id,
                    }
                )
                continue
            source_id = target.get("source_id")
            source = resolution.get("sources", {}).get(source_id)
            item = (
                source["evidence_items"].get(evidence_id)
                if source is not None
                else None
            )
            if item is None:
                errors.append(
                    {
                        "code": "quote_evidence_missing",
                        "claim_id": claim.get("claim_id"),
                        "source_id": source_id,
                        "evidence_id": evidence_id,
                    }
                )
                continue
            error = verify_quote(item, exact, paths, quote_min_chars)
            if error:
                error = {**error, "claim_id": claim.get("claim_id")}
                errors.append(error)
    return errors


def verify_independence(payload: dict, request: dict) -> tuple[dict, list[dict]]:
    """独立性举证校验（AC-F003-005）：basis 必须回引 provenance 或原文区间。

    返回 (per-claim independence group 映射, warnings)。无法举证 → 该 target
    按 independence_unknown（单一 source）处理，不参与 corroborated 派生；
    禁止以域名/URL 相似度、发布时间先后作为独立性依据。
    """
    groups: dict[tuple[str, str], str] = {}
    warnings: list[dict] = []
    allowed_fields = {"publisher", "derived_from", "independence_group"}
    for claim in payload.get("claims", []):
        claim_id = claim["claim_id"]
        independence = claim.get("independence")
        target_ids = {
            (t["source_id"], t["evidence_id"]) for t in claim.get("targets", [])
        }
        if not isinstance(independence, dict) or not independence.get("group_id"):
            for key in target_ids:
                groups[key] = "independence_unknown"
            warnings.append(
                {
                    "code": "independence_unknown",
                    "claim_id": claim_id,
                    "reason": "独立性判定缺失，按单一 source 处理（AC-F003-005）",
                }
            )
            continue
        basis = independence.get("basis") or []
        if not basis:
            for key in target_ids:
                groups[key] = "independence_unknown"
            warnings.append(
                {
                    "code": "independence_unknown",
                    "claim_id": claim_id,
                    "reason": "独立性判定无 basis 举证，按单一 source 处理",
                }
            )
            continue
        group_id = independence["group_id"]
        for entry in basis:
            key = (entry.get("source_id"), entry.get("evidence_id"))
            if key not in target_ids:
                warnings.append(
                    {
                        "code": "independence_basis_mismatch",
                        "claim_id": claim_id,
                        "reason": f"basis 引用了非 target: {key}",
                    }
                )
                continue
            field = entry.get("provenance_field")
            offset = entry.get("offset")
            if field not in allowed_fields and not (
                isinstance(offset, dict)
                and isinstance(offset.get("start"), int)
                and isinstance(offset.get("end"), int)
            ):
                warnings.append(
                    {
                        "code": "independence_unknown",
                        "claim_id": claim_id,
                        "source_id": entry.get("source_id"),
                        "reason": (
                            "basis 既未回引 provenance 字段也无原文区间，"
                            "按单一 source 处理"
                        ),
                    }
                )
                continue
            groups[key] = group_id
    return groups, warnings


def extract_observations(payload: dict) -> dict:
    """从 provider 输出提取 per-target observation（corroboration 输入）。

    observation 已下沉到 supporting_quotes 层（schema），每条与 evidence_id
    一一对应；按 (source_id, evidence_id) 汇总供成对比较——同一 claim 的
    多个 target 若模型给出不同 observation 可正确检出冲突（⑫ P1 修复）。
    """
    observations: dict = {}
    for claim in payload.get("claims", []):
        per_target = claim.get("observations") or []
        for obs_entry in per_target:
            evidence_id = obs_entry.get("evidence_id")
            if evidence_id is None:
                continue
            observations[evidence_id] = normalize_observation(obs_entry)
    return observations


def _policy_advisory_participates(root: Path) -> bool:
    """policy.yaml 的 validation.ruleset.advisory_participates_in_verdict。

    默认 False（advisory 只作参考展示、不参与 pass/fail，§8.2）；读取失败
    按默认处理，不抛（配置问题不阻断审计）。
    """
    try:
        import yaml

        policy_path = root / "config" / "policy.yaml"
        if not policy_path.exists():
            return False
        data = yaml.safe_load(policy_path.read_text(encoding="utf-8"))
        return bool(
            (data or {})
            .get("validation", {})
            .get("ruleset", {})
            .get("advisory_participates_in_verdict", False)
        )
    except Exception:
        return False


def compute_final_verdict(
    payload: dict,
    quote_errors: list[dict],
    coverage_errors: list[str],
    *,
    advisory_participates: bool = False,
) -> str:
    """顶层 verdict：覆盖义务满足 + 非 advisory 全部 supported + 引文逐字 → pass。

    - 引文校验失败的 claim 强制 unsupported（§8.2），并**回写** payload claims
      （⑬：报告/derived 读到的是改写后的 verdict，避免"证据支持但审计失败"
      的矛盾展示）；
    - advisory claim 不参与 pass/fail 判定（policy 默认 false，⑮）。
    """
    failed_claims = {e.get("claim_id") for e in quote_errors}
    verdicts = []
    for claim in payload.get("claims", []):
        if claim.get("advisory") is True and not advisory_participates:
            continue  # advisory 只作参考展示（覆盖义务仍要求其存在）
        if claim["claim_id"] in failed_claims:
            claim["verdict"] = "unsupported"  # 回写：报告/派生读改写后 verdict
            verdicts.append("unsupported")
            continue
        verdicts.append(claim["verdict"])
    if coverage_errors:
        return "fail"  # 覆盖义务由调用方转 not_run，此处不会到达
    if all(v == "supported" for v in verdicts):
        return "pass"
    if any(v in {"contradicted", "unsupported"} for v in verdicts):
        return "fail"
    return "fail"


def run_audit(
    root: Path,
    wiki_path: Path,
    provider,
    *,
    rule_ids: list[str] | None = None,
    quote_min_chars: int = 12,
) -> dict:
    """执行一次完整 LLM 证据审计；返回结构化结果（含写入的报告/not_run 记录路径）。

    流程：确定性校验 → 规则集 → ValidationRequest → provider 单次调用 →
    schema 校验 → 覆盖义务 → 模型引文二次校验 → independence/corroboration →
    append-only 报告（或 not_run 记录）。
    """
    paths = RepoPaths(root)
    validator = WikiValidator(root, quote_min_chars=quote_min_chars)
    vreport = validator.validate(wiki_path)
    if not vreport["valid"]:
        raise AuditBlocked(
            "deterministic_blocked",
            f"确定性校验未通过，不调用 provider: "
            f"{[e['code'] for e in vreport['errors']]}",
        )
    vreport["metadata"], _ = _read_metadata(wiki_path)
    ruleset_data = ruleset.load_ruleset(root, rule_ids)
    if ruleset_data["errors"]:
        raise AuditBlocked(
            "ruleset_unavailable",
            f"规则集组装失败: {ruleset_data['errors']}",
        )
    request = build_validation_request(vreport, ruleset_data, paths)
    response_schema = load_response_schema()

    result = provider.audit(request, response_schema)
    object_id = str(vreport["metadata"].get("id", ""))
    hashes = vreport["hashes"]

    if result.error_code is not None:
        record = _write_not_run(
            object_id, result.error_code, hashes, paths,
            provider_identity=result.provider_identity,
            message=result.error_message,
        )
        return _audit_outcome(provider, result, record, vreport)

    payload = result.payload
    schema_errors = check_response_schema(payload, response_schema)
    # AC-F003-011：provider 输出必须绑定被审计的 wiki（claim/target/quote 二次校验）
    if payload.get("wiki_id") != request.get("wiki_id"):
        schema_errors.append(
            f"wiki_id 不匹配: 响应 {payload.get('wiki_id')!r} != 请求 {request.get('wiki_id')!r}"
        )
    if schema_errors or model_declared_not_run(payload):
        reason = "malformed_output"
        record = _write_not_run(
            object_id, reason, hashes, paths,
            provider_identity=result.provider_identity,
            message=(
                f"输出违反 wiki-validation/v1: {schema_errors[:3]}"
                if schema_errors
                else "模型自行声明 not_run（被拒绝）"
            ),
        )
        return _audit_outcome(provider, result, record, vreport)

    coverage_errors = check_coverage(payload, request)
    if coverage_errors:
        record = _write_not_run(
            object_id, "incomplete_coverage", hashes, paths,
            provider_identity=result.provider_identity,
            message="; ".join(coverage_errors),
        )
        return _audit_outcome(provider, result, record, vreport)

    quote_errors = verify_model_quotes(
        payload, vreport["resolution"], paths, quote_min_chars
    )
    groups, independence_warnings = verify_independence(payload, request)
    observations = extract_observations(payload)
    corroboration_result = corroboration.compute_corroboration(
        vreport["resolution"].get("resolved_targets", []),
        vreport["resolution"].get("sources", {}),
        observations,
        model_groups=groups,  # ⑭ 模型经 provenance 举证的独立性覆盖
    )
    verdict = compute_final_verdict(
        payload,
        quote_errors,
        coverage_errors,
        advisory_participates=_policy_advisory_participates(root),
    )

    report = _build_report(
        object_id, verdict, vreport, result, ruleset_data, payload,
        quote_errors, corroboration_result, independence_warnings, paths,
    )
    record = _write_report(report, paths)
    return _audit_outcome(provider, result, record, vreport)


def _read_metadata(wiki_path: Path) -> tuple[dict, str]:
    """读取 wiki front matter（metadata, body）；失败抛 AuditBlocked。"""
    from ..front_matter import FrontMatter

    try:
        return FrontMatter.parse(wiki_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, ValueError, TypeError) as exc:
        raise AuditBlocked("wiki_unreadable", str(exc)) from exc


def _build_report(
    object_id: str,
    verdict: str,
    vreport: dict,
    result: ProviderResult,
    ruleset_data: dict,
    payload: dict,
    quote_errors: list[dict],
    corroboration_result: dict,
    independence_warnings: list[dict],
    paths,
) -> dict:
    """构造 append-only 验证报告（§8.4，只记录运行时安全摘要）。"""
    resolution = vreport["resolution"]
    bindings = []
    for target in resolution.get("resolved_targets", []):
        source_id = target["source_id"]
        evidence_id = target["evidence_id"]
        source = resolution.get("sources", {}).get(source_id)
        item = (
            source["evidence_items"].get(evidence_id)
            if source is not None
            else None
        )
        bindings.append(
            {
                "resolved_object_ref": target.get("resolved_object_ref", {}),
                "source_id": source_id,
                "evidence_id": evidence_id,
                "snapshot_sha256": target.get("snapshot_sha256"),
                "selector_sha256": (
                    item.get("selector_sha256") if item is not None else None
                ),
                "quote_sha256": (
                    sha256_text(canonical_quote(target.get("supporting_quote", "")))
                    if target.get("supporting_quote")
                    else None
                ),
            }
        )
    history = fail_history(object_id, paths)
    return {
        "schema_version": SCHEMA_VERSION,
        "wiki_id": object_id,
        "validator_version": "wiki-validator",
        "provider_identity": result.provider_identity,
        "call_id": result.call_id,
        "input_hash": result.input_hash,
        "provider_duration_ms": result.duration_ms,
        "provider_meta": result.meta,
        "ruleset_sha256": ruleset_data["ruleset_sha256"],
        "rule_refs": ruleset_data["rule_refs"],
        "audited_at": time.time(),
        "wiki_content_sha256": vreport["hashes"]["content_sha256"],
        "wiki_evidence_sha256": vreport["hashes"]["evidence_sha256"],
        "evidence_bindings": bindings,
        "claims": payload.get("claims", []),
        "unmapped_claims": payload.get("unmapped_claims", []),
        "contradictions": payload.get("contradictions", []),
        "missing_evidence": payload.get("missing_evidence", []),
        "quote_errors": quote_errors,
        "verdict": verdict,
        "corroboration": corroboration_result,
        "independence_warnings": independence_warnings,
        "fail_history": history,
    }


def _write_report(report: dict, paths) -> dict:
    """append-only 写报告：稳定内容核 hash 命名（⑰，运行时字段不参与）。

    同内容重跑（verdict/claims/quote_errors/corroboration 相同）→ 同名文件
    幂等覆盖，目录不随重跑无界增长；异内容并存（append-only 语义保持：
    不删除历史，只覆盖同内容副本）。文件名 ≠ 全文 hash，是内容标识。
    """
    stable = {
        key: value
        for key, value in report.items()
        if key not in RUNTIME_REPORT_FIELDS and not key.startswith("_")
    }
    report_sha256 = hash_canonical(stable)
    target = paths.audit_validation("wiki", report["wiki_id"]) / f"{report_sha256.removeprefix('sha256:')}.json"
    atomic_write(target, json.dumps(report, ensure_ascii=False, indent=2).encode("utf-8"))
    return {**report, "_path": str(target)}


def _write_not_run(
    object_id: str,
    reason: str,
    hashes: dict,
    paths,
    *,
    provider_identity: str,
    message: str | None,
) -> dict:
    """写 not_run 记录：只含运行时观测事实，不含 verdict/结论（§8.3/8.4）。

    记录仍是 append-only（内容 hash 命名），供页面显示"未做语义审计"原因；
    但绝不含 claim 判定，不能被误读为审计结论。诊断 message 不落盘
    （§8.4：报告只保存 opaque provider identity 与 not_run_reason，不保存
    endpoint/密钥/完整请求响应），由 CLI 直接输出。
    """
    record = {
        "schema_version": NOT_RUN_SCHEMA_VERSION,
        "wiki_id": object_id,
        "provider_identity": provider_identity,
        "not_run_reason": reason,
        "audited_at": time.time(),
        "wiki_content_sha256": hashes["content_sha256"],
        "wiki_evidence_sha256": hashes["evidence_sha256"],
    }
    # ⑰：not_run 记录的 hash 同样排除运行时字段（同原因重跑幂等覆盖）
    stable = {
        key: value
        for key, value in record.items()
        if key not in RUNTIME_REPORT_FIELDS
    }
    record_sha256 = hash_canonical(stable)
    target = paths.audit_validation("wiki", object_id) / f"{record_sha256.removeprefix('sha256:')}.json"
    atomic_write(target, json.dumps(record, ensure_ascii=False, indent=2).encode("utf-8"))
    record["_path"] = str(target)
    record["_diagnostic"] = message  # 仅 CLI 展示，不落盘
    return record


def _audit_outcome(provider, result: ProviderResult, record: dict, vreport: dict) -> dict:
    """归一审计结果（供 CLI/调用方展示）。

    诊断信息（_diagnostic）只进 outcome 由 CLI 打印，不写入报告文件
    （§8.4：报告只保存 opaque provider identity 与 not_run_reason）。
    """
    return {
        "wiki_id": record.get("wiki_id"),
        "provider_identity": result.provider_identity,
        "call_id": result.call_id,
        "input_hash": result.input_hash,
        "schema_version": record.get("schema_version"),
        "validation_state": (
            "not_run" if record.get("schema_version") == NOT_RUN_SCHEMA_VERSION
            else record.get("verdict", "not_run")
        ),
        "not_run_reason": record.get("not_run_reason"),
        "verdict": record.get("verdict"),
        "report_path": record.get("_path"),
        "diagnostic": record.get("_diagnostic"),  # ⑪：CLI 可见，不落盘
        "wiki_content_sha256": record.get("wiki_content_sha256"),
        "wiki_evidence_sha256": record.get("wiki_evidence_sha256"),
        "corroboration": record.get("corroboration"),
        "quote_errors": record.get("quote_errors", []),
        "fail_history": record.get("fail_history"),
        "deterministic_valid": vreport["valid"],
    }


def main(argv: list[str] | None = None) -> int:
    """audit CLI：对单个 Wiki 执行 LLM 证据审计并写入报告。"""
    parser = argparse.ArgumentParser(
        description="LLM evidence audit of a Wiki canonical file (F003)"
    )
    parser.add_argument("wiki", type=Path)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--min-chars", type=int, default=12)
    parser.add_argument(
        "--provider",
        default=None,
        help="provider 名称：agent-cli（默认，ducc/ducx）/ openai",
    )
    parser.add_argument(
        "--cli",
        default=None,
        help="agent CLI 路径（默认环境变量 MYKNOWLEDGE_LLM_CLI 或 ducc）",
    )
    args = parser.parse_args(argv)
    from .provider import make_provider

    provider = make_provider(args.provider, cli=args.cli)
    try:
        outcome = run_audit(
            args.root, args.wiki, provider, quote_min_chars=args.min_chars
        )
    except AuditBlocked as exc:
        print(json.dumps({"state": "blocked", "error_code": exc.code,
                          "message": exc.message}, ensure_ascii=False, indent=2))
        return 2
    print(json.dumps(outcome, ensure_ascii=False, indent=2))
    return 0
