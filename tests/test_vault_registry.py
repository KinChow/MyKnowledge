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
            self.assertEqual(report["available_scopes"], ["public", "local"])

    def test_backup_not_configured_warning_has_safe_next_action(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); subprocess.run(["git", "init", "-q", str(root)], check=True)
            manifest = root / "manifest.yaml"
            manifest.write_text(f"schema_version: 1\nlayout: direct-checkout\nworkspace_root: {root}\nvaults:\n  - {{id: public, path: .}}\n  - {{id: private, path: missing, confidentiality: internal}}\n", encoding="utf-8")
            warning = next(item for item in BackupManager(root, manifest).status()["backup_summary"]["warning"] if item["vault_id"] == "private")
            self.assertEqual(warning["code"], "backup_not_configured")
            self.assertNotIn(str(root), json.dumps(warning))
            self.assertIn("configure", warning["next_action"])

    def test_available_scopes_include_private_when_private_vault_is_ready(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); public = root / "public"; private = root / "private"
            for vault in (public, private):
                vault.mkdir(); subprocess.run(["git", "init", "-q", str(vault)], check=True)
            manifest = root / "manifest.yaml"
            manifest.write_text(f"schema_version: 1\nlayout: superproject\nworkspace_root: {root}\npublic_vault_id: public\nvaults:\n  - {{id: public, path: public}}\n  - {{id: private, path: private, confidentiality: internal}}\n", encoding="utf-8")
            report = VaultRegistry(public, manifest).check()
            self.assertEqual(report["available_scopes"], ["public", "local", "private"])

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

    def test_private_public_projection_permission_is_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); private = root / "private"; private.mkdir(); subprocess.run(["git", "init", "-q", str(private)], check=True)
            manifest = root / "manifest.yaml"
            manifest.write_text(f"schema_version: 1\nlayout: superproject\nworkspace_root: {root}\nvaults:\n  - {{id: private, path: private, confidentiality: internal, allow_public_projection: true}}\n", encoding="utf-8")
            report = VaultRegistry(root, manifest).check()
            self.assertEqual(report["vaults"][0]["reason"], "public_projection_confidentiality")

    def test_internal_public_projection_permission_is_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); subprocess.run(["git", "init", "-q", str(root)], check=True)
            manifest = root / "manifest.yaml"
            manifest.write_text(f"schema_version: 1\nlayout: direct-checkout\nworkspace_root: {root}\nvaults:\n  - {{id: public, path: ., confidentiality: internal, allow_public_projection: true}}\n", encoding="utf-8")
            report = VaultRegistry(root, manifest).check()
            self.assertEqual(report["vaults"][0]["reason"], "public_projection_confidentiality")

    def test_reference_rejects_cross_vault_even_when_target_exists(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); public = root / "public"; private = root / "private"
            for vault in (public, private):
                vault.mkdir(); subprocess.run(["git", "init", "-q", str(vault)], check=True)
            manifest = root / "manifest.yaml"
            manifest.write_text(f"schema_version: 1\nlayout: superproject\nworkspace_root: {root}\nvaults:\n  - {{id: public, path: public}}\n  - {{id: private, path: private}}\n", encoding="utf-8")
            result = VaultRegistry(public, manifest).validate_reference("public", "private", "source", "s")
            self.assertFalse(result["valid"])
            self.assertEqual(result["code"], "cross_vault_reference")

    def test_effective_confidentiality_propagates_from_upstream(self):
        self.assertEqual(VaultRegistry.effective_confidentiality("public", ["internal"]), "internal")
        self.assertEqual(VaultRegistry.effective_confidentiality("public", ["public"]), "public")

    def test_object_index_keeps_same_ids_separate_by_owner(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); public = root / "public"; private = root / "private"
            for vault in (public, private):
                (vault / "wiki").mkdir(parents=True); (vault / "wiki" / "same.md").write_text("x", encoding="utf-8")
                subprocess.run(["git", "init", "-q", str(vault)], check=True)
            manifest = root / "manifest.yaml"
            manifest.write_text(f"schema_version: 1\nlayout: superproject\nworkspace_root: {root}\nvaults:\n  - {{id: public, path: public}}\n  - {{id: private, path: private}}\n", encoding="utf-8")
            index = VaultRegistry(public, manifest).object_index()
            self.assertEqual(set(index), {("public", "wiki", "same"), ("private", "wiki", "same")})
            self.assertEqual({item["availability"] for item in index.values()}, {"available"})

    def test_local_projection_merges_same_ids_with_owner_and_private_scope(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); public = root / "public"; private = root / "private"
            for vault, text in ((public, "# Public\nbody"), (private, "# Private\nsecret")):
                (vault / "wiki").mkdir(parents=True)
                (vault / "wiki" / "same.md").write_text(text, encoding="utf-8")
                subprocess.run(["git", "init", "-q", str(vault)], check=True)
            manifest = root / "manifest.yaml"
            manifest.write_text(f"schema_version: 1\nlayout: superproject\nworkspace_root: {root}\npublic_vault_id: public\nvaults:\n  - {{id: public, path: public, confidentiality: public}}\n  - {{id: private, path: private, confidentiality: internal}}\n", encoding="utf-8")
            local = VaultRegistry(public, manifest).local_projection()
            refs = {tuple(item["object_ref"].values()) for item in local["items"]}
            self.assertEqual(refs, {("public", "wiki", "same"), ("private", "wiki", "same")})
            private_only = VaultRegistry(public, manifest).local_projection("private")
            self.assertEqual({item["vault_id"] for item in private_only["items"]}, {"private"})
            self.assertNotIn("secret", json.dumps({"schema_version": private_only["schema_version"], "items": []}))

    def test_local_projection_keeps_unavailable_vault_diagnostic(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); public = root / "public"; public.mkdir()
            subprocess.run(["git", "init", "-q", str(public)], check=True)
            manifest = root / "manifest.yaml"
            manifest.write_text(f"schema_version: 1\nlayout: superproject\nworkspace_root: {root}\nvaults:\n  - {{id: public, path: public}}\n  - {{id: private, path: missing, confidentiality: internal}}\n", encoding="utf-8")
            projection = VaultRegistry(public, manifest).local_projection()
            self.assertEqual(projection["unavailable_vaults"], [{"vault_id": "private", "state": "unavailable", "reason": "vault_unavailable"}])

    def test_local_projection_rejects_public_scope(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); subprocess.run(["git", "init", "-q", str(root)], check=True)
            with self.assertRaisesRegex(ValueError, "projection_scope_invalid"):
                VaultRegistry(root).local_projection("public")

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

    def test_backup_manifest_can_be_exported_without_claiming_verified_target(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); subprocess.run(["git", "init", "-q", str(root)], check=True)
            manager = BackupManager(root)
            created = manager.create_manifest("public")
            external = root.parent / (root.name + "-backup-target")
            try:
                external.mkdir()
                result = manager.export_manifest(root / created["path"], external)
                self.assertEqual(result["state"], "exported")
                self.assertEqual(result["backup_state"], "configured")
                self.assertTrue((external / Path(created["path"]).name).is_file())
            finally:
                (external / Path(created["path"]).name).unlink(missing_ok=True)
                external.rmdir() if external.is_dir() else None

    def test_backup_manifest_must_live_under_declared_owner(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); subprocess.run(["git", "init", "-q", str(root)], check=True)
            manager = BackupManager(root)
            created = manager.create_manifest("public")
            copied = root / "outside-backup.json"
            copied.write_bytes((root / created["path"]).read_bytes())
            result = manager.verify_manifest(copied)
            self.assertEqual(result["error_code"], "manifest_owner_mismatch")

    def test_backup_rejects_manifest_with_rehashed_tampered_durable_record(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); subprocess.run(["git", "init", "-q", str(root)], check=True)
            manager = BackupManager(root)
            operation = root / "audit" / "operations" / "op-one.json"; operation.parent.mkdir(parents=True)
            operation.write_text(json.dumps({"operation_id": "op-one", "state": "previewed", "record_sha256": "sha256:wrong"}) + "\n", encoding="utf-8")
            manifest = manager.create_manifest("public")
            data = json.loads((root / manifest["path"]).read_text())
            # Simulate an attacker changing both entry and manifest hashes.
            operation.write_text(json.dumps({"operation_id": "op-one", "state": "applied", "record_sha256": "sha256:wrong"}) + "\n", encoding="utf-8")
            for entry in data["entries"]:
                if entry["path"] == "audit/operations/op-one.json":
                    entry["sha256"] = "sha256:" + __import__("hashlib").sha256(operation.read_bytes()).hexdigest()
            data["manifest_sha256"] = "sha256:" + __import__("hashlib").sha256(__import__("tools.common", fromlist=["canonical_json"]).canonical_json({k: v for k, v in data.items() if k != "manifest_sha256"})).hexdigest()
            (root / manifest["path"]).write_text(json.dumps(data), encoding="utf-8")
            failed = manager.verify_manifest(root / manifest["path"])
            self.assertEqual(failed["error_code"], "durable_record_hash_mismatch")

    def test_verified_manifest_restores_to_empty_checkout(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); subprocess.run(["git", "init", "-q", str(root)], check=True)
            (root / "wiki").mkdir(); (root / "wiki" / "item.md").write_text("# item\n", encoding="utf-8")
            config = root / "manifest.yaml"
            config.write_text(f"schema_version: 1\nlayout: direct-checkout\nworkspace_root: {root}\nvaults:\n  - {{id: public, path: ., private_git_remote: opaque-backup}}\n", encoding="utf-8")
            manager = BackupManager(root, config); manifest = manager.create_manifest("public")
            with tempfile.TemporaryDirectory() as out:
                target = Path(out) / "checkout"
                restored = manager.restore_manifest(root / manifest["path"], target)
                self.assertEqual(restored["state"], "restored")
                self.assertEqual((target / "wiki" / "item.md").read_text(encoding="utf-8"), "# item\n")
            status = manager.status()
            self.assertEqual(next(v for v in status["vaults"] if v["vault_id"] == "public")["backup_state"], "verified")

    def test_restore_marker_tampering_does_not_derive_verified(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); subprocess.run(["git", "init", "-q", str(root)], check=True)
            config = root / "manifest.yaml"
            config.write_text(f"schema_version: 1\nlayout: direct-checkout\nworkspace_root: {root}\nvaults:\n  - {{id: public, path: ., private_git_remote: opaque-backup}}\n", encoding="utf-8")
            manager = BackupManager(root, config); manifest = manager.create_manifest("public")
            with tempfile.TemporaryDirectory() as out:
                manager.restore_manifest(root / manifest["path"], Path(out) / "checkout")
            marker = next((root / "audit" / "backup" / "restores").glob("*.json"))
            value = json.loads(marker.read_text(encoding="utf-8")); value["state"] = "forged"; marker.write_text(json.dumps(value), encoding="utf-8")
            status = manager.status()
            self.assertEqual(next(v for v in status["vaults"] if v["vault_id"] == "public")["backup_state"], "configured")

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

    def test_restore_cleans_partial_checkout_after_write_failure(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); subprocess.run(["git", "init", "-q", str(root)], check=True)
            (root / "wiki").mkdir(); (root / "wiki" / "one.md").write_text("one", encoding="utf-8")
            (root / "wiki" / "two.md").write_text("two", encoding="utf-8")
            manager = BackupManager(root); manifest = manager.create_manifest("public")
            with tempfile.TemporaryDirectory() as out:
                target = Path(out) / "checkout"
                original = __import__("tools.backup", fromlist=["atomic_write"]).atomic_write
                calls = {"count": 0}
                def fail_second(path, content, mode=0o600):
                    calls["count"] += 1
                    if calls["count"] == 2:
                        raise OSError("injected restore failure")
                    return original(path, content, mode)
                with mock.patch("tools.backup.atomic_write", side_effect=fail_second):
                    result = manager.restore_manifest(root / manifest["path"], target)
                self.assertEqual(result["state"], "failed")
                self.assertEqual(result["restored_entries"], 0)
                self.assertFalse(target.exists() and any(target.rglob("*")))

    def test_backup_status_derives_failed_from_corrupt_latest_manifest(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); subprocess.run(["git", "init", "-q", str(root)], check=True)
            config = root / "manifest.yaml"
            config.write_text(f"schema_version: 1\nlayout: direct-checkout\nworkspace_root: {root}\nvaults:\n  - {{id: public, path: ., private_git_remote: file://backup}}\n", encoding="utf-8")
            manager = BackupManager(root, config)
            created = manager.create_manifest("public")
            path = root / created["path"]
            data = json.loads(path.read_text(encoding="utf-8")); data["entries"] = "corrupt"
            path.write_text(json.dumps(data), encoding="utf-8")
            status = manager.status()
            vault = status["vaults"][0]
            self.assertEqual(vault["backup_state"], "failed")
            self.assertEqual(vault["backup_reason"], "manifest_invalid")

    def test_valid_manifest_alone_does_not_claim_verified_target(self):
        """配置了 target 但未完成恢复演练时，状态保持 configured。"""
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); subprocess.run(["git", "init", "-q", str(root)], check=True)
            config = root / "manifest.yaml"
            config.write_text(
                f"schema_version: 1\nlayout: direct-checkout\nworkspace_root: {root}\n"
                "vaults:\n  - {id: public, path: ., private_git_remote: file://backup}\n",
                encoding="utf-8",
            )
            manager = BackupManager(root, config)
            created = manager.create_manifest("public")
            assert manager.verify_manifest(root / created["path"])["backup_state"] == "verified"
            vault = next(item for item in manager.status()["vaults"] if item["vault_id"] == "public")
            self.assertEqual(vault["backup_state"], "configured")

    def test_backup_rejects_hardlink_entries(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); subprocess.run(["git", "init", "-q", str(root)], check=True)
            (root / "wiki").mkdir(); source = root / "outside"; source.write_text("secret", encoding="utf-8")
            (root / "wiki" / "linked.md").hardlink_to(source)
            with self.assertRaisesRegex(ValueError, "entry_hardlink"):
                BackupManager(root).create_manifest("public")


if __name__ == "__main__":
    unittest.main()
