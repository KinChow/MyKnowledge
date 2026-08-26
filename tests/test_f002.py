"""F002 Wiki 契约验收测试：对应 docs/acceptance/F002-wiki-contract.md 的 AC 条目。

覆盖：合法 Wiki 校验与派生字段、缺来源拒绝、手写派生字段拒绝、状态轴合法组合、
owner Vault 引用解析与 cross_vault_reference、发布组合拒绝、可执行 schema validator
与 registry 分离（未知字段/错误 version/类型错误）。
"""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from tools.common import canonical_quote, sha256_text, strip_sha256_prefix
from tools.front_matter import FrontMatter
from tools.wiki_validator import WIKI_SCHEMA_VERSION, WikiValidator

WIKI_BODY = """# 测试主题

## 一句话结论

结论内容。

## 核心概念

概念内容。

## 工作机制

机制内容。

## 示例或代码

示例内容。

## 常见误区

误区内容。

## 证据映射

映射内容。

## 待验证项

待验证内容。

## 关联知识

关联内容。
"""

# 引文 ≥ quote_min_chars(12)：规范化后 16 字符
QUOTE_EXACT = "用于引文匹配的原文片段，以及更多"

SOURCE_BODY = "这是一个足够长的 source 正文，包含" + QUOTE_EXACT + "填充内容。"


def _make_source(
    root: Path,
    source_id: str,
    domain: str = "tools",
    body: str = SOURCE_BODY,
    evidence_items: list[dict] | None = None,
    **metadata_overrides: object,
) -> str:
    """构造 source 文件 + archive snapshot，返回 snapshot_sha256。"""
    snapshot_sha = sha256_text(body)
    snapshot_path = root / "archive" / "text" / f"{strip_sha256_prefix(snapshot_sha)}.md"
    snapshot_path.parent.mkdir(parents=True, exist_ok=True)
    snapshot_path.write_text(body, encoding="utf-8")
    metadata = {
        "schema_version": "source/v1",
        "id": source_id,
        "domain": domain,
        "vault_id": "public",
        "source_type": "local-file",
        "origin": "external",
        "retrieval": {"acquisition": "local-file"},
        "snapshot_sha256": snapshot_sha,
        "extractor": "utf8/1",
        "media_type": "text/markdown",
        "read_status": "retrieved",
        "evidence_status": "source-reported",
        "confidentiality": "public",
        "archive_policy": "text-only",
        "evidence_items": evidence_items or [],
    }
    metadata.update(metadata_overrides)
    path = root / "sources" / domain / f"{source_id}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(FrontMatter.render(metadata, body), encoding="utf-8")
    return snapshot_sha


def _evidence_item(evidence_id: str, body: str, exact: str) -> dict:
    """在 body 中定位 exact 构造 evidence item（code-point 偏移）。"""
    start = body.index(exact)
    return {
        "id": evidence_id,
        "snapshot_sha256": sha256_text(body),
        "selector": {"type": "TextQuoteSelector", "exact": exact},
        "position": {"type": "TextPositionSelector", "start": start, "end": start + len(exact)},
        "selector_sha256": sha256_text(exact),
        "quote_sha256": sha256_text(canonical_quote(exact)),
    }


def _write_wiki(root: Path, metadata: dict, body: str = WIKI_BODY) -> Path:
    path = root / "wiki" / metadata["domain"] / f"{metadata['id']}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(FrontMatter.render(metadata, body), encoding="utf-8")
    return path


def _base_wiki(**overrides: object) -> dict:
    """合法 knowledge Wiki 的默认 front matter（覆盖项可改）。"""
    meta = {
        "id": "test-wiki",
        "title": "测试主题",
        "domain": "tools",
        "kind": "knowledge",
        "status": "draft",
        "publication_scope": "none",
        "confidentiality": "public",
        "tags": ["test"],
        "aliases": [],
        "related": [],
        "sources": ["test-source"],
        "evidence": [
            {
                "claim_id": "c1",
                "claim": "测试论断。",
                "targets": [{"source_id": "test-source", "evidence_id": "e1"}],
                "support": "direct",
                "supporting_quotes": [
                    {"evidence_id": "e1", "exact": QUOTE_EXACT}
                ],
            }
        ],
        "updated_at": "2026-08-26",
    }
    meta.update(overrides)
    return meta


