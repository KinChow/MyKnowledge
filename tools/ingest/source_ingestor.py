"""Source 导入与归档服务：URL 抓取、local-file/personal-note 导入、不可变 snapshot。

对应 F001 验收标准：所有写操作先 Preview 再由人工确认 Apply，抓取防 SSRF
（见 fetcher.py），local-file 防竞态，snapshot 与 manifest 追加不可覆盖。
经统一入口调用：``python -m tools.cli source ...``

设计：依赖倒置（服务依赖 Protocol 抽象）+ 开闭原则（source 类型经策略注册表扩展）。
"""

from __future__ import annotations

import argparse
import contextlib
import json
import os
import time
import uuid
import zlib
from pathlib import Path
from typing import NamedTuple, Protocol

from ..common import (
    atomic_write,
    canonical_json,
    crash_injection_point,
    hash_canonical,
    read_stable,
    safe_id,
    sha256_bytes,
    sha256_text,
    strip_sha256_prefix,
)
from ..front_matter import FrontMatter
from ..operation_store import OperationStore
from ..paths import RepoPaths
from ..vault_lock import LockBusyError, VaultLock
from .extractor import TextExtractor
from .fetcher import URLFetcher
from .source_validator import SourceValidator


def _block_error_code(exc: Exception) -> str:
    """将捕获的异常映射为结构化错误码（RuntimeError 消息本身即错误码）。"""
    if isinstance(exc, RuntimeError):
        return str(exc)
    if isinstance(exc, zlib.error):
        return "fetch_blocked:decompression_error"
    if isinstance(exc, LookupError):
        return "fetch_blocked:unknown_charset"
    if isinstance(exc, FileNotFoundError):
        return "path_unresolved"
    return type(exc).__name__


class Fetcher(Protocol):
    """URL 抓取抽象：实现见 URLFetcher（依赖倒置）。"""

    def fetch(self, url: str) -> tuple[bytes, str, str]: ...


class Extractor(Protocol):
    """正文提取抽象：实现见 TextExtractor。"""

    def extract(self, data: bytes, media_type: str) -> tuple[str, str]: ...


class Validator(Protocol):
    """请求校验抽象：实现见 SourceValidator。"""

    def validate_request(self, request: dict) -> list[dict]: ...


class OperationRepository(Protocol):
    """Operation 仓库抽象：实现见 OperationStore。"""

    def new(self, payload: dict) -> dict: ...

    def load(self, operation_id: str) -> dict: ...

    def update(self, record: dict, state: str, **fields: object) -> dict: ...


class AcquireResult(NamedTuple):
    """按 source_type 获取正文的结果（供 preview 写入 operation）。"""

    body: str
    extractor: str
    media_type: str
    original_hash: str | None
    original_stat: os.stat_result | None
    resolved_url: str | None = None


class SourceAcquirer(Protocol):
    """按 source_type 获取正文的策略抽象（开闭原则：新类型注册新策略）。"""

    source_type: str

    def acquire(self, request: dict, extractor: Extractor) -> AcquireResult: ...


class LocalFileAcquirer:
    """local-file 策略：稳定读取本地文件并提取正文，记录 hash 与 stat。"""

    source_type = "local-file"

    def acquire(self, request: dict, extractor: Extractor) -> AcquireResult:
        """稳定读取本地文件并提取正文，返回正文/提取器与 hash/stat。"""
        data, stat = read_stable(Path(request["input_path"]))
        media_type = request.get("media_type") or "application/octet-stream"
        body, extractor_name = extractor.extract(data, media_type)
        return AcquireResult(
            body=body,
            extractor=extractor_name,
            media_type=media_type,
            original_hash=sha256_bytes(data),
            original_stat=stat,
        )


class PersonalNoteAcquirer:
    """personal-note 策略：正文即用户输入，无外部原件。"""

    source_type = "personal-note"

    def acquire(self, request: dict, extractor: Extractor) -> AcquireResult:  # noqa: ARG002 - SourceAcquirer Protocol 统一签名
        """正文即用户输入，无外部原件（不经 extractor），直接构造 AcquireResult。"""
        body = request.get("body", "")
        return AcquireResult(
            body=body,
            extractor="personal-note/1",
            media_type="text/markdown",
            original_hash=None,
            original_stat=None,
        )


