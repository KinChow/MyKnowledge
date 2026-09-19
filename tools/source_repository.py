"""Source 内容对象的 CRUD 能力层（Repository 模式，ADR-0017 的 P2/P3 落点）。

设计取向（cosmicpython《Repository》"practicality beats purity"）：最简 add/get，
不引入无消费者的抽象。读侧复用 ``content_repository.locate_managed_object``（单份
定位实现），create 直接委派 ``ingest.SourceIngestor``（不重写采集），返回一律走
``tools.contract`` 统一信封（TD §14：单 status 轴 + 已登记 error_code + 效果进 payload）。

删除采用"引用完整性 RESTRICT + 软删 tombstone"的成熟组合（对齐 SQL
``ON DELETE RESTRICT`` 与逻辑删/墓碑做法，避免物理删导致证据链与账目不可逆丢失）：
被任一活跃 wiki 引用则阻断；否则向 append-only ``audit/retire`` 追加一条墓碑记录，
**不物理删** source/archive/manifest（内容寻址与账目不可变，见 paths.py 注释）。
"""

from __future__ import annotations

import json
import os
from pathlib import Path

from . import contract
from .common import canonical_json
from .content_repository import ObjectResolutionError, locate_managed_object
from .front_matter import FrontMatter
from .ingest.source_ingestor import SourceIngestor
from .paths import RepoPaths
from .vault_registry import VaultRegistry

_OBJECT_TYPE = "source"


class _VaultUnresolved(Exception):
    """vault 解析失败：携带 (status, error_code) 供各方法组装信封。"""

    def __init__(self, status: str, error_code: str) -> None:
        super().__init__(error_code)
        self.status = status
        self.error_code = error_code


def _resolve_owner_root(root: Path, vault_id: str) -> Path:
    """把 vault_id 解析为 owner 检出根（复用 VaultRegistry，只读）。

    ``vault_unavailable`` 归为可重试的 unavailable；其余解析失败（vault 不存在/
    路径非法）归为 blocked 的 invalid_object_ref（引用本身不合法，不可重试）。
    """
    try:
        return VaultRegistry(root).resolve_vault_path(vault_id)
    except ValueError as exc:
        code = str(exc)
        if code == "vault_unavailable":
            raise _VaultUnresolved("unavailable", "vault_unavailable") from exc
        raise _VaultUnresolved("blocked", "invalid_object_ref") from exc


def _retired_object_ids(paths: RepoPaths, object_type: str) -> set[str]:
    """读取 append-only retire 账本，返回已墓碑化的 object_id 集合。"""
    ledger = paths.audit_retire / f"{object_type}.jsonl"
    ids: set[str] = set()
    if not ledger.exists():
        return ids
    for raw in ledger.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line:
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            continue
        object_id = record.get("object_id")
        if isinstance(object_id, str):
            ids.add(object_id)
    return ids


def _append_retire(paths: RepoPaths, object_type: str, record: dict) -> None:
    """向 retire 账本追加一条墓碑记录（append-only + fsync，永不覆盖）。"""
    ledger = paths.audit_retire / f"{object_type}.jsonl"
    ledger.parent.mkdir(parents=True, exist_ok=True)
    with ledger.open("ab") as handle:
        handle.write(canonical_json(record) + b"\n")
        handle.flush()
        os.fsync(handle.fileno())


