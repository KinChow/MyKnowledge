"""存量 source 的定位判定与改判（§6.4 F010 澄清、§16.2 downgrade、LAY 迁移批次 2 前置）。

背景：163 篇存量全部登记为 `source_type: local-file` + `origin: external` + `read_status: retrieved`，
声明语义是"我抓到的外部原文副本"，事实是本人写的加工文档。这不是排版问题而是证据模型失真——
引用它们的 wiki 会被算成有外部来源支撑，可派生出 verified/attested。

本模块只做两件事：
- `classify` 只读，产出逐篇判定清单（external / intermediate / final）与判定依据；
- `apply` 按 **owner 确认过的清单** 把 intermediate/final 的 source 改判为 personal-note，
  走既有 preview/apply 协议，不绕过写入门禁。

判不准一律归 intermediate（更保守一侧，§6.7 "判不准按 personal 处理"的同一原则）。
"""

from __future__ import annotations

import json
import re
import subprocess
from contextlib import suppress
from dataclasses import dataclass, field
from pathlib import Path

from .common import (
    atomic_write,
    canonical_json,
    hash_canonical,
    new_operation_id,
    safe_id,
    safe_relative_path,
    sha256_text,
    strip_sha256_prefix,
)
from .front_matter import FrontMatter
from .paths import RepoPaths
from .vault_lock import LockBusyError, VaultLock

PLAN_SCHEMA_VERSION = "reposition-plan/v1"
CATEGORIES = ("external", "intermediate", "final")

_URL = re.compile(r"https?://[^\s)>\]]+")
_HEADING = re.compile(r"^#{1,6}\s", re.MULTILINE)
_UNFINISHED = re.compile(r"TODO|FIXME|待补|待验证|待确认|待完善|\?{2,}|？{2,}")


@dataclass(frozen=True)
class Thresholds:
    """final 的判定门槛。取值来自实测分布（163 篇正文中位数 1806 字符）。"""

    final_min_chars: int = 1500
    final_min_headings: int = 3


@dataclass
class Signals:
    """一篇 source 的可判定信号（全部来自文件本身，不猜测）。"""

    source_id: str
    domain: str
    path: str
    source_sha256: str
    body_chars: int
    headings: int
    external_links: int
    unfinished: bool
    origin: str | None
    source_type: str | None
    legacy_path: str | None
    reasons: list[str] = field(default_factory=list)


def _legacy_path(paths: RepoPaths, metadata: dict, source_id: str) -> str | None:
    """从 local-file sidecar 取原始 docs/ 路径（sidecar 被 Git 忽略，缺失是正常的）。"""
    local = metadata.get("local")
    if not isinstance(local, dict) or not str(local.get("path_ref", "")).startswith(
        "local-sidecar:"
    ):
        return None
    vault_id = str(local["path_ref"]).removeprefix("local-sidecar:").split("/")[0]
    sidecar = paths.state_local_sources(vault_id) / f"{source_id}.json"
    if not sidecar.is_file():
        return None
    try:
        recorded = json.loads(sidecar.read_text(encoding="utf-8")).get("path")
    except (OSError, ValueError):
        return None
    if not recorded:
        return None
    root = str(paths.root.resolve())
    return (
        str(Path(recorded).resolve()).removeprefix(root).lstrip("/")
        if str(Path(recorded).resolve()).startswith(root)
        else recorded
    )


def _signals(paths: RepoPaths, path: Path) -> Signals:
    text = path.read_text(encoding="utf-8")
    metadata, body = FrontMatter.parse(text)
    source_id = str(metadata.get("id") or path.stem)
    return Signals(
        source_id=source_id,
        domain=str(metadata.get("domain") or path.parent.name),
        path=str(path.relative_to(paths.root)),
        source_sha256=sha256_text(text),
        body_chars=len(body.strip()),
        headings=len(_HEADING.findall(body)),
        external_links=len(set(_URL.findall(body))),
        unfinished=bool(_UNFINISHED.search(body)),
        origin=metadata.get("origin"),
        source_type=metadata.get("source_type"),
        legacy_path=_legacy_path(paths, metadata, source_id),
    )


