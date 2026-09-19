"""Wiki 内容对象的 CRUD 能力层（Repository 模式，ADR-0017 的 P2/P3 落点）。

读/列举/owner 解析/定位-错误映射复用 `content_repository.ManagedObjectRepository`
基类；退休墓碑走 `retire_ledger`（均为单份实现，不跨模块借私有 API）。本模块只承载
wiki 域特有的删除：deprecate/delete=CASCADE —— 级联把绑定该 wiki 的 question 经
`QuestionStore.refresh_status` 置 disabled、向 `content/decisions/` 写一条 CDR，并向
`audit/retire` 追加墓碑。**不物理删** wiki/archive/manifest。重复调用幂等。
"""

from __future__ import annotations

import time
from pathlib import Path

from . import contract, retire_ledger
from .content_repository import (
    ManagedObjectRepository,
    ObjectResolutionError,
    locate_managed_object,
)
from .paths import RepoPaths
from .question import QuestionStore


class WikiRepository(ManagedObjectRepository):
    """Wiki 对象的 CRUD 能力层（read/list 继承基类；删除为 wiki 域 CASCADE 实现）。"""

    object_type = "wiki"
    read_schema = "wiki-read/v1"
    list_schema = "wiki-list/v1"

    # ---- D：CASCADE + 软删（retire tombstone） ----
    def delete(self, vault_id: str, object_id: str) -> dict:
        schema = "wiki-deprecate/v1"
        try:
            owner = self._owner(vault_id)
            locate_managed_object(owner, self.object_type, object_id)
        except ObjectResolutionError as exc:
            return self._error(schema, exc)

        bound, newly_disabled = self._cascade_disable_questions(owner, object_id)
        cdr_new = self._write_cdr(owner, vault_id, object_id, bound)
        paths = RepoPaths(owner)
        retire_new = not retire_ledger.is_retired(paths, self.object_type, object_id)
        if retire_new:
            retire_ledger.append_retire(
                paths,
                self.object_type,
                vault_id=vault_id,
                object_id=object_id,
                reason="deprecate_requested",
            )
        return contract.ok(
            schema,
            changed=retire_new or bool(newly_disabled) or cdr_new,
            retired=True,
            object_ref=self._ref(vault_id, object_id),
            disabled_questions=sorted(bound),
            newly_disabled=sorted(newly_disabled),
        )

    # deprecate 与 delete 在本能力层同义（软删 + CASCADE），提供别名以贴合调用语义。
    def deprecate(self, vault_id: str, object_id: str) -> dict:
        return self.delete(vault_id, object_id)

    # ---- helpers ----
    @staticmethod
    def _cascade_disable_questions(
        owner: Path, wiki_id: str
    ) -> tuple[list[str], list[str]]:
        """把绑定该 wiki 的 question 经 refresh_status 置 disabled（幂等）。

        返回 (全部绑定该 wiki 的 question id, 本次新置为 disabled 的 id)。
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
            except (OSError, ValueError):  # 损坏题目不阻断级联
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
        """写一条 CDR 到 content/decisions/；已存在则不重写（幂等）。"""
        cdr_path = RepoPaths(owner).decisions_root / f"cdr-wiki-{wiki_id}-retire.md"
        if cdr_path.exists():
            return False
        listed = (
            "\n".join(f"- {qid}" for qid in sorted(disabled_questions)) or "- （无）"
        )
        text = (
            f"# CDR：retire wiki `{wiki_id}`\n\n"
            f"- vault_id: {vault_id}\n"
            f"- object_type: wiki\n"
            f"- object_id: {wiki_id}\n"
            f"- recorded_at: {time.strftime('%Y-%m-%dT%H:%M:%S%z')}\n\n"
            f"## 决策\n\n软删（retire）该 wiki，并级联禁用其绑定的 question。"
            f"archive/manifest 与 wiki 正文不物理删除（内容寻址与账目不可变）。\n\n"
            f"## 级联禁用的 question\n\n{listed}\n"
        )
        cdr_path.parent.mkdir(parents=True, exist_ok=True)
        cdr_path.write_text(text, encoding="utf-8")
        return True
