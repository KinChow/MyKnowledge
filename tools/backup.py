"""Backup status and durable manifest primitives (F012, local-only)."""
from __future__ import annotations
import hashlib, json, time, uuid, shutil
from pathlib import Path
from .common import atomic_write, canonical_json, hash_canonical, safe_id
from .release_confirmation import validate_event
from .vault_registry import VaultRegistry
from .paths import RepoPaths

class BackupManager:
    def __init__(self, root: Path, manifest: Path | None = None) -> None:
        self.root = Path(root).resolve(); self.registry = VaultRegistry(self.root, manifest)

    def status(self) -> dict:
        report = self.registry.check()
        # A configured target is not verified merely because a manifest exists.
        # A malformed newest durable manifest is, however, an observable failure.
        for vault in report["vaults"]:
            if vault.get("backup_state") != "configured" or vault.get("state") != "available":
                continue
            try:
                owner = self.registry.resolve_vault_path(vault["vault_id"])
                manifests = sorted((owner / "audit" / "backup").glob("*.json"))
                if not manifests:
                    continue
                data = json.loads(manifests[-1].read_text(encoding="utf-8"))
                expected = "sha256:" + hashlib.sha256(canonical_json({k: v for k, v in data.items() if k != "manifest_sha256"})).hexdigest()
                if data.get("schema_version") != "backup-manifest/v1" or data.get("manifest_sha256") != expected or not isinstance(data.get("entries"), list):
                    vault["backup_state"] = "failed"
                    vault["backup_reason"] = "manifest_invalid"
                else:
                    restore_dir = owner / "audit" / "backup" / "restores"
                    markers = sorted(restore_dir.glob(f"{data.get('backup_id', '')}-*.json")) if restore_dir.is_dir() else []
                    for marker_path in reversed(markers):
                        marker = json.loads(marker_path.read_text(encoding="utf-8"))
                        marker_hash = "sha256:" + hashlib.sha256(canonical_json({k: v for k, v in marker.items() if k != "record_sha256"})).hexdigest()
                        if marker.get("schema_version") == "backup-restore-record/v1" and marker.get("manifest_sha256") == expected and marker.get("record_sha256") == marker_hash and marker.get("state") == "restored":
                            vault["backup_state"] = "verified"
                            vault["backup_reason"] = "isolated_restore_verified"
                            break
            except (OSError, ValueError, json.JSONDecodeError):
                vault["backup_state"] = "failed"
                vault["backup_reason"] = "manifest_unreadable"
        report["backup_summary"]["unverified_vault_ids"] = [x["vault_id"] for x in report["vaults"] if x["backup_state"] != "verified"]
        report["backup_summary"]["warning"] = [
            {"vault_id": v["vault_id"], "code": "backup_not_configured", "next_action": "configure and verify an owner-scoped backup target"}
            for v in report["vaults"] if v["backup_state"] == "unconfigured" and v["vault_id"] != "public"
        ]
        return report

    def create_manifest(self, vault_id: str = "public") -> dict:
        status = next((x for x in self.status()["vaults"] if x["vault_id"] == vault_id), None)
        if status is None: raise ValueError("vault_not_found")
        owner_root = self.registry.resolve_vault_path(vault_id)
        backup_id = "backup_" + uuid.uuid4().hex
        entries = []
        for folder in ("sources", "wiki", "archive", "audit", "practice"):
            base = owner_root / folder
            if not base.is_dir():
                continue
            for item in sorted(base.rglob("*")):
                if item.is_file() and not item.is_symlink():
                    if item.stat().st_nlink > 1:
                        raise ValueError("entry_hardlink")
                    entries.append({"path": str(item.relative_to(owner_root)), "sha256": "sha256:" + hashlib.sha256(item.read_bytes()).hexdigest(), "size": item.stat().st_size})
        data = {"schema_version": "backup-manifest/v1", "backup_id": backup_id, "vault_id": vault_id, "owner_root": ".", "generated_at": time.time(), "vault_state": status["state"], "backup_state": status["backup_state"], "head_sha256": status.get("head_sha256"), "entries": entries}
        data["manifest_sha256"] = "sha256:" + hashlib.sha256(canonical_json(data)).hexdigest()
        path = RepoPaths(owner_root).audit_backup / f"{backup_id}.json"
        atomic_write(path, canonical_json(data) + b"\n", 0o600)
        return {**data, "path": str(path.relative_to(owner_root))}

    def verify_manifest(self, manifest_path: Path) -> dict:
        """Verify one durable manifest without changing Vault or backup state."""
        path = Path(manifest_path)
        if not path.is_absolute():
            path = self.root / path
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            if data.get("schema_version") != "backup-manifest/v1":
                raise ValueError("manifest_schema_invalid")
            expected = "sha256:" + hashlib.sha256(canonical_json({k: v for k, v in data.items() if k != "manifest_sha256"})).hexdigest()
            if data.get("manifest_sha256") != expected:
                raise ValueError("hash_mismatch")
            vault_id = str(data.get("vault_id", ""))
            status = next((x for x in self.status()["vaults"] if x["vault_id"] == vault_id), None)
            if status is None:
                raise ValueError("vault_not_found")
            if status.get("state") != "available":
                raise ValueError("vault_unavailable")
            owner_root = self.registry.resolve_vault_path(vault_id)
            expected_dir = (owner_root / "audit" / "backup").resolve()
            try:
                path.resolve().relative_to(expected_dir)
            except ValueError as exc:
                raise ValueError("manifest_owner_mismatch") from exc
            for entry in data.get("entries", []):
                rel = Path(str(entry.get("path", "")))
                if rel.is_absolute() or ".." in rel.parts:
                    raise ValueError("entry_path_invalid")
                entry_path = owner_root / rel
                if not entry_path.is_file() or entry_path.is_symlink():
                    raise ValueError("entry_missing")
                if entry_path.stat().st_nlink > 1:
                    raise ValueError("entry_hardlink")
                actual = "sha256:" + hashlib.sha256(entry_path.read_bytes()).hexdigest()
                if actual != entry.get("sha256"):
                    raise ValueError("hash_mismatch")
                rel_text = rel.as_posix()
                if rel_text.startswith("audit/operations/"):
                    record = json.loads(entry_path.read_text(encoding="utf-8"))
                    if not record.get("record_sha256") or hash_canonical({k: v for k, v in record.items() if k != "record_sha256"}) != record.get("record_sha256"):
                        raise ValueError("durable_record_hash_mismatch")
                elif rel_text.startswith("release/public-confirmations/"):
                    event = json.loads(entry_path.read_text(encoding="utf-8"))
                    if not event.get("event_sha256") or not validate_event(event).get("valid"):
                        raise ValueError("confirmation_record_invalid")
            relative = str(path.resolve().relative_to(owner_root.resolve()))
            return {"state": "verified", "backup_state": "verified", "vault_id": vault_id, "manifest_sha256": expected, "path": relative}
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            try:
                relative = str(path.resolve().relative_to(self.root.resolve()))
            except ValueError:
                relative = None
            return {"state": "failed", "backup_state": "failed", "error_code": str(exc), "path": relative}

    def export_manifest(self, manifest_path: Path, target: Path) -> dict:
        """Copy a verified owner manifest to an explicit external target.

        This is transport evidence only; it never derives ``verified`` status.
        """
        checked = self.verify_manifest(manifest_path)
        if checked.get("backup_state") != "verified":
            return {"state": "blocked", "error_code": checked.get("error_code", "manifest_unverified")}
        source = Path(manifest_path)
        if not source.is_absolute():
            source = self.root / source
        destination = Path(target).expanduser().resolve()
        if destination == self.root or self.root in destination.parents:
            return {"state": "blocked", "error_code": "backup_target_invalid"}
        if destination.exists() and destination.is_dir():
            destination = destination / source.name
        destination.parent.mkdir(parents=True, exist_ok=True)
        atomic_write(destination, source.read_bytes(), 0o600)
        return {"state": "exported", "backup_state": "configured", "manifest_sha256": checked["manifest_sha256"], "target": str(destination)}

    def export_bundle(self, manifest_path: Path, target: Path) -> dict:
        """Export manifest and listed owner files into an explicit offline bundle."""
        checked = self.verify_manifest(manifest_path)
        if checked.get("backup_state") != "verified":
            return {"state": "blocked", "error_code": checked.get("error_code", "manifest_unverified")}
        source_manifest = Path(manifest_path)
        if not source_manifest.is_absolute():
            source_manifest = self.root / source_manifest
        bundle = Path(target).expanduser().resolve()
        if bundle == self.root or self.root in bundle.parents:
            return {"state": "blocked", "error_code": "backup_target_invalid"}
        if bundle.exists() and any(bundle.iterdir()):
            return {"state": "blocked", "error_code": "backup_target_not_empty"}
        bundle.mkdir(parents=True, exist_ok=True)
        data = json.loads(source_manifest.read_text(encoding="utf-8"))
        owner_root = self.registry.resolve_vault_path(str(data.get("vault_id", "")))
        try:
            atomic_write(bundle / "manifest.json", source_manifest.read_bytes(), 0o600)
            for entry in data.get("entries", []):
                rel = Path(str(entry.get("path", "")))
                if rel.is_absolute() or ".." in rel.parts:
                    raise ValueError("entry_path_invalid")
                source = owner_root / rel
                if not source.is_file() or source.is_symlink() or source.stat().st_nlink > 1:
                    raise ValueError("entry_invalid")
                destination = bundle / "payload" / rel
                destination.parent.mkdir(parents=True, exist_ok=True)
                atomic_write(destination, source.read_bytes(), 0o600)
            return {"state": "exported", "backup_state": "configured", "manifest_sha256": checked["manifest_sha256"], "target": str(bundle), "entry_count": len(data.get("entries", []))}
        except (OSError, ValueError) as exc:
            shutil.rmtree(bundle, ignore_errors=True)
            return {"state": "failed", "error_code": str(exc)}

    @staticmethod
    def verify_bundle(bundle: Path) -> dict:
        """Verify an offline bundle without reading any canonical checkout."""
        bundle = Path(bundle).resolve()
        try:
            data = json.loads((bundle / "manifest.json").read_text(encoding="utf-8"))
            expected = "sha256:" + hashlib.sha256(canonical_json({k: v for k, v in data.items() if k != "manifest_sha256"})).hexdigest()
            if data.get("schema_version") != "backup-manifest/v1" or data.get("manifest_sha256") != expected:
                raise ValueError("hash_mismatch")
            vault_id = data.get("vault_id")
            if not isinstance(vault_id, str):
                raise ValueError("vault_id_invalid")
            try:
                safe_id(vault_id)
            except ValueError as exc:
                raise ValueError("vault_id_invalid") from exc
            if not isinstance(data.get("entries"), list):
                raise ValueError("entries_invalid")
            for entry in data.get("entries", []):
                rel = Path(str(entry.get("path", "")))
                if rel.is_absolute() or ".." in rel.parts:
                    raise ValueError("entry_path_invalid")
                path = bundle / "payload" / rel
                if not path.is_file() or path.is_symlink() or path.stat().st_nlink > 1:
                    raise ValueError("entry_missing")
                actual = "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()
                if actual != entry.get("sha256"):
                    raise ValueError("hash_mismatch")
            return {"state": "verified", "backup_state": "verified", "manifest_sha256": expected, "entry_count": len(data.get("entries", []))}
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            return {"state": "failed", "backup_state": "failed", "error_code": str(exc)}

    @staticmethod
    def verify_restored_bundle(bundle: Path, target: Path) -> dict:
        """Verify the complete restored file set and owner marker in a target checkout."""
        bundle = Path(bundle).resolve()
        target = Path(target).resolve()
        checked = BackupManager.verify_bundle(bundle)
        if checked.get("backup_state") != "verified":
            return {"state": "failed", "error_code": checked.get("error_code", "bundle_unverified")}
        try:
            data = json.loads((bundle / "manifest.json").read_text(encoding="utf-8"))
            expected_manifest = checked["manifest_sha256"]
            expected_paths = set()
            for entry in data["entries"]:
                rel = Path(str(entry.get("path", "")))
                if rel.is_absolute() or ".." in rel.parts:
                    raise ValueError("entry_path_invalid")
                expected_paths.add(rel.as_posix())
                path = target / rel
                if not path.is_file() or path.is_symlink() or path.stat().st_nlink > 1:
                    raise ValueError("restored_entry_missing")
                actual = "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()
                if actual != entry.get("sha256"):
                    raise ValueError("restored_hash_mismatch")
            restore_dir = target / "audit" / "backup" / "restores"
            markers = sorted(restore_dir.glob(f"{data.get('backup_id', '')}-*.json")) if restore_dir.is_dir() else []
            valid_marker = False
            for marker_path in markers:
                marker = json.loads(marker_path.read_text(encoding="utf-8"))
                marker_hash = "sha256:" + hashlib.sha256(canonical_json({k: v for k, v in marker.items() if k != "record_sha256"})).hexdigest()
                if (marker.get("schema_version") == "backup-restore-record/v1"
                        and marker.get("vault_id") == data.get("vault_id")
                        and marker.get("manifest_sha256") == expected_manifest
                        and marker.get("record_sha256") == marker_hash
                        and marker.get("state") == "restored"):
                    valid_marker = True
                    break
            if not valid_marker:
                raise ValueError("restore_marker_missing")
            allowed_extra = {p.as_posix() for p in (target / "audit" / "backup" / "restores").rglob("*") if p.is_file()} if restore_dir.is_dir() else set()
            extras = []
            for path in target.rglob("*"):
                if not path.is_file() or path.is_symlink():
                    continue
                rel = path.relative_to(target).as_posix()
                if rel not in expected_paths and str(path) not in allowed_extra:
                    extras.append(rel)
            if extras:
                raise ValueError("restore_extra_entry")
            return {"state": "verified", "backup_state": "verified", "vault_id": data.get("vault_id"),
                    "manifest_sha256": expected_manifest, "entry_count": len(expected_paths)}
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            return {"state": "failed", "backup_state": "failed", "error_code": str(exc)}

    def restore_bundle(self, bundle: Path, target: Path) -> dict:
        """Restore a verified offline bundle into an explicitly empty checkout."""
        bundle = Path(bundle).resolve()
        target = Path(target).expanduser().resolve()
        if target == self.root or self.root in target.parents:
            return {"state": "blocked", "error_code": "restore_target_invalid"}
        checked = self.verify_bundle(bundle)
        if checked.get("backup_state") != "verified":
            return {"state": "blocked", "error_code": checked.get("error_code", "bundle_unverified")}
        if target.exists() and any(target.iterdir()):
            return {"state": "blocked", "error_code": "restore_target_not_empty"}
        target.mkdir(parents=True, exist_ok=True)
        created: list[Path] = []
        try:
            data = json.loads((bundle / "manifest.json").read_text(encoding="utf-8"))
            for entry in data.get("entries", []):
                rel = Path(str(entry.get("path", "")))
                if rel.is_absolute() or ".." in rel.parts:
                    raise ValueError("entry_path_invalid")
                source = bundle / "payload" / rel
                destination = target / rel
                if not source.is_file() or source.is_symlink() or source.stat().st_nlink > 1:
                    raise ValueError("entry_missing")
                destination.parent.mkdir(parents=True, exist_ok=True)
                atomic_write(destination, source.read_bytes(), 0o600)
                created.append(destination)
            marker = {"schema_version": "backup-restore-record/v1", "backup_id": data.get("backup_id"), "vault_id": data.get("vault_id"), "manifest_sha256": checked["manifest_sha256"], "restored_entries": len(created), "state": "restored", "recorded_at": time.time()}
            marker["record_sha256"] = "sha256:" + hashlib.sha256(canonical_json(marker)).hexdigest()
            marker_path = target / "audit" / "backup" / "restores" / f"{data.get('backup_id')}-{marker['record_sha256'].split(':', 1)[1][:16]}.json"
            atomic_write(marker_path, canonical_json(marker) + b"\n", 0o600)
            verified = self.verify_restored_bundle(bundle, target)
            if verified.get("backup_state") != "verified":
                raise ValueError(verified.get("error_code", "restore_verification_failed"))
            return {"state": "restored", "backup_state": "verified", "restored_entries": len(created), "target": str(target), "manifest_sha256": checked["manifest_sha256"]}
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            for path in reversed(created):
                path.unlink(missing_ok=True)
            for directory in sorted((p for p in target.rglob("*") if p.is_dir()), key=lambda p: len(p.parts), reverse=True):
                try:
                    directory.rmdir()
                except OSError:
                    pass
            try:
                target.rmdir()
            except OSError:
                pass
            return {"state": "failed", "error_code": str(exc), "restored_entries": 0}

    def restore_bundle_to_vault(self, bundle: Path, target: Path, target_vault_id: str) -> dict:
        """Restore a bundle only when its recorded owner matches an explicit target Vault.

        A filesystem path is not an identity boundary: callers must provide the
        intended Vault ID and the bundle owner must match before any target is
        created or modified.
        """
        try:
            owner = safe_id(str(target_vault_id))
        except ValueError:
            return {"state": "blocked", "error_code": "vault_id_invalid"}
        bundle_path = Path(bundle).resolve()
        checked = self.verify_bundle(bundle_path)
        if checked.get("backup_state") != "verified":
            return {"state": "blocked", "error_code": checked.get("error_code", "bundle_unverified")}
        try:
            data = json.loads((bundle_path / "manifest.json").read_text(encoding="utf-8"))
        except (OSError, ValueError, json.JSONDecodeError):
            return {"state": "blocked", "error_code": "bundle_unreadable"}
        if data.get("vault_id") != owner:
            return {
                "state": "blocked",
                "error_code": "cross_vault_restore",
                "source_vault_id": data.get("vault_id"),
                "target_vault_id": owner,
            }
        restored = self.restore_bundle(bundle_path, target)
        if restored.get("state") == "restored":
            restored["target_vault_id"] = owner
        return restored

    def restore_manifest(self, manifest_path: Path, target: Path) -> dict:
        """Restore verified local entries into an explicitly empty checkout."""
        target = Path(target).resolve()
        if target == self.root or self.root in target.parents:
            return {"state": "blocked", "error_code": "restore_target_invalid"}
        checked = self.verify_manifest(manifest_path)
        if checked.get("backup_state") != "verified":
            return {"state": "blocked", "error_code": checked.get("error_code", "manifest_unverified")}
        target.mkdir(parents=True, exist_ok=True)
        if any(target.iterdir()):
            return {"state": "blocked", "error_code": "restore_target_not_empty"}
        source_manifest = Path(manifest_path)
        if not source_manifest.is_absolute():
            source_manifest = self.root / source_manifest
        data = json.loads(source_manifest.read_text(encoding="utf-8"))
        owner_root = self.registry.resolve_vault_path(str(data.get("vault_id", "")))
        created: list[Path] = []
        try:
            for entry in data.get("entries", []):
                rel = Path(str(entry.get("path", "")))
                if rel.is_absolute() or ".." in rel.parts:
                    raise ValueError("entry_path_invalid")
                source = owner_root / rel
                destination = target / rel
                if not source.is_file() or source.is_symlink():
                    raise ValueError("entry_missing")
                if source.stat().st_nlink > 1:
                    raise ValueError("entry_hardlink")
                destination.parent.mkdir(parents=True, exist_ok=True)
                atomic_write(destination, source.read_bytes(), 0o600)
                created.append(destination)
            marker = {"schema_version": "backup-restore-record/v1", "backup_id": data.get("backup_id"), "vault_id": data.get("vault_id"), "manifest_sha256": checked["manifest_sha256"], "restored_entries": len(created), "state": "restored", "recorded_at": time.time()}
            marker["record_sha256"] = "sha256:" + hashlib.sha256(canonical_json(marker)).hexdigest()
            marker_dir = owner_root / "audit" / "backup" / "restores"
            marker_dir.mkdir(parents=True, exist_ok=True)
            atomic_write(marker_dir / f"{data.get('backup_id')}-{marker['record_sha256'].split(':', 1)[1][:16]}.json", canonical_json(marker) + b"\n", 0o600)
            return {"state": "restored", "backup_state": "verified", "restored_entries": len(created), "target": str(target)}
        except (OSError, ValueError) as exc:
            for path in reversed(created):
                path.unlink(missing_ok=True)
            # mkdir() may have created empty parent directories before a later
            # entry fails; remove only empty directories created in this target.
            for directory in sorted((p for p in target.rglob("*") if p.is_dir()), key=lambda p: len(p.parts), reverse=True):
                try:
                    directory.rmdir()
                except OSError:
                    pass
            try:
                target.rmdir()
            except OSError:
                pass
            return {"state": "failed", "error_code": str(exc), "restored_entries": 0}
