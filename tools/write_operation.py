"""通用 Preview/Apply 写入服务（F004）。

通用 writer 只负责文件事务与 operation 状态，不理解 Source/Wiki 领域字段。
领域校验由调用方在 preview 前完成；所有路径都必须位于当前仓库根目录。
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Callable, Mapping

from .common import atomic_write, canonical_json, crash_injection_point, hash_canonical, sha256_bytes
from .operation_store import OperationStore
from .vault_lock import LockBusyError, VaultLock
from .backup import BackupManager
from .vault_registry import VaultRegistry


class WriteOperation:
    def __init__(self, root: Path, *, projection_rebuilder: Callable[[dict], object] | None = None) -> None:
        self.root = Path(root).resolve()
        self.store = OperationStore(self.root)
        # Optional downstream projection/index hook. Canonical files commit first;
        # a failed hook leaves the operation recoverable as applied_index_pending.
        self.projection_rebuilder = projection_rebuilder

    def _vault_root(self, vault_id: str) -> Path:
        return self.root if vault_id == "public" else VaultRegistry(self.root).resolve_vault_path(vault_id)

    def _path(self, value: str, vault_id: str = "public") -> Path:
        vault_root = self._vault_root(vault_id)
        lexical = vault_root / value
        # Reject symlink components before resolve; resolving first would turn a
        # seemingly safe in-repo link into an unintended write target.
        current = vault_root
        for part in Path(value).parts:
            if part in {"", "."}:
                continue
            current = current / part
            if current.is_symlink():
                raise ValueError("path_symlink")
        path = lexical.resolve()
        try:
            path.relative_to(vault_root)
        except ValueError as exc:
            raise ValueError("path_outside_repo") from exc
        if path == vault_root:
            raise ValueError("invalid_target")
        return path

    def _operation_path(self, value: str, vault_id: str) -> Path:
        # Preserve the unary public path call used by existing integrations and
        # make private operations resolve against their owner checkout.
        return self._path(value) if vault_id == "public" else self._path(value, vault_id)

    def preview(self, files: Mapping[str, str], *, operation_type: str = "write", vault_id: str = "public") -> dict:
        if not files:
            return {"state": "blocked", "error_code": "empty_write"}
        try:
            targets = []
            vault_root = self._vault_root(vault_id)
            for name, content in sorted(files.items()):
                if not isinstance(content, str):
                    return {"state": "blocked", "error_code": "content_not_string"}
                path = self._path(name, vault_id)
                if path.exists() and path.stat().st_nlink > 1:
                    raise ValueError("path_hardlink")
                before = sha256_bytes(path.read_bytes()) if path.exists() else None
                targets.append({"path": str(path.relative_to(vault_root)), "before_hash": before, "content": content})
            input_hash = hash_canonical({"files": targets, "operation_type": operation_type, "vault_id": vault_id})
            diff_hash = hash_canonical({"files": [{"path": x["path"], "before_hash": x["before_hash"], "after_hash": sha256_bytes(x["content"].encode())} for x in targets]})
            record = self.store.new({"operation_type": operation_type, "target_vault": vault_id, "input_hash": input_hash, "diff_hash": diff_hash, "files": targets})
            return {"state": "previewed", "operation_id": record["operation_id"], "input_hash": input_hash, "diff_hash": diff_hash, "files": [{"path": x["path"], "before_hash": x["before_hash"]} for x in targets]}
        except (OSError, ValueError) as exc:
            return {"state": "blocked", "error_code": str(exc)}

    def apply(self, operation_id: str, *, confirmed: bool = False, actor_id: str = "local-user") -> dict:
        record, error = self.store.apply_preflight(operation_id, ("write", "source", "wiki", "rename", "retire", "purge"), confirmed)
        if error is not None:
            return error
        vault_id = str(record.get("target_vault", "public"))
        try:
            with VaultLock(self.root, vault_id, operation_id) as lock:
                record = self.store.load(operation_id)
                if record.get("state") != "previewed":
                    result = {"state": record.get("state"), "operation_id": operation_id}
                    if record.get("applied_files"):
                        result["applied_files"] = record["applied_files"]
                    return result
                if self.store.is_expired(record):
                    self.store.update(record, "expired", error_code="operation_expired")
                    return {"state": "expired", "operation_id": operation_id, "error_code": "operation_expired"}
                originals: dict[Path, bytes | None] = {}
                if record.get("operation_type") == "rename" and record.get("source_path"):
                    source_path = self._operation_path(str(record["source_path"]), vault_id)
                    if not source_path.exists():
                        self.store.update(record, "expired", error_code="path_unresolved")
                        return {"state": "expired", "operation_id": operation_id, "error_code": "path_unresolved"}
                    if record.get("source_before_hash") and sha256_bytes(source_path.read_bytes()) != record["source_before_hash"]:
                        self.store.update(record, "expired", error_code="hash_mismatch")
                        return {"state": "expired", "operation_id": operation_id, "error_code": "hash_mismatch"}
                    originals[source_path] = source_path.read_bytes()
                for item in record.get("files", []):
                    path = self._operation_path(item["path"], vault_id)
                    if path.exists() and path.stat().st_nlink > 1:
                        self.store.update(record, "expired", error_code="path_hardlink")
                        return {"state": "expired", "operation_id": operation_id, "error_code": "path_hardlink"}
                    current = sha256_bytes(path.read_bytes()) if path.exists() else None
                    if current != item.get("before_hash"):
                        self.store.update(record, "expired", error_code="hash_mismatch")
                        return {"state": "expired", "operation_id": operation_id, "error_code": "hash_mismatch"}
                    originals[path] = path.read_bytes() if path.exists() else None
                try:
                    intent_path = self.store.paths.commit_intent_file(operation_id)
                    intent = {"schema_version": "commit-intent/v1", "operation_id": operation_id, "operation_type": record.get("operation_type"), "vault_id": vault_id, "files": [{"path": item["path"], "before_hash": item.get("before_hash"), "after_hash": sha256_bytes(item["content"].encode("utf-8"))} for item in record.get("files", [])]}
                    intent["intent_sha256"] = hash_canonical(intent)
                    atomic_write(intent_path, canonical_json(intent) + b"\n", 0o600)
                    for index, item in enumerate(record["files"]):
                        # Re-check fencing before every replacement so a recovered lock
                        # cannot allow an old writer to continue committing.
                        lock.assert_owner()
                        if record.get("operation_type") == "purge":
                            self._operation_path(item["path"], vault_id).unlink()
                        else:
                            atomic_write(self._operation_path(item["path"], vault_id), item["content"].encode("utf-8"))
                        crash_injection_point(f"after_file_{index}")
                    if record.get("operation_type") == "rename" and record.get("source_path"):
                        self._operation_path(str(record["source_path"]), vault_id).unlink()
                    crash_injection_point("before_commit")
                except BaseException:
                    for path, content in originals.items():
                        if content is None:
                            path.unlink(missing_ok=True)
                        else:
                            atomic_write(path, content)
                    raise
                applied_files = [x["path"] for x in record["files"]]
                if self.projection_rebuilder is not None:
                    try:
                        self.projection_rebuilder({**record, "applied_files": applied_files})
                    except Exception as exc:
                        pending = self.store.update(
                            record,
                            "applied_index_pending",
                            actor_id=actor_id,
                            error_code="projection_failed",
                            applied_files=applied_files,
                            projection_error=type(exc).__name__,
                        )
                        return {
                            "state": pending["state"],
                            "operation_id": operation_id,
                            "error_code": "projection_failed",
                            "next_action": "recover_projection",
                        }
                applied = self.store.update(record, "applied", actor_id=actor_id, confirmation={"actor_type": "human", "actor_id": actor_id, "scope": "apply"}, applied_files=applied_files)
                if record.get("operation_type") == "retire":
                    marker = {"schema_version": "retire-marker/v1", "operation_id": operation_id, "vault_id": vault_id, "target": record["files"][0]["path"], "content_sha256": sha256_bytes(record["files"][0]["content"].encode("utf-8"))}
                    atomic_write(self.store.paths.audit_retire / f"{operation_id}.json", canonical_json(marker) + b"\n", 0o600)
                intent_path.unlink(missing_ok=True)
                return {"state": "applied", "operation_id": operation_id, "applied_files": applied["applied_files"]}
        except LockBusyError:
            return VaultLock.lock_busy_response(operation_id)
        except (OSError, ValueError) as exc:
            self.store.update(record, "expired", error_code="apply_failed")
            return {"state": "expired", "operation_id": operation_id, "error_code": "apply_failed", "detail": str(exc)}

    def recover(self, operation_id: str, *, projection_rebuilder: Callable[[dict], object] | None = None) -> dict:
        """Inspect an interrupted commit intent without guessing or overwriting files."""
        try:
            record = self.store.load(operation_id)
            rebuilder = projection_rebuilder or self.projection_rebuilder
            if record.get("state") == "applied_index_pending":
                if rebuilder is None:
                    return {
                        "state": "recovery_required",
                        "operation_id": operation_id,
                        "error_code": "projection_rebuilder_unavailable",
                    }
                try:
                    rebuilder(record)
                except Exception as exc:
                    return {
                        "state": "recovery_required",
                        "operation_id": operation_id,
                        "error_code": "projection_failed",
                        "detail": type(exc).__name__,
                    }
                applied = self.store.update(
                    record,
                    "applied",
                    actor_id="recovery",
                    confirmation={"actor_type": "human", "actor_id": "recovery", "scope": "apply"},
                    applied_files=record.get("applied_files", []),
                )
                self.store.paths.commit_intent_file(operation_id).unlink(missing_ok=True)
                return {
                    "state": "applied",
                    "operation_id": operation_id,
                    "recovered": True,
                    "applied_files": applied.get("applied_files", []),
                }
            intent_path = self.store.paths.commit_intent_file(operation_id)
            intent = __import__("json").loads(intent_path.read_text(encoding="utf-8"))
            expected_intent_hash = hash_canonical({k: v for k, v in intent.items() if k != "intent_sha256"})
            if (record.get("state") not in {"previewed", "expired"}
                    or intent.get("schema_version") != "commit-intent/v1"
                    or intent.get("intent_sha256") != expected_intent_hash
                    or intent.get("operation_id") != operation_id
                    or intent.get("vault_id") != record.get("target_vault", "public")):
                return {"state": "blocked", "operation_id": operation_id, "error_code": "recovery_invalid"}
            states = []
            for item in intent.get("files", []):
                path = self._operation_path(item["path"], str(record.get("target_vault", "public")))
                current = sha256_bytes(path.read_bytes()) if path.exists() else None
                states.append({"path": item["path"], "current_hash": current, "expected_hash": item.get("after_hash"), "before_hash": item.get("before_hash")})
            if all(item["current_hash"] == item["expected_hash"] for item in states):
                applied = self.store.update(record, "applied", actor_id="recovery", confirmation={"actor_type": "human", "actor_id": "recovery", "scope": "apply"}, applied_files=[item["path"] for item in states])
                intent_path.unlink(missing_ok=True)
                return {"state": "applied", "operation_id": operation_id, "recovered": True, "applied_files": applied["applied_files"]}
            return {"state": "recovery_required", "operation_id": operation_id, "error_code": "commit_intent_incomplete", "files": states}
        except (OSError, ValueError, TypeError, KeyError, __import__("json").JSONDecodeError) as exc:
            return {"state": "blocked", "operation_id": operation_id, "error_code": "recovery_invalid", "reason": str(exc)}

    def rename(self, source: str, target: str, *, vault_id: str = "public") -> dict:
        src, dst = self._path(source, vault_id), self._path(target, vault_id)
        if not src.exists():
            return {"state": "blocked", "error_code": "path_unresolved"}
        if dst.exists():
            return {"state": "blocked", "error_code": "target_exists"}
        result = self.preview({target: src.read_text(encoding="utf-8")}, operation_type="rename", vault_id=vault_id)
        if result.get("state") == "previewed":
            record = self.store.load(result["operation_id"])
            record["source_path"] = source
            record["source_before_hash"] = sha256_bytes(src.read_bytes())
            atomic_write(self.store.paths.state_operation_file(result["operation_id"]), canonical_json(record) + b"\n", 0o600)
            result.update({"source": source, "target": target})
        return result

    def retire(self, target: str, *, vault_id: str = "public") -> dict:
        path = self._path(target, vault_id)
        if not path.exists():
            return {"state": "blocked", "error_code": "path_unresolved"}
        return self.preview({target: path.read_text(encoding="utf-8")}, operation_type="retire", vault_id=vault_id)

    def purge(self, target: str, *, vault_id: str = "public") -> dict:
        """Prepare an irreversible purge only after an independently verified backup."""
        path = self._path(target, vault_id)
        if not path.exists():
            return {"state": "blocked", "error_code": "path_unresolved"}
        status = next((item for item in BackupManager(self.root).status().get("vaults", []) if item.get("vault_id") == vault_id), None)
        if not status or status.get("backup_state") != "verified":
            return {"state": "blocked", "error_code": "backup_not_verified", "vault_id": vault_id, "next_action": "verify an owner-scoped backup before purge"}
        return self.preview({target: path.read_text(encoding="utf-8")}, operation_type="purge", vault_id=vault_id)
