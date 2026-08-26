"""Backup status and durable manifest primitives (F012, local-only)."""
from __future__ import annotations
import hashlib, json, time, uuid
from pathlib import Path
from .common import atomic_write, canonical_json, hash_canonical
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
            except (OSError, ValueError, json.JSONDecodeError):
                vault["backup_state"] = "failed"
                vault["backup_reason"] = "manifest_unreadable"
        report["backup_summary"]["unverified_vault_ids"] = [x["vault_id"] for x in report["vaults"] if x["backup_state"] != "verified"]
        report["backup_summary"]["warning"] = [
            {"vault_id": v["vault_id"], "code": "backup_not_configured"}
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
            for entry in data.get("entries", []):
                rel = Path(str(entry.get("path", "")))
                if rel.is_absolute() or ".." in rel.parts:
                    raise ValueError("entry_path_invalid")
                entry_path = owner_root / rel
                if not entry_path.is_file() or entry_path.is_symlink():
                    raise ValueError("entry_missing")
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
                destination.parent.mkdir(parents=True, exist_ok=True)
                atomic_write(destination, source.read_bytes(), 0o600)
                created.append(destination)
            return {"state": "restored", "backup_state": "verified", "restored_entries": len(created), "target": str(target)}
        except (OSError, ValueError) as exc:
            for path in reversed(created):
                path.unlink(missing_ok=True)
            return {"state": "failed", "error_code": str(exc), "restored_entries": 0}
