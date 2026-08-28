"""doctor 自检：降级显性化（ADR-0011/0012）。"""
from __future__ import annotations
import json, subprocess, sys, tempfile
from pathlib import Path


def _run(root: Path):
    out = subprocess.run([sys.executable, "-m", "tools.doctor", "--root", str(root)],
                         capture_output=True, text=True, cwd=Path(__file__).resolve().parents[1])
    return out.returncode, json.loads(out.stdout)


def test_doctor_reports_missing_index_and_manifest_as_visible_warnings(tmp_path: Path):
    code, report = _run(tmp_path)
    assert code == 0  # 仅 warning 不是 error
    assert report["state"] == "degraded"
    names = {c["name"]: c for c in report["checks"]}
    assert names["public_projection"]["state"] == "warning"      # manifest 缺失可见
    assert names["fts5_index"]["state"] == "warning"             # 索引缺失可见 + next_action
    assert names["fts5_index"]["next_action"].startswith("python -m tools.cli index rebuild")
    assert "qmd" not in names  # qmd 已退役（§1808 修订），不再产生不可消除的告警


def test_doctor_flags_invalid_source_as_error(tmp_path: Path):
    src = tmp_path / "sources" / "tools"; src.mkdir(parents=True)
    (src / "broken.md").write_text("---\nschema_version: source/v1\nsnapshot_sha256: sha256:deadbeef\n---\n正文\n", encoding="utf-8")
    code, report = _run(tmp_path)
    assert code == 2 and report["state"] == "failing"
    names = {c["name"]: c for c in report["checks"]}
    assert names["sources"]["state"] == "error"