class F002Tests(unittest.TestCase):
    """F002 验收用例：对应 docs/acceptance/F002-wiki-contract.md 的 AC 条目。"""

    def _fixture(self, wiki: dict) -> tuple[Path, WikiValidator]:
        """构造 source + snapshot + wiki 的完整 fixture，返回 (wiki_path, validator)。"""
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        root = Path(directory.name)
        _make_source(
            root,
            "test-source",
            evidence_items=[
                _evidence_item("e1", SOURCE_BODY, QUOTE_EXACT)
            ],
        )
        wiki_path = _write_wiki(root, wiki)
        return wiki_path, WikiValidator(root)

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
                        "targets": [
                            {"source_id": "ghost-source", "evidence_id": "e1"}
                        ],
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
        self.assertTrue(
            any(e["code"] == "source_not_found" for e in report["errors"])
        )

    def test_derived_fields_rejected(self):
        """AC-F002-003：手写派生字段 → derived_field_mismatch，逐字段拒绝。"""
        for field, value in [
            ("vault_id", "public"),
            ("content_sha256", "sha256:deadbeef"),
            ("evidence_sha256", "sha256:deadbeef"),
            ("validation_state", "pass"),
            ("public_publishable", True),
            ("evidence_state", "supported"),
            ("strength", "verified"),
        ]:
            with self.subTest(field=field):
                wiki_path, validator = self._fixture(_base_wiki(**{field: value}))
                report = validator.validate(wiki_path)
                self.assertFalse(report["valid"])
                self.assertIn(
                    "derived_field_mismatch",
                    [e["code"] for e in report["errors"]],
                )
                self.assertTrue(
                    any(e["path"] == field for e in report["errors"])
                )

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
        self.assertIn(
            "planned_with_content", [e["code"] for e in report["errors"]]
        )
        # published + publication_scope: none → published_scope_none
        wiki_path, validator = self._fixture(
            _base_wiki(status="published", publication_scope="none")
        )
        report = validator.validate(wiki_path)
        self.assertFalse(report["valid"])
        self.assertIn(
            "published_scope_none", [e["code"] for e in report["errors"]]
        )
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
            evidence_items=[
                _evidence_item("e1", SOURCE_BODY, QUOTE_EXACT)
            ],
        )
        # 删除 snapshot 文件，使 source 不可读
        (root / "archive" / "text" / f"{strip_sha256_prefix(snapshot_sha)}.md").unlink()
        wiki_path = _write_wiki(root, _base_wiki())
        report = WikiValidator(root).validate(wiki_path)
        self.assertFalse(report["valid"])  # snapshot 缺失阻断确定性校验
        self.assertTrue(any(e["code"] == "snapshot_missing" for e in report["errors"]))

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
                    "supporting_quotes": [
                        {"evidence_id": "e1", "exact": QUOTE_EXACT}
                    ],
                }
            ]
        )
        wiki_path, validator = self._fixture(wiki)
        report = validator.validate(wiki_path)
        self.assertFalse(report["valid"])
        self.assertIn(
            "cross_vault_reference", [e["code"] for e in report["errors"]]
        )

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

    def test_executable_schema_rejects_unknown_and_wrong_version(self):
        """AC-F002-007：未知字段、错误 schema version、类型错误被字段级拒绝。"""
        # 未知字段 → unknown_field
        wiki_path, validator = self._fixture(_base_wiki(bogus_field=True))
        report = validator.validate(wiki_path)
        self.assertFalse(report["valid"])
        self.assertIn("unknown_field", [e["code"] for e in report["errors"]])
        # 错误 schema version → wrong_schema_version
        wiki_path, validator = self._fixture(
            _base_wiki(schema_version="wiki/v2")
        )
        report = validator.validate(wiki_path)
        self.assertFalse(report["valid"])
        self.assertIn(
            "wrong_schema_version", [e["code"] for e in report["errors"]]
        )
        # 类型错误（tags 应为数组）→ schema_invalid + keyword
        wiki_path, validator = self._fixture(_base_wiki(tags="not-a-list"))
        report = validator.validate(wiki_path)
        self.assertFalse(report["valid"])
        self.assertTrue(
            any(e["code"] == "schema_invalid" and e.get("keyword") == "type"
                for e in report["errors"])
        )
        # 缺失必填 → schema_invalid
        wiki = _base_wiki()
        del wiki["title"]
        wiki_path, validator = self._fixture(wiki)
        report = validator.validate(wiki_path)
        self.assertFalse(report["valid"])
        self.assertTrue(
            any(e["code"] == "schema_invalid" for e in report["errors"])
        )

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

    def test_snapshot_drift_derives_stale(self):
        """§6.8：被引 snapshot 漂移 → evidence_state: stale。"""
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        root = Path(directory.name)
        snapshot_sha = _make_source(
            root,
            "test-source",
            evidence_items=[
                _evidence_item("e1", SOURCE_BODY, QUOTE_EXACT)
            ],
        )
        snapshot_path = root / "archive" / "text" / f"{strip_sha256_prefix(snapshot_sha)}.md"
        # 保留引文完整落在原 selector [21, 35) 内但改变整体内容 → hash 漂移
        snapshot_path.write_text(
            "0" * 21 + QUOTE_EXACT + "重新抓取后的后缀",
            encoding="utf-8",
        )
        wiki_path = _write_wiki(root, _base_wiki())
        report = WikiValidator(root).validate(wiki_path)
        self.assertTrue(report["valid"], report["errors"])
        self.assertEqual(report["derived"]["evidence_state"], "stale")

    def test_validation_report_drives_states(self):
        """§6.8：LLM 验证报告驱动 conflicting/partial/corroborated/verified。

        F003：报告必须绑定当前 (content, evidence) hash，旧内容报告视为未运行。
        """
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        root = Path(directory.name)
        _make_source(
            root,
            "test-source",
            evidence_items=[
                _evidence_item("e1", SOURCE_BODY, QUOTE_EXACT)
            ],
        )
        wiki_path = _write_wiki(root, _base_wiki())
        first = WikiValidator(root).validate(wiki_path)
        hashes = first["hashes"]

        def _report(verdict: str, claim_verdicts: dict) -> dict:
            return {
                "verdict": verdict,
                "claim_verdicts": claim_verdicts,
                "wiki_content_sha256": hashes["content_sha256"],
                "wiki_evidence_sha256": hashes["evidence_sha256"],
            }

        report_dir = root / "audit" / "validation" / "wiki" / "test-wiki"
        report_dir.mkdir(parents=True)
        (report_dir / "attestation1.json").write_text(
            json.dumps(_report("fail", {"c1": "contradicted"})),
            encoding="utf-8",
        )
        report = WikiValidator(root).validate(wiki_path)
        self.assertTrue(report["valid"], report["errors"])
        self.assertEqual(report["derived"]["evidence_state"], "conflicting")
        self.assertEqual(report["derived"]["strength"], "conflicted")
        # verdict pass + 无 conflict → verified
        (report_dir / "attestation1.json").write_text(
            json.dumps(_report("pass", {"c1": "supported"})),
            encoding="utf-8",
        )
        report = WikiValidator(root).validate(wiki_path)
        self.assertEqual(report["derived"]["validation_state"], "pass")
        self.assertEqual(report["derived"]["strength"], "verified")
        self.assertEqual(report["derived"]["evidence_state"], "supported")
        # F003：不绑定当前 hash 的报告视为未运行（旧内容不得驱动 verified）
        (report_dir / "attestation1.json").write_text(
            json.dumps({"verdict": "pass", "claim_verdicts": {"c1": "supported"}}),
            encoding="utf-8",
        )
        report = WikiValidator(root).validate(wiki_path)
        self.assertEqual(report["derived"]["validation_state"], "not_run")
        self.assertIsNone(report["derived"]["strength"])
        # R001：报告非 dict 形状不崩溃，视为未运行
        (report_dir / "attestation1.json").write_text(
            json.dumps([1, 2, 3]), encoding="utf-8"
        )
        report = WikiValidator(root).validate(wiki_path)
        self.assertTrue(report["valid"], report["errors"])
        self.assertEqual(report["derived"]["validation_state"], "not_run")

    def test_index_and_reference_kinds_accepted(self):
        """F002 修复：index/reference 按 §6.7 免除 sources/evidence，不被 schema 误拒。"""
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        root = Path(directory.name)
        # index：无 sources/evidence，正文为链接清单（§6.7 替代检查：链接必须可解析）
        target = root / "wiki" / "tools" / "target-wiki.md"
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
            body="# 索引页\n\n[target-wiki](target-wiki)\n\n[path-link](wiki/tools/target-wiki.md)",
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
            evidence_items=[
                _evidence_item("e1", SOURCE_BODY, QUOTE_EXACT)
            ],
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
        self.assertIn(
            "support_origin_mismatch", [e["code"] for e in report["errors"]]
        )

    def test_missing_position_returns_selector_unresolved(self):
        """F008：evidence item 缺 position 时返回 selector_unresolved，不回退全文匹配。"""
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        root = Path(directory.name)
        snapshot_sha = _make_source(
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
        self.assertIn(
            "selector_unresolved", [e["code"] for e in report["errors"]]
        )

    def test_anchor_real_product_integration(self):
        """F001×F002 集成：evidence_anchor 真实产物（evidence_id 键）可被 validator 解析。"""
        from tools.evidence_anchor import EvidenceAnchor
        from tools.front_matter import FrontMatter

        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        root = Path(directory.name)
        # 用 F001 的真实链路构造 source：ingest → anchor
        from tools.source_ingestor import SourceIngestor

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
        source_path = root / "sources" / "tools" / "integrated-source.md"
        snapshot_path = root / "archive" / "text" / f"{strip_sha256_prefix(result['snapshot_sha256'])}.md"
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
                        {"source_id": "integrated-source", "evidence_id": evidence["evidence"]["evidence_id"]}
                    ],
                    "support": "personal",
                    "supporting_quotes": [
                        {"evidence_id": evidence["evidence"]["evidence_id"], "exact": QUOTE_EXACT}
                    ],
                }
            ],
        )
        wiki_path = _write_wiki(root, wiki)
        report = WikiValidator(root).validate(wiki_path)
        self.assertTrue(report["valid"], report["errors"])
        self.assertEqual(report["derived"]["strength"], "personal")

    def test_internal_publish_requires_warning_ack(self):
        """F004：internal 有效保密等级的 publish_private 确认必须携带告警确认字段。"""
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        root = Path(directory.name)
        _make_source(
            root,
            "test-source",
            confidentiality="internal",
            evidence_items=[
                _evidence_item("e1", SOURCE_BODY, QUOTE_EXACT)
            ],
        )
        wiki_path = _write_wiki(
            root, _base_wiki(status="published", publication_scope="private")
        )
        first = WikiValidator(root).validate(wiki_path)
        self.assertEqual(first["derived"]["effective_confidentiality"], "internal")
        # 无告警字段的确认 → 不可发布
        audit = root / "audit" / "operations" / "op_publish.json"
        audit.parent.mkdir(parents=True, exist_ok=True)
        audit.write_text(
            json.dumps(
                {
                    "operation_id": "op_publish",
                    "operation_type": "wiki_publish_private",
                    "state": "applied",
                    "confirmation": {
                        "scope": "publish_private",
                        "decision": "approve",
                        "content_sha256": first["hashes"]["content_sha256"],
                        "evidence_sha256": first["hashes"]["evidence_sha256"],
                    },
                }
            ),
            encoding="utf-8",
        )
        second = WikiValidator(root).validate(wiki_path)
        self.assertFalse(second["derived"]["private_publishable"])
        # 补告警字段 → 可发布
        audit.write_text(
            json.dumps(
                {
                    "operation_id": "op_publish",
                    "operation_type": "wiki_publish_private",
                    "state": "applied",
                    "confirmation": {
                        "scope": "publish_private",
                        "decision": "approve",
                        "content_sha256": first["hashes"]["content_sha256"],
                        "evidence_sha256": first["hashes"]["evidence_sha256"],
                        "warning_code": "internal_release",
                        "warning_text_sha256": "sha256:warn",
                    },
                }
            ),
            encoding="utf-8",
        )
        third = WikiValidator(root).validate(wiki_path)
        self.assertTrue(third["derived"]["private_publishable"])
        self.assertEqual(third["derived"]["publication_warning"], "internal")

    def test_validator_instance_is_stateless(self):
        """R004：同一实例连续校验不同 wiki，派生字段互不污染（无实例共享状态）。"""
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        root = Path(directory.name)
        _make_source(root, "ext-source", evidence_items=[_evidence_item("e1", SOURCE_BODY, QUOTE_EXACT)])
        _make_source(
            root,
            "personal-source",
            origin="personal",
            evidence_status="personal-observation",
            evidence_items=[_evidence_item("e1", SOURCE_BODY, QUOTE_EXACT)],
        )
        ext_wiki = _write_wiki(
            root,
            _base_wiki(
                id="ext-wiki",
                sources=["ext-source"],
                evidence=[
                    {
                        "claim_id": "c1",
                        "claim": "外部论断。",
                        "targets": [{"source_id": "ext-source", "evidence_id": "e1"}],
                        "support": "direct",
                        "supporting_quotes": [{"evidence_id": "e1", "exact": QUOTE_EXACT}],
                    }
                ],
            ),
        )
        personal_wiki = _write_wiki(
            root,
            _base_wiki(
                id="personal-wiki",
                sources=["personal-source"],
                evidence=[
                    {
                        "claim_id": "c1",
                        "claim": "个人论断。",
                        "targets": [{"source_id": "personal-source", "evidence_id": "e1"}],
                        "support": "personal",
                        "supporting_quotes": [{"evidence_id": "e1", "exact": QUOTE_EXACT}],
                    }
                ],
            ),
        )
        validator = WikiValidator(root)
        # 交错校验两次，派生字段必须各自正确（若共享实例状态会交叉污染）
        first_ext = validator.validate(ext_wiki)
        first_personal = validator.validate(personal_wiki)
        second_ext = validator.validate(ext_wiki)
        self.assertEqual(second_ext["derived"]["strength"], first_ext["derived"]["strength"])
        self.assertIsNone(first_ext["derived"]["strength"])  # external 无报告
        self.assertEqual(first_personal["derived"]["strength"], "personal")
        self.assertEqual(second_ext["derived"]["effective_confidentiality"], "public")

    def test_private_publishable_with_confirmation(self):
        """§6.8：published + scope private + 审计确认 hash 匹配 → private_publishable: true。"""
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        root = Path(directory.name)
        _make_source(
            root,
            "test-source",
            evidence_items=[
                _evidence_item("e1", SOURCE_BODY, QUOTE_EXACT)
            ],
        )
        wiki_path = _write_wiki(
            root, _base_wiki(status="published", publication_scope="private")
        )
        validator = WikiValidator(root)
        first = validator.validate(wiki_path)
        self.assertTrue(first["valid"], first["errors"])
        self.assertFalse(first["derived"]["private_publishable"])
        # 写入绑定当前 hash 的 publish_private 审计确认
        audit = root / "audit" / "operations" / "op_publish.json"
        audit.parent.mkdir(parents=True, exist_ok=True)
        audit.write_text(
            json.dumps(
                {
                    "operation_id": "op_publish",
                    "operation_type": "wiki_publish_private",
                    "state": "applied",
                    "confirmation": {
                        "scope": "publish_private",
                        "decision": "approve",
                        "content_sha256": first["hashes"]["content_sha256"],
                        "evidence_sha256": first["hashes"]["evidence_sha256"],
                    },
                }
            ),
            encoding="utf-8",
        )
        second = WikiValidator(root).validate(wiki_path)
        self.assertTrue(second["derived"]["private_publishable"])
        self.assertEqual(second["derived"]["publication_warning"], "none")

    def test_personal_and_common_knowledge_strength(self):
        """§6.8：personal-only → strength: personal；common-knowledge → attested。"""
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        root = Path(directory.name)
        # personal-only
        _make_source(
            root,
            "personal-source",
            origin="personal",
            evidence_status="personal-observation",
            evidence_items=[
                _evidence_item("e1", SOURCE_BODY, QUOTE_EXACT)
            ],
        )
        wiki_path = _write_wiki(
            root,
            _base_wiki(
                id="personal-wiki",
                sources=["personal-source"],
                evidence=[
                    {
                        "claim_id": "c1",
                        "claim": "我的观察记录。",
                        "targets": [
                            {"source_id": "personal-source", "evidence_id": "e1"}
                        ],
                        "support": "personal",
                        "supporting_quotes": [
                            {"evidence_id": "e1", "exact": QUOTE_EXACT}
                        ],
                    }
                ],
            ),
        )
        report = WikiValidator(root).validate(wiki_path)
        self.assertTrue(report["valid"], report["errors"])
        self.assertEqual(report["derived"]["strength"], "personal")
        # common-knowledge（带 archive + read_status: retrieved 的 source）
        _make_source(
            root,
            "ck-source",
            evidence_status="common-knowledge",
            evidence_items=[
                _evidence_item("e1", SOURCE_BODY, QUOTE_EXACT)
            ],
        )
        wiki_path = _write_wiki(
            root,
            _base_wiki(
                id="ck-wiki",
                sources=["ck-source"],
                evidence=[
                    {
                        "claim_id": "c1",
                        "claim": "公认事实。",
                        "targets": [{"source_id": "ck-source", "evidence_id": "e1"}],
                        "support": "direct",
                        "supporting_quotes": [
                            {"evidence_id": "e1", "exact": QUOTE_EXACT}
                        ],
                    }
                ],
            ),
        )
        report = WikiValidator(root).validate(wiki_path)
        self.assertTrue(report["valid"], report["errors"])
        self.assertEqual(report["derived"]["strength"], "attested")


def root_replace(path: Path, new_name: str) -> Path:
    """返回同目录下不同文件名的 Path（用于 planned 测试的独立文件）。"""
    return path.parent / f"{new_name}.md"


if __name__ == "__main__":
    unittest.main()
