"""Source 内容对象的 CRUD 能力层（Repository 模式，ADR-0017 的 P2/P3 落点）。

读/列举/owner 解析/定位-错误映射复用 `content_repository.ManagedObjectRepository`
基类（单份实现）；退休墓碑走 `retire_ledger`（单份实现）。本模块只承载 source 域
特有的 C/U/D：create 委派 `SourceIngestor`（不重写采集）、update 幂等且保留
`evidence_items`、delete=RESTRICT（被活跃 wiki 引用则阻断，否则软删）。
返回一律走 `tools.contract` 统一信封（TD §14）。
"""

from __future__ import annotations

from pathlib import Path

from . import contract, retire_ledger
from .content_repository import (
    ManagedObjectRepository,
    ObjectResolutionError,
    locate_managed_object,
)
from .front_matter import FrontMatter
from .ingest.source_ingestor import SourceIngestor
from .paths import RepoPaths


class SourceRepository(ManagedObjectRepository):
    """Source 对象的 CRUD 能力层（read/list 继承基类；C/U/D 为 source 域实现）。"""

    object_type = "source"
    read_schema = "source-read/v1"
    list_schema = "source-list/v1"

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
        再写回（每条 evidence item 自带指向锚定时快照的 snapshot_sha256，语义不受
        本次 body 变化影响）。
        """
        schema = "source-update/v1"
        source_id = request.get("source_id")
        if not isinstance(source_id, str) or not source_id:
            return contract.blocked(schema, "invalid_object_ref")
        try:
            old_path = locate_managed_object(self.root, self.object_type, source_id)
        except ObjectResolutionError as exc:
            return contract.blocked(schema, exc.code)
        try:
            old_meta, _ = FrontMatter.parse(old_path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, ValueError, TypeError) as exc:
            return contract.blocked(schema, "object_unreadable", reason=str(exc))
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
            owner = self._owner(vault_id)
            locate_managed_object(owner, self.object_type, object_id)
        except ObjectResolutionError as exc:
            return self._error(schema, exc)
        referrers = self._active_referrers(owner, object_id)
        if referrers:
            return contract.blocked(
                schema, "object_referenced", referenced_by=referrers
            )
        paths = RepoPaths(owner)
        if retire_ledger.is_retired(paths, self.object_type, object_id):
            return contract.ok(
                schema,
                changed=False,
                retired=True,
                object_ref=self._ref(vault_id, object_id),
            )
        retire_ledger.append_retire(
            paths,
            self.object_type,
            vault_id=vault_id,
            object_id=object_id,
            reason="retire_requested",
        )
        return contract.ok(
            schema,
            changed=True,
            retired=True,
            object_ref=self._ref(vault_id, object_id),
        )

    # ---- helpers ----
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
        retired = retire_ledger.retired_object_ids(paths, "wiki")
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
