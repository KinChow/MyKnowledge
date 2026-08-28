"""F002 门面编排：validate 全链路：对应 docs/acceptance/F002-wiki-contract.md 的 AC 条目。"""

from __future__ import annotations

from wiki_fixtures import (
    WikiTestCase,
    _base_wiki,
)

from tools.validation import WIKI_SCHEMA_VERSION


class WikiValidatorTests(WikiTestCase):
    def test_legal_knowledge_wiki(self):
        """AC-F002-001：合法 Wiki 校验通过并计算正确派生字段与可复现 hash。"""
        wiki_path, validator = self._fixture(_base_wiki())
        report = validator.validate(wiki_path)
        self.assertTrue(report["valid"], report["errors"])
        self.assertEqual(report["schema_version"], WIKI_SCHEMA_VERSION)
        derived = report["derived"]
        self.assertEqual(derived["evidence_state"], "supported")
        self.assertEqual(derived["validation_state"], "not_run")
        self.assertEqual(derived["availability"], "available")
        self.assertEqual(derived["availability_reason"], "none")
        self.assertEqual(derived["effective_confidentiality"], "public")
        self.assertIsNone(derived["strength"])  # 无 LLM 报告 → 等待补证
        self.assertFalse(derived["private_publishable"])
        self.assertFalse(derived["public_publishable"])
        self.assertFalse(derived["public_release"])
        # hash 可复现：同内容两次校验结果一致
        again = validator.validate(wiki_path)
        self.assertEqual(again["hashes"], report["hashes"])
        self.assertRegex(report["hashes"]["content_sha256"], r"^sha256:[0-9a-f]{64}$")
        self.assertRegex(report["hashes"]["evidence_sha256"], r"^sha256:[0-9a-f]{64}$")
