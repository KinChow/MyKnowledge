"""doctor 自检：把散落的降级/健康信号汇成一份结构化报告（ADR-0011 降级显性化）。

检查项全部复用现有探测与校验器，不引入新逻辑：
- projection manifest 可用性与条目数；
- 默认 FTS5 索引存在性/新鲜度（generated_from vs 当前 items hash）；
- QMD 可用性（fail-closed 探测）；
- sources 全量 schema/snapshot 一致性校验；
- archive 快照自证（文件名 == 正文 sha256，任何外部改写都在此暴露）；
- archive manifest 账目双向一致（source 的 snapshot 有 owner record；record 指向的快照在盘上）；
- 滞留的提交收尾（applied_index_pending 的 operation 无人重跑）；
- vault registry / 备份状态摘要。
退出码：任何 `error` 项存在时为 2，仅 warning 为 0。
`--assert-clean` 为门禁模式（pre-commit 钩子消费）：无 error 只打印一行摘要。
"""

from __future__ import annotations

import json
import sqlite3
import sys
from collections.abc import Iterator
from pathlib import Path

SOURCE_DOMAINS = (
    "computer-science",
    "multimedia",
    "reading-notes",
    "tools",
    "work-methods",
)


def _iter_source_files(root: Path) -> Iterator[Path]:
    """sources 域下的全部 source 文件（两条 source 检查共用同一份枚举口径）。"""
    for domain in SOURCE_DOMAINS:
        directory = root / "sources" / domain
        if not directory.is_dir():
            continue
        yield from sorted(directory.glob("*.md"))


def _check_sources(root: Path) -> tuple[str, dict]:
    """sources 全量 schema/snapshot 一致性（F010 教训项）。"""
    from .ingest.source_validator import SourceValidator

    validator = SourceValidator()
    invalid: list[str] = []
    checked = 0
    for path in _iter_source_files(root):
        checked += 1
        if validator.validate_source_file(path):
            invalid.append(str(path.relative_to(root)))
    if not invalid:
        return "ok", {"checked": checked}
    return "error", {
        "checked": checked,
        "invalid": invalid[:10],
        "invalid_count": len(invalid),
        "next_action": "investigate snapshot/front-matter drift before further writes",
    }


def _check_manifest_coverage(root: Path) -> tuple[str, dict]:
    """每篇 source 的 snapshot 必须在 archive manifest 中有 owner record（§5.6）。

    source 与 archive 两两自洽仍可能整体不一致：apply 在写完 source 之后、
    manifest 入账之前失败时，操作被标记 expired 且不可重放，账目缺口没有任何
    检查能看见（实测见 tests 的 after_source 注入点用例）。这条检查不关心缺口
    因何产生——手工编辑 source、迁移漏登记、多 vault 分片出错同样在此暴露。
    """
    from .archive_manifest import ArchiveManifest
    from .front_matter import FrontMatter

    registered = ArchiveManifest(root).snapshot_hashes()
    unregistered: list[str] = []
    checked = 0
    for path in _iter_source_files(root):
        checked += 1
        try:
            metadata, _ = FrontMatter.parse(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, ValueError):
            continue  # front matter 本身的问题由 sources 检查报告，不在此重复
        snapshot = metadata.get("snapshot_sha256")
        if snapshot and snapshot not in registered:
            unregistered.append(str(path.relative_to(root)))
    if not unregistered:
        return "ok", {"checked": checked, "records": len(registered)}
    return "error", {
        "checked": checked,
        "records": len(registered),
        "unregistered": unregistered[:10],
        "unregistered_count": len(unregistered),
        "next_action": "re-run `python -m tools.cli source preview/apply` for these sources to register the missing owner records",
    }


