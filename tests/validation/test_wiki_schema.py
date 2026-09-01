"""F002 schema 层：手写派生字段拒绝/可执行 schema：对应 docs/acceptance/F002-wiki-contract.md 的 AC 条目。"""

from __future__ import annotations

import tempfile
from pathlib import Path

from wiki_fixtures import (
    WikiTestCase,
    _base_wiki,
)

from tools.validation import WikiValidator


class SchemaTests(WikiTestCase):
    def test_private_validator_preserves_explicit_owner_vault(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            wiki = root / "content" / "wiki" / "planned.md"
            wiki.parent.mkdir(parents=True)
            wiki.write_text(
                "---\nschema_version: wiki/v1\nid: planned\ntitle: Planned\ndomain: tools\nkind: reference\nstatus: planned\n---\n",
                encoding="utf-8",
            )
            report = WikiValidator(root, vault_id="team-internal").validate(wiki)
            assert report["object_ref"]["vault_id"] == "team-internal"

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
                self.assertTrue(any(e["path"] == field for e in report["errors"]))

    def test_executable_schema_rejects_unknown_and_wrong_version(self):
        """AC-F002-007：未知字段、错误 schema version、类型错误被字段级拒绝。"""
        # 未知字段 → unknown_field
        wiki_path, validator = self._fixture(_base_wiki(bogus_field=True))
        report = validator.validate(wiki_path)
        self.assertFalse(report["valid"])
        self.assertIn("unknown_field", [e["code"] for e in report["errors"]])
        # 错误 schema version → wrong_schema_version
        wiki_path, validator = self._fixture(_base_wiki(schema_version="wiki/v2"))
        report = validator.validate(wiki_path)
        self.assertFalse(report["valid"])
        self.assertIn("wrong_schema_version", [e["code"] for e in report["errors"]])
        # 类型错误（tags 应为数组）→ schema_invalid + keyword
        wiki_path, validator = self._fixture(_base_wiki(tags="not-a-list"))
        report = validator.validate(wiki_path)
        self.assertFalse(report["valid"])
        self.assertTrue(
            any(
                e["code"] == "schema_invalid" and e.get("keyword") == "type"
                for e in report["errors"]
            )
        )
        # 缺失必填 → schema_invalid
        wiki = _base_wiki()
        del wiki["title"]
        wiki_path, validator = self._fixture(wiki)
        report = validator.validate(wiki_path)
        self.assertFalse(report["valid"])
        self.assertTrue(any(e["code"] == "schema_invalid" for e in report["errors"]))
