"""仓库布局值对象：集中定义 MyKnowledge 目录结构（对照设计规范 §4 目录树）。

来源：借鉴 cookiecutter.config.Paths（集中路径容器，https://github.com/cookiecutter/cookiecutter）
与 pathlib 组合模式。布局变更只改本类，业务代码只消费命名属性/方法。

目录树（§4，F008 practice 预留不读取）：
    sources/<domain>/  wiki/<domain>/  archive/{text,raw,manifest.jsonl}
    audit/{operations,validation}/  release/public-confirmations/
    config/json-schema/  state/{operations,locks,local-sources}/  queries/
"""

from __future__ import annotations

from pathlib import Path

from .common import strip_sha256_prefix


class RepoPaths:
    """不可变路径容器：构造时给定仓库根，暴露命名目录/文件方法。"""

    def __init__(self, root: Path) -> None:
        self.root = Path(root)

    # ---- 内容目录（§4） ----
    @property
    def sources_root(self) -> Path:
        return self.root / "sources"

    def sources_dir(self, domain: str) -> Path:
        return self.sources_root / domain

    def source_file(self, domain: str, source_id: str) -> Path:
        return self.sources_dir(domain) / f"{source_id}.md"

    @property
    def wiki_root(self) -> Path:
        return self.root / "wiki"

    def wiki_dir(self, domain: str) -> Path:
        return self.wiki_root / domain

    def wiki_file(self, domain: str, wiki_id: str) -> Path:
        return self.wiki_dir(domain) / f"{wiki_id}.md"

    # ---- archive（§5.6：不可变快照，text 进仓库、raw 走 LFS） ----
    @property
    def archive_text(self) -> Path:
        return self.root / "archive" / "text"

    @property
    def archive_raw(self) -> Path:
        return self.root / "archive" / "raw"

    @property
    def manifest(self) -> Path:
        return self.root / "archive" / "manifest.jsonl"

    def snapshot_file(self, snapshot_sha256: str) -> Path:
        return self.archive_text / f"{strip_sha256_prefix(snapshot_sha256)}.md"

    # ---- audit（durable records，§6.8 路径固定） ----
    @property
    def audit_operations(self) -> Path:
        return self.root / "audit" / "operations"

    def operation_file(self, operation_id: str) -> Path:
        return self.audit_operations / f"{operation_id}.json"

    def audit_validation(self, object_type: str, object_id: str) -> Path:
        return self.root / "audit" / "validation" / object_type / object_id

    # ---- release（public-safe 确认事件，§6.8） ----
    @property
    def release_confirmations(self) -> Path:
        return self.root / "release" / "public-confirmations"

    # ---- state（本机临时运行态，git 忽略，不是事实源） ----
    @property
    def state_operations(self) -> Path:
        return self.root / "state" / "operations"

    def state_operation_file(self, operation_id: str) -> Path:
        return self.state_operations / f"{operation_id}.json"

    @property
    def state_locks(self) -> Path:
        return self.root / "state" / "locks"

    def lock_file(self, vault_id: str) -> Path:
        return self.state_locks / f"{vault_id}.lock"

    def state_local_sources(self, vault_id: str) -> Path:
        return self.root / "state" / "local-sources" / vault_id

    # ---- queries（§4：public 投影 / local 检索） ----
    @property
    def queries_public(self) -> Path:
        return self.root / "queries" / "public"

    @property
    def queries_local(self) -> Path:
        return self.root / "queries" / "local"

    # ---- practice（F008 预留；当前版本不读取） ----
    @property
    def practice_questions(self) -> Path:
        return self.root / "practice" / "questions"

    # ---- config ----
    @property
    def config_dir(self) -> Path:
        return self.root / "config"

    # ---- state 扩展（§4：llm-validation / reading 运行缓存） ----
    @property
    def state_llm_validation(self) -> Path:
        return self.root / "state" / "llm-validation"

    @property
    def state_reading(self) -> Path:
        return self.root / "state" / "reading"
