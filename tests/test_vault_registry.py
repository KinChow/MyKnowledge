from __future__ import annotations

import subprocess
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tools.vault_registry import VaultRegistry
from tools.backup import BackupManager


class VaultRegistryTests(unittest.TestCase):
    def test_public_only_fallback_is_available(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            report = VaultRegistry(root).check()
            self.assertEqual(report["vaults"][0]["vault_id"], "public")
            self.assertEqual(report["vaults"][0]["state"], "available")
            self.assertEqual(report["vaults"][0]["backup_state"], "unconfigured")

    def test_multiple_vaults_and_unavailable_isolated(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            public = root / "public"
            private = root / "private"
            public.mkdir(); private.mkdir()
            subprocess.run(["git", "init", "-q", str(public)], check=True)
            manifest = root / "manifest.yaml"
            manifest.write_text("""schema_version: 1\nlayout: superproject\nworkspace_root: %s\npublic_vault_id: public\nvaults:\n  - {id: public, path: public, confidentiality: public, backup_state: unconfigured}\n  - {id: private, path: private-missing, confidentiality: internal, backup_state: unconfigured}\n""" % root, encoding="utf-8")
            report = VaultRegistry(public, manifest).check()
            states = {x["vault_id"]: x["state"] for x in report["vaults"]}
            self.assertEqual(states["private"], "unavailable")
            self.assertEqual(states["public"], "available")

    def test_same_object_id_across_vaults_is_not_a_conflict(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); public = root / "public"; private = root / "private"
            for vault in (public, private):
                (vault / "wiki").mkdir(parents=True)
                (vault / "wiki" / "same.md").write_text("# Same\n", encoding="utf-8")
                subprocess.run(["git", "init", "-q", str(vault)], check=True)
            manifest = root / "manifest.yaml"
            manifest.write_text(f"""schema_version: 1\nlayout: superproject\nworkspace_root: {root}\npublic_vault_id: public\nvaults:\n  - {{id: public, path: public}}\n  - {{id: private, path: private}}\n""", encoding="utf-8")
            report = VaultRegistry(public, manifest).check()
            self.assertEqual(report["conflicts"], [])
            self.assertEqual({x["object_count"] for x in report["vaults"]}, {1})

    def test_duplicate_object_id_inside_one_vault_is_reported_without_paths(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); (root / "wiki" / "a").mkdir(parents=True); (root / "wiki" / "b").mkdir(parents=True)
            (root / "wiki" / "a" / "same.md").write_text("a", encoding="utf-8")
            (root / "wiki" / "b" / "same.md").write_text("b", encoding="utf-8")
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            report = VaultRegistry(root).check()
            self.assertEqual(report["conflicts"][0]["code"], "duplicate_object_id")
            self.assertNotIn(str(root), json.dumps(report))

    def test_overlap_and_duplicate_are_reported(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); (root / "a").mkdir(); subprocess.run(["git", "init", "-q", str(root / "a")], check=True)
            manifest = root / "manifest.yaml"
            manifest.write_text("""schema_version: 1\nlayout: superproject\nworkspace_root: %s\nvaults:\n  - {id: a, path: a}\n  - {id: a, path: a}\n""" % root, encoding="utf-8")
            report = VaultRegistry(root, manifest).check()
            self.assertIn("duplicate_vault_id", {x["reason"] for x in report["vaults"]})

    def test_path_escape_is_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); manifest = root / "manifest.yaml"
            manifest.write_text("""schema_version: 1\nlayout: superproject\nworkspace_root: %s\nvaults:\n  - {id: public, path: ../outside}\n""" % root, encoding="utf-8")
            report = VaultRegistry(root, manifest).check()
            self.assertEqual(report["vaults"][0]["reason"], "path_invalid")

    def test_backup_manifest_verification_detects_tampering(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            manager = BackupManager(root)
            manifest = manager.create_manifest("public")
            self.assertTrue(manifest["entries"] == [] or all("path" in x and "sha256" in x for x in manifest["entries"]))
            checked = manager.verify_manifest(root / manifest["path"])
            self.assertEqual(checked["backup_state"], "verified")
            path = root / manifest["path"]
            data = json.loads(path.read_text(encoding="utf-8"))
            data["entries"] = [{"tampered": True}]
            path.write_text(json.dumps(data), encoding="utf-8")
            failed = manager.verify_manifest(path)
            self.assertEqual(failed["backup_state"], "failed")
            self.assertEqual(failed["error_code"], "hash_mismatch")

    def test_verified_manifest_restores_to_empty_checkout(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); subprocess.run(["git", "init", "-q", str(root)], check=True)
            (root / "wiki").mkdir(); (root / "wiki" / "item.md").write_text("# item\n", encoding="utf-8")
            manager = BackupManager(root); manifest = manager.create_manifest("public")
            with tempfile.TemporaryDirectory() as out:
                target = Path(out) / "checkout"
                restored = manager.restore_manifest(root / manifest["path"], target)
                self.assertEqual(restored["state"], "restored")
                self.assertEqual((target / "wiki" / "item.md").read_text(encoding="utf-8"), "# item\n")

    def test_practice_entries_are_owner_scoped_and_restored(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); subprocess.run(["git", "init", "-q", str(root)], check=True)
            practice = root / "practice" / "questions"; practice.mkdir(parents=True)
            (practice / "q-private.json").write_text('{"answer":"secret"}\n', encoding="utf-8")
            (root / "practice" / "reviews").mkdir(parents=True)
            (root / "practice" / "reviews" / "q-private.jsonl").write_text('{"score":1}\n', encoding="utf-8")
            manager = BackupManager(root); manifest = manager.create_manifest("public")
            paths = {entry["path"] for entry in manifest["entries"]}
            self.assertIn("practice/questions/q-private.json", paths)
            self.assertIn("practice/reviews/q-private.jsonl", paths)
            with tempfile.TemporaryDirectory() as out:
                restored = manager.restore_manifest(root / manifest["path"], Path(out) / "checkout")
                self.assertEqual(restored["state"], "restored")
                self.assertEqual((Path(out) / "checkout" / "practice" / "questions" / "q-private.json").read_text(), '{"answer":"secret"}\n')

    def test_private_manifest_does_not_read_public_or_escape_owner(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); public = root / "public"; private = root / "private"
            public.mkdir(); private.mkdir()
            for vault in (public, private): subprocess.run(["git", "init", "-q", str(vault)], check=True)
            (public / "wiki").mkdir(); (public / "wiki" / "public.md").write_text("public", encoding="utf-8")
            (private / "practice" / "questions").mkdir(parents=True); (private / "practice" / "questions" / "q.md").write_text("secret", encoding="utf-8")
            manifest_path = root / "manifest.yaml"
            manifest_path.write_text(f"schema_version: 1\nlayout: superproject\nworkspace_root: {root}\npublic_vault_id: public\nvaults:\n  - {{id: public, path: public}}\n  - {{id: private, path: private, confidentiality: internal}}\n", encoding="utf-8")
            manager = BackupManager(public, manifest_path); result = manager.create_manifest("private")
            paths = {entry["path"] for entry in result["entries"]}
            self.assertEqual(paths, {"practice/questions/q.md"})
            self.assertTrue(manager.verify_manifest(private / result["path"])["backup_state"] == "verified")

    def test_restore_requires_empty_target(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); subprocess.run(["git", "init", "-q", str(root)], check=True)
            manager = BackupManager(root); manifest = manager.create_manifest("public")
            with tempfile.TemporaryDirectory() as out:
                target = Path(out) / "checkout"; target.mkdir(); (target / "keep").write_text("x")
                result = manager.restore_manifest(root / manifest["path"], target)
                self.assertEqual(result["error_code"], "restore_target_not_empty")


if __name__ == "__main__":
    unittest.main()
