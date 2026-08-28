"""doctor 自检：把散落的降级/健康信号汇成一份结构化报告（ADR-0011 降级显性化）。

检查项全部复用现有探测与校验器，不引入新逻辑：
- projection manifest 可用性与条目数；
- 默认 FTS5 索引存在性/新鲜度（generated_from vs 当前 items hash）；
- QMD 可用性（fail-closed 探测）；
- sources 全量 schema/snapshot 一致性校验；
- vault registry / 备份状态摘要。
退出码：任何 `error` 项存在时为 2，仅 warning 为 0。
"""

from __future__ import annotations

import json
from pathlib import Path


def run_doctor(root: Path) -> dict:
    root = Path(root).resolve()
    report: dict = {"schema_version": "doctor/v1", "root": str(root), "checks": [], "errors": 0, "warnings": 0}

    def add(name: str, state: str, **fields) -> None:
        report["checks"].append({"name": name, "state": state, **fields})
        report["errors" if state == "error" else "warnings"] += 1 if state != "ok" else 0

    # 1. public projection manifest
    try:
        from .projection import PublicProjectionStore

        items = PublicProjectionStore(root).public_items(with_body=True)
        add("public_projection", "ok", item_count=len(items))
    except (OSError, ValueError) as exc:
        add("public_projection", "warning", reason=str(exc), next_action="python -m tools.cli projection generate")

    # 2. 默认 FTS5 索引新鲜度（§1808 修订：qmd 已退役，simple 分词的 FTS5 承担检索）
    from .indexing import SQLiteIndex, default_public_index_path
    from .common import hash_canonical

    index_path = default_public_index_path(root)
    if not index_path.exists():
        add("fts5_index", "warning", reason="index_missing", next_action="python -m tools.cli index rebuild --scope public --index state/index/public.sqlite3")
    else:
        try:
            index = SQLiteIndex(index_path)
            expected = hash_canonical([i for i in items]) if items else None
            fresh = expected is None or index.generated_from() == expected
            tokenizer = index.tokenizer()
            add("fts5_index", "ok" if fresh else "warning",
                reason=None if fresh else "index_stale", tokenizer=tokenizer,
                next_action=None if fresh else "同上 rebuild")
        except Exception as exc:  # sqlite3.Error 等
            add("fts5_index", "warning", reason=f"index_unreadable:{type(exc).__name__}", next_action="rebuild")

    # 3b. provider profile 与环境变量冲突（参考 cc-switch env-conflict 检测：
    # 同键双来源且值不同时显式告警，而非静默 env 优先）
    import os as _os
    from .validation.provider import _load_provider_profile

    profile = _load_provider_profile()
    if profile:
        conflicts = [k for k in ("base_url", "api_key", "model")
                     if _os.environ.get(f"OPENAI_{k.upper()}") and profile.get(k)
                     and _os.environ[f"OPENAI_{k.upper()}"] != profile.get(k)]
        add("provider_profile", "ok" if not conflicts else "warning",
            reason=None if not conflicts else f"env_profile_conflict:{','.join(conflicts)}",
            next_action=None if not conflicts else "unset the OPENAI_* env vars or align them with the profile; env silently wins")

    # 4. sources 全量校验（snapshot 一致性是 F010 教训项）
    from .ingest.source_validator import SourceValidator

    validator = SourceValidator()
    bad: list[str] = []
    checked = 0
    for dom in ("computer-science", "multimedia", "reading-notes", "tools", "work-methods"):
        d = root / "sources" / dom
        if not d.is_dir():
            continue
        for p in d.glob("*.md"):
            checked += 1
            if validator.validate_source_file(p):
                bad.append(str(p.relative_to(root)))
    if bad:
        add("sources", "error", checked=checked, invalid=bad[:10], invalid_count=len(bad),
            next_action="investigate snapshot/front-matter drift before further writes")
    else:
        add("sources", "ok", checked=checked)

    # 5. vault registry / 备份
    try:
        from .backup import BackupManager

        status = BackupManager(root).status()
        unverified = [v["vault_id"] for v in status.get("vaults", []) if v.get("backup_state") not in ("verified",) and v["vault_id"] != "public"]
        add("vaults_backup", "ok" if not unverified else "warning",
            vault_count=len(status.get("vaults", [])), unverified=unverified,
            next_action=None if not unverified else "configure and verify owner-scoped backups")
    except (OSError, ValueError) as exc:
        add("vaults_backup", "warning", reason=str(exc))

    report["state"] = "healthy" if report["errors"] == 0 and report["warnings"] == 0 else ("degraded" if report["errors"] == 0 else "failing")
    return report


def main(argv: list[str] | None = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(description="MyKnowledge health self-check")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args(argv)
    report = run_doctor(args.root)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 2 if report["errors"] else 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
