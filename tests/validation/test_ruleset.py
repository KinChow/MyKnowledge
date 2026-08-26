"""F003 规则集抽取：rule_refs/ruleset_sha256 与失效语义。

对应 docs/acceptance/F003-evidence-validation.md AC-F003-008（规则集与
ruleset_sha256 随结论持久化）与 AC-F003-015（规则措辞变化 → stale_ruleset）。
"""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from tools.validation import ruleset
from wiki_fixtures import _install_spec_doc


class RulesetTests(unittest.TestCase):
    def setUp(self) -> None:
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        # 复用共享 fixture（复制仓库真实规范文档）
        _install_spec_doc(self.root)

    def test_default_ruleset_extracts_all_refs(self):
        """§18 阶段三：默认规则集全部可定位，ruleset_sha256 稳定可重放。"""
        loaded = ruleset.load_ruleset(self.root)
        self.assertEqual(loaded["errors"], [])
        self.assertEqual(
            {ref["spec_id"] for ref in loaded["rule_refs"]},
            set(ruleset.DEFAULT_RULE_IDS),
        )
        for ref in loaded["rule_refs"]:
            self.assertEqual(ref["doc"], ruleset.SPEC_DOC)
            self.assertRegex(ref["extract_sha256"], r"^sha256:[0-9a-f]{64}$")
        # 重放：同文档同规则集 → 相同 sha256
        again = ruleset.load_ruleset(self.root)
        self.assertEqual(again["ruleset_sha256"], loaded["ruleset_sha256"])

    def test_section6_not_truncated_by_fenced_comments(self):
        """① P1 修复：代码围栏内的 # 注释/模板行不得截断章节抽取。

        规范文档 §6 含 yaml 围栏（884 行附近）与 markdown 模板（973 行），
        修复前 WIKI-001 只抽到 §6.1；修复后必须覆盖 §6.2–§6.9 全部小节。
        """
        text = (self.root / "docs" / "myknowledge-system-design.md").read_text(
            encoding="utf-8"
        )
        section6 = ruleset.extract_section(text, "## 6. Wiki 严格规范")
        self.assertIsNotNone(section6)
        # 关键子章节锚点必须存在（§6.2/§6.4/§6.8/§6.9）
        for anchor in (
            "6.2 Wiki 状态机",
            "6.4 Claim 和 Evidence",
            "6.8 声明字段、派生字段与合法组合",
            "6.9 引文规范化与逐字匹配",
        ):
            self.assertIn(anchor, section6)

    def test_policy_rule_ids_loaded(self):
        """② 修复：config/policy.yaml 的 rule_ids 为运行时配置事实源。"""
        # 复制仓库真实 policy.yaml（fixture 来自真实产物）
        repo_policy = (
            Path(__file__).resolve().parent.parent.parent
            / "config"
            / "policy.yaml"
        )
        policy_target = self.root / "config" / "policy.yaml"
        policy_target.parent.mkdir(parents=True, exist_ok=True)
        policy_target.write_text(
            repo_policy.read_text(encoding="utf-8"), encoding="utf-8"
        )
        loaded = ruleset.load_ruleset(self.root)
        policy_ids = ruleset.policy_rule_ids(self.root)
        self.assertIsNotNone(policy_ids)
        self.assertEqual(
            {ref["spec_id"] for ref in loaded["rule_refs"]}, set(policy_ids)
        )
        # policy 缺失 → 回退默认（不阻断）
        self.assertIsNone(ruleset.policy_rule_ids(self.root / "nonexistent"))

    def test_section_reorder_changes_ruleset_sha256(self):
        """AC-F003-015：规则措辞/章节变化改变 extract_sha256 → ruleset_sha256。"""
        before = ruleset.load_ruleset(self.root)["ruleset_sha256"]
        doc = self.root / "docs" / "myknowledge-system-design.md"
        text = doc.read_text(encoding="utf-8")
        doc.write_text(text.replace("规范化步骤按顺序执行", "规范化步骤按固定顺序执行"), encoding="utf-8")
        after = ruleset.load_ruleset(self.root)["ruleset_sha256"]
        self.assertNotEqual(before, after)

    def test_missing_doc_fails_closed(self):
        """规范文档缺失 → 错误返回（fail-closed，不静默跳过规则条目）。"""
        loaded = ruleset.load_ruleset(self.root / "nonexistent")
        self.assertEqual(loaded["rule_refs"], [])
        self.assertIsNone(loaded["ruleset_sha256"])
        self.assertTrue(any(e["code"] == "ruleset_doc_unreadable" for e in loaded["errors"]))

    def test_unknown_spec_id_rejected(self):
        """未知 spec ID 不静默跳过：返回 ruleset_spec_unknown。"""
        refs, errors = ruleset.build_rule_refs(self.root, ["VAL-001", "NOT-A-RULE"])
        self.assertEqual([r["spec_id"] for r in refs], ["VAL-001"])
        self.assertTrue(any(e["code"] == "ruleset_spec_unknown" for e in errors))


if __name__ == "__main__":
    unittest.main()
