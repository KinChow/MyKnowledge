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
        data = {"schema_version": "backup-manifest/v1", "backup_id": backup_id, "vault_id": vault_id, "generated_at": time.time(), "vault_state": status["state"], "backup_state": status["backup_state"], "head_sha256": status.get("head_sha256"), "entries": []}
        data["manifest_sha256"] = "sha256:" + hashlib.sha256(canonical_json(data)).hexdigest()
        path = RepoPaths(self.root).audit_backup / f"{backup_id}.json"
        atomic_write(path, canonical_json(data) + b"\n", 0o600)
        return {**data, "path": str(path.relative_to(self.root))}
