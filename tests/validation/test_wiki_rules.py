"""F002 domain rule 层：状态组合/kind 分支/矩阵：对应 docs/acceptance/F002-wiki-contract.md 的 AC 条目。"""

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
    root_replace,
)

from tools.common import strip_sha256_prefix
from tools.front_matter import FrontMatter
from tools.validation import WikiValidator


class RulesTests(WikiTestCase):
    def test_report_is_json_serializable(self):
        """校验报告必须能 json.dumps：CLI 与审计产物都要序列化它。

        实测事故（2026-08-29 首次校验真实 wiki）：resolution.sources[*].path
        存的是 PosixPath，`tools.cli validate` 在打印报告时抛 TypeError——
        此前所有测试都只读字段、从不序列化，所以一路没暴露。
        """
        import json

        wiki_path, validator = self._fixture(_base_wiki())
        report = validator.validate(wiki_path)
        self.assertTrue(report["valid"], report["errors"])
        payload = json.dumps(report, ensure_ascii=False)  # 不得抛 TypeError
        self.assertIn("test-source", payload)
        self.assertIsInstance(
            report["resolution"]["sources"]["test-source"]["path"], str
        )

    def test_missing_source_rejected(self):
        """AC-F002-002：kind: knowledge 没有有效 Source → 字段级错误。"""
        wiki_path, validator = self._fixture(_base_wiki(sources=[]))
        report = validator.validate(wiki_path)
        self.assertFalse(report["valid"])
        self.assertEqual(report["errors"][0]["code"], "source_missing")
        self.assertEqual(report["errors"][0]["path"], "sources")
        # 引用了不存在的 source（sources 与 target 一致 → source_not_found）
        wiki_path, validator = self._fixture(
            _base_wiki(
                sources=["ghost-source"],
                evidence=[
                    {
                        "claim_id": "c1",
                        "claim": "测试论断。",
                        "targets": [{"source_id": "ghost-source", "evidence_id": "e1"}],
                        "support": "direct",
                        "supporting_quotes": [
                            {"evidence_id": "e1", "exact": QUOTE_EXACT}
                        ],
                    }
                ],
            )
        )
        report = validator.validate(wiki_path)
        self.assertFalse(report["valid"])
        self.assertTrue(any(e["code"] == "source_not_found" for e in report["errors"]))

    def test_status_axis_combinations(self):
        """AC-F002-004：状态轴合法组合通过、非法组合逐字段拒绝。"""
        # planned：只允许五字段、无正文 → 合法
        wiki_path, validator = self._fixture(
            _base_wiki(
                id="planned-wiki",
                status="planned",
                sources=[],
                evidence=[],
            )
        )
        planned_path = root_replace(wiki_path, "planned-wiki")
        planned_path.write_text(
            FrontMatter.render(
                {
                    "id": "planned-wiki",
                    "title": "待写",
                    "domain": "tools",
                    "kind": "knowledge",
                    "status": "planned",
                },
                "",
            ),
            encoding="utf-8",
        )
        report = validator.validate(planned_path)
        self.assertTrue(report["valid"], report["errors"])
        # planned 带 evidence → planned_with_content
        wiki_path, validator = self._fixture(_base_wiki(status="planned"))
        report = validator.validate(wiki_path)
        self.assertFalse(report["valid"])
        self.assertIn("planned_with_content", [e["code"] for e in report["errors"]])
        # published + publication_scope: none → published_scope_none
        wiki_path, validator = self._fixture(
            _base_wiki(status="published", publication_scope="none")
        )
        report = validator.validate(wiki_path)
        self.assertFalse(report["valid"])
        self.assertIn("published_scope_none", [e["code"] for e in report["errors"]])
        # published 无审计确认 → private_publishable: false（派生，不阻断校验）
        wiki_path, validator = self._fixture(
            _base_wiki(status="published", publication_scope="private")
        )
        report = validator.validate(wiki_path)
        self.assertTrue(report["valid"], report["errors"])
        self.assertFalse(report["derived"]["private_publishable"])
        # availability: unavailable → evidence_state: unresolved（不是 missing）
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        root = Path(directory.name)
        snapshot_sha = _make_source(
            root,
            "test-source",
            evidence_items=[_evidence_item("e1", SOURCE_BODY, QUOTE_EXACT)],
        )
        # 删除 snapshot 文件，使 source 不可读
        (root / "archive" / "text" / f"{strip_sha256_prefix(snapshot_sha)}.md").unlink()
        wiki_path = _write_wiki(root, _base_wiki())
        report = WikiValidator(root).validate(wiki_path)
        self.assertFalse(report["valid"])  # snapshot 缺失阻断确定性校验
        self.assertTrue(any(e["code"] == "snapshot_missing" for e in report["errors"]))

    def test_publication_combo_rejected(self):
        """AC-F002-006：手写发布字段与非法发布组合 → 字段级拒绝。"""
        for field, value in [
            ("public_release", True),
            ("public_publishable", True),
            ("private_publishable", True),
            ("publication_warning", "internal"),
        ]:
            with self.subTest(field=field):
                wiki_path, validator = self._fixture(_base_wiki(**{field: value}))
                report = validator.validate(wiki_path)
                self.assertFalse(report["valid"])
                self.assertIn(
                    "derived_field_mismatch", [e["code"] for e in report["errors"]]
                )
                self.assertTrue(any(e["path"] == field for e in report["errors"]))

    def test_index_and_reference_kinds_accepted(self):
        """F002 修复：index/reference 按 §6.7 免除 sources/evidence，不被 schema 误拒。"""
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        root = Path(directory.name)
        # index：无 sources/evidence，正文为链接清单（§6.7 替代检查：链接必须可解析）
        target = root / "content" / "wiki" / "tools" / "target-wiki.md"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(
            "---\nid: target-wiki\ntitle: 目标\ndomain: tools\nkind: knowledge\n"
            "status: planned\n---\n",
            encoding="utf-8",
        )
        index = _write_wiki(
            root,
            {
                "id": "index-page",
                "title": "索引页",
                "domain": "tools",
                "kind": "index",
                "status": "draft",
                "publication_scope": "none",
                "confidentiality": "public",
                "tags": [],
                "aliases": [],
                "related": [],
                "sources": [],
                "evidence": [],
                "updated_at": "2026-08-26",
            },
            body="# 索引页\n\n[target-wiki](target-wiki)\n\n[path-link](content/wiki/tools/target-wiki.md)",
        )
        report = WikiValidator(root).validate(index)
        self.assertTrue(report["valid"], report["errors"])
        self.assertEqual(report["derived"]["strength"], "index")
        # 失效链接 → link_unresolved 阻断（§6.7 硬性要求）
        broken = _write_wiki(
            root,
            {
                "id": "index-broken",
                "title": "坏索引",
                "domain": "tools",
                "kind": "index",
                "status": "draft",
                "publication_scope": "none",
                "confidentiality": "public",
                "tags": [],
                "aliases": [],
                "related": [],
                "sources": [],
                "evidence": [],
                "updated_at": "2026-08-26",
            },
            body="# 索引页\n\n[ghost](ghost)",
        )
        report = WikiValidator(root).validate(broken)
        self.assertFalse(report["valid"])
        self.assertIn("link_unresolved", [e["code"] for e in report["errors"]])
        # reference：有 source、无 evidence
        _make_source(root, "ref-source")
        reference = _write_wiki(
            root,
            {
                "id": "reference-page",
                "title": "参考清单",
                "domain": "tools",
                "kind": "reference",
                "status": "draft",
                "publication_scope": "none",
                "confidentiality": "public",
                "tags": [],
                "aliases": [],
                "related": [],
                "sources": ["ref-source"],
                "evidence": [],
                "updated_at": "2026-08-26",
            },
            body="# 参考清单\n\n条目列表",
        )
        report = WikiValidator(root).validate(reference)
        self.assertTrue(report["valid"], report["errors"])
        self.assertEqual(report["derived"]["strength"], "reference")

    def test_support_origin_matrix_enforced(self):
        """F005：support: direct 不允许 origin: personal 的 source（§6.5 矩阵）。"""
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        root = Path(directory.name)
        _make_source(
            root,
            "personal-source",
            origin="personal",
            evidence_status="personal-observation",
            evidence_items=[_evidence_item("e1", SOURCE_BODY, QUOTE_EXACT)],
        )
        wiki = _base_wiki(
            sources=["personal-source"],
            evidence=[
                {
                    "claim_id": "c1",
                    "claim": "我的观察。",
                    "targets": [{"source_id": "personal-source", "evidence_id": "e1"}],
                    "support": "direct",  # 非法：personal source 只允许 personal/inferred
                    "supporting_quotes": [{"evidence_id": "e1", "exact": QUOTE_EXACT}],
                }
            ],
        )
        wiki_path = _write_wiki(root, wiki)
        report = WikiValidator(root).validate(wiki_path)
        self.assertFalse(report["valid"])
        self.assertIn("support_origin_mismatch", [e["code"] for e in report["errors"]])
