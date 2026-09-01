"""VAL-003 人工复议：fail 优先的安全阀，以及它的五条 fail-closed 约束。

背景（2026-09-01 实测）：同一页在 gpt-5.6-terra 与 ducx 上跑出 fail/pass 相反结论，
`load_validation_report` 因此改为 fail 优先。复议是唯一的推翻路径，且必须留痕。
"""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from wiki_fixtures import (
    QUOTE_EXACT,
    SOURCE_BODY,
    _base_wiki,
    _evidence_item,
    _install_spec_doc,
    _make_source,
    _write_wiki,
)

from tools.paths import RepoPaths
from tools.validation import WikiValidator
from tools.validation.override import OverrideBlocked, write_override


def _report(verdict: str, claims: list[dict], hashes: dict, ruleset: str) -> dict:
    return {
        "schema_version": "validation-report/v1",
        "wiki_id": "test-wiki",
        "verdict": verdict,
        "claims": claims,
        "ruleset_sha256": ruleset,
        "wiki_content_sha256": hashes["content_sha256"],
        "wiki_evidence_sha256": hashes["evidence_sha256"],
        "provider_identity": f"test:{verdict}",
    }


class OverrideTests(unittest.TestCase):
    """复议五条 fail-closed 约束：人签、绑定报告与内容、覆盖全部争议、理由必填、防篡改。"""

    def setUp(self) -> None:
        """构造一篇带 source/evidence 的 wiki、两份报告与复议目录。"""
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        _install_spec_doc(self.root)
        _make_source(
            self.root,
            "test-source",
            evidence_items=[_evidence_item("e1", SOURCE_BODY, QUOTE_EXACT)],
        )
        self.wiki_path = _write_wiki(self.root, _base_wiki())
        self.hashes = WikiValidator(self.root).validate(self.wiki_path)["hashes"]
        from tools.validation.ruleset import load_ruleset

        self.ruleset = load_ruleset(self.root)["ruleset_sha256"]
        self.report_dir = self.root / "audit" / "validation" / "wiki" / "test-wiki"
        self.report_dir.mkdir(parents=True)

    def _write_report(self, verdict: str, claim_verdict: str) -> str:
        """按生产命名口径落一份报告，返回它的稳定标识。"""
        from tools.validation.override import report_identity

        record = _report(
            verdict,
            [{"claim_id": "c1", "verdict": claim_verdict}],
            self.hashes,
            self.ruleset,
        )
        identity = report_identity(record)
        path = self.report_dir / f"{identity.removeprefix('sha256:')}.json"
        path.write_text(json.dumps(record, ensure_ascii=False), encoding="utf-8")
        return identity

    def _state(self) -> str:
        return WikiValidator(self.root).validate(self.wiki_path)["derived"][
            "validation_state"
        ]

    def test_fail_wins_over_a_later_pass_from_another_provider(self):
        """审计洗牌回归锁：换 provider 重跑到 pass 不得改变门禁结论。"""
        self._write_report("pass", "supported")
        self._write_report("fail", "partially_supported")
        self.assertEqual(self._state(), "fail")

    def test_signed_override_lets_the_pass_report_drive_again(self):
        """复议掉误判的 fail 后，同页的 pass 报告重新主导 validation_state。"""
        pass_identity = self._write_report("pass", "supported")
        fail_identity = self._write_report("fail", "partially_supported")
        self.assertEqual(self._state(), "fail")

        record = write_override(
            self.root,
            object_id="test-wiki",
            report_sha256=fail_identity,
            actor_id="test-owner",
            reason="引文与 claim 逐字对应，判定为模型误判",
            claim_ids=["c1"],
        )
        self.assertEqual(record["decision"], "misjudged")
        self.assertEqual(record["actor_type"], "human")
        self.assertEqual(record["report_sha256"], fail_identity)
        self.assertNotEqual(pass_identity, fail_identity)
        self.assertEqual(self._state(), "pass")

    def test_override_expires_when_content_changes(self):
        """复议绑定签署时的内容 hash：内容一改，复议不得顺延到新内容。"""
        from tools.validation.override import overridden_report_ids

        self._write_report("pass", "supported")
        fail_identity = self._write_report("fail", "partially_supported")
        write_override(
            self.root,
            object_id="test-wiki",
            report_sha256=fail_identity,
            actor_id="test-owner",
            reason="误判",
            claim_ids=["c1"],
        )
        self.assertEqual(self._state(), "pass")

        # 改正文 → content_sha256 变化（evidence 不变）
        self.wiki_path.write_text(
            self.wiki_path.read_text(encoding="utf-8") + "\n补充一段正文。\n",
            encoding="utf-8",
        )
        new_hashes = WikiValidator(self.root).validate(self.wiki_path)["hashes"]
        self.assertNotEqual(new_hashes["content_sha256"], self.hashes["content_sha256"])
        self.hashes = new_hashes

        paths = RepoPaths(self.root)
        self.assertEqual(overridden_report_ids("test-wiki", new_hashes, paths), set())

        # 新内容上重跑仍判 fail：旧复议不再生效，门禁重新收紧
        self._write_report("fail", "partially_supported")
        self.assertEqual(self._state(), "fail")

    def test_override_without_any_pass_report_falls_back_to_not_run(self):
        """复议掉唯一的 fail 报告 ≠ 自动 pass：没有可用判定就回落 not_run。"""
        fail_identity = self._write_report("fail", "partially_supported")
        write_override(
            self.root,
            object_id="test-wiki",
            report_sha256=fail_identity,
            actor_id="test-owner",
            reason="误判，但仓库里没有任何 pass 报告",
            claim_ids=["c1"],
        )
        self.assertEqual(self._state(), "not_run")

    def test_override_must_cover_every_disputed_claim(self):
        """只复议部分争议 claim 必须被拒：整份翻案需要覆盖全部非 supported。"""
        identity = self._write_report("fail", "partially_supported")
        with self.assertRaises(OverrideBlocked) as ctx:
            write_override(
                self.root,
                object_id="test-wiki",
                report_sha256=identity,
                actor_id="test-owner",
                reason="只复议一条",
                claim_ids=[],
            )
        self.assertEqual(ctx.exception.code, "claims_mismatch")

    def test_override_requires_a_reason_and_a_failed_report(self):
        """空白 reason 与对 pass 报告的复议都必须在写入前被拒。"""
        identity = self._write_report("fail", "partially_supported")
        with self.assertRaises(OverrideBlocked) as ctx:
            write_override(
                self.root,
                object_id="test-wiki",
                report_sha256=identity,
                actor_id="test-owner",
                reason="   ",
                claim_ids=["c1"],
            )
        self.assertEqual(ctx.exception.code, "reason_required")

        pass_identity = self._write_report("pass", "supported")
        with self.assertRaises(OverrideBlocked) as ctx:
            write_override(
                self.root,
                object_id="test-wiki",
                report_sha256=pass_identity,
                actor_id="test-owner",
                reason="pass 不需要复议",
                claim_ids=[],
            )
        self.assertEqual(ctx.exception.code, "report_not_failed")

    def test_tampered_override_record_is_ignored(self):
        """改写复议记录内容（record_sha256 不自证）后必须被忽略并恢复 fail。"""
        fail_identity = self._write_report("fail", "partially_supported")
        self._write_report("pass", "supported")
        record = write_override(
            self.root,
            object_id="test-wiki",
            report_sha256=fail_identity,
            actor_id="test-owner",
            reason="误判",
            claim_ids=["c1"],
        )
        self.assertEqual(self._state(), "pass")

        path = Path(record["path"])
        payload = json.loads(path.read_text(encoding="utf-8"))
        payload["reason"] = "被改写的理由"  # record_sha256 不再自证
        path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
        self.assertEqual(self._state(), "fail")


if __name__ == "__main__":
    unittest.main()