def _categorize(signals: Signals, thresholds: Thresholds) -> str:
    """三分类。external 只表示"存在可抓取的出处候选"，是否真的补 url 由 owner 决定。"""
    if signals.external_links:
        signals.reasons.append(
            f"正文含 {signals.external_links} 个外链，可能有可抓取出处"
        )
        return "external"
    if signals.unfinished:
        signals.reasons.append("正文含未完成标记（TODO/待补/待验证）")
        return "intermediate"
    if (
        signals.body_chars >= thresholds.final_min_chars
        and signals.headings >= thresholds.final_min_headings
    ):
        signals.reasons.append(
            f"正文 {signals.body_chars} 字符 / {signals.headings} 个标题，结构完整"
        )
        return "final"
    signals.reasons.append(
        f"正文 {signals.body_chars} 字符 / {signals.headings} 个标题，未达终版门槛"
    )
    return "intermediate"


def wiki_referenced_source_ids(root: Path) -> dict[str, list[str]]:
    """被保留 wiki 引用的 source_id → 引用它的 wiki id 列表（保护清单，不硬编码）。

    `content/wiki/` 里任何一篇通过 `sources` 或 `evidence.targets.source_id`
    引用的 source 都不能降级：搬走会让该页 `evidence_state` 变 `unresolved`，
    已发布页面同时失去可发布性。保护清单必须由实际引用推导——写死 id 会在
    下一次新增 wiki 时静默失效。
    """
    paths = RepoPaths(root)
    referenced: dict[str, list[str]] = {}
    if not paths.wiki_root.is_dir():
        return referenced
    for path in sorted(paths.wiki_root.rglob("*.md")):
        try:
            metadata, _ = FrontMatter.parse(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, ValueError):
            continue  # wiki 自身的格式问题由 validator 报告，不在此重复
        wiki_id = str(metadata.get("id") or path.stem)
        ids = {str(s) for s in metadata.get("sources") or []}
        for claim in metadata.get("evidence") or []:
            for target in (claim or {}).get("targets") or []:
                source_id = (target or {}).get("source_id")
                if source_id:
                    ids.add(str(source_id))
        for source_id in ids:
            referenced.setdefault(source_id, []).append(wiki_id)
    return {k: sorted(set(v)) for k, v in referenced.items()}


