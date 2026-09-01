"""Vault 独占写锁：基于 filelock 库的跨平台文件锁。

来源：https://github.com/tox-dev/py-filelock（MIT License，v3.32.4）
filelock 在 Unix 上封装 fcntl.flock、Windows 上封装 msvcrt；持锁进程退出
（含崩溃）时内核自动释放锁，无 PID 复用误判，锁文件常驻不删除，不存在
"删除残留锁"的删除-创建竞态。非阻塞获取（timeout=0）失败即 lock_busy。

已知限制（R006）：不支持 flock 的文件系统（如部分 NFS）上 filelock 会
静默降级为时间戳软锁，"崩溃自动释放"保证失效、互斥依赖旧锁过期——本工具
面向本地仓库（macOS/Linux 本地文件系统），如未来支持 NFS 挂载的仓库需要
启动时检测锁类型并在 soft lock 下降级为告警或拒绝。
"""

from __future__ import annotations

import contextlib
import json
import secrets
import time
from pathlib import Path

from filelock import FileLock, Timeout

from .common import (
    atomic_write,
    canonical_json,
    hash_canonical,
    safe_id,
    safe_operation_id,
)
from .paths import RepoPaths


class LockBusyError(RuntimeError):
    """vault 写锁被其他进程占用（专用异常类型，按类型捕获而非字符串比较）。"""


class VaultLock:
    """按 Vault 独占写锁（上下文管理器）。

    锁文件在 state/locks/ 下常驻（内容仅用于诊断）；互斥由 filelock 内部
    的系统锁保证。``lock_busy`` 语义：非阻塞获取失败即抛 LockBusyError。
    """

    def __init__(self, root: Path, vault_id: str, operation_id: str) -> None:
        self._vault_id = safe_id(vault_id)
        self._operation_id = operation_id
        self._lock = FileLock(RepoPaths(root).lock_file(self._vault_id))
        self._owner_file = (
            RepoPaths(root).lock_file(self._vault_id).with_suffix(".owner")
        )
        self.lock_token = secrets.token_urlsafe(24)
        self._acquired = False

    def __enter__(self) -> VaultLock:
        try:
            self._lock.acquire(timeout=0)
        except Timeout:
            raise LockBusyError() from None
        self._acquired = True
        atomic_write(
            self._owner_file,
            json.dumps(
                {"operation_id": self._operation_id, "lock_token": self.lock_token}
            ).encode("utf-8"),
            0o600,
        )
        # 记录当前持有者，便于人工排查归属（诊断信息写入失败不影响锁本身）
        with contextlib.suppress(AttributeError, OSError):
            self._lock.write_lock_file(
                {"operation_id": self._operation_id, "acquired_at": time.time()}
            )
        return self

    def assert_owner(self) -> None:
        try:
            data = json.loads(self._owner_file.read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            raise LockBusyError("lock_owner_missing") from exc
        if (
            data.get("operation_id") != self._operation_id
            or data.get("lock_token") != self.lock_token
        ):
            raise LockBusyError("lock_fence_mismatch")

    def __exit__(self, *exc_info: object) -> None:
        if self._acquired:
            try:
                self.assert_owner()
                self._owner_file.unlink(missing_ok=True)
            except LockBusyError:
                pass
            self._lock.release()
            self._acquired = False

    @staticmethod
    def lock_busy_response(operation_id: str) -> dict:
        """构造 lock_busy 结构化错误响应（source_ingestor 与 evidence_anchor 共用）。"""
        return {
            "state": "blocked",
            "operation_id": operation_id,
            "error_code": "lock_busy",
        }

    @staticmethod
    def recover(
        root: Path, vault_id: str, operation_id: str, actor_id: str = "local-user"
    ) -> dict:
        """Recover an orphaned owner sidecar only after acquiring the kernel lock."""
        vault_id = safe_id(vault_id)
        safe_operation_id(operation_id)
        paths = RepoPaths(Path(root))
        lock = FileLock(paths.lock_file(vault_id))
        owner_file = paths.lock_file(vault_id).with_suffix(".owner")
        try:
            lock.acquire(timeout=0)
        except Timeout:
            return {
                "state": "blocked",
                "error_code": "lock_busy",
                "vault_id": vault_id,
                "operation_id": operation_id,
            }
        try:
            try:
                old = json.loads(owner_file.read_text(encoding="utf-8"))
            except (OSError, ValueError, json.JSONDecodeError):
                return {
                    "state": "blocked",
                    "error_code": "lock_owner_missing",
                    "vault_id": vault_id,
                    "operation_id": operation_id,
                }
            record = {
                "schema_version": "audit-record/v1",
                "record_type": "lock-recovery",
                "vault_id": vault_id,
                "operation_id": operation_id,
                "old_operation_id": old.get("operation_id"),
                "actor_id": actor_id,
                "recovered_at": time.time(),
            }
            record["record_sha256"] = hash_canonical(record)
            audit_dir = Path(root).resolve() / "audit" / "operations"
            audit_dir.mkdir(parents=True, exist_ok=True)
            audit_path = audit_dir / f"lock-recovery-{secrets.token_hex(12)}.json"
            atomic_write(audit_path, canonical_json(record) + b"\n", 0o600)
            owner_file.unlink(missing_ok=True)
            return {
                "state": "recovered",
                "vault_id": vault_id,
                "operation_id": operation_id,
                "record_sha256": record["record_sha256"],
            }
        finally:
            lock.release()


class VaultLockGroup:
    """Acquire multiple Vault locks in UTF-8 stable order to prevent deadlocks."""

    def __init__(
        self, root: Path, vault_ids: list[str] | tuple[str, ...], operation_id: str
    ) -> None:
        self.root = Path(root)
        self.vault_ids = tuple(sorted({safe_id(str(value)) for value in vault_ids}))
        self.operation_id = operation_id
        self.locks: list[VaultLock] = []

    def __enter__(self) -> VaultLockGroup:
        try:
            for vault_id in self.vault_ids:
                lock = VaultLock(self.root, vault_id, self.operation_id)
                lock.__enter__()
                self.locks.append(lock)
            return self
        except BaseException:
            for lock in reversed(self.locks):
                lock.__exit__(None, None, None)
            self.locks.clear()
            raise

    def assert_owner(self) -> None:
        for lock in self.locks:
            lock.assert_owner()

    def __exit__(self, *exc_info: object) -> None:
        for lock in reversed(self.locks):
            lock.__exit__(*exc_info)
        self.locks.clear()
