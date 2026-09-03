"""F002 引用解析与引文校验：对应 docs/acceptance/F002-wiki-contract.md 的 AC 条目。"""

from __future__ import annotations

import tempfile
from pathlib import Path

from wiki_fixtures import (
    QUOTE_EXACT,
    SOURCE_BODY,
    WikiTestCase,
    _base_wiki,
    _evidence_item,
    _make_source,
    _write_wiki,
)

from tools.common import sha256_text, strip_sha256_prefix
from tools.front_matter import FrontMatter
from tools.validation import WikiValidator


class ResolutionTests(WikiTestCase):
    def test_duplicate_evidence_id_is_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            source = root / "content" / "sources" / "tools" / "dup" / "dup.md"
            source.parent.mkdir(parents=True)
            metadata = {
                "schema_version": "source/v1",
                "id": "dup",
                "domain": "tools",
                "source_type": "personal-note",
                "origin": "personal",
                "retrieval": {"acquisition": "personal-note"},
                "snapshot_sha256": "sha256:s",
                "evidence_items": [
                    {"evidence_id": "e1", "snapshot_sha256": "sha256:s"},
                    {"evidence_id": "e1", "snapshot_sha256": "sha256:s"},
                ],
            }
            source.write_text(FrontMatter.render(metadata, "body"), encoding="utf-8")
            from tools.paths import RepoPaths
            from tools.validation.resolution import resolve_source

            resolved, errors = resolve_source("dup", RepoPaths(root))
            self.assertIsNotNone(resolved)
            self.assertIn("duplicate_evidence_id", {item["code"] for item in errors})

    def test_owner_vault_reference_resolution(self):
        """AC-F002-005：target 解析为完整 object ref；显式跨 Vault target 拒绝。"""
        # 正常解析：resolved ref 进入 evidence hash 且稳定可复现
        wiki_path, validator = self._fixture(_base_wiki())
        report = validator.validate(wiki_path)
        self.assertTrue(report["valid"], report["errors"])
        # 显式跨 Vault target → cross_vault_reference
        wiki = _base_wiki(
            evidence=[
                {
                    "claim_id": "c1",
                    "claim": "测试论断。",
                    "targets": [
                        {
                            "source_id": "test-source",
                            "evidence_id": "e1",
                            "vault_id": "private",
                        }
                    ],
                    "support": "direct",
                    "supporting_quotes": [{"evidence_id": "e1", "exact": QUOTE_EXACT}],
                }
            ]
        )
        wiki_path, validator = self._fixture(wiki)
        report = validator.validate(wiki_path)
        self.assertFalse(report["valid"])
        self.assertIn("cross_vault_reference", [e["code"] for e in report["errors"]])

    def test_quote_verbatim_matching(self):
        """§6.9：引文必须在 evidence item 范围内逐字命中；规范化容忍排版空白。"""
        # 引文与原文仅空白差异（多个空格 vs 单个）→ 规范化后通过
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        root = Path(directory.name)
        body = "原文包含全角引号“测试”与 多个   空白。"
        _make_source(
            root,
            "test-source",
            body=body,
            evidence_items=[_evidence_item("e1", body, "全角引号“测试”与 多个   空白")],
        )
        wiki = _base_wiki(
            evidence=[
                {
                    "claim_id": "c1",
                    "claim": "测试论断。",
                    "targets": [{"source_id": "test-source", "evidence_id": "e1"}],
                    "support": "direct",
                    "supporting_quotes": [
                        # 与原文仅空白差异（双空格→单空格）：规范化后应逐字命中
                        {"evidence_id": "e1", "exact": "全角引号“测试”与 多个 空白"}
                    ],
                }
            ]
        )
        wiki_path = _write_wiki(root, wiki)
        report = WikiValidator(root).validate(wiki_path)
        self.assertTrue(report["valid"], report["errors"])
        # 引文不在范围内 → quote_mismatch
        wiki = _base_wiki(
            evidence=[
                {
                    "claim_id": "c1",
                    "claim": "测试论断。",
                    "targets": [{"source_id": "test-source", "evidence_id": "e1"}],
                    "support": "direct",
                    "supporting_quotes": [
                        {"evidence_id": "e1", "exact": "完全不存在的引文内容，用于测试"}
                    ],
                }
            ]
        )
        wiki_path = _write_wiki(root, wiki)
        report = WikiValidator(root).validate(wiki_path)
        self.assertFalse(report["valid"])
        self.assertTrue(any(e["code"] == "quote_mismatch" for e in report["errors"]))

    def test_missing_position_returns_selector_unresolved(self):
        """F008：evidence item 缺 position 时返回 selector_unresolved，不回退全文匹配。"""
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        root = Path(directory.name)
        _make_source(
            root,
            "test-source",
            evidence_items=[
                {
                    "id": "e1",
                    "snapshot_sha256": sha256_text(SOURCE_BODY),
                    "selector": {"type": "TextQuoteSelector", "exact": QUOTE_EXACT},
                    "selector_sha256": "sha256:x",
                    "quote_sha256": "sha256:y",
                    # 无 position
                }
            ],
        )
        wiki_path = _write_wiki(root, _base_wiki())
        report = WikiValidator(root).validate(wiki_path)
        self.assertFalse(report["valid"])
        self.assertIn("selector_unresolved", [e["code"] for e in report["errors"]])

    def test_anchor_real_product_integration(self):
        """F001×F002 集成：evidence_anchor 真实产物（evidence_id 键）可被 validator 解析。"""
        from tools.evidence_anchor import EvidenceAnchor
        from tools.ingest.source_ingestor import SourceIngestor

        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        root = Path(directory.name)
        # 用 F001 的真实链路构造 source：ingest → anchor
        ingestor = SourceIngestor(root)
        result = ingestor.preview(
            {
                "source_type": "personal-note",
                "domain": "tools",
                "origin": "personal",
                "body": SOURCE_BODY,
                "source_id": "integrated-source",
            }
        )
        ingestor.apply(result["operation_id"], confirmed=True)
        source_path = (
            root
            / "content"
            / "sources"
            / "tools"
            / "integrated-source"
            / "integrated-source.md"
        )
        snapshot_path = (
            root
            / "archive"
            / "text"
            / f"{strip_sha256_prefix(result['snapshot_sha256'])}.md"
        )
        anchor_service = EvidenceAnchor(root)
        evidence = anchor_service.preview(
            source_path, snapshot_path, QUOTE_EXACT, min_chars=12
        )
        anchor_service.apply(evidence["operation_id"], confirmed=True)
        # wiki 引用该 source（origin: personal → support: personal）
        wiki = _base_wiki(
            id="integrated-wiki",
            sources=["integrated-source"],
            evidence=[
                {
                    "claim_id": "c1",
                    "claim": "集成验证论断。",
                    "targets": [
                        {
                            "source_id": "integrated-source",
                            "evidence_id": evidence["evidence"]["evidence_id"],
                        }
                    ],
                    "support": "personal",
                    "supporting_quotes": [
                        {
                            "evidence_id": evidence["evidence"]["evidence_id"],
                            "exact": QUOTE_EXACT,
                        }
                    ],
                }
            ],
        )
        wiki_path = _write_wiki(root, wiki)
        report = WikiValidator(root).validate(wiki_path)
        self.assertTrue(report["valid"], report["errors"])
        self.assertEqual(report["derived"]["strength"], "personal")
