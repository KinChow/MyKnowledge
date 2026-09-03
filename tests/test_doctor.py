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


def test_manifest_records_tolerate_historical_archive_prefix(tmp_path: Path):
    """LAY-004：批次 3 布局下，账目里写着 `archive/` 的历史路径仍必须解析成功。

    fixture 取真实产物——本仓库 `archive/manifest.jsonl` 的全部账目行与它们指向的
    真实快照，按 §4.6 目标布局搬到 `ledger/archive/` 下。账目 append-only 不可改写，
    若按记录原样拼路径，迁移当天全部历史账目会一起报 `snapshot_missing`，把一次
    目录搬迁伪装成数据丢失。
    """
    import shutil

    from tools.doctor import _check_manifest_records
    from tools.paths import RepoPaths

    repo = Path(__file__).resolve().parents[1]
    real_manifest = repo / "archive" / "manifest.jsonl"
    lines = [ln for ln in real_manifest.read_text(encoding="utf-8").splitlines() if ln]
    assert len(lines) > 100, "fixture 必须是真实全量账目，不是构造的小样本"

    # 账目放在当前布局认定的位置（`paths.manifest` 会随批次 3 一起前移，用例不锁死它），
    # 快照只放在 §4.6 的目标位置——这正是"账目写历史前缀、实物在新位置"的迁移态。
    manifest_path = RepoPaths(tmp_path).manifest
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(real_manifest, manifest_path)
    target_text = tmp_path / "ledger" / "archive" / "text"
    target_text.mkdir(parents=True)
    for entry in (json.loads(ln) for ln in lines):
        written = str(entry["archive_path"])
        assert written.startswith("archive/"), "本用例的前提是账目里是历史前缀"
        src = repo / written
        if src.is_file():
            shutil.copy2(src, target_text / src.name)

    state, fields = _check_manifest_records(tmp_path)
    assert fields["checked"] == len(lines)
    assert state == "ok", fields.get("broken")


def test_record_path_resolution_prefers_the_current_layout(tmp_path: Path):
    """历史目录残留时，解析必须落在当前布局那一份，不能悄悄读回旧文件。"""
    from tools.paths import RepoPaths

    for prefix in ("archive/text", "ledger/archive/text"):
        (tmp_path / prefix).mkdir(parents=True)
        (tmp_path / prefix / "x.md").write_text(prefix, encoding="utf-8")

    resolved = RepoPaths(tmp_path).resolve_record_path("archive/text/x.md")
    assert resolved == tmp_path / "ledger" / "archive" / "text" / "x.md"
    assert RepoPaths(tmp_path).resolve_record_path("archive/text/missing.md") is None


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
    src = tmp_path / "content" / "sources" / "tools"
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
        "content/sources/tools/orphan-note/orphan-note.md"
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


def test_doctor_flags_a_stranded_projection_rebuild(tmp_path: Path):
    """canonical 已提交但派生重建失败的 operation 必须被点名（recover 不会自愈）。

    实测动机：这种滞留态对其余检查全不可见——projection 与索引一起停在旧版本，
    `fts5_index` 比的是"索引 vs projection"故报 ok，doctor 会说 healthy，而新
    内容在检索里查不到。next_action 必须是能真正执行的命令。
    """
    from tools.write_operation import WriteOperation

    service = WriteOperation(tmp_path)
    first = service.preview(
        {"content/wiki/a.md": "---\nschema_version: wiki/v1\nid: a\n---\n一\n"}
    )
    assert service.apply(first["operation_id"], confirmed=True)["state"] == "applied"
    _, baseline = _run(tmp_path)
    assert baseline["state"] == "healthy"  # 基线干净，排除其它噪声

    def boom(_record):
        raise OSError("index rebuild failed")

    stuck = WriteOperation(tmp_path, projection_rebuilder=boom)
    second = stuck.preview(
        {"content/wiki/b.md": "---\nschema_version: wiki/v1\nid: b\n---\n二\n"}
    )
    operation_id = second["operation_id"]
    assert stuck.apply(operation_id, confirmed=True)["state"] == "applied_index_pending"

    code, report = _run(tmp_path)
    assert code == 0  # 派生数据滞后是降级，不是内容损坏
    names = {c["name"]: c for c in report["checks"]}
    assert names["pending_operations"]["state"] == "warning"
    assert names["pending_operations"]["pending"] == [operation_id]
    assert names["fts5_index"]["state"] == "ok"  # 正是这条看不见滞留
    assert (
        names["pending_operations"]["next_action"]
        == f"python -m tools.cli write --recover {operation_id}"
    )

    assert service.recover(operation_id)["state"] == "applied"
    _, healed = _run(tmp_path)
    assert healed["state"] == "healthy"


