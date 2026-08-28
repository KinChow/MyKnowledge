"""Explicit cross-Vault copy/move operations (F011).

Transfers are local, owner-aware operations. They do not create cross-Vault
references; callers must choose a new target object and review its
confidentiality before applying.
"""
from __future__ import annotations

from pathlib import Path

from .common import atomic_write, canonical_json, hash_canonical, safe_id, sha256_bytes
from .operation_store import OperationStore
from .vault_lock import LockBusyError, VaultLockGroup
from .vault_registry import VaultRegistry


class VaultTransfer:
    def __init__(self, root: Path, manifest: Path | None = None) -> None:
        self.root = Path(root).resolve()
        self.registry = VaultRegistry(self.root, manifest)
        self.store = OperationStore(self.root)

    def _vault_confidentiality(self, vault_id: str) -> str:
        data = self.registry._load()
        for item in data["vaults"]:
            if str(item.get("id")) == vault_id:
                return str(item.get("confidentiality", "public"))
        raise ValueError("vault_not_found")

    def _path(self, vault_id: str, relative: str) -> Path:
        safe_id(vault_id)
        if not isinstance(relative, str) or not relative or Path(relative).is_absolute() or ".." in Path(relative).parts:
            raise ValueError("path_invalid")
        owner = self.registry.resolve_vault_path(vault_id)
        path = (owner / relative).resolve()
        try:
            path.relative_to(owner)
        except ValueError as exc:
            raise ValueError("path_outside_repo") from exc
        current = owner
        for part in Path(relative).parts:
            current = current / part
            if current.is_symlink():
                raise ValueError("path_symlink")
        return path

    def preview(self, source_vault_id: str, source_path: str, target_vault_id: str,
                target_path: str, *, move: bool = False) -> dict:
        try:
            source_vault_id = safe_id(source_vault_id)
            target_vault_id = safe_id(target_vault_id)
            source = self._path(source_vault_id, source_path)
            target = self._path(target_vault_id, target_path)
            source_conf = self._vault_confidentiality(source_vault_id)
            target_conf = self._vault_confidentiality(target_vault_id)
            source_status = next(x for x in self.registry.check()["vaults"] if x["vault_id"] == source_vault_id)
            target_status = next(x for x in self.registry.check()["vaults"] if x["vault_id"] == target_vault_id)
            if source_vault_id == target_vault_id:
                return {"state": "blocked", "error_code": "same_vault_transfer"}
            if source_status.get("state") != "available" or target_status.get("state") != "available":
                return {"state": "blocked", "error_code": "vault_unavailable"}
            if not source.is_file() or source.is_symlink():
                return {"state": "blocked", "error_code": "source_unavailable"}
            if source.stat().st_nlink > 1:
                return {"state": "blocked", "error_code": "source_hardlink"}
            if target.exists():
                return {"state": "blocked", "error_code": "target_exists"}
            if source_conf == "internal" and target_conf != "internal":
                return {"state": "blocked", "error_code": "confidentiality_downgrade",
                        "source_vault_id": source_vault_id, "target_vault_id": target_vault_id}
            content = source.read_bytes()
            source_hash = sha256_bytes(content)
            operation_type = "move" if move else "copy"
            input_hash = hash_canonical({"operation_type": operation_type, "source_vault_id": source_vault_id,
                                         "source_path": source_path, "target_vault_id": target_vault_id,
                                         "target_path": target_path, "source_hash": source_hash})
            record = self.store.new({"operation_type": operation_type, "target_vault": target_vault_id,
                                     "source_vault": source_vault_id, "source_path": source_path,
                                     "target_path": target_path, "source_hash": source_hash,
                                     "input_hash": input_hash, "content": content.decode("utf-8", errors="strict")})
            return {"state": "previewed", "operation_id": record["operation_id"], "source_vault_id": source_vault_id,
                    "target_vault_id": target_vault_id, "source_path": source_path, "target_path": target_path,
                    "source_hash": source_hash, "input_hash": input_hash, "requires_confirmation": True}
        except (OSError, UnicodeDecodeError, ValueError, StopIteration) as exc:
            return {"state": "blocked", "error_code": str(exc)}

    def apply(self, operation_id: str, *, confirmed: bool = False, actor_id: str = "local-user", confirmation: dict | None = None) -> dict:
        record, error = self.store.apply_preflight(operation_id, ("copy", "move"), confirmed)
        if error is not None:
            return error
        # 与 write 通道同语义：提供确认事件时严格校验（跨 vault 迁移是高敏感
        # 操作，F011 review 补齐确认一致性）
        confirmed_event = None
        if confirmation is not None:
            from .operation_store import validate_apply_confirmation
            code = validate_apply_confirmation(record, confirmation)
            if code is not None:
                return {"state": "blocked", "operation_id": operation_id, "error_code": code, "next_action": "re-preview and have a human confirm the current hashes"}
            confirmed_event = confirmation
        source_vault = str(record.get("source_vault", "")); target_vault = str(record.get("target_vault", ""))
        try:
            with VaultLockGroup(self.root, [source_vault, target_vault], operation_id) as locks:
                source = self._path(source_vault, str(record["source_path"]))
                target = self._path(target_vault, str(record["target_path"]))
                if not source.is_file() or source.is_symlink() or source.stat().st_nlink > 1:
                    return self.store.update(record, "expired", error_code="source_changed") | {"state": "expired", "error_code": "source_changed"}
                if sha256_bytes(source.read_bytes()) != record.get("source_hash"):
                    return self.store.update(record, "expired", error_code="hash_mismatch") | {"state": "expired", "error_code": "hash_mismatch"}
                if target.exists():
                    return self.store.update(record, "expired", error_code="target_exists") | {"state": "expired", "error_code": "target_exists"}
                locks.assert_owner()
                atomic_write(target, record["content"].encode("utf-8"), 0o600)
                try:
                    if sha256_bytes(target.read_bytes()) != record.get("source_hash"):
                        raise ValueError("target_hash_mismatch")
                    if record.get("operation_type") == "move":
                        locks.assert_owner()
                        source.unlink()
                except BaseException:
                    target.unlink(missing_ok=True)
                    raise
                updated = self.store.update(record, "applied", actor_id=actor_id,
                                            confirmation=confirmed_event or {"actor_type": "human", "actor_id": actor_id, "scope": "apply"},
                                            applied_files=[str(record["target_path"])])
                return {"state": "applied", "operation_id": operation_id, "source_vault_id": source_vault,
                        "target_vault_id": target_vault, "applied_files": updated["applied_files"]}
        except LockBusyError:
            return {"state": "blocked", "operation_id": operation_id, "error_code": "lock_busy"}
        except (OSError, ValueError) as exc:
            self.store.update(record, "expired", error_code="apply_failed")
            return {"state": "expired", "operation_id": operation_id, "error_code": "apply_failed", "detail": str(exc)}