class FetchAcquirer:
    """fetch 策略：抓取 URL 并提取正文（非 local-file/personal-note 的 source_type 默认走此）。"""

    source_type = "fetch"

    def __init__(self, fetcher: Fetcher) -> None:
        self.fetcher = fetcher

    def acquire(self, request: dict, extractor: Extractor) -> AcquireResult:
        """抓取 URL 并提取正文，返回正文/提取器与解析后 URL。"""
        fetched_body, resolved_url, content_type = self.fetcher.fetch(request["url"])
        body, extractor_name = extractor.extract(fetched_body, content_type)
        return AcquireResult(
            body=body,
            extractor=extractor_name,
            media_type=content_type,
            original_hash=None,
            original_stat=None,
            resolved_url=resolved_url,
        )


class SourceIngestor:
    """Source 导入与归档服务：两阶段（preview → apply）写入 source/snapshot/manifest。

    依赖经构造函数注入（依赖倒置），source 类型经策略注册表分派（开闭原则）。
    """

    def __init__(self, root: Path) -> None:
        self.root = root
        self.paths = RepoPaths(root)
        self.store: OperationRepository = OperationStore(root)
        self.validator: Validator = SourceValidator()
        fetcher: Fetcher = URLFetcher()
        self.fetcher = fetcher
        self.extractor: Extractor = TextExtractor()
        self._acquirers: dict[str, SourceAcquirer] = {
            LocalFileAcquirer.source_type: LocalFileAcquirer(),
            PersonalNoteAcquirer.source_type: PersonalNoteAcquirer(),
            FetchAcquirer.source_type: FetchAcquirer(fetcher),
        }

    def preview(self, request: dict) -> dict:
        """校验并预览导入请求，生成 previewed 操作；底层异常统一转为结构化 blocked。"""
        try:
            errors = self.validator.validate_request(request)
            if errors:
                return {"state": "blocked", "errors": errors}
            source_id = request.get("source_id") or safe_id(
                "source-" + uuid.uuid4().hex[:12]
            )
            source_type = request["source_type"]
            acquirer = (
                self._acquirers.get(source_type)
                or self._acquirers[FetchAcquirer.source_type]
            )
            acquired = acquirer.acquire(request, self.extractor)
            body = acquired.body
            if not isinstance(body, str):
                return {
                    "state": "blocked",
                    "errors": [{"code": "schema_invalid", "path": "body"}],
                }
            if not body.strip():
                return {"state": "blocked", "errors": [{"code": "source_empty"}]}
            snapshot_hash = sha256_text(body)
            target = self.paths.source_file(request["domain"], source_id)
            target_hash = sha256_bytes(target.read_bytes()) if target.exists() else None
            payload = {
                "operation_type": "source_ingest",
                "target_vault": "public",
                "source_id": source_id,
                "domain": request["domain"],
                "source_type": source_type,
                "input_path": request.get("input_path"),
                "input_realpath": (
                    str(Path(request["input_path"]).resolve())
                    if request.get("input_path")
                    else None
                ),
                "url": request.get("url"),
                "input_hash": acquired.original_hash,
                "target_hash": target_hash,
                "snapshot_sha256": snapshot_hash,
                "extractor": acquired.extractor,
                "media_type": acquired.media_type,
                "network_required": source_type not in {"local-file", "personal-note"},
                "body": acquired.body,
                "stat": (
                    {
                        "dev": acquired.original_stat.st_dev,
                        "ino": acquired.original_stat.st_ino,
                        "size": acquired.original_stat.st_size,
                        "mtime_ns": acquired.original_stat.st_mtime_ns,
                    }
                    if acquired.original_stat is not None
                    else None
                ),
            }
            if acquired.resolved_url is not None:
                payload["resolved_url"] = acquired.resolved_url
            operation = self.store.new(payload)
            return {
                "operation_id": operation["operation_id"],
                "state": "previewed",
                "source_id": source_id,
                "snapshot_sha256": snapshot_hash,
                "input_hash": acquired.original_hash,
                "extractor": acquired.extractor,
                "media_type": acquired.media_type,
                "network_required": operation["network_required"],
            }
        except (OSError, RuntimeError, LookupError, zlib.error) as exc:
            return {"state": "blocked", "errors": [{"code": _block_error_code(exc)}]}

    def apply(
        self,
        operation_id: str,
        confirmed: bool = False,
        actor_id: str = "local-user",
    ) -> dict:
        """确认并执行导入操作：preflight → 取锁 → 分阶段执行，失败一律结构化返回。"""
        _record, preflight_error = self.store.apply_preflight(
            operation_id, "source_ingest", confirmed
        )
        if preflight_error is not None:
            return preflight_error
        try:
            with VaultLock(self.root, "public", operation_id):
                return self._apply_locked(operation_id, actor_id)
        except LockBusyError:
            return VaultLock.lock_busy_response(operation_id)

    def _expire(self, record: dict, error_code: str, operation_id: str) -> dict:
        """把操作标记为 expired 并返回结构化错误（所有前置校验失败的唯一出口）。"""
        self.store.update(record, "expired", error_code=error_code)
        return {
            "state": "expired",
            "error_code": error_code,
            "operation_id": operation_id,
        }

    def _apply_locked(self, operation_id: str, actor_id: str) -> dict:
        """锁内主流程：复查状态/TTL → 复验输入与目标 → 落盘 → 提交。"""
        record = self.store.load(operation_id)
        if record.get("state") != "previewed":
            return {"state": record.get("state"), "operation_id": operation_id}
        if self.store.is_expired(record):
            return self._expire(record, "operation_expired", operation_id)

        body = record["body"]
        if record["input_path"]:
            input_error = self._revalidate_input(record)
            if input_error is not None:
                return self._expire(record, input_error, operation_id)

        snapshot_hash = sha256_text(body)
        source_id = record["source_id"]
        source_path = self.paths.source_file(record["domain"], source_id)
        if not self._target_writable(record, source_path, snapshot_hash):
            return self._expire(record, "hash_mismatch", operation_id)

        archive_path = self.paths.snapshot_file(snapshot_hash)
        metadata = self._source_metadata(record, snapshot_hash)
        try:
            self._write_artifacts(record, body, metadata, source_path, archive_path)
        except OSError:
            self._rollback_uncommitted(record, source_path, source_id)
            return {
                "state": "expired",
                "operation_id": operation_id,
                "error_code": "apply_failed",
            }
        crash_injection_point("before_commit")
        self.store.update(
            record,
            "applied",
            confirmation={
                "actor_type": "human",
                "actor_id": actor_id,
                "scope": "apply",
                "confirmed_at": time.time(),
            },
            applied_files=[
                str(source_path.relative_to(self.root)),
                str(archive_path.relative_to(self.root)),
            ],
        )
        return {
            "state": "applied",
            "operation_id": operation_id,
            "source_id": source_id,
            "snapshot_sha256": snapshot_hash,
            "source_path": str(source_path),
        }

    def _revalidate_input(self, record: dict) -> str | None:
        """local-file 导入在 apply 时复验来源：内容/stat/realpath 任一漂移即失效。

        返回错误码或 None（通过）。
        """
        if record.get("stat") is None:
            return "record_invalid"
        try:
            data, stat = read_stable(Path(record["input_path"]))
        except OSError:
            return "path_unresolved"
        except RuntimeError:
            return "hash_mismatch"
        stat_fields = record.get("stat") or {}
        stat_keys = ("dev", "ino", "size", "mtime_ns")
        if (
            sha256_bytes(data) != record["input_hash"]
            or not all(k in stat_fields for k in stat_keys)
            or (stat.st_dev, stat.st_ino, stat.st_size, stat.st_mtime_ns)
            != tuple(stat_fields[k] for k in stat_keys)
        ):
            return "hash_mismatch"
        if (
            record.get("input_realpath")
            and str(Path(record["input_path"]).resolve()) != record["input_realpath"]
        ):
            # symlink/hard-link 改指使来源路径不再解析到 preview 时的同一文件
            # （AC-F001-008 根域逃逸防护），按路径失效处理
            return "path_unresolved"
        return None

    def _target_writable(
        self, record: dict, source_path: Path, snapshot_hash: str
    ) -> bool:
        """目标 source 是否仍与 preview 时一致，或已被本操作写过（可幂等补写）。

        崩溃恢复：apply 在任意中间点崩溃后，source 可能已由本操作写入（front
        matter snapshot_sha256 一致）——放行并幂等补写，使新建与覆盖导入都可
        重放恢复（WAL 重放语义）。
        """
        current = (
            sha256_bytes(source_path.read_bytes()) if source_path.exists() else None
        )
        if current == record.get("target_hash"):
            return True
        try:
            existing_meta, _ = FrontMatter.parse(
                source_path.read_text(encoding="utf-8")
            )
        except (OSError, ValueError, UnicodeError):
            return False
        return existing_meta.get("snapshot_sha256") == snapshot_hash

    def _source_metadata(self, record: dict, snapshot_hash: str) -> dict:
        """source front matter（§5.4）：不含 local 段，由 sidecar 写入时补。"""
        personal = record["source_type"] == "personal-note"
        return {
            "schema_version": "source/v1",
            "id": record["source_id"],
            "domain": record["domain"],
            "vault_id": "public",
            "source_type": record["source_type"],
            "origin": "personal" if personal else "external",
            "retrieval": {
                "acquisition": (
                    "personal-note"
                    if personal
                    else ("local-file" if record["input_path"] else "fetch")
                ),
                **({"url": record["url"]} if record.get("url") else {}),
                **(
                    {"resolved_url": record["resolved_url"]}
                    if record.get("resolved_url")
                    else {}
                ),
            },
            "snapshot_sha256": snapshot_hash,
            "extractor": record["extractor"],
            "media_type": record["media_type"],
            "read_status": "retrieved",
            "confidentiality": "public",
            "archive_policy": "text-only",
        }

    def _write_artifacts(
        self,
        record: dict,
        body: str,
        metadata: dict,
        source_path: Path,
        archive_path: Path,
    ) -> None:
        """按 archive → sidecar → source → manifest 顺序落盘（含崩溃注入点）。

        顺序是恢复语义的一部分：archive 内容寻址先落，source 最后带 manifest
        入账；任一步 OSError 由调用方回滚未提交状态。
        """
        if not archive_path.exists():
            atomic_write(archive_path, body.encode("utf-8"))
        crash_injection_point("after_archive")
        if record["input_path"]:
            metadata["local"] = self._write_sidecar(record)
        atomic_write(source_path, FrontMatter.render(metadata, body).encode("utf-8"))
        crash_injection_point("after_source")
        self._append_manifest(
            self._manifest_entry(
                record, body, metadata["snapshot_sha256"], archive_path
            )
        )
        crash_injection_point("after_manifest")

    def _write_sidecar(self, record: dict) -> dict:
        """local-file 的运行态 sidecar（0600），返回 front matter 的 local 段。"""
        source_id = record["source_id"]
        sidecar = self.paths.state_local_sources("public") / f"{source_id}.json"
        sidecar.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        sidecar.parent.chmod(0o700)
        realpath = str(Path(record["input_path"]).resolve())
        atomic_write(
            sidecar,
            canonical_json(
                {
                    "schema_version": "local-file-sidecar/v1",
                    "vault_id": "public",
                    "source_id": source_id,
                    "path": realpath,
                    "realpath_sha256": sha256_text(realpath),
                    "file_sha256": record["input_hash"],
                    "device": record["stat"]["dev"],
                    "inode": record["stat"]["ino"],
                    "byte_size": record["stat"]["size"],
                    "media_type": record["media_type"],
                    "observed_at": time.time(),
                }
            )
            + b"\n",
            0o600,
        )
        return {
            "file_sha256": record["input_hash"],
            "path_ref": f"local-sidecar:public/{source_id}",
        }

    def _manifest_entry(
        self, record: dict, body: str, snapshot_hash: str, archive_path: Path
    ) -> dict:
        """archive manifest 条目（§5.6）：record_id 由不变量派生，用于幂等去重。"""
        entry = {
            "record_id": strip_sha256_prefix(
                hash_canonical(
                    {
                        "vault_id": "public",
                        "source_id": record["source_id"],
                        "snapshot_sha256": snapshot_hash,
                        "extractor": record["extractor"],
                    }
                )
            ),
            "vault_id": "public",
            "owner_object_ref": {"type": "source", "id": record["source_id"]},
            "snapshot_sha256": snapshot_hash,
            "archive_path": str(archive_path.relative_to(self.root)),
            "physical_blob_key": snapshot_hash,
            "availability": "available",
            "availability_reason": "none",
            "confidentiality": "public",
            "media_type": record["media_type"],
            "extractor": record["extractor"],
            "extractor_options_sha256": hash_canonical({}),
            "normalization_version": "canonical-text-v1",
            "canonical_byte_length": len(body.encode("utf-8")),
            "physical_blob_length": archive_path.stat().st_size,
            "compression": "identity",
        }
        entry["record_sha256"] = hash_canonical(entry)
        return entry

    def _append_manifest(self, entry: dict) -> None:
        """幂等追加 manifest：record_id 已存在则跳过；写入后 fsync 文件与目录。

        manifest 是跨 vault 全局单文件，互斥依赖当前 per-vault 锁（R009）：
        target_vault 目前硬编码 "public" 无实际竞争；引入多 vault 写入时
        manifest 追加需全局锁或按 vault 分片。
        """
        manifest = self.paths.manifest
        manifest.parent.mkdir(parents=True, exist_ok=True)
        existing_ids = set()
        if manifest.exists():
            with manifest.open(encoding="utf-8", errors="replace") as handle:
                for raw_line in handle:
                    line = raw_line.strip()
                    if not line:
                        continue
                    try:
                        existing_ids.add(json.loads(line)["record_id"])
                    except (json.JSONDecodeError, KeyError):
                        continue
        if entry["record_id"] in existing_ids:
            return
        with manifest.open("ab") as handle:
            handle.write(canonical_json(entry) + b"\n")
            handle.flush()
            os.fsync(handle.fileno())
        directory_fd = os.open(manifest.parent, os.O_RDONLY)
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)

    def _rollback_uncommitted(
        self, record: dict, source_path: Path, source_id: str
    ) -> None:
        """提交点（store.update applied）之前失败时的清理。

        仅当本次新建（preview 时目标不存在）才删除已写入的 source；覆盖场景新
        内容保留在 source 文件、待重放提交（atomic_write 已替换旧文件，旧内容
        不可恢复——重放 recovery 使 manifest/state 与新内容一致，无人重放时为
        静默不一致态，属已知权衡）。sidecar 是运行缓存一并清理，archive 内容
        寻址保留无害。
        """
        if record.get("target_hash") is None:
            with contextlib.suppress(OSError):
                source_path.unlink(missing_ok=True)
        with contextlib.suppress(OSError):
            self.paths.state_local_sources("public").joinpath(
                f"{source_id}.json"
            ).unlink(missing_ok=True)
        self.store.update(record, "expired", error_code="apply_failed")


