"""F010 R5b：本人综合（synthesis/personal claim）的端到端证据（2026-08-28）。

R5b 决策：检索确认无外部出处的个人总结，迁移终点是 wiki 层——
以 personal-note source 作为 provenance，claim 用 support: personal，
evidence_state 表达映射完整性、strength 降级 personal，不因证据门禁阻断。
"""
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from tests.wiki_fixtures import (
    QUOTE_EXACT,
    SOURCE_BODY,
    _base_wiki,
    _evidence_item,
    _make_source,
    _write_wiki,
)
from tools.validation import WikiValidator


class PersonalSynthesisTests(unittest.TestCase):
    def test_personal_note_synthesis_claim_is_valid_and_degrades_strength(self):
        import tempfile
        from pathlib import Path
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            _make_source(
                root,
                "my-synthesis",
                source_type="personal-note",
                origin="personal",
                retrieval={"acquisition": "personal-note"},
                evidence_items=[_evidence_item("e1", SOURCE_BODY, QUOTE_EXACT)],
            )
            wiki = _base_wiki(
                sources=["my-synthesis"],
                evidence=[{
                    "claim_id": "c1",
                    "claim": "本人综合的结论。",
                    "targets": [{"source_id": "my-synthesis", "evidence_id": "e1"}],
                    "support": "personal",
                    "supporting_quotes": [{"evidence_id": "e1", "exact": QUOTE_EXACT}],
                }],
            )
            path = _write_wiki(root, wiki)
            report = WikiValidator(root).validate(path)
            self.assertTrue(report["valid"], report["errors"])
            # evidence_state 表达映射完整性（引文定位成功 -> supported）；
            # personal 降级体现在 strength（§6.8：全 personal 支撑 -> personal）
            self.assertEqual(report["derived"]["evidence_state"], "supported")
            self.assertEqual(report["derived"]["strength"], "personal")
            # personal strength 不在证据阻断集合：published 路径不被证据门禁挡住
            self.assertNotIn(report["derived"]["evidence_state"],
                             {"missing", "partial", "conflicting", "unresolved", "stale"})


if __name__ == "__main__":
    unittest.main()