def test_doctor_assert_clean_is_quiet_when_healthy_and_loud_on_error(tmp_path: Path):
    code, stdout, stderr = _run_gate(tmp_path)
    assert code == 0 and stdout == "doctor: degraded (warnings=2)" and stderr == ""

    snapshot = _write_snapshot(tmp_path, "正文\n")
    snapshot.write_text("被改写的正文\n", encoding="utf-8")
    code, stdout, stderr = _run_gate(tmp_path)
    assert code == 2 and stdout == ""
    assert json.loads(stderr)["errors"] == 1


def test_doctor_enumerates_domains_not_on_the_historical_allowlist(
    tmp_path: Path, real_import
):
    """域名不得硬编码：新增 domain 必须被枚举到，否则 checked 少算而仍报 ok。"""
    real_import(tmp_path, "新域枚举验证正文内容", "new-domain-note")
    moved = tmp_path / "content" / "sources" / "brand-new-domain"
    moved.mkdir(parents=True)
    (
        tmp_path
        / "content"
        / "sources"
        / "tools"
        / "new-domain-note"
        / "new-domain-note.md"
    ).rename(moved / "new-domain-note.md")
    _, report = _run(tmp_path)
    names = {c["name"]: c for c in report["checks"]}
    assert names["sources"]["checked"] == 1  # 落在 allowlist 之外的域仍被检查
    assert names["manifest_coverage"]["checked"] == 1


def test_doctor_fails_closed_when_content_exists_but_enumeration_is_empty(
    tmp_path: Path, real_import
):
    """静默归零的回归锁：布局与 paths.py 不一致时，「检查了 0 个」必须是 error。

    实测（2026-09-01）：批次 2 之前的实现里，sources/ 一旦搬走，_check_sources 与
    _check_manifest_coverage 双双返回 ok/checked=0，doctor 仍 healthy——而验收标准
    正是"doctor 无新增告警"，等于空洞门禁。这里模拟反向漂移（内容退回 §4.6 的
    历史位置而代码已指向 content/），两个方向共用同一条判据。
    """
    real_import(tmp_path, "静默归零验证正文内容", "silent-zero-note")
    (tmp_path / "content" / "sources").rename(tmp_path / "sources")

    code, report = _run(tmp_path)
    assert code == 2 and report["state"] == "failing"
    names = {c["name"]: c for c in report["checks"]}
    for name in ("sources", "manifest_coverage"):
        assert names[name]["state"] == "error", name
        assert names[name]["reason"] == "layout_mismatch"
        assert "§4.6" in names[name]["next_action"]

    gate_code, stdout, stderr = _run_gate(tmp_path)
    assert gate_code == 2 and stdout == ""
    assert json.loads(stderr)["errors"] >= 2


