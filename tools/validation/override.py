"""人工复议：把某一份被判误判的 LLM `fail` 报告排除在派生之外（VAL-003）。

背景（2026-09-01 实测）：同一页内容在三个模型上跑出 fail/pass 相反结论，且同一
模型对同一条 claim 两次判定不一致。`load_validation_report` 因此改为 **fail 优先**
（更保守一侧，防止"换 provider 重跑到 pass"的审计洗牌）。但 fail 优先的代价是
**任何一次模型误判都能永久卡住一页**，而模型判定本身有随机性。

出路不是放宽门禁（多数表决 = 刷票门槛变高而已），而是让人的判断留痕：owner 可以
对某份 fail 报告签一条复议记录，声明"我读过这份 fail，它是误判"。该报告此后不再
参与派生，但复议这件事本身是 append-only 审计记录，绑定报告标识与当前内容 hash——
内容一改，复议自动失效。

约束（全部 fail-closed）：
- 只有 `actor_type: human` 能签；Agent 不得代签（ADR-0010 同一原则）；
- 必须绑定被复议报告的稳定标识与当前 `(content, evidence)` hash；
- 必须逐条列出复议的 claim，且必须覆盖该报告里**全部**非 `supported` 的 claim——
  只复议一条就整份翻案是不允许的；
- `reason` 必填：没有理由的复议等于静默绕过。
"""

from __future__ import annotations

import json
import time
from pathlib import Path

from ..common import atomic_write, hash_canonical, safe_id
from ..paths import RepoPaths
from .derived import read_json_dict

SCHEMA_VERSION = "validation-override/v1"
DECISION = "misjudged"
SUPPORTED_VERDICTS = frozenset({"supported"})


class OverrideBlocked(Exception):
    """复议被拒（结构化错误码，不静默降级）。"""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.message = message


def report_identity(report: dict) -> str:
    """报告的稳定标识（与 `audit._write_report` 的命名口径同源）。"""
    from .audit import RUNTIME_REPORT_FIELDS

    stable = {
        key: value
        for key, value in report.items()
        if key not in RUNTIME_REPORT_FIELDS and not key.startswith("_")
    }
    return hash_canonical(stable)


def overrides_dir(paths: RepoPaths, object_id: str) -> Path:
    """复议记录目录（放子目录：`load_validation_report` 的顶层 glob 不会误读）。"""
    return paths.audit_validation("wiki", object_id) / "overrides"


def overridden_report_ids(object_id: str, hashes: dict | None, paths) -> set[str]:
    """当前内容下有效的复议记录所覆盖的报告标识集合。"""
    directory = overrides_dir(paths, object_id)
    if not directory.is_dir():
        return set()
    valid: set[str] = set()
    for path in sorted(directory.glob("*.json")):
        record = read_json_dict(path)
        if record is None or record.get("schema_version") != SCHEMA_VERSION:
            continue
        if record.get("actor_type") != "human" or record.get("decision") != DECISION:
            continue
        if hashes is not None and (
            record.get("wiki_content_sha256") != hashes["content_sha256"]
            or record.get("wiki_evidence_sha256") != hashes["evidence_sha256"]
        ):
            continue  # 绑定的是旧内容：复议随内容变化自动失效
        expected = hash_canonical(
            {k: v for k, v in record.items() if k != "record_sha256"}
        )
        if record.get("record_sha256") != expected:
            continue  # 自哈希不自证：视为无效记录
        report_sha256 = record.get("report_sha256")
        if isinstance(report_sha256, str):
            valid.add(report_sha256)
    return valid


def _find_report(object_id: str, report_sha256: str, paths) -> dict:
    directory = paths.audit_validation("wiki", object_id)
    stem = report_sha256.removeprefix("sha256:")
    path = directory / f"{stem}.json"
    record = read_json_dict(path) if path.is_file() else None
    if record is None:
        raise OverrideBlocked("report_not_found", f"未找到报告 {stem}")
    if record.get("schema_version") != "validation-report/v1":
        raise OverrideBlocked("report_schema_invalid", "只能复议 validation-report/v1")
    if record.get("verdict") != "fail":
        raise OverrideBlocked("report_not_failed", "只有 fail 报告需要复议")
    return record