class SourceRepository:
    """Source 对象的 CRUD 能力层（owner Vault 上下文内，实例仅持有仓库根）。"""

    def __init__(self, root: Path) -> None:
        self.root = Path(root)

    # ---- R：读取与列举（复用 content_repository 单份定位） ----
    def read(self, vault_id: str, object_id: str) -> dict:
        schema = "source-read/v1"
        try:
            owner = _resolve_owner_root(self.root, vault_id)
        except _VaultUnresolved as exc:
            return contract.result(schema, exc.status, error_code=exc.error_code)
        try:
            path = locate_managed_object(owner, _OBJECT_TYPE, object_id)
        except ObjectResolutionError as exc:
            return contract.blocked(schema, exc.code)
        try:
            metadata, body = FrontMatter.parse(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, ValueError, TypeError) as exc:
            return contract.blocked(schema, "source_unreadable", reason=str(exc))
        return contract.ok(
            schema,
            object_ref=self._object_ref(vault_id, object_id),
            metadata=metadata,
            body=body,
        )

    def list(self, vault_id: str) -> dict:  # noqa: A003 - Repository 契约方法名
        schema = "source-list/v1"
        try:
            owner = _resolve_owner_root(self.root, vault_id)
        except _VaultUnresolved as exc:
            return contract.result(schema, exc.status, error_code=exc.error_code)
        items = [
            {"object_ref": self._object_ref(vault_id, path.stem)}
            for path in RepoPaths(owner).iter_source_files()
        ]
        items.sort(key=lambda item: item["object_ref"]["object_id"])
        return contract.ok(schema, items=items)

    # ---- C：委派 SourceIngestor（不重写采集） ----
    def create(self, request: dict) -> dict:
        schema = "source-create/v1"
        result = SourceIngestor(self.root).ingest(request)
        if result.get("state") == "applied":
            return contract.ok(
                schema,
                changed=True,
                source_id=result["source_id"],
                snapshot_sha256=result["snapshot_sha256"],
                applied_files=result.get("applied_files", []),
            )
        return contract.blocked(
            schema, "source_ingest_failed", errors=self._ingest_errors(result)
        )

    # ---- U：幂等更新，且必须保留已锚定的 evidence_items ----
    def update(self, request: dict) -> dict:
        """重导入 source：同 body（按 snapshot_sha256）为 noop，evidence_items 必保留。

        真实缺陷回归点：``SourceIngestor`` 重写 source front matter 时不落
        ``evidence_items``，直接重导入会清空已锚定证据。此处先取旧证据，重导入后
        再写回，保证锚定跨重导入存活（每条 evidence item 自带 snapshot_sha256，
        指向其被锚定时的快照，语义不受本次 body 变化影响）。
        """
        schema = "source-update/v1"
        source_id = request.get("source_id")
        if not isinstance(source_id, str) or not source_id:
            return contract.blocked(schema, "invalid_object_ref")
        try:
            old_path = locate_managed_object(self.root, _OBJECT_TYPE, source_id)
        except ObjectResolutionError as exc:
            return contract.blocked(schema, exc.code)
        try:
            old_meta, _ = FrontMatter.parse(old_path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, ValueError, TypeError) as exc:
            return contract.blocked(schema, "source_unreadable", reason=str(exc))
        old_evidence = old_meta.get("evidence_items") or []
        old_snapshot = old_meta.get("snapshot_sha256")

        result = SourceIngestor(self.root).ingest(request)
        if result.get("state") != "applied":
            return contract.blocked(
                schema, "source_ingest_failed", errors=self._ingest_errors(result)
            )
        new_snapshot = result["snapshot_sha256"]
        self._restore_evidence(Path(result["source_path"]), old_evidence)
        return contract.ok(
            schema,
            changed=new_snapshot != old_snapshot,
            source_id=source_id,
            snapshot_sha256=new_snapshot,
        )

    # ---- D：RESTRICT + 软删（retire tombstone） ----
    def delete(self, vault_id: str, object_id: str) -> dict:
        schema = "source-retire/v1"
        try:
            owner = _resolve_owner_root(self.root, vault_id)
        except _VaultUnresolved as exc:
            return contract.result(schema, exc.status, error_code=exc.error_code)
        try:
            locate_managed_object(owner, _OBJECT_TYPE, object_id)
        except ObjectResolutionError as exc:
            return contract.blocked(schema, exc.code)
        referrers = self._active_referrers(owner, object_id)
        if referrers:
            return contract.blocked(
                schema, "object_referenced", referenced_by=referrers
            )
        paths = RepoPaths(owner)
        if object_id in _retired_object_ids(paths, _OBJECT_TYPE):
            return contract.ok(
                schema,
                changed=False,
                retired=True,
                object_ref=self._object_ref(vault_id, object_id),
            )
        _append_retire(
            paths,
            _OBJECT_TYPE,
            {
                "schema_version": "retire-record/v1",
                "vault_id": vault_id,
                "object_type": _OBJECT_TYPE,
                "object_id": object_id,
                "reason": "retire_requested",
            },
        )
        return contract.ok(
            schema,
            changed=True,
            retired=True,
            object_ref=self._object_ref(vault_id, object_id),
        )

    # ---- helpers ----
    @staticmethod
    def _object_ref(vault_id: str, object_id: str) -> dict:
        return {
            "vault_id": vault_id,
            "object_type": _OBJECT_TYPE,
            "object_id": object_id,
        }

    @staticmethod
    def _ingest_errors(result: dict) -> list[dict]:
        errors = result.get("errors")
        if errors:
            return errors
        code = result.get("error_code")
        return [{"code": code}] if code else []

    @staticmethod
    def _restore_evidence(source_path: Path, evidence_items: list) -> None:
        """重导入后把旧 evidence_items 写回 front matter（无旧证据则 no-op）。"""
        if not evidence_items:
            return
        metadata, body = FrontMatter.parse(source_path.read_text(encoding="utf-8"))
        if metadata.get("evidence_items"):
            return
        metadata["evidence_items"] = evidence_items
        source_path.write_text(FrontMatter.render(metadata, body), encoding="utf-8")

    @staticmethod
    def _active_referrers(owner: Path, source_id: str) -> list[str]:
        """返回通过 sources/evidence.targets 引用该 source 的活跃 wiki id。

        活跃 = 未被 retire 且 front-matter ``status != disabled``。不可读的 wiki
        跳过（不阻断删除，也不误报引用）。
        """
        paths = RepoPaths(owner)
        wiki_root = paths.wiki_root
        if not wiki_root.is_dir():
            return []
        retired = _retired_object_ids(paths, "wiki")
        referrers: set[str] = set()
        for wiki_path in sorted(wiki_root.rglob("*.md")):
            if not wiki_path.is_file() or wiki_path.is_symlink():
                continue
            wiki_id = wiki_path.stem
            if wiki_id in retired:
                continue
            try:
                metadata, _ = FrontMatter.parse(wiki_path.read_text(encoding="utf-8"))
            except (OSError, UnicodeError, ValueError, TypeError):
                continue
            if str(metadata.get("status")) == "disabled":
                continue
            refs = set(metadata.get("sources") or [])
            for claim in metadata.get("evidence") or []:
                if not isinstance(claim, dict):
                    continue
                for target in claim.get("targets") or []:
                    if isinstance(target, dict) and target.get("source_id"):
                        refs.add(target["source_id"])
            if source_id in refs:
                referrers.add(wiki_id)
        return sorted(referrers)