def main(argv: list[str] | None = None) -> int:
    """source_ingestor CLI：预览/应用 Source 导入（local-file/personal-note/url）。"""
    parser = argparse.ArgumentParser(
        description="Preview/apply MyKnowledge Source ingestion"
    )
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--from-file", dest="input_path")
    parser.add_argument("--personal-note")
    parser.add_argument("--url")
    parser.add_argument("--source-id")
    parser.add_argument("--domain", default="tools")
    parser.add_argument("--media-type", default="text/plain")
    parser.add_argument("--apply")
    parser.add_argument(
        "--confirm",
        action="store_true",
        help="confirm the operation as the invoking human",
    )
    parser.add_argument("--actor-id", default="local-user")
    args = parser.parse_args(argv)
    ingestor = SourceIngestor(args.root)
    if args.apply:
        print(
            json.dumps(
                ingestor.apply(
                    args.apply,
                    confirmed=args.confirm,
                    actor_id=args.actor_id,
                ),
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0
    if args.input_path:
        request = {
            "source_type": "local-file",
            "domain": args.domain,
            "input_path": args.input_path,
            "source_id": args.source_id,
            "media_type": args.media_type,
        }
    elif args.personal_note is not None:
        request = {
            "source_type": "personal-note",
            "domain": args.domain,
            "body": args.personal_note,
            "source_id": args.source_id,
            "origin": "personal",
        }
    elif args.url:
        request = {
            "source_type": "doc",
            "domain": args.domain,
            "url": args.url,
            "source_id": args.source_id,
        }
    else:
        parser.error(
            "one of --from-file, --personal-note, --url or --apply is required"
        )
    result = ingestor.preview(request)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result.get("state") != "blocked" else 2