def _legacy_first_commit_at(root: Path, legacy_path: str | None) -> str | None:
    """`legacy_path` 首次进入 Git 的作者时间（ISO 8601），取不到返回 None。

    为什么不是文件 mtime：实测 161 篇存量的 `docs/` 原文与 `content/sources/`
    副本 mtime 全是 2026-08-28（迁移当天重写过），mtime 已被抹平成噪声。Git
    首次提交时间是仓库里唯一还留着的时间事实。

    字段名刻意叫 `legacy_first_commit_at` 而不是 `created_at`：它是"首次进入
    Git 的时间"，不是写作时间——实测 161 篇里 156 篇落在同一天（2025-07-06），
    那是一次批量导入，叫 `created_at` 会让人把导入日误读成创作日。
    """
    if not legacy_path:
        return None
    try:
        result = subprocess.run(
            [
                "git",
                "log",
                "--diff-filter=A",
                "--follow",
                "--format=%aI",
                "--",
                legacy_path,
            ],
            cwd=str(Path(root).resolve()),
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    lines = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    return lines[-1] if lines else None


def classify(root: Path, thresholds: Thresholds | None = None) -> dict:
    """只读：产出逐篇判定清单，交 owner 逐篇确认后才能进入 apply。"""
    paths = RepoPaths(root)
    thresholds = thresholds or Thresholds()
    retained = wiki_referenced_source_ids(root)
    items = []
    for path in paths.iter_source_files():
        signals = _signals(paths, path)
        category = _categorize(signals, thresholds)
        retained_by = retained.get(signals.source_id, [])
        if retained_by:
            signals.reasons.append(
                f"被 wiki {'/'.join(retained_by)} 引用，必须留在 content/sources/"
            )
        items.append(
            {
                "source_id": signals.source_id,
                "domain": signals.domain,
                "path": signals.path,
                "source_sha256": signals.source_sha256,
                "current": {
                    "source_type": signals.source_type,
                    "origin": signals.origin,
                },
                "suggested_category": category,
                "category": category,
                "retained_by": retained_by,
                "legacy_path": signals.legacy_path,
                "legacy_first_commit_at": _legacy_first_commit_at(
                    root, signals.legacy_path
                ),
                "signals": {
                    "body_chars": signals.body_chars,
                    "headings": signals.headings,
                    "external_links": signals.external_links,
                    "unfinished": signals.unfinished,
                },
                "reasons": signals.reasons,
            }
        )
    return {
        "schema_version": PLAN_SCHEMA_VERSION,
        "confirmed": False,
        "thresholds": {
            "final_min_chars": thresholds.final_min_chars,
            "final_min_headings": thresholds.final_min_headings,
        },
        "counts": {c: sum(1 for i in items if i["category"] == c) for c in CATEGORIES},
        "retained": sorted(i["source_id"] for i in items if i["retained_by"]),
        "relocatable": sum(1 for i in items if not i["retained_by"]),
        # 时间事实取不到的篇数必须显式可见：落位会重写文件、抹掉最后一点时间痕迹，
        # 这个计数是 owner 判断"落位后还剩多少时间信息"的唯一依据
        "legacy_time_unresolved": sum(
            1
            for i in items
            if not i["retained_by"] and not i.get("legacy_first_commit_at")
        ),
        "items": items,
    }


def _load_plan(plan_path: Path) -> tuple[dict | None, dict | None]:
    """加载 owner 确认过的清单；未确认或格式不符一律 fail-closed。"""
    try:
        plan = json.loads(plan_path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None, {"state": "blocked", "error_code": "plan_unreadable"}
    if plan.get("schema_version") != PLAN_SCHEMA_VERSION:
        return None, {"state": "blocked", "error_code": "plan_schema_mismatch"}
    if plan.get("confirmed") is not True:
        return None, {
            "state": "blocked",
            "error_code": "plan_not_confirmed",
            "next_action": "owner 逐篇核对 category 后把 confirmed 改为 true",
        }
    return plan, None


def _title_from_body(body: str, fallback: str) -> str:
    """取正文首个 H1 作标题；没有就退回 source_id（不编造标题）。"""
    for line in body.splitlines():
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped[2:].strip() or fallback
    return fallback


def _duplicate_legacy_groups(plan: dict) -> list[dict]:
    """同一 legacy_path 被导入成多个 source 的分组（重复导入是既存事实）。"""
    groups: dict[str, list[str]] = {}
    for item in plan.get("items") or []:
        legacy_path = item.get("legacy_path")
        if legacy_path:
            groups.setdefault(legacy_path, []).append(str(item.get("source_id")))
    return [
        {"legacy_path": path, "source_ids": sorted(ids)}
        for path, ids in sorted(groups.items())
        if len(ids) > 1
    ]


def _write_cdr(root: Path, plan: dict, relocated: list[str], actor_id: str) -> str:
    """整批降级只写一条 CDR：一次决策一条记录，不写 161 条假装逐篇决策过。"""
    paths = RepoPaths(root)
    plan_sha256 = hash_canonical(plan)
    record_id = f"CDR-{strip_sha256_prefix(plan_sha256)[:12]}"
    duplicates = _duplicate_legacy_groups(plan)
    metadata = {
        "id": record_id,
        "content_verdict": "downgrade",
        "actor_id": actor_id,
        "plan_sha256": plan_sha256,
        "relocated_count": len(relocated),
        "relocated_source_ids": relocated,
        "retained_source_ids": plan.get("retained") or [],
        "duplicate_legacy_paths": duplicates,
    }
    body = (
        "# 存量 source 整批降级落位\n\n"
        "## 判定\n\n"
        f"{len(relocated)} 篇被误登记为 `source/v1` 的加工文档整批降级到 "
        "`content/working/`。它们不是外部来源的快照，而是本人整理的加工内容——"
        "登记为 source 会让引用它们的 wiki 看起来有外部证据支撑（可派生 "
        "`verified`/`attested`），这是失真。\n\n"
        "## 保留项\n\n"
        f"{', '.join(metadata['retained_source_ids']) or '（无）'}"
        "：被保留的 wiki 通过 `sources`/`evidence.targets` 实际引用，"
        "搬走会让那些页面 `evidence_state` 变 `unresolved`。\n\n"
        "## 重复导入\n\n"
        f"{len(duplicates)} 组同一 `legacy_path` 被导入成多个 source"
        "（清单见 front matter `duplicate_legacy_paths`）。降级阶段两份都落位、"
        "不做内容取舍：去重属于逐篇升级时的判断，批量阶段替人选一份等于替人"
        "做内容决策。\n\n"
        "## 不做的事\n\n"
        "- `archive/` 快照与 `manifest.jsonl` 一律不动：曾经导入过是事实，"
        "append-only 账目不因改判而重写；\n"
        "- 不批量升级进 `content/wiki/`：升级是逐篇人工动作（CHN-001）。\n"
    )
    target = paths.decisions_root / f"{record_id}.md"
    atomic_write(target, FrontMatter.render(metadata, body).encode("utf-8"))
    return record_id


def apply(root: Path, plan_path: Path, *, actor_id: str = "local-user") -> dict:
    """按确认清单把存量 source 整批降级落位到 `content/working/`（CHN-001）。

    落位不是改判：这些文档从来不是外部来源的快照，`content/working/` 才是
    加工阶段内容的归属层。落位文件只保留 `title`/`domain`/`legacy_path`/
    `snapshot_sha256` 四个字段——前两个用于人找回它，`legacy_path` 满足
    working 层入口约束，`snapshot_sha256` 让原始字节仍可自证。它不再有
    `schema_version: source/v1`，因此不再有 object 身份，也不能被 wiki 的
    `evidence.targets` 引用。

    `archive/` 快照与 manifest 一律不动（append-only 历史）；被保留 wiki 引用
    的 source 一律不搬（`retained_by` 非空即跳过，判据由引用推导而非硬编码）。
    """
    plan, error = _load_plan(plan_path)
    if error is not None:
        return error

    operation_id = new_operation_id()
    try:
        # 落位是不可逆的批量写（写 working 层 + 删除 source 文件），必须与
        # ingest/anchor/apply 共用同一把 public vault 独占写锁，否则两条写入
        # 路径会交错在同一批文件上。
        with VaultLock(root, "public", operation_id):
            return _relocate(root, plan, actor_id, operation_id)
    except LockBusyError:
        return VaultLock.lock_busy_response(operation_id)


def _validate_plan_item(item: dict, paths: RepoPaths) -> dict | None:
    """前置校验一条 plan item 的必需字段与路径安全（C004）；非法时返回 blocked 段。

    plan 是外部可改写的输入（confirmed:true 即可进入 apply）：`path`/`domain`/
    `source_id` 直接用于拼接文件路径并 `unlink`，`..`/绝对路径/多级 domain 都
    可能把删除引到仓库外或非 source 位置。因此拼接前先归一再拒绝，与
    `record_path_candidates` 同一条口径（`safe_relative_path`）。
    """
    for key in ("source_id", "path", "domain"):
        if not item.get(key):
            return {
                "state": "blocked",
                "error_code": "plan_item_incomplete",
                "missing": key,
            }
    try:
        safe_id(str(item["source_id"]))
        rel_path = safe_relative_path(str(item["path"]))
        rel_domain = safe_relative_path(str(item["domain"]))
    except ValueError:
        return {"state": "blocked", "error_code": "plan_item_invalid"}
    if "/" in rel_domain:  # domain 是单段目录名，不是路径
        return {"state": "blocked", "error_code": "plan_item_invalid"}
    source = paths.root / rel_path
    if not _contained_in(source, paths.sources_root):
        # path 必须落在 content/sources/ 内：只允许降级 source，不允许借
        # unlink 删除仓库内其他位置的文件
        return {"state": "blocked", "error_code": "plan_item_invalid"}
    return None


def _contained_in(candidate: Path, base: Path) -> bool:
    """candidate 是否在 base 目录内（resolve 后判断，防 symlink 逃逸）。"""
    try:
        base_real = base.resolve(strict=False)
        target = candidate.resolve(strict=False)
    except OSError:
        return False
    return target == base_real or base_real in target.parents


def _write_failure_intent(
    intent_path: Path, intent: dict, error_code: str, detail: str
) -> None:
    """把 commit-intent 标记为 failed（durable 失败出口，append 不重写历史）。"""
    failed = {
        **intent,
        "state": "failed",
        "error_code": error_code,
        "detail": detail,
    }
    failed["intent_sha256"] = hash_canonical(
        {k: v for k, v in failed.items() if k != "intent_sha256"}
    )
    atomic_write(intent_path, canonical_json(failed) + b"\n", 0o600)


def _collect_relocatable(paths: RepoPaths, plan: dict) -> tuple[list[dict], list[dict]]:
    """前置校验全部 plan item，产出逐条结果与待落位条目（本阶段不写任何文件）。

    返回值 (results, relocatable)：results 覆盖 retained/blocked/relocated 全部判定；
    relocatable 是已通过全部前置校验、等待写入 working 层的条目。校验逻辑独立成
    函数，避免 `_relocate` 同时承担"判定 + 写盘 + 回滚"导致复杂度过高。
    """
    results: list[dict] = []
    relocatable: list[dict] = []
    for item in plan.get("items", []):
        source_id = item.get("source_id")
        if item.get("retained_by"):
            results.append(
                {
                    "source_id": source_id,
                    "state": "retained",
                    "retained_by": item["retained_by"],
                }
            )
            continue
        validation_error = _validate_plan_item(item, paths)
        if validation_error is not None:
            results.append({"source_id": source_id, **validation_error})
            continue
        source = paths.root / safe_relative_path(str(item["path"]))
        if not source.is_file():
            results.append(
                {
                    "source_id": source_id,
                    "state": "blocked",
                    "error_code": "source_missing",
                }
            )
            continue
        text = source.read_text(encoding="utf-8")
        if sha256_text(text) != item.get("source_sha256"):
            # 清单产出后文件被改过：判定依据已失效，必须重新 classify
            results.append(
                {
                    "source_id": source_id,
                    "state": "blocked",
                    "error_code": "source_drifted",
                }
            )
            continue
        legacy_path = item.get("legacy_path")
        if not legacy_path:
            # working 层入口约束：缺 source_ref 又缺 legacy_path 不得写入
            results.append(
                {
                    "source_id": source_id,
                    "state": "blocked",
                    "error_code": "legacy_path_missing",
                }
            )
            continue
        metadata, body = FrontMatter.parse(text)
        target = (
            paths.working_root
            / safe_relative_path(str(item["domain"]))
            / f"{safe_id(str(item['source_id']))}.md"
        )
        if target.exists():
            results.append(
                {
                    "source_id": source_id,
                    "state": "blocked",
                    "error_code": "target_exists",
                }
            )
            continue
        front_matter = {
            "title": _title_from_body(body, str(item["source_id"])),
            "domain": item["domain"],
            "legacy_path": legacy_path,
            "snapshot_sha256": metadata.get("snapshot_sha256"),
        }
        # 时间事实来自清单（classify 在真实仓库里用 Git 首次提交时间求得），apply
        # 不重算：apply 已经在删文件了，让它同时去推断时间只会多一个不可复核的输入。
        # 取不到时不写该键——空值假装有时间比缺键更糟。
        if item.get("legacy_first_commit_at"):
            front_matter["legacy_first_commit_at"] = item["legacy_first_commit_at"]
        relocatable.append(
            {
                "source_id": str(item["source_id"]),
                "source": source,
                "target": target,
                "text": text,
                "body": body,
                "front_matter": front_matter,
            }
        )
    return results, relocatable


def _relocate(root: Path, plan: dict, actor_id: str, operation_id: str) -> dict:
    """在已持 public vault 写锁的前提下执行落位（只由 apply 调用）。

    落位是不可逆批量写（写 working + 删 source），必须 durable：循环前写
    commit-intent 到 ``state/commit-intents/``，循环内任一 item 失败即回滚已删
    source、移除已写 target、把 intent 标记 failed，返回结构化错误码而非
    traceback——绝不留下"删了一半、没有记录"的状态。
    """
    paths = RepoPaths(root)
    results, relocatable = _collect_relocatable(paths, plan)
    relocated: list[str] = []
    if not relocatable:
        return {
            "schema_version": "reposition-result/v1",
            "relocated": 0,
            "retained": sum(1 for r in results if r.get("state") == "retained"),
            "blocked": sum(1 for r in results if r.get("state") == "blocked"),
            "decision_id": None,
            "results": results,
        }
    intent_path = paths.commit_intent_file(operation_id)
    intent = {
        "schema_version": "reposition-commit-intent/v1",
        "operation_id": operation_id,
        "plan_sha256": hash_canonical(plan),
        "items": [
            {
                "source": str(r["source"].relative_to(paths.root)),
                "target": str(r["target"].relative_to(paths.root)),
                "source_sha256": sha256_text(r["text"]),
            }
            for r in relocatable
        ],
    }
    intent["intent_sha256"] = hash_canonical(
        {k: v for k, v in intent.items() if k != "intent_sha256"}
    )
    originals: dict[Path, bytes] = {}
    written: list[Path] = []
    try:
        atomic_write(intent_path, canonical_json(intent) + b"\n", 0o600)
        for r in relocatable:
            atomic_write(
                r["target"],
                FrontMatter.render(r["front_matter"], r["body"]).encode("utf-8"),
            )
            written.append(r["target"])
            originals[r["source"]] = r["text"].encode("utf-8")
            r["source"].unlink()
            relocated.append(r["source_id"])
            results.append(
                {
                    "source_id": r["source_id"],
                    "state": "relocated",
                    "target": str(r["target"].relative_to(paths.root)),
                }
            )
    except OSError as exc:
        # 失败出口：回滚已删 source、移除已写 target、intent 标记 failed
        for source, data in originals.items():
            atomic_write(source, data)
        for target in written:
            target.unlink(missing_ok=True)
        with suppress(OSError):
            _write_failure_intent(intent_path, intent, "apply_failed", str(exc))
        return {
            "schema_version": "reposition-result/v1",
            "state": "blocked",
            "operation_id": operation_id,
            "error_code": "apply_failed",
            "detail": str(exc),
            "relocated": 0,
            "retained": sum(1 for r in results if r.get("state") == "retained"),
            "blocked": sum(1 for r in results if r.get("state") == "blocked"),
            "decision_id": None,
            "results": results,
        }
    intent_path.unlink(missing_ok=True)
    decision_id = _write_cdr(root, plan, relocated, actor_id) if relocated else None
    return {
        "schema_version": "reposition-result/v1",
        "relocated": len(relocated),
        "retained": sum(1 for r in results if r.get("state") == "retained"),
        "blocked": sum(1 for r in results if r.get("state") == "blocked"),
        "decision_id": decision_id,
        "results": results,
    }
