"""通用 Preview/Apply 写入服务（F004）。

通用 writer 只负责文件事务与 operation 状态，不理解 Source/Wiki 领域字段。
领域校验由调用方在 preview 前完成；所有路径都必须位于当前仓库根目录。
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Mapping

from .common import atomic_write, canonical_json, crash_injection_point, hash_canonical, sha256_bytes
from .operation_store import OperationStore
from .vault_lock import LockBusyError, VaultLock


class WriteOperation:
    def __init__(self, root: Path) -> None:
        self.root = Path(root).resolve()
        self.store = OperationStore(self.root)

    def _path(self, value: str) -> Path:
        path = (self.root / value).resolve()
        try:
            path.relative_to(self.root)
        except ValueError as exc:
            raise ValueError("path_outside_repo") from exc
        if path == self.root:
            raise ValueError("invalid_target")
        return path

    def preview(self, files: Mapping[str, str], *, operation_type: str = "write", vault_id: str = "public") -> dict:
        if not files:
            return {"state": "blocked", "error_code": "empty_write"}
        try:
            targets = []
            for name, content in sorted(files.items()):
                if not isinstance(content, str):
                    return {"state": "blocked", "error_code": "content_not_string"}
                path = self._path(name)
                before = sha256_bytes(path.read_bytes()) if path.exists() else None
                targets.append({"path": str(path.relative_to(self.root)), "before_hash": before, "content": content})
            input_hash = hash_canonical({"files": targets, "operation_type": operation_type, "vault_id": vault_id})
            diff_hash = hash_canonical({"files": [{"path": x["path"], "before_hash": x["before_hash"], "after_hash": sha256_bytes(x["content"].encode())} for x in targets]})
            record = self.store.new({"operation_type": operation_type, "target_vault": vault_id, "input_hash": input_hash, "diff_hash": diff_hash, "files": targets})
            return {"state": "previewed", "operation_id": record["operation_id"], "input_hash": input_hash, "diff_hash": diff_hash, "files": [{"path": x["path"], "before_hash": x["before_hash"]} for x in targets]}
        except (OSError, ValueError) as exc:
            return {"state": "blocked", "error_code": str(exc)}

    def apply(self, operation_id: str, *, confirmed: bool = False, actor_id: str = "local-user") -> dict:
        record, error = self.store.apply_preflight(operation_id, ("write", "source", "wiki", "rename", "retire"), confirmed)
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
                    source_path = self._path(str(record["source_path"]))
                    if not source_path.exists():
                        self.store.update(record, "expired", error_code="path_unresolved")
                        return {"state": "expired", "operation_id": operation_id, "error_code": "path_unresolved"}
                    originals[source_path] = source_path.read_bytes()
                for item in record.get("files", []):
                    path = self._path(item["path"])
                    current = sha256_bytes(path.read_bytes()) if path.exists() else None
                    if current != item.get("before_hash"):
                        self.store.update(record, "expired", error_code="hash_mismatch")
                        return {"state": "expired", "operation_id": operation_id, "error_code": "hash_mismatch"}
                    originals[path] = path.read_bytes() if path.exists() else None
                try:
                    intent_path = self.store.paths.commit_intent_file(operation_id)
                    intent = {"schema_version": "commit-intent/v1", "operation_id": operation_id, "operation_type": record.get("operation_type"), "vault_id": vault_id, "files": [{"path": item["path"], "before_hash": item.get("before_hash"), "after_hash": sha256_bytes(item["content"].encode("utf-8"))} for item in record.get("files", [])]}
                    atomic_write(intent_path, canonical_json(intent) + b"\n", 0o600)
                    for index, item in enumerate(record["files"]):
                        # Re-check fencing before every replacement so a recovered lock
                        # cannot allow an old writer to continue committing.
                        lock.assert_owner()
                        atomic_write(self._path(item["path"]), item["content"].encode("utf-8"))
                        crash_injection_point(f"after_file_{index}")
                    if record.get("operation_type") == "rename" and record.get("source_path"):
                        self._path(str(record["source_path"])).unlink()
                    crash_injection_point("before_commit")
                except BaseException:
                    for path, content in originals.items():
                        if content is None:
                            path.unlink(missing_ok=True)
                        else:
                            atomic_write(path, content)
                    raise
                applied = self.store.update(record, "applied", actor_id=actor_id, confirmation={"actor_type": "human", "actor_id": actor_id, "scope": "apply"}, applied_files=[x["path"] for x in record["files"]])
                if record.get("operation_type") == "retire":
                    marker = {"schema_version": "retire-marker/v1", "operation_id": operation_id, "vault_id": vault_id, "target": record["files"][0]["path"], "content_sha256": sha256_bytes(record["files"][0]["content"].encode("utf-8"))}
                    atomic_write(self.store.paths.audit_retire / f"{operation_id}.json", canonical_json(marker) + b"\n", 0o600)
                intent_path.unlink(missing_ok=True)
                return {"state": "applied", "operation_id": operation_id, "applied_files": applied["applied_files"]}
        except LockBusyError:
            return VaultLock.lock_busy_response(operation_id)
        except OSError:
            self.store.update(record, "expired", error_code="apply_failed")
            return {"state": "expired", "operation_id": operation_id, "error_code": "apply_failed"}

    def recover(self, operation_id: str) -> dict:
        """Inspect an interrupted commit intent without guessing or overwriting files."""
        try:
            record = self.store.load(operation_id)
            intent_path = self.store.paths.commit_intent_file(operation_id)
            intent = __import__("json").loads(intent_path.read_text(encoding="utf-8"))
            if record.get("state") != "previewed" or intent.get("schema_version") != "commit-intent/v1":
                return {"state": "blocked", "operation_id": operation_id, "error_code": "recovery_invalid"}
            states = []
            for item in intent.get("files", []):
                path = self._path(item["path"])
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
        src, dst = self._path(source), self._path(target)
        if not src.exists():
            return {"state": "blocked", "error_code": "path_unresolved"}
        if dst.exists():
            return {"state": "blocked", "error_code": "target_exists"}
        result = self.preview({target: src.read_text(encoding="utf-8")}, operation_type="rename", vault_id=vault_id)
        if result.get("state") == "previewed":
            record = self.store.load(result["operation_id"])
            record["source_path"] = source
            atomic_write(self.store.paths.state_operation_file(result["operation_id"]), canonical_json(record) + b"\n", 0o600)
            result.update({"source": source, "target": target})
        return result

    def retire(self, target: str, *, vault_id: str = "public") -> dict:
        path = self._path(target)
        if not path.exists():
            return {"state": "blocked", "error_code": "path_unresolved"}
        return self.preview({target: path.read_text(encoding="utf-8")}, operation_type="retire", vault_id=vault_id)
