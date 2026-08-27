"""F003 LLM 证据审计编排：覆盖义务、not_run 语义、引文二次校验、报告写入。

对应 docs/myknowledge-system-design.md §17.2 LLM validation tests 与
AC-F003-003/007/008/011/014/015/016。所有 provider 均为 FakeProvider
（mock 结构化输出），真实 LLM 只作为集成测试，不作为离线单元测试依赖。
"""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from tools.common import sha256_text
from tools.validation.audit import (
    AuditBlocked,
    check_coverage,
    provider_allows_request,
    run_audit,
)
from tools.validation.confirm import ConfirmationBlocked, create_confirmation
from tools.validation.derived import SCHEMA_VERSION
from tools.validation.provider import ProviderResult, build_input_hash
from tools.validation.validator import WikiValidator
from wiki_fixtures import (
    QUOTE_EXACT,
    SOURCE_BODY,
    WikiTestCase,
    _base_wiki,
    _evidence_item,
    _install_spec_doc,
    _make_source,
    _write_wiki,
)


class FakeProvider:
    """mock structured-output provider：固定 payload 或固定错误码。"""

    def __init__(self, payload: dict | None = None, error_code: str | None = None) -> None:
        self.payload = payload
        self.error_code = error_code
        self.calls: list[dict] = []

    def audit(self, request: dict, response_schema: dict) -> ProviderResult:
        self.calls.append(request)
        input_hash = build_input_hash(request)
        if self.error_code is not None:
            return ProviderResult(
                "fake", "call_test", input_hash,
                error_code=self.error_code, error_message="fake error",
            )
        return ProviderResult("fake", "call_test", input_hash, payload=self.payload)


def _payload(
    wiki_id: str = "test-wiki",
    verdicts: tuple[str, ...] = ("supported",),
    exact: str = QUOTE_EXACT,
    claim_ids: tuple[str, ...] = ("c1",),
    **overrides: object,
) -> dict:
    """构造符合 wiki-validation/v1 的合法 provider 输出（fixture）。"""
    claims = []
    for idx, (claim_id, verdict) in enumerate(zip(claim_ids, verdicts)):
        claims.append(
            {
                "claim_id": claim_id,
                "verdict": verdict,
                "targets": [{"source_id": "test-source", "evidence_id": "e1"}],
                "supporting_quotes": [{"evidence_id": "e1", "exact": exact}],
                "applied_rule_refs": ["VAL-001"],
                "rationale": f"引文 {idx + 1} 支持该论断",
                "rationale_offsets": [
                    {"source_id": "test-source", "evidence_id": "e1",
                     "start": 0, "end": min(10, len(exact))}
                ],
            }
        )
    payload = {
        "wiki_id": wiki_id,
        "verdict": "pass",
        "claims": claims,
        "call_id": "call_test",
        "unmapped_claims": [],
        "contradictions": [],
        "missing_evidence": [],
    }
    payload.update(overrides)
    return payload


class AuditSetup(WikiTestCase):
    def setUp(self) -> None:
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        _install_spec_doc(self.root)
        _make_source(
            self.root,
            "test-source",
            evidence_items=[_evidence_item("e1", SOURCE_BODY, QUOTE_EXACT)],
        )
        self.wiki_path = _write_wiki(self.root, _base_wiki())
        self.provider = FakeProvider()


