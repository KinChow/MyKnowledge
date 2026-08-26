from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tools.common import sha256_bytes
from tools.vault_lock import VaultLock
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