def test_doctor_lists_overdue_working_notes_and_never_touches_them(tmp_path: Path):
    """LAY-003：`content/working/` TTL 到期只产生按域分组的清单（report-only）。

    两个不变量同时锁住：到期是 warning 而不是 error（不阻断提交），并且文件
    逐字节不变——`ttl_action: report-only` 的含义是工具永不代替人删除。
    """
    working = tmp_path / "content" / "working" / "tools"
    working.mkdir(parents=True)
    note = working / "scratch.md"
    note.write_text(
        "---\nsource_ref: content/sources/tools/x.md\ncreated_at: '2020-01-01'\n---\n草稿\n",
        encoding="utf-8",
    )
    before = note.read_bytes()

    code, report = _run(tmp_path)
    assert code == 0  # 到期不是错误
    check = {c["name"]: c for c in report["checks"]}["working_ttl"]
    assert check["state"] == "warning"
    assert check["ttl_action"] == "report-only"
    assert check["reason"] == "working_ttl_exceeded"
    assert list(check["overdue"]) == ["tools"]  # 按域分组
    entry = check["overdue"]["tools"][0]
    assert entry["path"] == "content/working/tools/scratch.md"
    assert entry["basis"] == "created_at"
    assert note.read_bytes() == before


def test_doctor_working_ttl_groups_by_full_parent_path(tmp_path: Path):
    """working 层多级目录时分组键取完整父路径，不把首段当成 domain。

    存量 161 篇按「升级档位/域」两级放置（`content/working/a-external/computer-science/`），
    只取首段会把分诊目录 `a-external` 报成 domain——那是错报，不是简化。
    """
    working = tmp_path / "content" / "working" / "a-external" / "computer-science"
    working.mkdir(parents=True)
    (working / "gcc.md").write_text(
        "---\nlegacy_path: docs/computer-science/gcc.md\ncreated_at: '2020-01-01'\n---\n草稿\n",
        encoding="utf-8",
    )

    code, report = _run(tmp_path)
    assert code == 0
    check = {c["name"]: c for c in report["checks"]}["working_ttl"]
    assert list(check["overdue"]) == ["a-external/computer-science"]
    entry = check["overdue"]["a-external/computer-science"][0]
    assert entry["path"] == "content/working/a-external/computer-science/gcc.md"


def test_doctor_working_ttl_can_be_disabled_but_stays_visible(tmp_path: Path):
    """`ttl_days: unlimited` 关闭滞留判定，但报告仍点出在册篇数与"已关闭"这件事。

    owner 2026-09-01 把 TTL 设为无限：落位后长期停留是预期状态。关闭必须显式
    可见（`ttl_days: unlimited` + `reason: ttl_disabled`），不能表现成"检查通过"。
    """
    working = tmp_path / "content" / "working" / "tools"
    working.mkdir(parents=True)
    (working / "ancient.md").write_text(
        "---\nsource_ref: content/sources/tools/x.md\ncreated_at: '2020-01-01'\n---\n草稿\n",
        encoding="utf-8",
    )
    config = tmp_path / "config"
    config.mkdir(exist_ok=True)
    (config / "policy.yaml").write_text(
        "layers:\n  working:\n    ttl_days: unlimited\n", encoding="utf-8"
    )

    code, report = _run(tmp_path)
    assert code == 0
    check = {c["name"]: c for c in report["checks"]}["working_ttl"]
    assert check["state"] == "ok"
    assert check["ttl_days"] == "unlimited"
    assert check["reason"] == "ttl_disabled"
    assert check["checked"] == 1
    assert "overdue" not in check


def test_doctor_working_ttl_falls_back_to_mtime_and_says_so(tmp_path: Path):
    """基准退化必须可见：无 `created_at` 时用 mtime，并在报告里标明 basis。"""
    import os
    import time

    working = tmp_path / "content" / "working"
    working.mkdir(parents=True)
    note = working / "undated.md"
    note.write_text(
        "---\nsource_ref: content/sources/tools/x.md\n---\n草稿\n", encoding="utf-8"
    )
    old = time.time() - 400 * 86400
    os.utime(note, (old, old))

    code, report = _run(tmp_path)
    assert code == 0
    check = {c["name"]: c for c in report["checks"]}["working_ttl"]
    assert check["overdue"]["(root)"][0]["basis"] == "mtime"
