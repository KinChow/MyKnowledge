"""backup.py 结果信封归一到 tools.contract 的契约测试（A 线 Infra 簇）。

断言点：公共返回带 schema_version(name/vN) + 单一 status 轴；成功 ok、失败 blocked
且携带已登记的顶层 error_code；原状态机的领域字段（state/backup_state/…）作为
payload 加法保留，语义不丢。
"""

from __future__ import annotations

import json
import subprocess
import tempfile
from pathlib import Path

from tools import contract
from tools.backup import BackupManager


def _git_init(root: Path) -> None:
    subprocess.run(["git", "init", "-q", str(root)], check=True)


def test_manifest_and_verify_are_ok_envelopes():
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        _git_init(root)
        manager = BackupManager(root)
        created = manager.create_manifest("public")
        assert created["status"] == "ok"
        assert created["schema_version"] == "backup-manifest/v1"
        assert "path" in created and isinstance(created["entries"], list)

        checked = manager.verify_manifest(root / created["path"])
        assert checked["status"] == "ok"
        assert checked["schema_version"] == "backup-verify/v1"
        # 终态：无 dual-field——成功只由 status 表达，无结果级 state/backup_state。
        assert "state" not in checked and "backup_state" not in checked
        assert checked["manifest_sha256"].startswith("sha256:")


def test_tampered_manifest_is_blocked_with_registered_code():
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        _git_init(root)
        manager = BackupManager(root)
        created = manager.create_manifest("public")
        path = root / created["path"]
        data = json.loads(path.read_text(encoding="utf-8"))
        data["entries"] = [{"tampered": True}]
        path.write_text(json.dumps(data), encoding="utf-8")

        failed = manager.verify_manifest(path)
        assert failed["status"] == "blocked"
        assert failed["error_code"] == "hash_mismatch"
        assert failed["error_code"] in contract.ERROR_CODES
        assert failed["schema_version"] == "backup-verify/v1"
        assert "state" not in failed and "backup_state" not in failed


def test_restore_target_precondition_is_blocked_envelope():
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        _git_init(root)
        manager = BackupManager(root)
        created = manager.create_manifest("public")
        blocked = manager.restore_manifest(root / created["path"], root / "inside")
        assert blocked["status"] == "blocked"
        assert blocked["error_code"] == "restore_target_invalid"
        assert blocked["error_code"] in contract.ERROR_CODES