class AuditTests(AuditSetup):
    def _run(self, payload: dict | None = None, error_code: str | None = None):
        self.provider.payload = payload
        self.provider.error_code = error_code
        return run_audit(self.root, self.wiki_path, self.provider)

    def _reports(self) -> list[Path]:
        base = self.root / "audit" / "validation" / "wiki" / "test-wiki"
        return sorted(base.glob("*.json")) if base.exists() else []

    def test_internal_request_requires_provider_opt_in(self):
        request = {"claims": [{"targets": [{"confidentiality": "internal"}]}]}
        self.assertFalse(provider_allows_request(self.provider, request))
        self.provider.supports_internal = True
        self.assertTrue(provider_allows_request(self.provider, request))

    def test_internal_request_is_blocked_before_provider_call(self):
        """Internal evidence requires explicit provider capability and stays redacted."""
        source_path = self.root / "sources" / "tools" / "test-source.md"
        source_path.write_text(
            source_path.read_text(encoding="utf-8").replace(
                "confidentiality: public", "confidentiality: internal", 1
            ),
            encoding="utf-8",
        )
        outcome = self._run(_payload())
        self.assertEqual(outcome["validation_state"], "not_run")
        self.assertEqual(outcome["not_run_reason"], "provider_unavailable")
        self.assertEqual(self.provider.calls, [])
        report_text = "\n".join(
            p.read_text(encoding="utf-8") for p in self._reports()
        )
        self.assertNotIn(SOURCE_BODY, report_text)
        self.assertNotIn("endpoint", report_text.lower())
        self.assertNotIn("api_key", report_text.lower())

    def test_all_supported_passes(self):
        """§17.2：全部 supported → verdict pass + 报告写入 + hash 绑定。"""
        outcome = self._run(_payload())
        self.assertEqual(outcome["verdict"], "pass")
        self.assertEqual(outcome["validation_state"], "pass")
        files = self._reports()
        self.assertEqual(len(files), 1)
        record = json.loads(files[0].read_text(encoding="utf-8"))
        self.assertEqual(record["schema_version"], SCHEMA_VERSION)
        self.assertEqual(record["wiki_id"], "test-wiki")
        self.assertEqual(record["call_id"], "call_test")
        self.assertIn("ruleset_sha256", record)
        self.assertEqual(len(record["evidence_bindings"]), 1)
        binding = record["evidence_bindings"][0]
        self.assertEqual(binding["source_id"], "test-source")
        self.assertEqual(binding["evidence_id"], "e1")
        # 报告驱动派生：validate 后 validation_state: pass
        report = WikiValidator(self.root).validate(self.wiki_path)
        self.assertEqual(report["derived"]["validation_state"], "pass")
        self.assertEqual(report["derived"]["strength"], "verified")

    def test_partially_supported_fails(self):
        outcome = self._run(_payload(verdicts=("partially_supported",)))
        self.assertEqual(outcome["verdict"], "fail")
        report = WikiValidator(self.root).validate(self.wiki_path)
        self.assertEqual(report["derived"]["validation_state"], "fail")
        self.assertEqual(report["derived"]["evidence_state"], "partial")

    def test_unsupported_fails(self):
        outcome = self._run(_payload(verdicts=("unsupported",)))
        self.assertEqual(outcome["verdict"], "fail")

    def test_contradicted_fails_conflicting(self):
        outcome = self._run(_payload(verdicts=("contradicted",)))
        self.assertEqual(outcome["verdict"], "fail")
        report = WikiValidator(self.root).validate(self.wiki_path)
        self.assertEqual(report["derived"]["evidence_state"], "conflicting")

    def test_unmapped_fails(self):
        outcome = self._run(_payload(verdicts=("unmapped",)))
        self.assertEqual(outcome["verdict"], "fail")

    def test_malformed_json_not_run(self):
        """malformed 输出 → not_run: malformed_output（不是 fail）。"""
        outcome = self._run(_payload(wiki_id="wrong-wiki"))
        self.assertEqual(outcome["validation_state"], "not_run")
        self.assertEqual(outcome["not_run_reason"], "malformed_output")
        report = WikiValidator(self.root).validate(self.wiki_path)
        self.assertEqual(report["derived"]["validation_state"], "not_run")

    def test_provider_unavailable_not_run(self):
        outcome = self._run(error_code="provider_unavailable")
        self.assertEqual(outcome["validation_state"], "not_run")
        self.assertEqual(outcome["not_run_reason"], "provider_unavailable")

    def test_provider_timeout_exception_is_normalized_to_not_run(self):
        class TimeoutProvider(FakeProvider):
            def audit(self, request: dict, response_schema: dict) -> ProviderResult:
                raise TimeoutError("deadline")
        outcome = run_audit(self.root, self.wiki_path, TimeoutProvider())
        self.assertEqual(outcome["validation_state"], "not_run")
        self.assertEqual(outcome["not_run_reason"], "context_exceeded")

    def test_model_self_declared_not_run_rejected(self):
        """AC-F003-014：模型自行声明 not_run 被拒绝（协议不可用）。"""
        outcome = self._run(_payload(not_run="provider_unavailable"))
        self.assertEqual(outcome["validation_state"], "not_run")
        self.assertEqual(outcome["not_run_reason"], "malformed_output")

    def test_incomplete_coverage_missing_claim(self):
        """漏掉 claim → not_run: incomplete_coverage，不保存部分结论。"""
        outcome = self._run(_payload(claim_ids=("c2",)))
        self.assertEqual(outcome["validation_state"], "not_run")
        self.assertEqual(outcome["not_run_reason"], "incomplete_coverage")
        # 不保存部分结论：目录里只有 not_run 记录（无 verdict 报告）
        records = [json.loads(p.read_text(encoding="utf-8")) for p in self._reports()]
        self.assertTrue(all(r["schema_version"] != SCHEMA_VERSION for r in records))

    def test_incomplete_coverage_rejects_extra_claim(self):
        """provider 增加请求之外的 claim 也必须整次 not_run。"""
        payload = _payload()
        payload["claims"].append(
            {
                "claim_id": "unexpected",
                "verdict": "supported",
                "targets": [{"source_id": "test-source", "evidence_id": "e1"}],
                "supporting_quotes": [{"evidence_id": "e1", "exact": QUOTE_EXACT}],
                "applied_rule_refs": ["VAL-001"],
                "rationale": "额外 claim 不属于本次请求",
                "rationale_offsets": [
                    {"source_id": "test-source", "evidence_id": "e1", "start": 0, "end": 10}
                ],
            }
        )
        outcome = self._run(payload)
        self.assertEqual(outcome["validation_state"], "not_run")
        self.assertEqual(outcome["not_run_reason"], "incomplete_coverage")
        records = [json.loads(p.read_text(encoding="utf-8")) for p in self._reports()]
        self.assertTrue(all(r["schema_version"] != SCHEMA_VERSION for r in records))

    def test_incomplete_coverage_missing_quote(self):
        """supporting_quotes 未覆盖全部 target → incomplete_coverage。"""
        payload = _payload()
        payload["claims"][0]["supporting_quotes"] = []
        outcome = self._run(payload)
        self.assertEqual(outcome["not_run_reason"], "incomplete_coverage")

    def test_incomplete_coverage_no_rule_refs(self):
        payload = _payload()
        payload["claims"][0]["applied_rule_refs"] = []
        outcome = self._run(payload)
        self.assertEqual(outcome["not_run_reason"], "incomplete_coverage")

    def test_incomplete_coverage_unknown_rule_ref(self):
        payload = _payload()
        payload["claims"][0]["applied_rule_refs"] = ["NOT-A-RULE"]
        outcome = self._run(payload)
        self.assertEqual(outcome["not_run_reason"], "incomplete_coverage")

    def test_incomplete_coverage_no_rationale_offsets(self):
        """rationale 无引用区间 → incomplete_coverage（泛泛结论不满足举证义务）。"""
        payload = _payload()
        payload["claims"][0]["rationale_offsets"] = []
        outcome = self._run(payload)
        self.assertEqual(outcome["not_run_reason"], "incomplete_coverage")

    def test_quote_mismatch_forces_unsupported(self):
        """§8.2：模型引文未逐字命中 selector → 强制 unsupported（无论模型 verdict）。"""
        payload = _payload(exact="与原文完全不同的引文内容填充")
        outcome = self._run(payload)
        self.assertEqual(outcome["verdict"], "fail")
        self.assertEqual(len(outcome["quote_errors"]), 1)
        self.assertEqual(outcome["quote_errors"][0]["code"], "quote_mismatch")

    def test_quote_too_short_forces_unsupported(self):
        payload = _payload(exact="太短")
        outcome = self._run(payload)
        self.assertEqual(outcome["verdict"], "fail")
        self.assertEqual(outcome["quote_errors"][0]["code"], "quote_too_short")

    def test_deterministic_blocked_no_provider_call(self):
        """确定性校验失败 → AuditBlocked，不调用 provider、不写记录。"""
        bad_wiki = _write_wiki(
            self.root,
            {**_base_wiki(), "sources": ["ghost-source"]},
        )
        with self.assertRaises(AuditBlocked) as ctx:
            run_audit(self.root, bad_wiki, self.provider)
        self.assertEqual(ctx.exception.code, "deterministic_blocked")
        self.assertEqual(self.provider.calls, [])
        self.assertEqual(self._reports(), [])

    def test_report_append_only_idempotent(self):
        """⑰ 修复：同内容重跑幂等覆盖（同名文件），异内容并存不删历史。

        报告 hash 只含稳定内容核（verdict/claims/corroboration/ruleset 等），
        audited_at/call_id 等运行时字段不参与文件名。
        """
        self._run(_payload())
        self.assertEqual(len(self._reports()), 1)
        # 同内容重跑 → 覆盖同名文件（目录不随重跑无界增长）
        self._run(_payload())
        self.assertEqual(len(self._reports()), 1)
        # 异内容（verdict 不同）→ 并存
        self._run(_payload(verdicts=("contradicted",)))
        self.assertEqual(len(self._reports()), 2)

    def test_advisory_excluded_from_verdict(self):
        """⑮ 修复：advisory claim 不参与 pass/fail（policy 默认 false）。

        advisory claim 判 unsupported 不影响顶层 verdict；覆盖义务仍要求其存在。
        """
        payload = _payload()
        payload["claims"][0]["advisory"] = True
        payload["claims"][0]["verdict"] = "unsupported"
        outcome = self._run(payload)
        self.assertEqual(outcome["verdict"], "pass")

    def test_quote_failure_rewrites_claim_verdict(self):
        """⑬ 修复：引文二次校验失败的 claim 在报告中回写 unsupported。

        报告与 derived 读到改写后的 verdict（避免"证据支持但审计失败"矛盾展示）。
        """
        payload = _payload(exact="与原文完全不同的引文内容填充")
        outcome = self._run(payload)
        self.assertEqual(outcome["verdict"], "fail")
        record = json.loads(self._reports()[-1].read_text(encoding="utf-8"))
        self.assertEqual(record["claims"][0]["verdict"], "unsupported")
        report = WikiValidator(self.root).validate(self.wiki_path)
        self.assertEqual(report["derived"]["evidence_state"], "partial")

    def test_multitarget_observation_conflict(self):
        """⑫ P1 修复：observation 下沉 per-target 后，多 target 冲突可检出。

        同一 claim 两个不同独立组的 target 各带 observation，其中一个给出
        相反谓词 → corroboration 判 conflicting（修复前同 claim 复制同一
        observation 恒 supports_same，冲突检测路径失效）。
        """
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        root = Path(directory.name)
        _install_spec_doc(root)
        _make_source(
            root,
            "src-a",
            evidence_items=[_evidence_item("e1", SOURCE_BODY, QUOTE_EXACT)],
        )
        _make_source(
            root,
            "src-b",
            evidence_items=[_evidence_item("e2", SOURCE_BODY, QUOTE_EXACT)],
            provenance={"independence_group": "g2"},
        )
        meta = _base_wiki()
        meta["sources"] = ["src-a", "src-b"]
        meta["evidence"] = [
            {
                "claim_id": "c1",
                "claim": "测试论断。",
                "targets": [
                    {"source_id": "src-a", "evidence_id": "e1"},
                    {"source_id": "src-b", "evidence_id": "e2"},
                ],
                "support": "direct",
                "supporting_quotes": [
                    {"evidence_id": "e1", "exact": QUOTE_EXACT},
                    {"evidence_id": "e2", "exact": QUOTE_EXACT},
                ],
            }
        ]
        wiki_path = _write_wiki(root, meta)
        payload = _payload()
        claim = payload["claims"][0]
        claim["targets"] = [
            {"source_id": "src-a", "evidence_id": "e1"},
            {"source_id": "src-b", "evidence_id": "e2"},
        ]
        claim["supporting_quotes"] = [
            {"evidence_id": "e1", "exact": QUOTE_EXACT},
            {"evidence_id": "e2", "exact": QUOTE_EXACT},
        ]
        claim["rationale_offsets"] = [
            {"source_id": "src-a", "evidence_id": "e1", "start": 0, "end": 10},
            {"source_id": "src-b", "evidence_id": "e2", "start": 0, "end": 10},
        ]
        claim["observations"] = [
            {"evidence_id": "e1", "subject": "命题", "predicate": "等于", "object": "值"},
            {"evidence_id": "e2", "subject": "命题", "predicate": "不等于", "object": "值"},
        ]
        provider = FakeProvider(payload=payload)
        outcome = run_audit(root, wiki_path, provider)
        # 模型逐条 supported → 顶层 verdict pass；但 observation 冲突 →
        # corroboration conflicting（确定性证据链矛盾，阻断发布）
        self.assertEqual(outcome["verdict"], "pass")
        self.assertEqual(
            outcome["corroboration"]["evidence_state"], "conflicting"
        )
        report = WikiValidator(root).validate(wiki_path)
        self.assertEqual(report["derived"]["evidence_state"], "conflicting")
        self.assertFalse(report["derived"]["private_publishable"])

    def test_fail_history_tracked(self):
        """AC-F003-016：fail 历史 append-only 统计，重跑不刷绿隐藏历史。"""
        self._run(_payload(verdicts=("contradicted",)))
        self._run(_payload())
        report = WikiValidator(self.root).validate(self.wiki_path)
        history = report["derived"]["fail_history"]
        self.assertEqual(history["fail_count"], 1)
        self.assertEqual(history["last_fail_rule_refs"], ["VAL-001"])

    def test_ruleset_change_marks_stale(self):
        """AC-F003-015：规范措辞变化 → stale_ruleset（可见、不阻断）。"""
        self._run(_payload())
        doc = self.root / "docs" / "myknowledge-system-design.md"
        text = doc.read_text(encoding="utf-8")
        doc.write_text(
            text.replace("规范化步骤按顺序执行", "规范化步骤按固定顺序执行"),
            encoding="utf-8",
        )
        report = WikiValidator(self.root).validate(self.wiki_path)
        self.assertEqual(report["derived"]["validation_state"], "stale_ruleset")

    def test_request_contains_ruleset_and_quote_context(self):
        """ValidationRequest 带规则集与已通过确定性检查的 target 上下文。"""
        self._run(_payload())
        request = self.provider.calls[0]
        self.assertEqual(request["wiki_id"], "test-wiki")
        self.assertIn("ruleset_sha256", request["ruleset"])
        claim = request["claims"][0]
        self.assertEqual(claim["claim_id"], "c1")
        target = claim["targets"][0]
        self.assertEqual(target["source_id"], "test-source")
        self.assertIn(QUOTE_EXACT, target["quote"])  # 上下文含 snapshot 片段
        self.assertIn("provenance", target)