def _check_manifest_records(root: Path) -> tuple[str, dict]:
    """反向账目：每条 owner record 指向的快照必须在盘上、且路径与 hash 自洽（§5.6）。

    与 manifest_coverage 合起来才是双向验证：正向保证"source 有账"，反向保证
    "账有实物"。账目指向不存在的快照同样是证据链断裂——evidence 会解析不到正文。
    反过来"有快照没账目"故意不报错：apply 在 after_archive 之后失败会留下内容
    寻址的孤儿快照，重放命中同一文件，无害（实测全库 225 快照/225 条账目，
    当前无孤儿）。
    """
    from .archive_manifest import ArchiveManifest

    broken: list[dict] = []
    checked = 0
    for entry in ArchiveManifest(root).entries():
        checked += 1
        archive_path = str(entry.get("archive_path") or "")
        snapshot = str(entry.get("snapshot_sha256") or "").removeprefix("sha256:")
        if not archive_path or not snapshot:
            reason = "record_fields_missing"
        elif not (root / archive_path).is_file():
            reason = "snapshot_missing"
        elif Path(archive_path).stem != snapshot:
            reason = "path_hash_mismatch"
        else:
            continue
        broken.append(
            {
                "record_id": entry.get("record_id"),
                "archive_path": archive_path,
                "reason": reason,
            }
        )
    if not broken:
        return "ok", {"checked": checked}
    return "error", {
        "checked": checked,
        "broken": broken[:10],
        "broken_count": len(broken),
        "next_action": "restore the missing archive snapshots from git or backup; owner records are append-only and must not be edited",
    }


def _check_pending_operations(root: Path) -> tuple[str, dict]:
    """滞留的 applied_index_pending：canonical 已提交、派生重建失败且无人重跑。

    实测（2026-08-29）：这种 operation 对其余检查完全不可见——projection 与
    索引一起停在旧版本，`fts5_index` 比的是"索引 vs projection"，两者一致所以
    报 ok；`public_projection` 只看 manifest 可读。结果是 canonical 里的新内容
    在检索/站点里查不到，而 doctor 说 healthy。recover 是显式操作，不会自愈，
    所以必须在这里点名。
    """
    from .paths import RepoPaths

    directory = RepoPaths(root).state_operations
    if not directory.is_dir():
        return "ok", {"checked": 0}
    pending: list[str] = []
    checked = 0
    for path in sorted(directory.glob("*.json")):
        checked += 1
        try:
            record = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, ValueError):
            continue  # operation 记录损坏由 apply 侧 fail-closed 处理，不在此重复
        if record.get("state") == "applied_index_pending":
            pending.append(str(record.get("operation_id") or path.stem))
    if not pending:
        return "ok", {"checked": checked}
    return "warning", {
        "checked": checked,
        "pending": pending[:10],
        "pending_count": len(pending),
        "reason": "projection_rebuild_pending",
        "next_action": f"python -m tools.cli write --recover {pending[0]}",
    }


def _check_archive_integrity(root: Path) -> tuple[str, dict]:
    """archive 快照自证：文件名就是正文 sha256（§5.6 不可变快照）。

    这条检查不依赖"谁改的"——任何格式化器/编辑器/同步工具改写快照都会在此暴露。
    实测教训（2026-08-28）：`ruff format` 会格式化 Markdown 内的 python 代码块。
    """
    from .common import sha256_text
    from .paths import RepoPaths

    drifted: list[str] = []
    checked = 0
    archive_text = RepoPaths(root).archive_text
    if archive_text.is_dir():
        for snapshot in sorted(archive_text.glob("*.md")):
            checked += 1
            try:
                actual = sha256_text(snapshot.read_text(encoding="utf-8"))
            except (OSError, UnicodeError) as exc:
                drifted.append(f"{snapshot.name}:{type(exc).__name__}")
                continue
            if actual != f"sha256:{snapshot.stem}":
                drifted.append(snapshot.name)
    if not drifted:
        return "ok", {"checked": checked}
    return "error", {
        "checked": checked,
        "drifted": drifted[:10],
        "drifted_count": len(drifted),
        "next_action": "git checkout -- archive/text and re-run; a tool rewrote immutable snapshots",
    }


