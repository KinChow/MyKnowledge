"""通用 Preview/Apply 写入服务（F004）。

通用 writer 只负责文件事务与 operation 状态，不理解 Source/Wiki 领域字段。
领域校验由调用方在 preview 前完成；所有路径都必须位于当前仓库根目录。

结构（设计质量重构 2026-08-28）：
- 协作者经构造注入（store / vault_root_resolver / backup_state_for /
  projection_rebuilder），默认实现是唯一具体绑定点——测试不再 mock.patch；
- ``apply`` 只保留通用事务骨架（前置→提交→收尾），rename/retire/purge 的
  类型差异收敛到 ``_TYPE_POLICIES`` 的 per-type hook 表（OCP：新增操作
  类型只加表项，不改事务骨架）；
- ``apply`` 与 ``recover`` 共享 ``_finalize``（状态推进 + projection
  重建 + retire marker + intent 清理）。
"""

from __future__ import annotations

import json
from collections.abc import Callable, Mapping
from dataclasses import dataclass, field
from pathlib import Path

from .backup import BackupManager
from .common import (
    atomic_write,
    canonical_json,
    hash_canonical,
    injection_point,
    sha256_bytes,
)
from .operation_store import OperationStore, validate_apply_confirmation
from .vault_lock import LockBusyError, VaultLock
from .vault_registry import VaultRegistry

OPERATION_TYPES = ("write", "source", "wiki", "rename", "retire", "purge")


def public_projection_rebuilder(root: Path) -> Callable[[dict], object]:
    """AC-F004-009 真实 rebuild hook：public vault apply 后重建 projection + 默认 FTS5 索引。

    索引重建失败与 projection 失败同一语义（applied_index_pending + 显式
    recover 重跑）——索引是派生运行缓存，不静默降级。
    """

    def rebuild(_record: dict) -> object:
        from .public_projection import PublicProjectionGenerator

        result = PublicProjectionGenerator(root).generate()
        from .indexing import rebuild_default_public_index

        rebuild_default_public_index(root)
        return result

    return rebuild


@dataclass(frozen=True)
class _TypePolicy:
    """operation_type 的差异 hook 表：只声明与通用 write 不同的行为。"""

    # 写入目标的方式（默认原子写正文；purge 为删除）
    commit_file: Callable[[Path, str], None] = field(
        default=lambda path, content: atomic_write(path, content.encode("utf-8"))
    )
    # 提交后、状态推进前的领域产物（默认无；retire 写 marker）
    post_commit: Callable[[WriteOperation, dict, str], None] | None = None


def _write_retire_marker(
    service: WriteOperation, record: dict, operation_id: str
) -> None:
    vault_id = str(record.get("target_vault", "public"))
    marker = {
        "schema_version": "retire-marker/v1",
        "operation_id": operation_id,
        "vault_id": vault_id,
        "target": record["files"][0]["path"],
        "content_sha256": sha256_bytes(record["files"][0]["content"].encode("utf-8")),
    }
    atomic_write(
        service.store.paths.audit_retire / f"{operation_id}.json",
        canonical_json(marker) + b"\n",
        0o600,
    )


_TYPE_POLICIES: dict[str, _TypePolicy] = {
    "purge": _TypePolicy(commit_file=lambda path, _content: path.unlink()),
    "retire": _TypePolicy(post_commit=_write_retire_marker),
}


