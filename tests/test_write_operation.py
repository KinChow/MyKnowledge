from __future__ import annotations

import tempfile
import json
import unittest
from pathlib import Path
from unittest import mock

from tools.common import sha256_bytes
from tools.vault_lock import LockBusyError, VaultLock
from tools.write_operation import WriteOperation


class WriteOperationTests(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()
