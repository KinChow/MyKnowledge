"""WikiValidator.validate 报告顶层信封归一测试（加法式，valid 不当 status）。"""

from __future__ import annotations

import tempfile
from pathlib import Path

from tools.validation.validator import WIKI_SCHEMA_VERSION, WikiValidator


def test_validate_report_carries_ok_status_and_keeps_valid_field():
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        # 不存在的路径：校验器仍"跑通"并给出确定性结论 → status ok，valid False。
        report = WikiValidator(root).validate(root / "missing.md")
        assert report["schema_version"] == WIKI_SCHEMA_VERSION
        assert report["status"] == "ok"
        assert report["valid"] is False
        assert report["errors"][0]["code"] == "path_unresolved"
