from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tools.vault_registry import VaultRegistry


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


if __name__ == "__main__":
    unittest.main()
