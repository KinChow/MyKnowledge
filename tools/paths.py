"""仓库布局值对象：集中定义 MyKnowledge 目录结构（对照设计规范 §4 目录树）。

来源：借鉴 cookiecutter.config.Paths（集中路径容器，https://github.com/cookiecutter/cookiecutter）
与 pathlib 组合模式。布局变更只改本类，业务代码只消费命名属性/方法。

目录树（§4.6 目标布局，F008 practice 预留不读取）：
    content/{sources,wiki}/<domain>/   ledger/{archive,audit,release}/
    var/{queries,state,reports}/       config/json-schema/
本轮已完成批次 1（var/）；content/ 与 ledger/ 仍为历史平铺路径，按 §4.6 分批迁移。
"""

from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path

from .common import is_contained_regular_file, safe_relative_path, strip_sha256_prefix

# §4.6 路径域迁移映射：历史前缀 -> 目标前缀。这是读取侧历史路径容忍与布局漂移
# 检测共用的唯一一张表——两处各写一份必然漂移。
LAYOUT_MIGRATIONS: dict[str, str] = {
    "queries/": "var/queries/",
    "state/": "var/state/",
    "reports/": "var/reports/",
    "sources/": "content/sources/",
    "wiki/": "content/wiki/",
    "practice/": "content/practice/",
    "archive/": "ledger/archive/",
    "audit/": "ledger/audit/",
    "release/": "ledger/release/",
}