def _require_object_id(object_id: str) -> str:
    """校验 object_id 用于路径拼接（C004）：非法时抛 OverrideBlocked。"""
    try:
        return safe_id(object_id)
    except ValueError as exc:
        raise OverrideBlocked(
            "object_id_invalid", f"object_id 非法: {object_id}"
        ) from exc


def _require_report_sha256(report_sha256: str) -> str:
    """校验 report_sha256 是可拼接的文件名（64 位 hex）：非法时抛 OverrideBlocked。"""
    stem = report_sha256.removeprefix("sha256:")
    if len(stem) != 64 or any(c not in "0123456789abcdef" for c in stem):
        raise OverrideBlocked(
            "report_sha256_invalid", f"report_sha256 非法: {report_sha256}"
        )
    return stem


def write_override(
    root: Path,
    *,
    object_id: str,
    report_sha256: str,
    actor_id: str,
    reason: str,
    claim_ids: list[str],
) -> dict:
    """写入一条复议记录；任何前置不满足一律抛 `OverrideBlocked`。"""
    paths = RepoPaths(root)
    if not reason or not reason.strip():
        raise OverrideBlocked("reason_required", "复议必须给出理由")
    object_id = _require_object_id(object_id)
    _require_report_sha256(report_sha256)
    try:
        safe_id(actor_id)
    except ValueError as exc:
        raise OverrideBlocked("actor_invalid", f"actor_id 非法: {actor_id}") from exc

    report = _find_report(object_id, report_sha256, paths)
    disputed = sorted(
        str(claim.get("claim_id"))
        for claim in report.get("claims") or []
        if isinstance(claim, dict) and claim.get("verdict") not in SUPPORTED_VERDICTS
    )
    if sorted(set(claim_ids)) != disputed:
        raise OverrideBlocked(
            "claims_mismatch",
            f"必须逐条复议该报告的全部非 supported claim: {disputed}",
        )

    from .validator import WikiValidator

    wiki_path = paths.wiki_root / f"{object_id}.md"
    if not wiki_path.is_file():
        matches = list(paths.wiki_root.rglob(f"{object_id}.md"))
        if not matches:
            raise OverrideBlocked("object_not_found", f"未找到 wiki {object_id}")
        wiki_path = matches[0]
    vreport = WikiValidator(root).validate(wiki_path)
    hashes = vreport.get("hashes") or {}
    if not hashes:
        raise OverrideBlocked("object_invalid", "wiki 确定性校验未通过，先修校验错误")
    if (
        report.get("wiki_content_sha256") != hashes["content_sha256"]
        or report.get("wiki_evidence_sha256") != hashes["evidence_sha256"]
    ):
        raise OverrideBlocked(
            "report_stale", "该报告绑定的不是当前内容，无需复议（已自动失效）"
        )

    record = {
        "schema_version": SCHEMA_VERSION,
        "object_ref": {
            "vault_id": "public",
            "object_type": "wiki",
            "object_id": object_id,
        },
        "report_sha256": report_identity(report),
        "report_provider_identity": report.get("provider_identity"),
        "decision": DECISION,
        "reviewed_claim_ids": disputed,
        "reason": reason.strip(),
        "actor_id": actor_id,
        "actor_type": "human",
        "reviewed_at": time.time(),
        "wiki_content_sha256": hashes["content_sha256"],
        "wiki_evidence_sha256": hashes["evidence_sha256"],
        "ruleset_sha256": report.get("ruleset_sha256"),
    }
    record["record_sha256"] = hash_canonical(record)
    target = (
        overrides_dir(paths, object_id)
        / f"{record['record_sha256'].removeprefix('sha256:')}.json"
    )
    try:
        atomic_write(
            target, json.dumps(record, ensure_ascii=False, indent=2).encode("utf-8")
        )
    except OSError as exc:
        raise OverrideBlocked("write_failed", f"复议记录写入失败: {exc}") from exc
    return {**record, "path": str(target)}
