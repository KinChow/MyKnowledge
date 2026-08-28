"""人工审计确认写入（F003 AC-F003-007/013）：operation-confirmation/v1。

人工审计是对当前 ``(content_sha256, evidence_sha256)`` 的一次显式背书
（TD 人工审计）：确认记录包含两个内容 hash、DeterministicReport 摘要
hash、LLM 审计状态（not_run/pass/fail/stale_ruleset 及其 ruleset_sha256）
与历史 fail 次数。

双路径写入（§8.4 + F002 derived 消费）：
- ``audit/validation/wiki/<id>/<confirmation_sha256>.json``：规范路径，
  内容 hash 命名、append-only；
- ``audit/operations/op_*.json``：operation/v1 记录（``scope: publish_private``
  confirmation），供 derived.has_private_confirmation 判定 publishability。

前置门禁（AC-F003-013）：确定性校验必须通过；LLM ``fail`` 阻断；
缺少/失效的确认阻断。LLM ``not_run``/``pass``/``stale_ruleset`` 都允许
人工确认（不提高/不降低要求）。
"""

from __future__ import annotations

import argparse
import contextlib
import json
import time
import uuid
from pathlib import Path

from ..common import atomic_write, canonical_json, hash_canonical, redact, safe_id
from ..paths import RepoPaths
from .derived import fail_history
from .validator import WikiValidator

CONFIRMATION_SCHEMA_VERSION = "operation-confirmation/v1"
# LLM 状态中允许人工确认的集合（AC-F003-013：fail 阻断，其余不提高要求）
ALLOWED_LLM_STATES = {"not_run", "pass", "stale_ruleset"}


class ConfirmationBlocked(Exception):
    """确认前置失败（确定性/LLM fail/内部状态）；不写任何确认记录。"""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.message = message


def deterministic_report_sha256(vreport: dict) -> str:
    """DeterministicReport 摘要 hash：稳定字段的 canonical hash。

    覆盖确定性结论（valid/errors/warnings）与内容绑定（hashes/派生状态），
    供确认记录重放核对"人确认的就是这份确定性报告"。
    """
    return hash_canonical(
        {
            "valid": vreport["valid"],
            "errors": vreport["errors"],
            "warnings": vreport["warnings"],
            "hashes": vreport["hashes"],
            "derived": {
                "evidence_state": vreport["derived"]["evidence_state"],
                "validation_state": vreport["derived"]["validation_state"],
                "availability": vreport["derived"]["availability"],
                "strength": vreport["derived"]["strength"],
            },
        }
    )