def run_doctor(root: Path) -> dict:
    root = Path(root).resolve()
    report: dict = {
        "schema_version": "doctor/v1",
        "root": str(root),
        "checks": [],
        "errors": 0,
        "warnings": 0,
    }

    def add(name: str, state: str, **fields) -> None:
        report["checks"].append({"name": name, "state": state, **fields})
        report["errors" if state == "error" else "warnings"] += (
            1 if state != "ok" else 0
        )

    # 1. public projection manifest
    try:
        from .projection import PublicProjectionStore

        items = PublicProjectionStore(root).public_items(with_body=True)
        add("public_projection", "ok", item_count=len(items))
    except (OSError, ValueError) as exc:
        add(
            "public_projection",
            "warning",
            reason=str(exc),
            next_action="python -m tools.cli projection generate",
        )

    # 2. 默认 FTS5 索引新鲜度（§1808 修订：qmd 已退役，simple 分词的 FTS5 承担检索）
    from .common import hash_canonical
    from .indexing import SQLiteIndex, default_public_index_path

    index_path = default_public_index_path(root)
    if not index_path.exists():
        add(
            "fts5_index",
            "warning",
            reason="index_missing",
            next_action="python -m tools.cli index rebuild --scope public --index state/index/public.sqlite3",
        )
    else:
        try:
            index = SQLiteIndex(index_path)
            expected = hash_canonical([i for i in items]) if items else None
            fresh = expected is None or index.generated_from() == expected
            tokenizer = index.tokenizer()
            add(
                "fts5_index",
                "ok" if fresh else "warning",
                reason=None if fresh else "index_stale",
                tokenizer=tokenizer,
                next_action=None if fresh else "同上 rebuild",
            )
        except (sqlite3.Error, OSError, ValueError) as exc:
            # 只吞"索引不可读"这类环境事实；工具自身的类型/属性错误必须冒出来
            add(
                "fts5_index",
                "warning",
                reason=f"index_unreadable:{type(exc).__name__}",
                next_action="rebuild",
            )

    # 3b. provider profile 与环境变量冲突（参考 cc-switch env-conflict 检测：
    # 同键双来源且值不同时显式告警，而非静默 env 优先）
    import os as _os

    from .validation.provider import _load_provider_profile

    profile = _load_provider_profile()
    if profile:
        conflicts = [
            k
            for k in ("base_url", "api_key", "model")
            if _os.environ.get(f"OPENAI_{k.upper()}")
            and profile.get(k)
            and _os.environ[f"OPENAI_{k.upper()}"] != profile.get(k)
        ]
        add(
            "provider_profile",
            "ok" if not conflicts else "warning",
            reason=None
            if not conflicts
            else f"env_profile_conflict:{','.join(conflicts)}",
            next_action=None
            if not conflicts
            else "unset the OPENAI_* env vars or align them with the profile; env silently wins",
        )

    # 4. sources 全量校验（snapshot 一致性是 F010 教训项）
    state, fields = _check_sources(root)
    add("sources", state, **fields)

    # 4b. archive 快照自证（文件名 == 正文 sha256）
    state, fields = _check_archive_integrity(root)
    add("archive_integrity", state, **fields)

    # 4c. manifest 账目双向一致（source 有账 / 账有实物）
    state, fields = _check_manifest_coverage(root)
    add("manifest_coverage", state, **fields)
    state, fields = _check_manifest_records(root)
    add("manifest_records", state, **fields)

    # 4d. 滞留的提交收尾（canonical 已提交、projection/索引未重建）
    state, fields = _check_pending_operations(root)
    add("pending_operations", state, **fields)

    # 5. vault registry / 备份
    try:
        from .backup import BackupManager

        status = BackupManager(root).status()
        unverified = [
            v["vault_id"]
            for v in status.get("vaults", [])
            if v.get("backup_state") not in ("verified",) and v["vault_id"] != "public"
        ]
        add(
            "vaults_backup",
            "ok" if not unverified else "warning",
            vault_count=len(status.get("vaults", [])),
            unverified=unverified,
            next_action=None
            if not unverified
            else "configure and verify owner-scoped backups",
        )
    except (OSError, ValueError) as exc:
        add("vaults_backup", "warning", reason=str(exc))

    report["state"] = (
        "healthy"
        if report["errors"] == 0 and report["warnings"] == 0
        else ("degraded" if report["errors"] == 0 else "failing")
    )
    return report


def main(argv: list[str] | None = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(description="MyKnowledge health self-check")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument(
        "--assert-clean",
        action="store_true",
        help="门禁模式：健康/降级只打印一行，出现 error 时把报告打到 stderr 并退出 2",
    )
    args = parser.parse_args(argv)
    report = run_doctor(args.root)
    if not args.assert_clean:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 2 if report["errors"] else 0
    if report["errors"]:
        print(json.dumps(report, ensure_ascii=False, indent=2), file=sys.stderr)
        return 2
    print(f"doctor: {report['state']} (warnings={report['warnings']})")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
