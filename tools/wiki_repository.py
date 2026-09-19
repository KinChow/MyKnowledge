"""Wiki 内容对象的 CRUD 能力层（Repository 模式，ADR-0017 的 P2/P3 落点）。

读侧复用 ``content_repository.locate_managed_object``（单份定位实现）。删除采用
"级联删 CASCADE"的成熟做法（对齐 SQL ``ON DELETE CASCADE`` 与逻辑删/墓碑）：
deprecate/delete 会级联把绑定该 wiki 的 question 经 ``QuestionStore.refresh_status``
置 disabled、向 ``content/decisions/`` 写一条 CDR（内容决策记录），并向 append-only
``audit/retire`` 追加墓碑记录。**不物理删** wiki/archive/manifest。重复调用幂等。

返回一律走 ``tools.contract`` 统一信封（TD §14：单 status 轴 + 已登记 error_code +
效果进 payload）。retire 账本读写与 vault 解析复用 ``source_repository`` 的单份实现。
"""

from __future__ import annotations

import time
from pathlib import Path

from . import contract
from .content_repository import ObjectResolutionError, locate_managed_object
from .front_matter import FrontMatter
from .paths import RepoPaths
from .question import QuestionStore
from .source_repository import (
    _append_retire,
    _resolve_owner_root,
    _retired_object_ids,
    _VaultUnresolved,
)

_OBJECT_TYPE = "wiki"


class WikiRepository:
    """Wiki 对象的 CRUD 能力层（owner Vault 上下文内，实例仅持有仓库根）。"""

    def __init__(self, root: Path) -> None:
        self.root = Path(root)

    # ---- R：读取与列举（复用 content_repository 单份定位） ----
    def read(self, vault_id: str, object_id: str) -> dict:
        schema = "wiki-read/v1"
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
        schema = "wiki-list/v1"
        try:
            owner = _resolve_owner_root(self.root, vault_id)
        except _VaultUnresolved as exc:
            return contract.result(schema, exc.status, error_code=exc.error_code)
        wiki_root = RepoPaths(owner).wiki_root
        items = []
        if wiki_root.is_dir():
            for path in sorted(wiki_root.rglob("*.md")):
                if not path.is_file() or path.is_symlink():
                    continue
                items.append({"object_ref": self._object_ref(vault_id, path.stem)})
        items.sort(key=lambda item: item["object_ref"]["object_id"])
        return contract.ok(schema, items=items)

    # ---- D：CASCADE + 软删（retire tombstone） ----
    def delete(self, vault_id: str, object_id: str) -> dict:
        schema = "wiki-deprecate/v1"
        try:
            owner = _resolve_owner_root(self.root, vault_id)
        except _VaultUnresolved as exc:
            return contract.result(schema, exc.status, error_code=exc.error_code)
        try:
            locate_managed_object(owner, _OBJECT_TYPE, object_id)
        except ObjectResolutionError as exc:
            return contract.blocked(schema, exc.code)

        bound, newly_disabled = self._cascade_disable_questions(owner, object_id)
        cdr_new = self._write_cdr(owner, vault_id, object_id, bound)
        paths = RepoPaths(owner)
        retire_new = object_id not in _retired_object_ids(paths, _OBJECT_TYPE)
        if retire_new:
            _append_retire(
                paths,
                _OBJECT_TYPE,
                {
                    "schema_version": "retire-record/v1",
                    "vault_id": vault_id,
                    "object_type": _OBJECT_TYPE,
                    "object_id": object_id,
                    "reason": "deprecate_requested",
                },
            )
        return contract.ok(
            schema,
            changed=retire_new or bool(newly_disabled) or cdr_new,
            retired=True,
            object_ref=self._object_ref(vault_id, object_id),
            disabled_questions=sorted(bound),
            newly_disabled=sorted(newly_disabled),
        )

    # deprecate 与 delete 在本能力层同义（软删 + CASCADE），提供别名以贴合调用语义。
    def deprecate(self, vault_id: str, object_id: str) -> dict:
        return self.delete(vault_id, object_id)

    # ---- helpers ----
    @staticmethod
    def _object_ref(vault_id: str, object_id: str) -> dict:
        return {
            "vault_id": vault_id,
            "object_type": _OBJECT_TYPE,
            "object_id": object_id,
        }

    @staticmethod
    def _cascade_disable_questions(
        owner: Path, wiki_id: str
    ) -> tuple[list[str], list[str]]:
        """把绑定该 wiki 的 question 经 refresh_status 置 disabled（幂等）。

        返回 (全部绑定该 wiki 的 question id, 本次新置为 disabled 的 id)。
        refresh_status 仅在 status != disabled 时改写，故用调用前状态判定"新禁用"。
        """
        store = QuestionStore(owner)
        directory = store.paths.practice_questions
        bound: list[str] = []
        newly_disabled: list[str] = []
        if not directory.is_dir():
            return bound, newly_disabled
        for path in sorted(directory.glob("*.json")):
            question_id = path.stem
            try:
                question = store.load(question_id)
            except (OSError, ValueError) as exc:  # noqa: BLE001 - 损坏题目不阻断级联
                _ = exc
                continue
            if str((question.get("wiki_claim") or {}).get("wiki_id")) != wiki_id:
                continue
            was_enabled = question.get("status") != "disabled"
            store.refresh_status(question_id, {"valid": False})
            bound.append(question_id)
            if was_enabled:
                newly_disabled.append(question_id)
        return bound, newly_disabled

    @staticmethod
    def _write_cdr(
        owner: Path, vault_id: str, wiki_id: str, disabled_questions: list[str]
    ) -> bool:
        """写一条 CDR（内容决策记录）到 content/decisions/；已存在则不重写（幂等）。"""
        cdr_path = (
            RepoPaths(owner).decisions_root / f"cdr-{_OBJECT_TYPE}-{wiki_id}-retire.md"
        )
        if cdr_path.exists():
            return False
        listed = (
            "\n".join(f"- {qid}" for qid in sorted(disabled_questions)) or "- （无）"
        )
        text = (
            f"# CDR：retire wiki `{wiki_id}`\n\n"
            f"- vault_id: {vault_id}\n"
            f"- object_type: {_OBJECT_TYPE}\n"
            f"- object_id: {wiki_id}\n"
            f"- recorded_at: {time.strftime('%Y-%m-%dT%H:%M:%S%z')}\n\n"
            f"## 决策\n\n软删（retire）该 wiki，并级联禁用其绑定的 question。"
            f"archive/manifest 与 wiki 正文不物理删除（内容寻址与账目不可变）。\n\n"
            f"## 级联禁用的 question\n\n{listed}\n"
        )
        cdr_path.parent.mkdir(parents=True, exist_ok=True)
        cdr_path.write_text(text, encoding="utf-8")
        return True