class ConfirmTests(AuditSetup):
    def setUp(self) -> None:
        super().setUp()
        # publishable 派生要求 status: published（§6.8）
        self.wiki_path = _write_wiki(
            self.root,
            _base_wiki(status="published", publication_scope="private"),
        )
    def test_confirm_writes_dual_paths(self):
        """AC-F003-007：确认写入 audit/validation/ + operation 记录。"""
        create_confirmation(self.root, self.wiki_path, actor_id="local-user")
        validation_dir = (
            self.root / "audit" / "validation" / "wiki" / "test-wiki"
        )
        confirmation_files = [
            p for p in validation_dir.glob("*.json")
            if "confirmation" not in p.name
        ]
        # 确认记录 schema_version: operation-confirmation/v1
        confirmations = []
        for p in validation_dir.glob("*.json"):
            record = json.loads(p.read_text(encoding="utf-8"))
            if record.get("schema_version") == "operation-confirmation/v1":
                confirmations.append(record)
        self.assertEqual(len(confirmations), 1)
        record = confirmations[0]
        self.assertEqual(record["decision"], "approve")
        self.assertIn("content_sha256", record)
        self.assertIn("evidence_sha256", record)
        self.assertIn("deterministic_report_sha256", record)
        self.assertEqual(record["llm_state"], "not_run")
        # operation 记录：has_private_confirmation 可消费 → publishable
        ops = list((self.root / "audit" / "operations").glob("op_*.json"))
        self.assertEqual(len(ops), 1)
        report = WikiValidator(self.root).validate(self.wiki_path)
        self.assertTrue(report["derived"]["private_publishable"])

    def test_confirm_blocked_by_llm_fail(self):
        """AC-F003-013：LLM fail 阻断人工确认（白名单门禁 fail-closed）。"""
        self.provider.payload = _payload(verdicts=("contradicted",))
        run_audit(self.root, self.wiki_path, self.provider)
        with self.assertRaises(ConfirmationBlocked) as ctx:
            create_confirmation(self.root, self.wiki_path, actor_id="local-user")
        self.assertEqual(ctx.exception.code, "llm_state_blocks_confirmation")

    def test_confirm_blocked_by_deterministic(self):
        bad_wiki = _write_wiki(
            self.root,
            {**_base_wiki(), "sources": ["ghost-source"]},
        )
        with self.assertRaises(ConfirmationBlocked) as ctx:
            create_confirmation(self.root, bad_wiki, actor_id="local-user")
        self.assertEqual(ctx.exception.code, "deterministic_blocked")

    def test_content_change_invalidates_confirmation(self):
        """AC-F003-003：正文变化 → 旧确认失效，不得继续 publishable。"""
        create_confirmation(self.root, self.wiki_path, actor_id="local-user")
        wiki_path = self.wiki_path
        text = wiki_path.read_text(encoding="utf-8")
        wiki_path.write_text(text.replace("# 测试主题", "# 测试主题改"), encoding="utf-8")
        report = WikiValidator(self.root).validate(wiki_path)
        self.assertFalse(report["derived"]["private_publishable"])
        self.assertEqual(report["derived"]["validation_state"], "not_run")


if __name__ == "__main__":
    unittest.main()
