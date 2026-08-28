"""doctor 自检：降级显性化（ADR-0011/0012）。"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def _run(root: Path):
    out = subprocess.run(
        [sys.executable, "-m", "tools.doctor", "--root", str(root)],
        capture_output=True,
        text=True,
        cwd=Path(__file__).resolve().parents[1],
    )
    return out.returncode, json.loads(out.stdout)


def _run_gate(root: Path):
    """门禁模式：无 error 时只有一行 stdout，有 error 时报告走 stderr。"""
    out = subprocess.run(
        [sys.executable, "-m", "tools.doctor", "--root", str(root), "--assert-clean"],
        capture_output=True,
        text=True,
        cwd=Path(__file__).resolve().parents[1],
    )
    return out.returncode, out.stdout.strip(), out.stderr


def _write_snapshot(root: Path, body: str) -> Path:
    """按生产约定落一份快照：文件名 == 正文 sha256（tools.common.sha256_text）。"""
    from tools.common import sha256_text

    archive = root / "archive" / "text"
    archive.mkdir(parents=True, exist_ok=True)
    path = archive / f"{sha256_text(body).removeprefix('sha256:')}.md"
    path.write_text(body, encoding="utf-8")
    return path


def test_doctor_reports_missing_index_and_manifest_as_visible_warnings(tmp_path: Path):
    code, report = _run(tmp_path)
    assert code == 0  # 仅 warning 不是 error
    assert report["state"] == "degraded"
    names = {c["name"]: c for c in report["checks"]}
    assert names["public_projection"]["state"] == "warning"  # manifest 缺失可见
    assert names["fts5_index"]["state"] == "warning"  # 索引缺失可见 + next_action
    assert names["fts5_index"]["next_action"].startswith(
        "python -m tools.cli index rebuild"
    )
    assert "qmd" not in names  # qmd 已退役（§1808 修订），不再产生不可消除的告警


def test_doctor_flags_invalid_source_as_error(tmp_path: Path):
    src = tmp_path / "sources" / "tools"
    src.mkdir(parents=True)
    (src / "broken.md").write_text(
        "---\nschema_version: source/v1\nsnapshot_sha256: sha256:deadbeef\n---\n正文\n",
        encoding="utf-8",
    )
    code, report = _run(tmp_path)
    assert code == 2 and report["state"] == "failing"
    names = {c["name"]: c for c in report["checks"]}
    assert names["sources"]["state"] == "error"


def test_doctor_accepts_snapshot_whose_name_matches_its_body(tmp_path: Path):
    _write_snapshot(tmp_path, "# 快照正文\n\n```python\na = 1;\n```\n")
    _, report = _run(tmp_path)
    names = {c["name"]: c for c in report["checks"]}
    assert names["archive_integrity"] == {
        "name": "archive_integrity",
        "state": "ok",
        "checked": 1,
    }


def test_doctor_flags_externally_rewritten_archive_snapshot(tmp_path: Path):
    """任何工具改写不可变快照都必须失败——不依赖"谁改的"。

    这里复现 2026-08-28 的真实事故形态：ruff format 把 Markdown 里的
    `a = 1;` 规范成 `a = 1`，快照正文与文件名 sha256 失配。
    """
    snapshot = _write_snapshot(tmp_path, "```python\na = 1;\n```\n")
    snapshot.write_text("```python\na = 1\n```\n", encoding="utf-8")
    code, report = _run(tmp_path)
    assert code == 2 and report["state"] == "failing"
    names = {c["name"]: c for c in report["checks"]}
    assert names["archive_integrity"]["state"] == "error"
    assert names["archive_integrity"]["drifted"] == [snapshot.name]
    assert names["archive_integrity"]["next_action"].startswith("git checkout --")


def test_doctor_flags_source_snapshot_missing_from_manifest(
    tmp_path: Path, real_import
):
    """正向：source 与 archive 各自自洽、manifest 缺 owner record 时必须报错。

    fixture 走真实导入产出合法 source+快照，再清空 manifest 复现 F001 的缺口形态：
    apply 写完 source 后失败、账目未入账，且操作已 expired 不可重放
    （见 tests/ingest 的 after_source 注入点用例）。
    """
    real_import(tmp_path, "账目缺口验证正文内容", "orphan-note")
    _, report = _run(tmp_path)
    names = {c["name"]: c for c in report["checks"]}
    assert names["sources"]["state"] == "ok"
    assert names["manifest_coverage"]["state"] == "ok"
    assert names["manifest_records"]["state"] == "ok"

    (tmp_path / "archive" / "manifest.jsonl").write_text("", encoding="utf-8")
    code, report = _run(tmp_path)
    assert code == 2 and report["state"] == "failing"
    names = {c["name"]: c for c in report["checks"]}
    assert names["sources"]["state"] == "ok"  # source 自身合法
    assert names["archive_integrity"]["state"] == "ok"  # 快照自证通过
    assert names["manifest_coverage"]["state"] == "error"  # 只有正向账目缺口
    assert names["manifest_coverage"]["unregistered"] == [
        "sources/tools/orphan-note.md"
    ]
    assert "source preview/apply" in names["manifest_coverage"]["next_action"]


def test_doctor_flags_owner_record_pointing_at_a_missing_snapshot(
    tmp_path: Path, real_import
):
    """反向：账目在、快照不在（证据链断裂，evidence 解析不到正文）必须报错。

    删除快照文件不会被 archive_integrity 发现（它只校验在盘文件），也不会被
    manifest_coverage 发现（source 的 snapshot 仍有账）——这正是补反向检查的理由。
    """
    entry = real_import(tmp_path, "反向账目验证正文内容", "record-note")
    (tmp_path / entry["archive_path"]).unlink()
    code, report = _run(tmp_path)
    assert code == 2 and report["state"] == "failing"
    names = {c["name"]: c for c in report["checks"]}
    assert names["archive_integrity"]["state"] == "ok"
    assert names["manifest_coverage"]["state"] == "ok"
    assert names["manifest_records"]["state"] == "error"
    assert names["manifest_records"]["broken"] == [
        {
            "record_id": entry["record_id"],
            "archive_path": entry["archive_path"],
            "reason": "snapshot_missing",
        }
    ]


def test_doctor_flags_owner_record_whose_path_contradicts_its_hash(
    tmp_path: Path, real_import
):
    """反向：record 的 archive_path 与 snapshot_sha256 必须互证（防账目被改写）。"""
    entry = real_import(tmp_path, "账目自证验证正文内容", "twisted-note")
    other = _write_snapshot(tmp_path, "另一份正文\n")
    manifest = tmp_path / "archive" / "manifest.jsonl"
    manifest.write_text(
        json.dumps({**entry, "archive_path": f"archive/text/{other.name}"}) + "\n",
        encoding="utf-8",
    )
    code, report = _run(tmp_path)
    assert code == 2
    names = {c["name"]: c for c in report["checks"]}
    assert names["manifest_records"]["broken"][0]["reason"] == "path_hash_mismatch"


def test_doctor_assert_clean_is_quiet_when_healthy_and_loud_on_error(tmp_path: Path):
    code, stdout, stderr = _run_gate(tmp_path)
    assert code == 0 and stdout == "doctor: degraded (warnings=2)" and stderr == ""

    snapshot = _write_snapshot(tmp_path, "正文\n")
    snapshot.write_text("被改写的正文\n", encoding="utf-8")
    code, stdout, stderr = _run_gate(tmp_path)
    assert code == 2 and stdout == ""
    assert json.loads(stderr)["errors"] == 1