def create_confirmation(
    root: Path,
    wiki_path: Path,
    *,
    actor_id: str,
    decision: str = "approve",
    quote_min_chars: int = 12,
) -> dict:
    """对当前 Wiki 写入人工审计确认（先校验后写入，写失败抛结构化错误）。

    返回确认记录（含写入路径）；任何门禁失败抛 ConfirmationBlocked。
    """
    if decision not in {"approve", "reject"}:
        raise ConfirmationBlocked("invalid_decision", f"decision: {decision}")
    try:
        safe_id(actor_id)
    except ValueError as exc:
        raise ConfirmationBlocked("invalid_actor_id", str(exc)) from exc
    paths = RepoPaths(root)
    validator = WikiValidator(root, quote_min_chars=quote_min_chars)
    vreport = validator.validate(wiki_path)
    if not vreport["valid"]:
        raise ConfirmationBlocked(
            "deterministic_blocked",
            f"确定性校验未通过，不写确认: {[e['code'] for e in vreport['errors']]}",
        )
    derived = vreport["derived"]
    object_id = str(vreport["object_ref"]["object_id"])
    hashes = vreport["hashes"]
    history = fail_history(object_id, paths)
    # AC-F003-013：白名单门禁（fail-closed，㉑）——unavailable 及任何
    # 未来新增状态默认阻断；LLM fail 阻断发布；not_run 不提高/降低要求
    if derived["validation_state"] not in ALLOWED_LLM_STATES:
        raise ConfirmationBlocked(
            "llm_state_blocks_confirmation",
            f"LLM 审计状态 {derived['validation_state']} 阻断人工确认"
            f"（允许: {sorted(ALLOWED_LLM_STATES)}）",
        )
    # LLM 状态与 ruleset_sha256：pass/fail 报告携带 ruleset；not_run 无
    llm_state = derived["validation_state"]
    ruleset_sha256 = None
    if vreport["validation_report"] is not None:
        ruleset_sha256 = vreport["validation_report"].get("ruleset_sha256")
    record = {
        "schema_version": CONFIRMATION_SCHEMA_VERSION,
        "object_ref": {
            "vault_id": "public",
            "object_type": "wiki",
            "object_id": object_id,
        },
        "scope": "publish",
        "decision": decision,
        "actor_id": actor_id,
        "confirmed_at": time.time(),
        "content_sha256": hashes["content_sha256"],
        "evidence_sha256": hashes["evidence_sha256"],
        "deterministic_report_sha256": deterministic_report_sha256(vreport),
        "llm_state": llm_state,
        "ruleset_sha256": ruleset_sha256,
        "fail_history": history,
    }
    record_sha256 = hash_canonical(record)
    record["confirmation_sha256"] = record_sha256
    target = (
        paths.audit_validation("wiki", object_id)
        / f"{record_sha256.removeprefix('sha256:')}.json"
    )
    try:
        atomic_write(
            target,
            json.dumps(record, ensure_ascii=False, indent=2).encode("utf-8"),
        )
    except OSError as exc:
        raise ConfirmationBlocked(
            "confirmation_write_failed", f"确认记录写入失败: {exc}"
        ) from exc
    # operation/v1 审计记录（derived.has_private_confirmation 消费：
    # scope: publish_private + hash 匹配）
    operation_id = "op_" + uuid.uuid4().hex
    operation = {
        "schema_version": "operation/v1",
        "operation_id": operation_id,
        "operation_type": "publish_wiki",
        "state": "applied",
        "created_at": record["confirmed_at"],
        "updated_at": record["confirmed_at"],
        "target_vault": "public",
        "target_ref": {
            "object_type": "wiki",
            "object_id": object_id,
        },
        "confirmation": {
            "scope": "publish_private",
            "decision": decision,
            "actor_id": actor_id,
            "content_sha256": hashes["content_sha256"],
            "evidence_sha256": hashes["evidence_sha256"],
            "wiki_content_sha256": hashes["content_sha256"],
            "wiki_evidence_sha256": hashes["evidence_sha256"],
            "deterministic_report_sha256": record["deterministic_report_sha256"],
            "llm_state": llm_state,
            "ruleset_sha256": ruleset_sha256,
            "fail_history": history,
        },
    }
    operation["record_sha256"] = hash_canonical(
        operation
    )  # §1239：durable record 必须带自哈希
    audit_path = paths.operation_file(operation_id)
    try:
        atomic_write(
            audit_path,
            canonical_json(redact(operation)) + b"\n",
            0o600,
        )
    except OSError as exc:
        # ㉑ 双写补偿：operation 写失败时删除已写 confirmation（保持
        # confirmation 先行 = fail-closed：绝不留下"确认在、op 缺失"的
        # 不一致状态），并归一为结构化错误
        with contextlib.suppress(OSError):
            target.unlink()
        raise ConfirmationBlocked(
            "operation_write_failed", f"operation 记录写入失败: {exc}"
        ) from exc
    return {**record, "_path": str(target), "operation_id": operation_id}


def main(argv: list[str] | None = None) -> int:
    """confirm CLI：对单个 Wiki 写入人工审计确认（approve/reject）。"""
    parser = argparse.ArgumentParser(
        description="Human audit confirmation of a Wiki (operation-confirmation/v1)"
    )
    parser.add_argument("wiki", type=Path)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--actor-id", required=True)
    parser.add_argument("--decision", choices=["approve", "reject"], default="approve")
    parser.add_argument("--min-chars", type=int, default=12)
    args = parser.parse_args(argv)
    try:
        record = create_confirmation(
            args.root,
            args.wiki,
            actor_id=args.actor_id,
            decision=args.decision,
            quote_min_chars=args.min_chars,
        )
    except ConfirmationBlocked as exc:
        print(
            json.dumps(
                {"state": "blocked", "error_code": exc.code, "message": exc.message},
                ensure_ascii=False,
                indent=2,
            )
        )
        return 2
    print(json.dumps(record, ensure_ascii=False, indent=2))
    return 0
