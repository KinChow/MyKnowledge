"""Backup status and durable manifest primitives (F012, local-only)."""
from __future__ import annotations
import hashlib, json, time, uuid
from pathlib import Path
from .common import atomic_write, canonical_json
from .vault_registry import VaultRegistry
from .paths import RepoPaths

class BackupManager:
    def __init__(self, root: Path, manifest: Path | None = None) -> None:
        self.root = Path(root).resolve(); self.registry = VaultRegistry(self.root, manifest)

    def status(self) -> dict:
        report = self.registry.check()
        report["backup_summary"]["warning"] = [
            {"vault_id": v["vault_id"], "code": "backup_not_configured"}
            for v in report["vaults"] if v["backup_state"] == "unconfigured" and v["vault_id"] != "public"
        ]
        return report

    def create_manifest(self, vault_id: str = "public") -> dict:
        status = next((x for x in self.status()["vaults"] if x["vault_id"] == vault_id), None)
        if status is None: raise ValueError("vault_not_found")
        backup_id = "backup_" + uuid.uuid4().hex
        entries = []
        if vault_id == "public":
            for folder in ("sources", "wiki", "archive", "audit"):
                base = self.root / folder
                if not base.is_dir():
                    continue
                for item in sorted(base.rglob("*")):
                    if item.is_file() and not item.is_symlink():
                        entries.append({"path": str(item.relative_to(self.root)), "sha256": "sha256:" + hashlib.sha256(item.read_bytes()).hexdigest(), "size": item.stat().st_size})
        data = {"schema_version": "backup-manifest/v1", "backup_id": backup_id, "vault_id": vault_id, "generated_at": time.time(), "vault_state": status["state"], "backup_state": status["backup_state"], "head_sha256": status.get("head_sha256"), "entries": entries}
        data["manifest_sha256"] = "sha256:" + hashlib.sha256(canonical_json(data)).hexdigest()
        path = RepoPaths(self.root).audit_backup / f"{backup_id}.json"
        atomic_write(path, canonical_json(data) + b"\n", 0o600)
        return {**data, "path": str(path.relative_to(self.root))}

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
            for entry in data.get("entries", []):
                entry_path = self.root / str(entry.get("path", ""))
                if not entry_path.is_file() or entry_path.is_symlink():
                    raise ValueError("entry_missing")
                actual = "sha256:" + hashlib.sha256(entry_path.read_bytes()).hexdigest()
                if actual != entry.get("sha256"):
                    raise ValueError("hash_mismatch")
            relative = str(path.resolve().relative_to(self.root.resolve()))
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
        created: list[Path] = []
        try:
            for entry in data.get("entries", []):
                rel = Path(str(entry.get("path", "")))
                if rel.is_absolute() or ".." in rel.parts:
                    raise ValueError("entry_path_invalid")
                source = self.root / rel
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
