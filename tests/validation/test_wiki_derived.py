"""F002 派生字段计算与确认：对应 docs/acceptance/F002-wiki-contract.md 的 AC 条目。"""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from tools.common import canonical_quote, sha256_text, strip_sha256_prefix
from tools.front_matter import FrontMatter
from tools.validation import WIKI_SCHEMA_VERSION, WikiValidator
from wiki_fixtures import (
    QUOTE_EXACT,
    SOURCE_BODY,
    WIKI_BODY,
    WikiTestCase,
    _base_wiki,
    _evidence_item,
    _install_spec_doc,
    _make_source,
    _write_wiki,
    root_replace,
)


class DerivedTests(WikiTestCase):
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

        F003：报告必须绑定当前 (content, evidence) hash + ruleset_sha256
        （真实产物格式 validation-report/v1）；旧内容/旧格式报告视为未运行。
        """
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        root = Path(directory.name)
        _install_spec_doc(root)
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
        from tools.validation.ruleset import load_ruleset

        current_ruleset = load_ruleset(root)

        def _report(verdict: str, claim_verdicts: dict) -> dict:
            return {
                "schema_version": "validation-report/v1",
                "verdict": verdict,
                "claim_verdicts": claim_verdicts,
                "ruleset_sha256": current_ruleset["ruleset_sha256"],
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
        # AC-F003-015：规则集变化只标 stale_ruleset，不使人工确认失效
        (report_dir / "attestation1.json").write_text(
            json.dumps(
                {
                    **_report("pass", {"c1": "supported"}),
                    "ruleset_sha256": "sha256:" + "0" * 64,
                }
            ),
            encoding="utf-8",
        )
        report = WikiValidator(root).validate(wiki_path)
        self.assertEqual(report["derived"]["validation_state"], "stale_ruleset")
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


