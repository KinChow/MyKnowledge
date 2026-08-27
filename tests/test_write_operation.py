from __future__ import annotations

import tempfile
import json
import unittest
import subprocess
from pathlib import Path
from unittest import mock

from tools.common import sha256_bytes
from tools.vault_lock import LockBusyError, VaultLock, VaultLockGroup
from tools.write_operation import WriteOperation


class WriteOperationTests(unittest.TestCase):
    def test_private_vault_write_uses_owner_checkout_root(self):
        with tempfile.TemporaryDirectory() as d:
            workspace = Path(d); public = workspace / "public"; private = workspace / "private"
            public.mkdir(); private.mkdir()
            subprocess.run(["git", "init", "-q", str(public)], check=True)
            subprocess.run(["git", "init", "-q", str(private)], check=True)
            manifest = workspace / "vaults.yaml"
            manifest.write_text(f"schema_version: 1\nlayout: superproject\nworkspace_root: {workspace}\nvaults:\n  - {{id: public, path: public}}\n  - {{id: private, path: private, confidentiality: internal}}\n", encoding="utf-8")
            service = WriteOperation(public)
            with mock.patch("tools.write_operation.VaultRegistry", lambda root: __import__("tools.vault_registry", fromlist=["VaultRegistry"]).VaultRegistry(root, manifest)):
                preview = service.preview({"wiki/private.md": "secret"}, vault_id="private")
                self.assertEqual(preview["state"], "previewed")
                self.assertEqual(service.apply(preview["operation_id"], confirmed=True)["state"], "applied")
            self.assertEqual((private / "wiki" / "private.md").read_text(encoding="utf-8"), "secret")
            self.assertFalse((public / "wiki" / "private.md").exists())

    def test_preview_is_read_only_and_apply_requires_confirmation(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            service = WriteOperation(root)
            preview = service.preview({"wiki/a.md": "hello"})
            self.assertEqual(preview["state"], "previewed")
            self.assertFalse((root / "wiki/a.md").exists())
            self.assertEqual(service.apply(preview["operation_id"])["state"], "awaiting_confirmation")
            self.assertEqual(service.apply(preview["operation_id"], confirmed=True)["state"], "applied")

    def test_apply_is_idempotent(self):
        with tempfile.TemporaryDirectory() as d:
            service = WriteOperation(Path(d))
            op = service.preview({"a.md": "one"})["operation_id"]
            first = service.apply(op, confirmed=True)
            second = service.apply(op, confirmed=True)
            self.assertEqual(first, second)

    def test_hash_change_blocks_without_overwrite(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            target = root / "a.md"
            target.write_text("old", encoding="utf-8")
            service = WriteOperation(root)
            op = service.preview({"a.md": "new"})["operation_id"]
            target.write_text("other", encoding="utf-8")
            result = service.apply(op, confirmed=True)
            self.assertEqual(result["error_code"], "hash_mismatch")
            self.assertEqual(target.read_text(encoding="utf-8"), "other")

    def test_apply_path_race_returns_structured_failure(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); service = WriteOperation(root)
            op = service.preview({"nested/a.md": "new"})["operation_id"]
            (root / "nested").mkdir(parents=True)
            (root / "outside").mkdir()
            (root / "nested").rmdir()
            (root / "nested").symlink_to(root / "outside", target_is_directory=True)
            result = service.apply(op, confirmed=True)
            self.assertEqual(result["state"], "expired")
            self.assertEqual(result["error_code"], "apply_failed")
            self.assertIn("path_symlink", result["detail"])
            self.assertFalse((root / "outside" / "a.md").exists())

    def test_tampered_durable_audit_blocks_apply(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); service = WriteOperation(root)
            op = service.preview({"a.md": "new"})["operation_id"]
            audit = root / "audit" / "operations" / f"{op}.json"
            value = json.loads(audit.read_text(encoding="utf-8")); value["state"] = "applied"
            audit.write_text(json.dumps(value), encoding="utf-8")
            result = service.apply(op, confirmed=True)
            self.assertEqual(result["error_code"], "hash_mismatch")
            self.assertFalse((root / "a.md").exists())

    def test_path_escape_is_blocked(self):
        with tempfile.TemporaryDirectory() as d:
            result = WriteOperation(Path(d)).preview({"../escape.md": "x"})
            self.assertEqual(result["error_code"], "path_outside_repo")

    def test_symlink_and_hardlink_targets_are_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); target = root / "real.md"; target.write_text("old", encoding="utf-8")
            (root / "alias.md").symlink_to(target)
            service = WriteOperation(root)
            self.assertEqual(service.preview({"alias.md": "new"})["error_code"], "path_symlink")
            linked = root / "linked.md"; linked.hardlink_to(target)
            self.assertEqual(service.preview({"linked.md": "new"})["error_code"], "path_hardlink")

    def test_lock_busy_is_structured(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            service = WriteOperation(root)
            op = service.preview({"a.md": "x"})["operation_id"]
            lock = VaultLock(root, "public", "other")
            with lock:
                result = service.apply(op, confirmed=True)
            self.assertEqual(result["error_code"], "lock_busy")

    def test_fencing_token_rejects_replaced_owner(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            lock = VaultLock(root, "public", "op-one")
            with lock:
                lock._owner_file.write_text(json.dumps({"operation_id": "op-two", "lock_token": "stolen"}), encoding="utf-8")
                with self.assertRaises(LockBusyError):
                    lock.assert_owner()

    def test_stale_lock_recovery_requires_free_kernel_lock_and_writes_audit(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            lock = VaultLock(root, "public", "op-old")
            lock._owner_file.parent.mkdir(parents=True, exist_ok=True)
            lock._owner_file.write_text(json.dumps({"operation_id": "op-old", "lock_token": "stale"}), encoding="utf-8")
            result = VaultLock.recover(root, "public", "op-recover", "alice")
            self.assertEqual(result["state"], "recovered")
            self.assertFalse(lock._owner_file.exists())
            records = list((root / "audit" / "operations").glob("lock-recovery-*.json"))
            self.assertEqual(len(records), 1)
            record = json.loads(records[0].read_text(encoding="utf-8"))
            self.assertEqual(record["record_type"], "lock-recovery")
            self.assertEqual(record["old_operation_id"], "op-old")

    def test_stale_lock_recovery_does_not_break_live_lock(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            with VaultLock(root, "public", "op-live"):
                result = VaultLock.recover(root, "public", "op-recover")
                self.assertEqual(result["error_code"], "lock_busy")

    def test_multi_vault_lock_group_orders_and_releases_all(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            with VaultLockGroup(root, ["zeta", "alpha", "alpha"], "op-group") as group:
                self.assertEqual(group.vault_ids, ("alpha", "zeta"))
                group.assert_owner()
                self.assertTrue((root / "state" / "locks" / "alpha.owner").exists())
                self.assertTrue((root / "state" / "locks" / "zeta.owner").exists())
            self.assertFalse((root / "state" / "locks" / "alpha.owner").exists())
            self.assertFalse((root / "state" / "locks" / "zeta.owner").exists())

    def test_multi_vault_lock_group_releases_acquired_locks_on_failure(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            with VaultLock(root, "zeta", "other"):
                with self.assertRaises(LockBusyError):
                    with VaultLockGroup(root, ["alpha", "zeta"], "op-group"):
                        pass
                self.assertFalse((root / "state" / "locks" / "alpha.owner").exists())

    def test_multi_file_failure_rolls_back(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "a.md").write_text("old", encoding="utf-8")
            service = WriteOperation(root)
            op = service.preview({"a.md": "new", "b.md": "created"})["operation_id"]
            original = service._path
            calls = {"n": 0}

            def fail_once(name):
                calls["n"] += 1
                if calls["n"] == 2:
                    raise OSError("injected")
                return original(name)

            with mock.patch.object(service, "_path", side_effect=fail_once):
                result = service.apply(op, confirmed=True)
            self.assertEqual(result["error_code"], "apply_failed")
            self.assertEqual((root / "a.md").read_text(encoding="utf-8"), "old")
            self.assertFalse((root / "b.md").exists())

    def test_failed_apply_keeps_intent_for_explicit_recovery(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); (root / "a.md").write_text("old", encoding="utf-8")
            service = WriteOperation(root)
            op = service.preview({"a.md": "new", "b.md": "created"})["operation_id"]
            original = service._path
            calls = {"n": 0}
            def fail_after_first(name):
                calls["n"] += 1
                if calls["n"] == 3:
                    raise OSError("injected")
                return original(name)
            with mock.patch.object(service, "_path", side_effect=fail_after_first):
                result = service.apply(op, confirmed=True)
            self.assertEqual(result["error_code"], "apply_failed")
            self.assertTrue((root / "state" / "commit-intents" / f"{op}.json").exists())
            self.assertEqual(service.recover(op)["state"], "recovery_required")
            self.assertEqual((root / "a.md").read_text(encoding="utf-8"), "old")

    def test_rename_and_retire_have_distinct_operation_types(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "old.md").write_text("body", encoding="utf-8")
            service = WriteOperation(root)
            renamed = service.rename("old.md", "new.md")
            self.assertEqual(renamed["operation_id"].startswith("op_"), True)
            record = service.store.load(renamed["operation_id"])
            self.assertEqual(record["operation_type"], "rename")
            retired = service.retire("old.md")
            self.assertEqual(service.store.load(retired["operation_id"])["operation_type"], "retire")
            result = service.apply(retired["operation_id"], confirmed=True)
            self.assertEqual(result["state"], "applied")
            marker = root / "audit" / "retire" / f"{retired['operation_id']}.json"
            self.assertTrue(marker.exists())
            self.assertEqual(json.loads(marker.read_text())["schema_version"], "retire-marker/v1")

    def test_commit_intent_is_removed_after_apply(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); service = WriteOperation(root)
            op = service.preview({"a.md": "new"})["operation_id"]
            self.assertEqual(service.apply(op, confirmed=True)["state"], "applied")
            self.assertFalse((root / "state" / "commit-intents" / f"{op}.json").exists())

    def test_purge_requires_verified_owner_backup(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); target = root / "wiki.md"; target.write_text("sensitive", encoding="utf-8")
            result = WriteOperation(root).purge("wiki.md")
            self.assertEqual(result["error_code"], "backup_not_verified")
            self.assertTrue(target.exists())

    def test_recover_commit_intent_marks_fully_written_files_applied(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); service = WriteOperation(root)
            preview = service.preview({"a.md": "new"}); op = preview["operation_id"]
            record = service.store.load(op)
            from tools.common import atomic_write, canonical_json
            intent = {"schema_version": "commit-intent/v1", "operation_id": op, "operation_type": "write", "vault_id": "public", "files": [{"path": "a.md", "before_hash": None, "after_hash": sha256_bytes(b"new")}]}
            atomic_write(root / "state" / "commit-intents" / f"{op}.json", canonical_json(intent) + b"\n", 0o600)
            (root / "a.md").write_text("new", encoding="utf-8")
            result = service.recover(op)
            self.assertEqual(result["state"], "applied")


if __name__ == "__main__":
    unittest.main()