class RepoPaths:
    """不可变路径容器：构造时给定仓库根，暴露命名目录/文件方法。"""

    def __init__(self, root: Path) -> None:
        self.root = Path(root)

    # ---- 数据域根（§4.4：content 人写 / ledger 机器追加 / var 可重建） ----
    @property
    def var_root(self) -> Path:
        return self.root / "var"

    def migrated_candidates(self, historical: str) -> list[Path]:
        """§4.6 表里某个历史相对路径的全部可能物理位置（历史 + 目标）。

        用途有两个：判断"canonical 内容是不是搬到别处去了"（布局漂移检测），
        以及解析 append-only 记录里写下的历史路径（LAY-004 读取侧容忍）。
        """
        key = historical.rstrip("/") + "/"
        target = LAYOUT_MIGRATIONS.get(key, key)
        return [self.root / key.rstrip("/"), self.root / target.rstrip("/")]

    def record_path_candidates(self, relative: str) -> list[Path]:
        """append-only 记录里某个相对路径的候选物理位置（LAY-004 读取侧容忍）。

        记录不可改写，所以 §4.6 迁移之后旧账目里仍写着 `archive/text/<hash>.md`。
        顺序固定为「当前布局 → 记录原样」：当前布局优先，避免历史目录残留时把读取
        悄悄引到旧文件上——那会让"账目指向的实物"与"实际发布用的实物"分叉。

        入参先过 `safe_relative_path`（C004）：账目是外部可改写的输入，`..` 与绝对
        路径必须在拼接之前就拒掉，非法时抛 `ValueError("unsafe_record_path")`。
        """
        text = safe_relative_path(relative)
        candidates = [self.root / text]
        for historical, target in LAYOUT_MIGRATIONS.items():
            if text.startswith(historical):
                candidates.insert(0, self.root / (target + text[len(historical) :]))
                break
            if text.startswith(target):
                candidates.append(self.root / (historical + text[len(target) :]))
                break
        # 去重但保序（当前布局与记录原样可能相同）
        return list(dict.fromkeys(candidates))

    def resolve_record_path(self, relative: str) -> Path | None:
        """返回第一个真实存在且在仓库内的候选；都不存在时返回 None。

        存在性判定走 `is_contained_regular_file`：`Path.is_file()` 会跟随符号链接，
        仓库内一个指向外部的链接就能让账目"自证通过"而实物在仓库外（C004）。
        """
        for candidate in self.record_path_candidates(relative):
            if is_contained_regular_file(self.root, candidate):
                return candidate
        return None

    # ---- 内容目录（§4） ----
    @property
    def content_root(self) -> Path:
        return self.root / "content"

    @property
    def sources_root(self) -> Path:
        return self.content_root / "sources"

    def sources_dir(self, domain: str) -> Path:
        return self.sources_root / domain

    def source_file(self, domain: str, source_id: str) -> Path:
        """A3 布局：source 落位 `sources/<domain>/<id>/<id>.md`（目录式，容纳原件/衍生媒体）。

        原文为 `sources/<domain>/<id>.md`；A3 把每个 source 收进以 id 命名的目录，
        原始附件（`<id>.<ext>`）、衍生媒体（`media/`）、转录（`transcript/`）与 .md 同驻。
        """
        return self.source_dir(domain, source_id) / f"{source_id}.md"

    def source_dir(self, domain: str, source_id: str) -> Path:
        """A3 目录：`sources/<domain>/<id>/`。"""
        return self.sources_dir(domain) / source_id

    def source_attachment(self, domain: str, source_id: str, filename: str) -> Path:
        """source 目录内的附件路径（原始件 `<id>.<ext>`、衍生 `media/<name>` 等）。"""
        return self.source_dir(domain, source_id) / filename

    def raw_file(self, raw_sha256: str, suffix: str = "") -> Path:
        """证据链原始字节的不可变存放路径（LFS）：`archive/raw/<sha><suffix>`。"""
        return self.archive_raw / f"{strip_sha256_prefix(raw_sha256)}{suffix}"

    def source_raw_staging(self, operation_id: str, suffix: str = "") -> Path:
        """fetch 原件在 preview→apply 之间的暂存路径（apply 后清除，不留垃圾）。"""
        return self.state_root / "source-raw" / f"{operation_id}{suffix}"

    def source_domains(self) -> list[str]:
        """sources 下实际存在的域目录。

        故意扫盘而不是硬编码域名列表：硬编码会在新增 domain 时静默漏检
        （doctor 的 `checked` 少算而仍报 ok），这与布局变更导致的静默归零同型。
        """
        root = self.sources_root
        if not root.is_dir():
            return []
        return sorted(p.name for p in root.iterdir() if p.is_dir())

    def iter_source_files(self) -> Iterator[Path]:
        """全部 source 文件（枚举口径的唯一入口，布局变更只影响 sources_root）。

        A3 布局下 source 收进 `<domain>/<id>/` 目录，用 rglob 递归；`media/`/`transcript/`
        子目录的附件非 .md，不会被误收。
        """
        for domain in self.source_domains():
            yield from sorted(self.sources_dir(domain).rglob("*.md"))

    @property
    def wiki_root(self) -> Path:
        return self.content_root / "wiki"

    def wiki_dir(self, domain: str) -> Path:
        return self.wiki_root / domain

    def wiki_file(self, domain: str, wiki_id: str) -> Path:
        return self.wiki_dir(domain) / f"{wiki_id}.md"

    # ---- unmanaged 层（§4.5：无 object 身份、不进 projection/hash/query-result） ----
    @property
    def working_root(self) -> Path:
        return self.content_root / "working"

    @property
    def journal_root(self) -> Path:
        return self.content_root / "journal"

    def journal_dir(self, year: int | str, month: int | str) -> Path:
        return self.journal_root / f"{year}" / f"{int(month):02d}"

    @property
    def decisions_root(self) -> Path:
        return self.content_root / "decisions"

    @property
    def unmanaged_roots(self) -> tuple[Path, Path, Path]:
        """三个 unmanaged 层（枚举口径唯一入口，供 TTL 报告与文本检索共用）。"""
        return (self.working_root, self.journal_root, self.decisions_root)

    @property
    def object_roots(self) -> tuple[tuple[str, Path], ...]:
        """(object_type, 物理根)：有 object 身份的两层（§4.5 managed 层）。

        枚举口径必须集中：同一份 `(("wiki","wiki"),("source","sources"))` 元组
        在 vault_registry 里出现过三次，目录搬走后三处一起静默返回空集合。
        """
        return (("wiki", self.wiki_root), ("source", self.sources_root))

    @property
    def backup_roots(self) -> tuple[Path, ...]:
        """必须进备份的 owner 数据根（§4.3：content 与 ledger 都不可重建）。

        备份枚举不得自己写目录名：批次 2 实测教训——`("sources", "wiki", ...)`
        这样的硬编码元组在目录搬走后会静默产出"只含 archive/audit"的 manifest，
        restore 仍报成功，canonical 内容悄悄丢掉。
        """
        return (
            self.sources_root,
            self.wiki_root,
            self.content_root / "practice",
            self.archive_root,
            self.audit_root,
        )

    # ---- ledger（§4.4：机器写、append-only；批次 3 迁入 ledger/ 只改这三个属性） ----
    @property
    def archive_root(self) -> Path:
        return self.root / "archive"

    @property
    def audit_root(self) -> Path:
        return self.root / "audit"

    @property
    def release_root(self) -> Path:
        return self.root / "release"

    # ---- archive（§5.6：不可变快照，text 进仓库、raw 走 LFS） ----
    @property
    def archive_text(self) -> Path:
        return self.archive_root / "text"

    @property
    def archive_raw(self) -> Path:
        return self.archive_root / "raw"

    @property
    def manifest(self) -> Path:
        return self.archive_root / "manifest.jsonl"

    def snapshot_file(self, snapshot_sha256: str) -> Path:
        return self.archive_text / f"{strip_sha256_prefix(snapshot_sha256)}.md"

    # ---- audit（durable records，§6.8 路径固定） ----
    @property
    def audit_operations(self) -> Path:
        return self.audit_root / "operations"

    def operation_file(self, operation_id: str) -> Path:
        return self.audit_operations / f"{operation_id}.json"

    def audit_validation(self, object_type: str, object_id: str) -> Path:
        return self.audit_root / "validation" / object_type / object_id

    @property
    def audit_backup(self) -> Path:
        return self.audit_root / "backup"

    @property
    def audit_retire(self) -> Path:
        return self.audit_root / "retire"

    # ---- release（public-safe 确认事件，§6.8） ----
    @property
    def release_confirmations(self) -> Path:
        return self.release_root / "public-confirmations"

    # ---- state（本机临时运行态，git 忽略，不是事实源） ----
    @property
    def state_root(self) -> Path:
        return self.var_root / "state"

    @property
    def state_index(self) -> Path:
        """默认 FTS5 索引目录。

        `indexing` 侧的"从索引路径反推 root"必须与这里同源：此前那边按
        `state/index` 数层级，批次 1 迁到 `var/state/index/` 之后反推出的 root
        少了一层（得到 `<root>/var`）。布局约定只能有一处。
        """
        return self.state_root / "index"

    @property
    def state_operations(self) -> Path:
        return self.var_root / "state" / "operations"

    def state_operation_file(self, operation_id: str) -> Path:
        return self.state_operations / f"{operation_id}.json"

    @property
    def state_commit_intents(self) -> Path:
        return self.var_root / "state" / "commit-intents"

    def commit_intent_file(self, operation_id: str) -> Path:
        return self.state_commit_intents / f"{operation_id}.json"

    @property
    def state_locks(self) -> Path:
        return self.var_root / "state" / "locks"

    def lock_file(self, vault_id: str) -> Path:
        return self.state_locks / f"{vault_id}.lock"

    def state_local_sources(self, vault_id: str) -> Path:
        return self.var_root / "state" / "local-sources" / vault_id

    @property
    def capability_token(self) -> Path:
        """local API 能力令牌（父目录须 0700，声明在 policy `security.local_api`）。"""
        return self.state_root / "capability-token"

    @property
    def release_lock(self) -> Path:
        """public 发布期的独占锁（声明在 policy `build.release_lock_path`）。"""
        return self.state_root / "public-release.lock"

    # ---- queries / reports（§4：public 投影 / local 检索 / 只读报告） ----
    @property
    def queries_root(self) -> Path:
        return self.var_root / "queries"

    @property
    def reports_root(self) -> Path:
        return self.var_root / "reports"

    @property
    def queries_public(self) -> Path:
        return self.queries_root / "public"

    @property
    def queries_local(self) -> Path:
        return self.queries_root / "local"

    # ---- practice（F008 预留；当前版本不读取） ----
    @property
    def practice_questions(self) -> Path:
        return self.content_root / "practice" / "questions"

    @property
    def practice_reviews_root(self) -> Path:
        return self.content_root / "practice" / "reviews"

    def practice_reviews(self, question_id: str) -> Path:
        return self.practice_reviews_root / f"{question_id}.jsonl"

    # ---- config ----
    @property
    def config_dir(self) -> Path:
        return self.root / "config"

    @property
    def vaults_local_manifest(self) -> Path:
        return self.config_dir / "vaults.local.yaml"

    # ---- state 扩展（§4：llm-validation / reading 运行缓存） ----
    @property
    def state_llm_validation(self) -> Path:
        return self.var_root / "state" / "llm-validation"

    @property
    def state_reading(self) -> Path:
        return self.var_root / "state" / "reading"
