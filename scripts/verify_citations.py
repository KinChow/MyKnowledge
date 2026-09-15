#!/usr/bin/env python3
"""引文可验证性回归检查器（A0-5，ADR-0019 第一条硬门禁）。

背景：`doctor --assert-clean` 只校验 source 的 `snapshot_sha256` 与 archive 快照
一致，**不**校验 `evidence_items[].selector` 能否命中快照，也不校验 wiki claim 的
`supporting_quotes[].exact` 是否真的逐字出现在被引 source 的快照里。因此全库
数百条锚点与 581 条 wiki 引文目前零回归保护——内容漂移会静默通过全部门禁。

本脚本只读，不改任何 canonical 文件，也不接进 `validate`（ADR-0019 仍为 Proposed）。
它把 ADR-0019 第 2 条表格中「per-claim 引文可验证性」拆成四条可执行检查：

  (a) wiki claim 的 `supporting_quotes[].exact` 能否在其 `evidence_id` 对应的
      source 快照中逐字命中 → `not_verbatim_in_snapshot`
  (b) source 的 `evidence_items[].selector.exact` 能否在其 `snapshot_sha256` 指向
      的快照中逐字命中，且 `position.start/end` 与重算结果一致
      → `not_verbatim_in_snapshot` / `position_mismatch` / `exact_ambiguous`
  (c) `evidence_items[].selector` 的 `prefix`/`suffix` 是否与快照中该位置的上下文
      一致 → `prefix_mismatch` / `suffix_mismatch`
  (d) `evidence_id` 是否可解析到某个 source（悬空 id 检出）
      → `dangling_evidence_id`

另附一项一致性检查（不属已知 23 条基线，单独列出便于甄别）：
  - wiki claim 的 `supporting_quotes[].exact` 与对应 source selector 的 `exact`
    是否一致 → `differs_from_source_selector`
  - source 快照文件是否存在、`sha256` 是否与声明一致
    → `snapshot_unresolved` / `snapshot_sha256_mismatch`

用法（仓库根目录）：
    .venv/bin/python scripts/verify_citations.py
    .venv/bin/python scripts/verify_citations.py --root /path/to/repo
    .venv/bin/python scripts/verify_citations.py --json-out var/reports/citations.json
    .venv/bin/python scripts/verify_citations.py --quiet

返回码：0 = 干净；2 = 检出失败项。
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.common import canonical_quote, hash_canonical, sha256_text  # noqa: E402
from tools.front_matter import FrontMatter  # noqa: E402

# 归一化口径下的已知失败基线 = 0。
#
# 历史更正（2026-09-15）：本常量原先为 {differs: 12, not_verbatim: 11}，来源是用
# 【原始字节】比对得出的 23 例差异。实测该 23 例全部是 NBSP↔空格、弯引号↔ASCII、
# 换行折叠一类【归一化级】差异；经 canonical_quote（ADR-0005 / AC-F001-013）后
# 23/23 命中快照且与 source selector 相等——**真实坏引文为 0**。
# 因此基线改为 0：任何非零 actual 都意味着确实出现了引文不一致，报告会将其标为
# over_detected，应按回归失败处理。
KNOWN_BASELINE = {
    "differs_from_source_selector": 0,
    "not_verbatim_in_snapshot": 0,
}

CONTEXT_CHARS = 32


def _snapshot_path(root: Path, digest: str) -> Path:
    """按 content-addressed 命名定位 archive 快照。"""
    return root / "archive/text" / f"{digest.rsplit(':', maxsplit=1)[-1]}.md"


def _read_snapshot(root, digest, cache):
    """读取（并缓存）快照文本；返回 (text, error_code)。"""
    if digest in cache:
        return cache[digest]
    path = _snapshot_path(root, digest)
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        cache[digest] = (None, "snapshot_unresolved")
        return cache[digest]
    if sha256_text(text) != digest:
        cache[digest] = (text, "snapshot_sha256_mismatch")
        return cache[digest]
    cache[digest] = (text, None)
    return cache[digest]


def _index_sources(root):
    """建立 evidence_id → owner 反查表与 source 索引。

    返回 (evidence_owner, source_records)：
      evidence_owner: evidence_id → (source_id, source_path, evidence_item)
      source_records: source_id → (source_path, metadata)
    """
    evidence_owner = {}
    source_records = {}
    for path in sorted((root / "content/sources").rglob("*.md")):
        metadata, _ = FrontMatter.parse(path.read_text(encoding="utf-8"))
        source_id = str(metadata.get("id") or path.stem)
        source_records[source_id] = (path, metadata)
        for item in metadata.get("evidence_items") or []:
            evidence_id = item.get("evidence_id")
            if evidence_id:
                evidence_owner.setdefault(evidence_id, (source_id, path, item))
    return evidence_owner, source_records


def _failure(
    layer, object_id, object_path, claim_id, evidence_id, error_code, detail=None
):
    """构造统一形状的失败记录（含 object_id / claim_id / evidence_id / error_code）。"""
    record = {
        "layer": layer,
        "object_id": object_id,
        "object_path": object_path,
        "claim_id": claim_id,
        "evidence_id": evidence_id,
        "error_code": error_code,
    }
    if detail is not None:
        record["detail"] = detail
    return record


def _check_source_evidence(root, source_records, snapshot_cache):
    """检查 (b)(c)(e)：source evidence_items 的 selector 能否命中其声明快照，且哈希自证。"""
    failures = []
    checked = 0
    for source_id, (path, metadata) in source_records.items():
        items = metadata.get("evidence_items") or []
        if not items:
            continue
        rel = str(path.relative_to(root))
        for item in items:
            checked += 1
            evidence_id = item.get("evidence_id")
            selector = item.get("selector") or {}
            exact = selector.get("exact") if isinstance(selector, dict) else None
            digest = str(
                item.get("snapshot_sha256") or metadata.get("snapshot_sha256") or ""
            )
            text, snap_error = _read_snapshot(root, digest, snapshot_cache)
            if snap_error is not None:
                failures.append(
                    _failure("source", source_id, rel, None, evidence_id, snap_error)
                )
                continue
            if not isinstance(exact, str) or exact == "":
                failures.append(
                    _failure(
                        "source",
                        source_id,
                        rel,
                        None,
                        evidence_id,
                        "selector_exact_missing",
                    )
                )
                continue

            hits = [i for i in range(len(text)) if text.startswith(exact, i)]
            if not hits:
                failures.append(
                    _failure(
                        "source",
                        source_id,
                        rel,
                        None,
                        evidence_id,
                        "not_verbatim_in_snapshot",
                    )
                )
                continue
            if len(hits) > 1:
                failures.append(
                    _failure(
                        "source",
                        source_id,
                        rel,
                        None,
                        evidence_id,
                        "exact_ambiguous",
                        detail={"hit_count": len(hits), "first_start": hits[0]},
                    )
                )
                continue

            start = hits[0]
            end = start + len(exact)
            position = item.get("position") or {}
            if position.get("start") != start or position.get("end") != end:
                failures.append(
                    _failure(
                        "source",
                        source_id,
                        rel,
                        None,
                        evidence_id,
                        "position_mismatch",
                        detail={
                            "declared": [position.get("start"), position.get("end")],
                            "recomputed": [start, end],
                        },
                    )
                )
            if selector.get("prefix") != text[max(0, start - CONTEXT_CHARS) : start]:
                failures.append(
                    _failure(
                        "source", source_id, rel, None, evidence_id, "prefix_mismatch"
                    )
                )
            if selector.get("suffix") != text[end : end + CONTEXT_CHARS]:
                failures.append(
                    _failure(
                        "source", source_id, rel, None, evidence_id, "suffix_mismatch"
                    )
                )

            # (e) 哈希重算（抽出为独立函数以控制本函数复杂度）。
            failures.extend(
                _check_evidence_hashes(
                    source_id, rel, evidence_id, item, text, start, exact, digest
                )
            )
    return checked, failures


def _check_evidence_hashes(
    source_id, rel, evidence_id, item, text, start, exact, digest
):
    """检查 (e)：selector_sha256 / quote_sha256 必须与快照内容一致。

    公式与写入侧 ``tools/evidence_anchor.py:69-85`` 逐字相同，且 prefix/suffix 取
    【快照派生值】而非声明值——这样才能同时暴露"声明值被篡改"与"哈希被篡改"
    两种情形。2026-09-15 复核发现此前的实现从不重算哈希，故这两类篡改完全漏报。

    ``end`` 由 ``start + len(exact)`` 现算：它是冗余信息，单独传参会触发 PLR0913。
    """
    end = start + len(exact)
    failures = []
    recomputed_selector = hash_canonical(
        {
            "snapshot_sha256": digest,
            "start": start,
            "end": end,
            "exact": exact,
            "prefix": text[max(0, start - CONTEXT_CHARS) : start],
            "suffix": text[end : end + CONTEXT_CHARS],
        }
    )
    if item.get("selector_sha256") != recomputed_selector:
        failures.append(
            _failure(
                "source",
                source_id,
                rel,
                None,
                evidence_id,
                "selector_sha256_mismatch",
                detail={
                    "declared": item.get("selector_sha256"),
                    "recomputed": recomputed_selector,
                },
            )
        )
    recomputed_quote = sha256_text(canonical_quote(exact))
    if item.get("quote_sha256") != recomputed_quote:
        failures.append(
            _failure(
                "source",
                source_id,
                rel,
                None,
                evidence_id,
                "quote_sha256_mismatch",
                detail={
                    "declared": item.get("quote_sha256"),
                    "recomputed": recomputed_quote,
                },
            )
        )
    return failures


def _check_wiki_quotes(root, evidence_owner, snapshot_cache):
    """检查 (a)(d)(f)：wiki claim 的 supporting_quotes 能否解析并逐字命中快照。

    (f) 归属校验是同一 target 集合上的附加断言，因此不改变 ``components_checked``
    的分母口径。
    """
    failures = []
    quotes = claims = files = 0
    for path in sorted((root / "content/wiki").rglob("*.md")):
        metadata, _ = FrontMatter.parse(path.read_text(encoding="utf-8"))
        evidence = metadata.get("evidence") or []
        if not evidence:
            continue
        files += 1
        rel = str(path.relative_to(root))
        wiki_id = str(metadata.get("id") or path.stem)
        for claim in evidence:
            claims += 1
            claim_id = claim.get("claim_id")

            # (f) 归属校验：targets[].source_id 必须与 evidence_id 实际所属的 source 一致。
            # 不一致意味着 claim 挂着【别的 source 的】证据；而这种张冠李戴恰恰能
            # 通过其余全部校验（evidence_id 可解析、引文逐字命中、selector 一致），
            # 2026-09-15 复核实测为完全漏报面。
            for target in claim.get("targets") or []:
                target_eid = target.get("evidence_id")
                declared_source = target.get("source_id")
                owner_entry = evidence_owner.get(target_eid)
                if owner_entry is None:
                    failures.append(
                        _failure(
                            "wiki",
                            wiki_id,
                            rel,
                            claim_id,
                            target_eid,
                            "dangling_evidence_id",
                        )
                    )
                    continue
                actual_source = owner_entry[0]
                if declared_source != actual_source:
                    failures.append(
                        _failure(
                            "wiki",
                            wiki_id,
                            rel,
                            claim_id,
                            target_eid,
                            "target_source_mismatch",
                            detail={
                                "declared": declared_source,
                                "actual": actual_source,
                            },
                        )
                    )

            for quote in claim.get("supporting_quotes") or []:
                quotes += 1
                evidence_id = quote.get("evidence_id")
                exact = quote.get("exact")
                owner = evidence_owner.get(evidence_id)
                if owner is None:
                    failures.append(
                        _failure(
                            "wiki",
                            wiki_id,
                            rel,
                            claim_id,
                            evidence_id,
                            "dangling_evidence_id",
                        )
                    )
                    continue
                source_id, source_path, item = owner
                digest = str(item.get("snapshot_sha256") or "")
                text, snap_error = _read_snapshot(root, digest, snapshot_cache)
                if snap_error is not None:
                    failures.append(
                        _failure(
                            "wiki",
                            wiki_id,
                            rel,
                            claim_id,
                            evidence_id,
                            snap_error,
                            detail={
                                "source_id": source_id,
                                "source_path": str(source_path.relative_to(root)),
                            },
                        )
                    )
                    continue
                source_exact = (item.get("selector") or {}).get("exact")
                # 归一化比对：ADR-0005 / AC-F001-013 要求锚定工具与验证器共用
                # canonical_quote。原始字节比对会把 NBSP↔空格、弯引号↔ASCII、
                # 换行折叠一类归一化级差异误报为非一致（2026-09-15 实测全库 23 例）。
                if canonical_quote(exact) != canonical_quote(source_exact or ""):
                    failures.append(
                        _failure(
                            "wiki",
                            wiki_id,
                            rel,
                            claim_id,
                            evidence_id,
                            "differs_from_source_selector",
                            detail={
                                "source_id": source_id,
                                "source_path": str(source_path.relative_to(root)),
                            },
                        )
                    )
                if not isinstance(exact, str) or canonical_quote(
                    exact
                ) not in canonical_quote(text):
                    failures.append(
                        _failure(
                            "wiki",
                            wiki_id,
                            rel,
                            claim_id,
                            evidence_id,
                            "not_verbatim_in_snapshot",
                            detail={
                                "source_id": source_id,
                                "source_path": str(source_path.relative_to(root)),
                            },
                        )
                    )
    return files, claims, quotes, failures


def run(root):
    """执行全部检查，返回结构化报告。"""
    evidence_owner, source_records = _index_sources(root)
    snapshot_cache = {}

    source_checked, source_failures = _check_source_evidence(
        root, source_records, snapshot_cache
    )
    wiki_files, wiki_claims, wiki_quotes, wiki_failures = _check_wiki_quotes(
        root, evidence_owner, snapshot_cache
    )

    failures = source_failures + wiki_failures
    by_error_code = Counter(f["error_code"] for f in failures)
    by_layer = Counter(f["layer"] for f in failures)

    known_comparison = {}
    for code, expected in KNOWN_BASELINE.items():
        actual = by_error_code.get(code, 0)
        delta = actual - expected
        known_comparison[code] = {
            "expected": expected,
            "actual": actual,
            "delta": delta,
            "relation": "match"
            if delta == 0
            else ("over_detected" if delta > 0 else "under_detected"),
        }
    known_total = sum(KNOWN_BASELINE.values())
    actual_known_total = sum(by_error_code.get(code, 0) for code in KNOWN_BASELINE)
    known_comparison["_total"] = {
        "expected": known_total,
        "actual": actual_known_total,
        "delta": actual_known_total - known_total,
        "relation": "match"
        if actual_known_total == known_total
        else (
            "over_detected" if actual_known_total > known_total else "under_detected"
        ),
    }

    distinct = {
        (f["layer"], f["object_path"], f["claim_id"], f["evidence_id"])
        for f in failures
    }
    per_wiki = Counter(
        f["object_id"]
        for f in wiki_failures
        if f["error_code"] == "differs_from_source_selector"
    )

    return {
        "state": "clean" if not failures else "flagged",
        "totals": {
            "sources_with_evidence": sum(
                1 for _, (_, m) in source_records.items() if m.get("evidence_items")
            ),
            "source_evidence_items_checked": source_checked,
            "wiki_files_checked": wiki_files,
            "wiki_claims_checked": wiki_claims,
            "wiki_supporting_quotes_checked": wiki_quotes,
            "components_checked": source_checked + wiki_quotes,
            "exact_evidence_items_in_index": len(evidence_owner),
        },
        "failures_count": len(failures),
        "distinct_failing_objects": len(distinct),
        "by_error_code": dict(by_error_code.most_common()),
        "by_layer": dict(by_layer),
        "failing_wikis": dict(per_wiki.most_common()),
        "known_baseline_comparison": known_comparison,
        "failures": failures,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="引文可验证性回归检查器（只读，ADR-0019 硬门禁原型）"
    )
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--json-out", type=Path, help="把完整报告写到该路径")
    parser.add_argument(
        "--quiet", action="store_true", help="只输出汇总，不输出逐项失败清单"
    )
    args = parser.parse_args(argv)
    root = args.root.resolve()

    report = run(root)
    if args.quiet:
        report = {k: v for k, v in report.items() if k != "failures"}
    text = json.dumps(report, ensure_ascii=False, indent=2)
    print(text)
    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(text + "\n", encoding="utf-8")
    return 0 if report["state"] == "clean" else 2


if __name__ == "__main__":
    raise SystemExit(main())
