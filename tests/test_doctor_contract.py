"""doctor 顶层信封归一测试：run_doctor 报告带 schema_version + status=ok。

健康结论（healthy/degraded/failing）与逐项 state 仍是领域字段（加法保留），
status 只表达"自检跑通"这一契约层结论。
"""

from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path

from tools.doctor import run_doctor


def test_run_doctor_report_is_ok_envelope_with_domain_state():
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        subprocess.run(["git", "init", "-q", str(root)], check=True)
        report = run_doctor(root)
        assert report["schema_version"] == "doctor/v1"
        assert report["status"] == "ok"
        # 领域字段仍在：健康结论与逐项检查不被 status 吞掉。
        assert report["health"] in {"healthy", "degraded", "failing"}
        assert isinstance(report["checks"], list)
