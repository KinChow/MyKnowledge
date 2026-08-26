"""Private vault registry and read-only readiness report (F011)."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

import yaml

from .common import canonical_json, safe_id
from .paths import RepoPaths


class VaultRegistry:
    def __init__(self, root: Path, manifest: Path | None = None) -> None:
        self.root = Path(root).resolve()
        self.manifest = manifest or RepoPaths(self.root).vaults_local_manifest

    def _load(self) -> dict:
        if self.manifest.exists():
            data = yaml.safe_load(self.manifest.read_text(encoding="utf-8")) or {}
        else:
            data = {"schema_version": 1, "layout": "direct-checkout", "workspace_root": None, "public_vault_id": "public", "vaults": [{"id": "public", "path": ".", "type": "git-checkout", "confidentiality": "public", "required": True, "allow_public_projection": True, "backup_state": "unconfigured"}]}
        if not isinstance(data, dict) or not isinstance(data.get("vaults"), list):
            raise ValueError("manifest_invalid")
        return data

    @staticmethod
    def _backup_state(item: dict) -> str:
        remote = item.get("private_git_remote")
        backup = item.get("encrypted_backup_target")
        if not remote and not backup:
            return "unconfigured"
        return "configured"

    def resolve_vault_path(self, vault_id: str) -> Path:
        """Resolve one owner checkout without exposing its path in reports."""
        data = self._load()
        workspace = self.root if data.get("workspace_root") in (None, "") else Path(data["workspace_root"]).expanduser().resolve()
        layout = data.get("layout", "direct-checkout")
        for item in data["vaults"]:
            if str(item.get("id", "")) != vault_id:
                continue
            raw_path = item.get("path")
            if raw_path == "." and vault_id == data.get("public_vault_id", "public") and layout == "direct-checkout":
                path = self.root
            elif not isinstance(raw_path, str) or not raw_path or Path(raw_path).is_absolute():
                raise ValueError("path_invalid")
            else:
                path = (workspace / raw_path).resolve()
            path.relative_to(workspace)
            if not path.is_dir():
                raise ValueError("vault_unavailable")
            return path
        raise ValueError("vault_not_found")

    def check(self) -> dict:
        data = self._load()
        layout = data.get("layout", "direct-checkout")
        if layout not in {"direct-checkout", "superproject"}:
            raise ValueError("layout_invalid")
        workspace = self.root if data.get("workspace_root") in (None, "") else Path(data["workspace_root"]).expanduser().resolve()
        statuses: list[dict] = []
        resolved: list[tuple[str, Path]] = []
        available_paths: dict[str, Path] = {}
        seen: set[str] = set()
        for item in data["vaults"]:
            vault_id = str(item.get("id", ""))
            status = {"vault_id": vault_id, "state": "unavailable", "reason": "manifest_invalid", "backup_state": self._backup_state(item), "object_count": None}
            try:
                safe_id(vault_id)
                if vault_id in seen:
                    raise ValueError("duplicate_vault_id")
                seen.add(vault_id)
                confidentiality = item.get("confidentiality", "public" if vault_id == data.get("public_vault_id", "public") else "internal")
                if confidentiality not in {"public", "internal"}:
                    raise ValueError("confidentiality_invalid")
                if bool(item.get("allow_public_projection", False)) and (
                    vault_id != data.get("public_vault_id", "public") or confidentiality != "public"
                ):
                    raise ValueError("public_projection_confidentiality")
                raw_path = item.get("path")
                if raw_path == "." and vault_id == data.get("public_vault_id", "public") and layout == "direct-checkout":
                    path = self.root
                elif not isinstance(raw_path, str) or not raw_path or Path(raw_path).is_absolute():
                    raise ValueError("path_invalid")
                else:
                    path = (workspace / raw_path).resolve()
                try:
                    path.relative_to(workspace)
                except ValueError as exc:
                    raise ValueError("path_invalid") from exc
                for other_id, other in resolved:
                    if path == other or path in other.parents or other in path.parents:
                        raise ValueError("path_overlap")
                resolved.append((vault_id, path))
                if not path.is_dir():
                    raise ValueError("vault_unavailable")
                probe = subprocess.run(["git", "-C", str(path), "rev-parse", "--show-toplevel"], capture_output=True, text=True, timeout=5, check=False)
                if probe.returncode != 0 or Path(probe.stdout.strip()).resolve() != path:
                    raise ValueError("git_worktree_invalid")
                head = subprocess.run(["git", "-C", str(path), "rev-parse", "HEAD"], capture_output=True, text=True, timeout=5, check=False)
                status.update({"state": "available", "reason": "none", "head_sha256": "sha256:" + hashlib.sha256(head.stdout.strip().encode()).hexdigest() if head.returncode == 0 else None})
                available_paths[vault_id] = path
            except (OSError, ValueError, subprocess.SubprocessError) as exc:
                status["reason"] = str(exc)
            statuses.append(status)
        statuses.sort(key=lambda x: x["vault_id"])
        conflicts: list[dict] = []
        affected: list[dict] = []
        for status in statuses:
            path = available_paths.get(status["vault_id"])
            if path is None:
                continue
            seen_objects: set[tuple[str, str]] = set()
            count = 0
            for object_type, folder in (("wiki", "wiki"), ("source", "sources")):
                base = path / folder
                for item in sorted(base.rglob("*.md")) if base.is_dir() else []:
                    if not item.is_file() or item.is_symlink():
                        continue
                    key = (object_type, item.stem)
                    ref = {"vault_id": status["vault_id"], "object_type": object_type, "object_id": item.stem}
                    if key in seen_objects:
                        conflicts.append({"code": "duplicate_object_id", "object_ref": ref})
                        affected.append(ref)
                    else:
                        seen_objects.add(key)
                        count += 1
            status["object_count"] = count
        available_scopes: list[str] = []
        if any(item["vault_id"] == "public" and item["state"] == "available" for item in statuses):
            available_scopes.append("public")
        if any(item["state"] == "available" for item in statuses):
            available_scopes.append("local")
        if any(item["vault_id"] != "public" and item["state"] == "available" for item in statuses):
            available_scopes.append("private")
        report = {"schema_version": "vault-check/v1", "generated_from": "sha256:" + hashlib.sha256(str(self.root).encode()).hexdigest(), "vaults": statuses, "conflicts": conflicts, "affected_object_refs": affected, "backup_summary": {"unverified_vault_ids": [x["vault_id"] for x in statuses if x["backup_state"] != "verified"]}, "available_scopes": available_scopes, "report_sha256": ""}
        report["report_sha256"] = "sha256:" + hashlib.sha256(canonical_json({k: v for k, v in report.items() if k != "report_sha256"})).hexdigest()
        return report

    def validate_reference(self, owner_vault_id: str, target_vault_id: str | None = None,
                           object_type: str = "source", object_id: str = "") -> dict:
        """Validate an owner-scoped reference without guessing across vaults."""
        owner = safe_id(str(owner_vault_id))
        target = owner if target_vault_id in (None, "") else safe_id(str(target_vault_id))
        result = {"valid": False, "code": None, "owner_vault_id": owner,
                  "target_vault_id": target, "object_ref": {
                      "vault_id": target, "object_type": object_type, "object_id": object_id}}
        if target != owner:
            result["code"] = "cross_vault_reference"
            return result
        report = self.check()
        status = next((item for item in report["vaults"] if item["vault_id"] == target), None)
        if status is None:
            result["code"] = "vault_not_found"
            return result
        if status["state"] != "available":
            result["code"] = "vault_unavailable"
            return result
        if any(conflict.get("object_ref") == result["object_ref"] for conflict in report["conflicts"]):
            result["code"] = "duplicate_object_id"
            return result
        result["valid"] = True
        result["code"] = "ok"
        return result

    def object_index(self) -> dict[tuple[str, str, str], dict]:
        """Build an owner-aware local object index with no physical paths in values."""
        report = self.check()
        index: dict[tuple[str, str, str], dict] = {}
        for status in report["vaults"]:
            vault_id = status["vault_id"]
            if status["state"] != "available":
                continue
            try:
                root = self.resolve_vault_path(vault_id)
            except (OSError, ValueError):
                continue
            for object_type, folder in (("wiki", "wiki"), ("source", "sources")):
                base = root / folder
                for path in sorted(base.rglob("*.md")) if base.is_dir() else []:
                    if not path.is_file() or path.is_symlink():
                        continue
                    key = (vault_id, object_type, path.stem)
                    if key in index:
                        index[key] = {"vault_id": vault_id, "object_type": object_type, "object_id": path.stem, "availability": "conflict", "availability_reason": "duplicate_object_id"}
                        continue
                    index[key] = {"vault_id": vault_id, "object_type": object_type, "object_id": path.stem, "availability": "available", "availability_reason": "none"}
        return index

    @staticmethod
    def effective_confidentiality(owner_confidentiality: str, upstream_confidentialities: list[str] | None = None) -> str:
        """Propagate the highest confidentiality from owner and upstream objects."""
        levels = {"public": 0, "internal": 1}
        values = [owner_confidentiality, *(upstream_confidentialities or [])]
        return "internal" if max((levels.get(value, 1) for value in values), default=0) else "public"


def main(argv: list[str] | None = None) -> int:
    import argparse
    parser = argparse.ArgumentParser(description="Check MyKnowledge vaults")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--manifest", type=Path)
    args = parser.parse_args(argv)
    try:
        print(json.dumps(VaultRegistry(args.root, args.manifest).check(), ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError) as exc:
        print(json.dumps({"state": "blocked", "error_code": str(exc)}, ensure_ascii=False))
        return 2
