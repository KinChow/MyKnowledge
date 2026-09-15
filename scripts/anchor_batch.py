#!/usr/bin/env python3
"""批量建立 evidence 锚点（幂等写、直接落盘）。

背景：ADR-0019 把锚定重新归类为「幂等派生」而非「审批写操作」——
`EvidenceAnchor.anchor()` 是纯计算、`apply_evidence()` 已实现幂等
（同一 `(snapshot_sha256, position)` 返回既有 item），因此不需要
`store.new` / `apply_preflight` / `VaultLock` / operation 状态机。

本脚本只调这两个静态方法，把引文锚点直接追加进 source front matter 的
`evidence_items`，并输出 `claim 引文 → evidence_id` 映射供 wiki claim 的
`targets` 回填使用。

用法（仓库根目录）：
    .venv/bin/python scripts/anchor_batch.py --dry-run
    .venv/bin/python scripts/anchor_batch.py --mapping-out var/pilot/anchor-map.json

幂等：重复执行返回既有 evidence_id（`apply_evidence` 的幂等语义），不产生重复锚点。
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.evidence_anchor import EvidenceAnchor  # noqa: E402
from tools.front_matter import FrontMatter  # noqa: E402

NOTES_DIR = Path("content/working/computer-science")
SUMMARY_SECTION = "一句话结论"
MIN_CHARS = 12


def _index_sources(root: Path) -> dict[str, Path]:
    """object id → source canonical 路径。"""
    index: dict[str, Path] = {}
    for path in sorted((root / "content/sources").rglob("*.md")):
        metadata, _ = FrontMatter.parse(path.read_text(encoding="utf-8"))
        index[str(metadata.get("id") or path.stem)] = path
    return index


def _snapshot_path(root: Path, metadata: dict) -> Path:
    digest = str(metadata.get("snapshot_sha256", "")).split(":")[-1]
    return root / "archive/text" / f"{digest}.md"


def _anchor_one(
    root: Path, source_path: Path, exact: str
) -> tuple[dict | None, str | None]:
    """在 source 的快照中锚定一条引文；返回 (evidence, error_code)。"""
    metadata, _ = FrontMatter.parse(source_path.read_text(encoding="utf-8"))
    snapshot = _snapshot_path(root, metadata)
    try:
        evidence = EvidenceAnchor.anchor(
            snapshot.read_text(encoding="utf-8"), exact, MIN_CHARS
        )
    except ValueError as exc:
        return None, str(exc)
    except OSError:
        return None, "snapshot_unresolved"
    return evidence, None


def _summary_quote(note: Path) -> str | None:
    """取笔记「一句话结论」小节的首句作为该笔记自身的锚定引文。"""
    body = note.read_text(encoding="utf-8")
    section = re.search(
        rf"^##\s+{SUMMARY_SECTION}\s*$(.*?)(?=^##\s|\Z)", body, re.M | re.S
    )
    if not section:
        return None
    text = re.sub(r"^[\s>*\-#|]+", "", section.group(1).strip())
    first = re.split(r"(?<=[。！？])", text)[0].strip()
    return first or None


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="批量建立 evidence 锚点（幂等写）")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--dry-run", action="store_true", help="只解析不落盘")
    parser.add_argument(
        "--only",
        choices=("all", "cs336", "notes"),
        default="all",
        help="cs336=仅 .claims.json 引文；notes=仅笔记摘要首句",
    )
    parser.add_argument(
        "--mapping-out", type=Path, help="写出 claim 引文→evidence_id 映射"
    )
    args = parser.parse_args(argv)
    root = args.root.resolve()

    index = _index_sources(root)
    issues: Counter[str] = Counter()
    mapping: list[dict] = []
    claimed: Counter[str] = Counter()

    jobs: list[tuple[str, str, str]] = []  # (source_id, exact, origin_label)
    if args.only in {"all", "cs336"}:
        for claims_file in sorted(NOTES_DIR.glob("llm-*.claims.json")):
            for item in json.loads(claims_file.read_text(encoding="utf-8")):
                jobs.append((item["source_id"], item["exact_quote"], claims_file.stem))
    if args.only in {"all", "notes"}:
        for note in sorted(NOTES_DIR.glob("llm-*.md")):
            quote = _summary_quote(note)
            if quote is None:
                issues["note_summary_missing"] += 1
                continue
            jobs.append((f"working-computer-science-{note.stem}", quote, note.stem))

    for source_id, exact, origin in jobs:
        source_path = index.get(source_id)
        if source_path is None:
            issues["source_missing"] += 1
            continue
        evidence, error = _anchor_one(root, source_path, exact)
        if error is not None:
            issues[error] += 1
            continue
        if not args.dry_run:
            evidence = EvidenceAnchor.apply_evidence(source_path, evidence)
        claimed[source_id] += 1
        mapping.append(
            {
                "source_id": source_id,
                "origin": origin,
                "exact": exact,
                "evidence_id": evidence["evidence_id"],
                "position": evidence["position"],
                "snapshot_sha256": evidence["snapshot_sha256"],
            }
        )

    report = {
        "state": "dry_run" if args.dry_run else "applied",
        "anchored": len(mapping),
        "unresolved": dict(issues),
        "sources_touched": len(claimed),
        "per_source": dict(claimed.most_common()),
    }
    if args.mapping_out and not args.dry_run:
        args.mapping_out.parent.mkdir(parents=True, exist_ok=True)
        args.mapping_out.write_text(
            json.dumps(mapping, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        report["mapping_out"] = str(args.mapping_out)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if not issues else 2


if __name__ == "__main__":
    raise SystemExit(main())