class WriteOperation:
    def __init__(
        self,
        root: Path,
        *,
        store: OperationStore | None = None,
        vault_root_resolver: Callable[[str], Path] | None = None,
        backup_state_for: Callable[[str], str | None] | None = None,
        projection_rebuilder: Callable[[dict], object] | None = None,
    ) -> None:
        self.root = Path(root).resolve()
        # 协作者注入点：None 时绑定默认具体实现（唯一耦合处，可被测试替换）
        self.store = store or OperationStore(self.root)
        self._vault_root_resolver = vault_root_resolver or self._default_vault_root
        self._backup_state_for = backup_state_for or self._default_backup_state
        # Optional downstream projection/index hook. Canonical files commit first;
        # a failed hook leaves the operation recoverable as applied_index_pending.
        self.projection_rebuilder = projection_rebuilder

    # ---- 协作者默认实现（DIP 的具体绑定点） ----

    def _default_vault_root(self, vault_id: str) -> Path:
        return (
            self.root
            if vault_id == "public"
            else VaultRegistry(self.root).resolve_vault_path(vault_id)
        )

    def _default_backup_state(self, vault_id: str) -> str | None:
        status = next(
            (
                item
                for item in BackupManager(self.root).status().get("vaults", [])
                if item.get("vault_id") == vault_id
            ),
            None,
        )
        return status.get("backup_state") if status else None

    # ---- 路径解析 ----

    def _vault_root(self, vault_id: str) -> Path:
        return self._vault_root_resolver(vault_id)

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
        return (
            self._path(value) if vault_id == "public" else self._path(value, vault_id)
        )

    # ---- Preview 族 ----

    def preview(
        self,
        files: Mapping[str, str],
        *,
        operation_type: str = "write",
        vault_id: str = "public",
    ) -> dict:
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
                targets.append(
                    {
                        "path": str(path.relative_to(vault_root)),
                        "before_hash": before,
                        "content": content,
                    }
                )
            input_hash = hash_canonical(
                {
                    "files": targets,
                    "operation_type": operation_type,
                    "vault_id": vault_id,
                }
            )
            diff_hash = hash_canonical(
                {
                    "files": [
                        {
                            "path": x["path"],
                            "before_hash": x["before_hash"],
                            "after_hash": sha256_bytes(x["content"].encode()),
                        }
                        for x in targets
                    ]
                }
            )
            record = self.store.new(
                {
                    "operation_type": operation_type,
                    "target_vault": vault_id,
                    "input_hash": input_hash,
                    "diff_hash": diff_hash,
                    "files": targets,
                }
            )
            return {
                "state": "previewed",
                "operation_id": record["operation_id"],
                "input_hash": input_hash,
                "diff_hash": diff_hash,
                "files": [
                    {"path": x["path"], "before_hash": x["before_hash"]}
                    for x in targets
                ],
            }
        except (OSError, ValueError) as exc:
            return {"state": "blocked", "error_code": str(exc)}

    def rename(self, source: str, target: str, *, vault_id: str = "public") -> dict:
        src, dst = self._path(source, vault_id), self._path(target, vault_id)
        if not src.exists():
            return {"state": "blocked", "error_code": "path_unresolved"}
        if dst.exists():
            return {"state": "blocked", "error_code": "target_exists"}
        result = self.preview(
            {target: src.read_text(encoding="utf-8")},
            operation_type="rename",
            vault_id=vault_id,
        )
        if result.get("state") == "previewed":
            record = self.store.load(result["operation_id"])
            record["source_path"] = source
            record["source_before_hash"] = sha256_bytes(src.read_bytes())
            atomic_write(
                self.store.paths.state_operation_file(result["operation_id"]),
                canonical_json(record) + b"\n",
                0o600,
            )
            result.update({"source": source, "target": target})
        return result

    def retire(self, target: str, *, vault_id: str = "public") -> dict:
        path = self._path(target, vault_id)
        if not path.exists():
            return {"state": "blocked", "error_code": "path_unresolved"}
        return self.preview(
            {target: path.read_text(encoding="utf-8")},
            operation_type="retire",
            vault_id=vault_id,
        )

    def purge(self, target: str, *, vault_id: str = "public") -> dict:
        """Prepare an irreversible purge only after an independently verified backup."""
        path = self._path(target, vault_id)
        if not path.exists():
            return {"state": "blocked", "error_code": "path_unresolved"}
        if self._backup_state_for(vault_id) != "verified":
            return {
                "state": "blocked",
                "error_code": "backup_not_verified",
                "vault_id": vault_id,
                "next_action": "verify an owner-scoped backup before purge",
            }
        return self.preview(
            {target: path.read_text(encoding="utf-8")},
            operation_type="purge",
            vault_id=vault_id,
        )

    # ---- Apply：通用事务骨架 ----

    def apply(
        self,
        operation_id: str,
        *,
        confirmed: bool = False,
        actor_id: str = "local-user",
        confirmation: dict | None = None,
    ) -> dict:
        record, error = self.store.apply_preflight(
            operation_id, OPERATION_TYPES, confirmed
        )
        if error is not None:
            return error
        vault_id = str(record.get("target_vault", "public"))
        # AC-F004-006：提供确认事件时必须严格校验（human actor + hash 绑定），
        # 失败 fail-closed 且不改变任何目标文件或 operation 状态。
        confirmed_event = None
        if confirmation is not None:
            code = validate_apply_confirmation(record, confirmation)
            if code is not None:
                return {
                    "state": "blocked",
                    "operation_id": operation_id,
                    "error_code": code,
                    "next_action": "re-preview and have a human confirm the current hashes",
                }
            confirmed_event = confirmation
        try:
            with VaultLock(self.root, vault_id, operation_id) as lock:
                record = self.store.load(operation_id)
                if record.get("state") != "previewed":
                    result = {
                        "state": record.get("state"),
                        "operation_id": operation_id,
                    }
                    if record.get("applied_files"):
                        result["applied_files"] = record["applied_files"]
                    return result
                if self.store.is_expired(record):
                    self.store.update(record, "expired", error_code="operation_expired")
                    return {
                        "state": "expired",
                        "operation_id": operation_id,
                        "error_code": "operation_expired",
                    }
                originals, pre_error = self._collect_originals(
                    record, vault_id, operation_id
                )
                if pre_error is not None:
                    return pre_error
                intent_path = self._commit_files(
                    record, vault_id, operation_id, lock, originals
                )
                applied_files = [x["path"] for x in record["files"]]
                confirmation_record = confirmed_event or {
                    "actor_type": "human",
                    "actor_id": actor_id,
                    "scope": "apply",
                }
                return self._finalize(
                    record,
                    operation_id,
                    actor_id,
                    confirmation_record,
                    applied_files,
                    recovered=False,
                    intent_path=intent_path,
                )
        except LockBusyError:
            return VaultLock.lock_busy_response(operation_id)
        except (OSError, ValueError) as exc:
            self.store.update(record, "expired", error_code="apply_failed")
            return {
                "state": "expired",
                "operation_id": operation_id,
                "error_code": "apply_failed",
                "detail": str(exc),
            }

    def _collect_originals(
        self, record: dict, vault_id: str, operation_id: str
    ) -> tuple[dict[Path, bytes | None], dict | None]:
        """Apply 前置复查：rename 源 + 每文件 hardlink/hash 校验，收集回滚原状。"""
        originals: dict[Path, bytes | None] = {}
        if record.get("operation_type") == "rename" and record.get("source_path"):
            source_path = self._operation_path(str(record["source_path"]), vault_id)
            if not source_path.exists():
                self.store.update(record, "expired", error_code="path_unresolved")
                return originals, {
                    "state": "expired",
                    "operation_id": operation_id,
                    "error_code": "path_unresolved",
                }
            if (
                record.get("source_before_hash")
                and sha256_bytes(source_path.read_bytes())
                != record["source_before_hash"]
            ):
                self.store.update(record, "expired", error_code="hash_mismatch")
                return originals, {
                    "state": "expired",
                    "operation_id": operation_id,
                    "error_code": "hash_mismatch",
                }
            originals[source_path] = source_path.read_bytes()
        for item in record.get("files", []):
            path = self._operation_path(item["path"], vault_id)
            if path.exists() and path.stat().st_nlink > 1:
                self.store.update(record, "expired", error_code="path_hardlink")
                return originals, {
                    "state": "expired",
                    "operation_id": operation_id,
                    "error_code": "path_hardlink",
                }
            current = sha256_bytes(path.read_bytes()) if path.exists() else None
            if current != item.get("before_hash"):
                self.store.update(record, "expired", error_code="hash_mismatch")
                return originals, {
                    "state": "expired",
                    "operation_id": operation_id,
                    "error_code": "hash_mismatch",
                }
            originals[path] = path.read_bytes() if path.exists() else None
        return originals, None

    def _commit_files(
        self,
        record: dict,
        vault_id: str,
        operation_id: str,
        lock: VaultLock,
        originals: dict[Path, bytes | None],
    ) -> Path:
        """写 commit-intent 并原子提交全部目标文件；失败回滚到 originals 后重抛。"""
        policy = _TYPE_POLICIES.get(str(record.get("operation_type")), _TypePolicy())
        intent_path = self.store.paths.commit_intent_file(operation_id)
        intent = {
            "schema_version": "commit-intent/v1",
            "operation_id": operation_id,
            "operation_type": record.get("operation_type"),
            "vault_id": vault_id,
            "files": [
                {
                    "path": item["path"],
                    "before_hash": item.get("before_hash"),
                    "after_hash": sha256_bytes(item["content"].encode("utf-8")),
                }
                for item in record.get("files", [])
            ],
        }
        intent["intent_sha256"] = hash_canonical(intent)
        atomic_write(intent_path, canonical_json(intent) + b"\n", 0o600)
        try:
            for index, item in enumerate(record["files"]):
                # Re-check fencing before every replacement so a recovered lock
                # cannot allow an old writer to continue committing.
                lock.assert_owner()
                policy.commit_file(
                    self._operation_path(item["path"], vault_id), item["content"]
                )
                injection_point(f"after_file_{index}")
            if record.get("operation_type") == "rename" and record.get("source_path"):
                self._operation_path(str(record["source_path"]), vault_id).unlink()
            injection_point("before_commit")
        except BaseException:
            for path, content in originals.items():
                if content is None:
                    path.unlink(missing_ok=True)
                else:
                    atomic_write(path, content)
            raise
        return intent_path

    def _finalize(
        self,
        record: dict,
        operation_id: str,
        actor_id: str,
        confirmation_record: dict,
        applied_files: list[str],
        *,
        recovered: bool,
        intent_path: Path | None = None,
    ) -> dict:
        """共享收尾：projection 重建 -> applied 状态 -> per-type 产物 -> intent 清理。"""
        vault_id = str(record.get("target_vault", "public"))
        rebuilder = self.projection_rebuilder
        if rebuilder is None and vault_id == "public":
            # AC-F004-009：public apply 默认重建 public projection；
            # 失败进入 applied_index_pending，由显式 recover 重跑。
            rebuilder = public_projection_rebuilder(self.root)
        if rebuilder is not None:
            try:
                rebuilder({**record, "applied_files": applied_files})
            # noqa 理由：rebuilder 是注入的外部钩子（默认实现会拉起 projection +
            # 索引重建），异常面不可枚举；canonical 已提交，必须把任何失败都收敛为
            # applied_index_pending 让 recover 重跑，而不是让异常穿透丢掉已提交状态。
            except Exception as exc:  # noqa: BLE001
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
        applied = self.store.update(
            record,
            "applied",
            actor_id=actor_id,
            confirmation=confirmation_record,
            applied_files=applied_files,
        )
        policy = _TYPE_POLICIES.get(str(record.get("operation_type")))
        if policy is not None and policy.post_commit is not None:
            policy.post_commit(self, record, operation_id)
        intent = (
            intent_path
            if intent_path is not None
            else self.store.paths.commit_intent_file(operation_id)
        )
        # F-1：canonical 已提交且状态已 applied，intent 清理失败不得把
        # operation 翻回 expired（外层 except 会误报 apply_failed）。
        # 显式暴露 warning，不静默吞异常。
        cleanup_warning = None
        try:
            intent.unlink(missing_ok=True)
        except OSError:
            cleanup_warning = "intent_cleanup_failed"
        result = {
            "state": "applied",
            "operation_id": operation_id,
            "applied_files": applied["applied_files"],
        }
        if cleanup_warning is not None:
            result["warnings"] = [cleanup_warning]
        if recovered:
            result["recovered"] = True
        return result

    def _cleanup_intent_after_applied(
        self, applied: dict, operation_id: str, *, recovered: bool
    ) -> dict:
        """F-1：applied 之后的 intent 清理失败不翻转状态，只在结果暴露 warning。"""
        result = {
            "state": "applied",
            "operation_id": operation_id,
            "applied_files": applied.get("applied_files", []),
        }
        if recovered:
            result["recovered"] = True
        try:
            self.store.paths.commit_intent_file(operation_id).unlink(missing_ok=True)
        except OSError:
            result["warnings"] = ["intent_cleanup_failed"]
        return result

    # ---- Recover ----

    def recover(
        self,
        operation_id: str,
        *,
        projection_rebuilder: Callable[[dict], object] | None = None,
    ) -> dict:
        """Inspect an interrupted commit intent without guessing or overwriting files."""
        try:
            record = self.store.load(operation_id)
            vault_id = str(record.get("target_vault", "public"))
            rebuilder = projection_rebuilder or self.projection_rebuilder
            if rebuilder is None and vault_id == "public":
                rebuilder = public_projection_rebuilder(self.root)
            if record.get("state") == "applied_index_pending":
                if rebuilder is None:
                    return {
                        "state": "recovery_required",
                        "operation_id": operation_id,
                        "error_code": "projection_rebuilder_unavailable",
                    }
                try:
                    rebuilder(record)
                except Exception as exc:  # noqa: BLE001 - 同上：注入钩子的异常面不可枚举
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
                    confirmation={
                        "actor_type": "human",
                        "actor_id": "recovery",
                        "scope": "apply",
                    },
                    applied_files=record.get("applied_files", []),
                )
                return self._cleanup_intent_after_applied(
                    applied, operation_id, recovered=True
                )
            intent_path = self.store.paths.commit_intent_file(operation_id)
            intent = json.loads(intent_path.read_text(encoding="utf-8"))
            expected_intent_hash = hash_canonical(
                {k: v for k, v in intent.items() if k != "intent_sha256"}
            )
            if (
                record.get("state") not in {"previewed", "expired"}
                or intent.get("schema_version") != "commit-intent/v1"
                or intent.get("intent_sha256") != expected_intent_hash
                or intent.get("operation_id") != operation_id
                or intent.get("vault_id") != record.get("target_vault", "public")
            ):
                return {
                    "state": "blocked",
                    "operation_id": operation_id,
                    "error_code": "recovery_invalid",
                }
            states = []
            for item in intent.get("files", []):
                path = self._operation_path(
                    item["path"], str(record.get("target_vault", "public"))
                )
                current = sha256_bytes(path.read_bytes()) if path.exists() else None
                states.append(
                    {
                        "path": item["path"],
                        "current_hash": current,
                        "expected_hash": item.get("after_hash"),
                        "before_hash": item.get("before_hash"),
                    }
                )
            if all(item["current_hash"] == item["expected_hash"] for item in states):
                applied = self.store.update(
                    record,
                    "applied",
                    actor_id="recovery",
                    confirmation={
                        "actor_type": "human",
                        "actor_id": "recovery",
                        "scope": "apply",
                    },
                    applied_files=[item["path"] for item in states],
                )
                return self._cleanup_intent_after_applied(
                    applied, operation_id, recovered=True
                )
            return {
                "state": "recovery_required",
                "operation_id": operation_id,
                "error_code": "commit_intent_incomplete",
                "files": states,
            }
        except (OSError, ValueError, TypeError, KeyError, json.JSONDecodeError) as exc:
            return {
                "state": "blocked",
                "operation_id": operation_id,
                "error_code": "recovery_invalid",
                "reason": str(exc),
            }
