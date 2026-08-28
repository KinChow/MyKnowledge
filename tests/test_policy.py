"""config/policy.yaml 唯一加载入口的 fail-closed 语义。

对应"策略读取失败不得静默按默认值继续"这条约束：策略里的
``advisory_participates_in_verdict`` / ``rule_ids`` 直接决定审计口径，
文件写坏时必须变成结构化阻断，而不是悄悄换成内置默认值。

历史问题：ruleset.py 与 audit.py 各自 `yaml.safe_load` + `except Exception:
return 默认值`，策略损坏时审计照跑并写出"已审"记录。
"""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from tools import policy
from tools.validation import audit, ruleset


class PolicyLoaderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        (self.root / "config").mkdir(parents=True)

    def _write_policy(self, text: str) -> None:
        (self.root / "config" / "policy.yaml").write_text(text, encoding="utf-8")

    def test_missing_policy_is_empty_not_error(self):
        """策略文件不存在是合法状态（默认值在调用方），返回空映射。"""
        self.assertEqual(policy.load_policy(self.root), {})
        self.assertIsNone(policy.policy_value(self.root, "validation", "ruleset"))
        self.assertEqual(
            policy.policy_value(self.root, "validation", "missing", default="fallback"),
            "fallback",
        )

    def test_valid_policy_reads_nested_value(self):
        self._write_policy(
            "validation:\n  ruleset:\n    advisory_participates_in_verdict: true\n"
        )
        self.assertIs(
            policy.policy_value(
                self.root,
                "validation",
                "ruleset",
                "advisory_participates_in_verdict",
                default=False,
            ),
            True,
        )

    def test_broken_yaml_raises_policy_invalid(self):
        self._write_policy("validation:\n  ruleset: [unclosed\n")
        with self.assertRaises(ValueError) as caught:
            policy.load_policy(self.root)
        self.assertEqual(str(caught.exception), "policy_invalid")

    def test_non_mapping_policy_raises_policy_invalid(self):
        self._write_policy("- just\n- a\n- list\n")
        with self.assertRaises(ValueError) as caught:
            policy.load_policy(self.root)
        self.assertEqual(str(caught.exception), "policy_invalid")

    def test_empty_policy_file_is_empty_mapping(self):
        self._write_policy("")
        self.assertEqual(policy.load_policy(self.root), {})


class PolicyConsumerFailClosedTests(unittest.TestCase):
    """两个消费方在策略损坏时必须结构化阻断，而不是回退默认值。"""

    def setUp(self) -> None:
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        (self.root / "config").mkdir(parents=True)
        (self.root / "config" / "policy.yaml").write_text(
            "validation:\n  ruleset: [unclosed\n", encoding="utf-8"
        )

    def test_load_ruleset_reports_policy_invalid(self):
        loaded = ruleset.load_ruleset(self.root)
        self.assertEqual(loaded["rule_refs"], [])
        self.assertIsNone(loaded["ruleset_sha256"])
        self.assertEqual([e["code"] for e in loaded["errors"]], ["policy_invalid"])

    def test_explicit_rule_ids_bypass_policy(self):
        """显式传入 rule_ids 时不读策略：损坏的策略不应阻断显式调用。"""
        loaded = ruleset.load_ruleset(self.root, ["WIKI-001"])
        self.assertNotEqual([e["code"] for e in loaded["errors"]], ["policy_invalid"])

    def test_advisory_switch_blocks_audit(self):
        with self.assertRaises(audit.AuditBlocked) as caught:
            audit._policy_advisory_participates(self.root)
        self.assertEqual(caught.exception.code, "policy_invalid")


if __name__ == "__main__":
    unittest.main()
