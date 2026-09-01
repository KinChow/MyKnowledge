"""布局迁移不变量（LAY-001~004）：搬目录不得改写历史、不得让门禁静默通过。

这些用例锁定的是 2026-09-01 实测出来的两个盲区：
- `applied_files` 里的历史相对路径是事实，读取侧必须容忍（LAY-004）；
- 「检查了 0 个」不得判为 ok（回归锁在 tests/test_doctor.py）。
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _run_doctor(root: Path):
    out = subprocess.run(
        [sys.executable, "-m", "tools.doctor", "--root", str(root)],
        capture_output=True,
        text=True,
        cwd=ROOT,
    )
    return out.returncode, json.loads(out.stdout)


def _recompute(record: dict) -> str:
    from tools.common import hash_canonical

    return hash_canonical({k: v for k, v in record.items() if k != "record_sha256"})


def test_historical_applied_files_paths_are_not_rewritten_by_any_reader():
    """真实 durable 记录（不合成）：含历史 applied_files 的记录 hash 必须逐条自证。

    §4.6 的不变量：`applied_files` 记录的是**当时**的相对路径，受 record_sha256
    覆盖且受 audit.append_only 约束。任何为了"修正路径"而改写记录的做法都会在
    这里失败。
    """
    records = sorted((ROOT / "audit" / "operations").glob("*.json"))
    assert records, "真实审计记录缺失，本用例不接受合成 fixture"
    with_paths = 0
    for path in records:
        record = json.loads(path.read_text(encoding="utf-8"))
        assert record["record_sha256"] == _recompute(record), path.name
        if record.get("applied_files"):
            with_paths += 1
    assert with_paths > 0


def test_doctor_does_not_resolve_applied_files_after_a_layout_move(tmp_path: Path):
    """LAY-004 读取侧：canonical 搬走后，历史 applied_files 不得被判成缺失/滞留。

    实测结论：doctor 全程不解析 applied_files（唯一消费方是 F010 rollback 的
    前缀白名单与错误响应回显），因此批次 2 不需要额外的容忍代码——但这条断言
    必须存在，否则后续给 doctor 加检查项时很容易顺手去 stat 这些路径。
    """
    from tools.operation_store import OperationStore
    from tools.write_operation import WriteOperation

    service = WriteOperation(tmp_path)
    preview = service.preview(
        {
            "content/wiki/moved.md": "---\nschema_version: wiki/v1\nid: moved\n---\n正文\n"
        }
    )
    operation_id = preview["operation_id"]
    applied = service.apply(operation_id, confirmed=True)
    assert applied["state"] == "applied"
    assert applied["applied_files"] == ["content/wiki/moved.md"]

    # 模拟一次层间搬移：正文升级/退回到另一层，历史记录保持旧路径
    (tmp_path / "content" / "working").mkdir(parents=True, exist_ok=True)
    (tmp_path / "content" / "wiki" / "moved.md").rename(
        tmp_path / "content" / "working" / "moved.md"
    )
    assert not (tmp_path / applied["applied_files"][0]).exists()

    code, report = _run_doctor(tmp_path)
    assert code == 0, report
    names = {c["name"]: c for c in report["checks"]}
    assert names["pending_operations"]["state"] == "ok"
    assert operation_id not in json.dumps(report, ensure_ascii=False)

    # 审计快照未被任何读取方改写
    store = OperationStore(tmp_path)
    assert store.verify_audit(operation_id) is None
    durable = json.loads(
        (tmp_path / "audit" / "operations" / f"{operation_id}.json").read_text(
            encoding="utf-8"
        )
    )
    assert durable["applied_files"] == ["content/wiki/moved.md"]
    assert durable["record_sha256"] == _recompute(durable)


def test_record_path_rejects_traversal_and_absolute_paths():
    """账目路径是外部可改写的输入：`..`/绝对路径必须在拼接前拒绝（C004）。

    owner review（2026-09-01）指出的洞：`resolve_record_path` 原来直接拼接，
    `archive_path: "../../etc/passwd"` 会让"账目指向的实物"落在仓库外。
    """
    import pytest

    from tools.paths import RepoPaths

    paths = RepoPaths(ROOT)
    for hostile in (
        "../../etc/passwd",
        "archive/../../etc/passwd",
        "/etc/passwd",
        "",
        "   ",
        "./",
        "C:/Windows/win.ini",
    ):
        with pytest.raises(ValueError, match="unsafe_record_path"):
            paths.record_path_candidates(hostile)


def test_record_path_does_not_follow_symlinks_out_of_the_repo(tmp_path: Path):
    """仓库内一个指向外部的符号链接不得让账目"自证通过"（C004）。"""
    from tools.paths import RepoPaths

    outside = tmp_path / "outside"
    outside.mkdir()
    real = outside / "evil.md"
    real.write_text("仓库外的正文", encoding="utf-8")

    repo = tmp_path / "repo"
    (repo / "archive" / "text").mkdir(parents=True)
    (repo / "archive" / "text" / "evil.md").symlink_to(real)

    assert RepoPaths(repo).resolve_record_path("archive/text/evil.md") is None


def test_doctor_reports_an_unsafe_archive_path_instead_of_snapshot_missing(
    tmp_path: Path,
):
    """越界账目要有自己的错误码，不能混进"快照缺失"。"""
    from tools.doctor import _check_manifest_records
    from tools.paths import RepoPaths

    manifest = RepoPaths(tmp_path).manifest
    manifest.parent.mkdir(parents=True, exist_ok=True)
    manifest.write_text(
        json.dumps(
            {
                "record_id": "rec-hostile",
                "archive_path": "../../etc/passwd",
                "snapshot_sha256": "sha256:" + "0" * 64,
            }
        )
        + "\n",
        encoding="utf-8",
    )

    state, fields = _check_manifest_records(tmp_path)
    assert state == "error"
    assert fields["broken"][0]["reason"] == "archive_path_unsafe"


def test_default_index_root_is_inferred_from_the_current_layout(tmp_path: Path):
    """从索引路径反推 root 必须与 `RepoPaths.state_index` 同源。

    回归锁：批次 1 之后索引在 `var/state/index/`，而反推逻辑仍按 `state/index`
    数层级，算出的 root 是 `<root>/var`——Retriever 于是拿错的 root 读 projection。
    """
    from tools.indexing import _infer_index_root, default_public_index_path

    index_path = default_public_index_path(tmp_path)
    assert index_path.parent == tmp_path / "var" / "state" / "index"
    assert _infer_index_root(index_path) == tmp_path.resolve()
    assert _infer_index_root(tmp_path / "elsewhere" / "public.sqlite3") is None


def test_path_contract_holds_for_the_real_config():
    """真实仓库里 config 声明与 `RepoPaths` 派生值必须逐条一致（LAY-001）。"""
    from tools.path_contract import check

    state, fields = check(ROOT)
    assert state == "ok", fields.get("drifted")
    assert fields["checked"] >= 30  # 覆盖面不得悄悄缩小
    assert fields["sources"] == ["policy", "schemas"]


def test_path_contract_catches_a_renamed_directory(tmp_path: Path):
    """把 config 里的一处路径改名（模拟批次 3 漏改）必须报 error。"""
    import shutil

    from tools.path_contract import check

    config = tmp_path / "config"
    config.mkdir()
    for name in ("policy.yaml", "schemas.yaml"):
        shutil.copy2(ROOT / "config" / name, config / name)
    policy = config / "policy.yaml"
    policy.write_text(
        policy.read_text(encoding="utf-8").replace(
            "public_confirmation_path: release/public-confirmations",
            "public_confirmation_path: ledger/release/public-confirmations",
        ),
        encoding="utf-8",
    )

    state, fields = check(tmp_path)
    assert state == "error"
    keys = [d["key"] for d in fields["drifted"]]
    assert "policy:release.public_confirmation_path" in keys
    assert fields["drifted"][0]["reason"] == "path_declaration_drift"


def test_path_contract_is_visibly_skipped_when_config_is_absent(tmp_path: Path):
    """配置整体缺失时"没检查"要和"检查通过"区分开，不装作比对成功。"""
    from tools.path_contract import check

    state, fields = check(tmp_path)
    assert state == "ok"
    assert fields == {"checked": 0, "reason": "config_absent"}


def test_path_contract_tolerates_reordered_list_declarations(tmp_path: Path):
    """列表型声明只做成员判定：调换 YAML 顺序在语义上没变，不得报漂移。

    owner review（2026-09-01）质疑"门禁会不会太严"，这就是过严的一例——原实现
    把规则绑在列表下标上。
    """
    import shutil

    from tools.path_contract import check

    config = tmp_path / "config"
    config.mkdir()
    for name in ("policy.yaml", "schemas.yaml"):
        shutil.copy2(ROOT / "config" / name, config / name)
    policy = config / "policy.yaml"
    policy.write_text(
        policy.read_text(encoding="utf-8").replace(
            "    - var/queries/public/\n    - content/wiki/\n",
            "    - content/wiki/\n    - var/queries/public/\n",
        ),
        encoding="utf-8",
    )

    assert check(tmp_path)[0] == "ok"


def test_path_contract_still_catches_a_removed_list_member(tmp_path: Path):
    """放宽到成员判定之后，删掉代码实际使用的那个路径仍必须报错。"""
    import shutil

    from tools.path_contract import check

    config = tmp_path / "config"
    config.mkdir()
    for name in ("policy.yaml", "schemas.yaml"):
        shutil.copy2(ROOT / "config" / name, config / name)
    policy = config / "policy.yaml"
    original = policy.read_text(encoding="utf-8")
    patched = original.replace("    - content/working/\n", "", 1)
    assert patched != original, "fixture 前提：policy 里确实声明了 content/working/"
    policy.write_text(patched, encoding="utf-8")

    state, fields = check(tmp_path)
    assert state == "error"
    reasons = {d["reason"] for d in fields["drifted"]}
    assert "path_declaration_missing_member" in reasons


def test_snapshot_reached_through_an_in_repo_symlink_is_accepted(tmp_path: Path):
    """把 archive 目录 symlink 到仓库内另一处是合理布局，不得判成缺失。

    与 `test_record_path_does_not_follow_symlinks_out_of_the_repo` 成对：控制的
    目标是"逃出仓库"，不是"用了符号链接"。
    """
    from tools.paths import RepoPaths

    real = tmp_path / "big-disk" / "text"
    real.mkdir(parents=True)
    (real / "x.md").write_text("正文", encoding="utf-8")
    (tmp_path / "archive").mkdir()
    (tmp_path / "archive" / "text").symlink_to(real)

    resolved = RepoPaths(tmp_path).resolve_record_path("archive/text/x.md")
    assert resolved is not None
