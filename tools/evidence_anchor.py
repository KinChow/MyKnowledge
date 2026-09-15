"""Evidence 锚定：在 source 快照中定位引文并生成 W3C selector 与 hash。

锚定是**幂等派生**，不是审批写操作（ADR-0019）：``anchor()`` 是纯计算，
``apply_evidence()`` 已实现幂等（同一 ``(snapshot_sha256, position)`` 返回既有
item），因此**直接落盘**——不经 preview/apply 两阶段、不需人工确认、不取写锁、
不写 operation 记录。

对应 AC-F001-011/012：偏移量按 Unicode code point 计算，selector 可复现。
经统一入口调用：``python -m tools.cli anchor ...``
"""

from __future__ import annotations

import argparse
import json
import re
import uuid
from pathlib import Path

from .common import (
    atomic_write,
    canonical_quote,
    sha256_text,
)
from .front_matter import FrontMatter


class EvidenceAnchor:
    """Evidence 锚定服务：定位唯一引文、生成 selector/hash，并幂等写回 source。"""

    @staticmethod
    def anchor(
        snapshot: str,
        exact: str,
        min_chars: int = 12,
        *,
        media_fragment: str | None = None,
    ) -> dict:
        """在快照文本中定位唯一引文，生成 selector 与 hash。

        引文过短、未命中或多处命中时分别抛 ValueError（quote_too_short、
        selector_unresolved、ambiguous_selector），不做自动选取。
        """
        if len(canonical_quote(exact)) < min_chars:
            raise ValueError("quote_too_short")
        if media_fragment is not None:
            EvidenceAnchor._validate_media_fragment(media_fragment)
        hits = [i for i in range(len(snapshot)) if snapshot.startswith(exact, i)]
        if not hits:
            raise ValueError("selector_unresolved")
        if len(hits) > 1:
            raise ValueError("ambiguous_selector")
        start = hits[0]
        end = start + len(exact)
        snapshot_hash = sha256_text(snapshot)
        selector = {
            "type": "TextQuoteSelector",
            "exact": exact,
            "prefix": snapshot[max(0, start - 32) : start],
            "suffix": snapshot[end : end + 32],
        }
        position = {"type": "TextPositionSelector", "start": start, "end": end}
        # ADR-0019 §5：`selector_sha256` / `quote_sha256` 是**校验值**而非指针——
        # 它们与同一记录里的 `selector` / `exact` 冗余（可由后者现算），因此不落盘。
        # 改 canonical 内容这件事由 git 提供篡改可见性，不需要记录内自带的指纹。
        evidence = {
            "evidence_id": "evidence-" + uuid.uuid4().hex[:12],
            "snapshot_sha256": snapshot_hash,
            "selector": selector,
            "position": position,
        }
        if media_fragment is not None:
            evidence["locator"] = {"media_fragment": media_fragment}
        return evidence

    @staticmethod
    def _validate_media_fragment(value: str) -> None:
        match = re.fullmatch(
            r"#t=(?P<start>\d+(?:\.\d+)?)(?:,(?P<end>\d+(?:\.\d+)?))?",
            value,
        )
        if not match:
            raise ValueError("media_fragment_invalid")
        if match.group("end") is not None and float(match.group("end")) < float(
            match.group("start")
        ):
            raise ValueError("media_fragment_invalid")

    @staticmethod
    def apply_evidence(source_path: Path, evidence: dict) -> dict:
        """将 evidence 写入 source front matter 的 evidence_items；漂移时抛 stale。

        同一 (snapshot_sha256, position) 已存在时返回既有 evidence item（幂等）。
        """
        metadata, body = FrontMatter.parse(source_path.read_text(encoding="utf-8"))
        if metadata.get("snapshot_sha256") != evidence["snapshot_sha256"]:
            raise ValueError("stale")
        items = metadata.setdefault("evidence_items", [])
        for item in items:
            if (
                item.get("snapshot_sha256") == evidence["snapshot_sha256"]
                and item.get("position") == evidence["position"]
            ):
                return item
        items.append(evidence)
        atomic_write(source_path, FrontMatter.render(metadata, body).encode("utf-8"))
        return evidence

    @staticmethod
    def anchor_evidence(
        source_path: Path,
        snapshot_path: Path,
        exact: str,
        min_chars: int = 12,
        media_fragment: str | None = None,
    ) -> dict:
        """锚定一条引文并直接写入 source（幂等）——取代原 preview→apply 两阶段。

        source 声明的 ``snapshot_sha256`` 与快照实际内容不符时抛
        ``ValueError("stale")``，不落盘。
        """
        snapshot = snapshot_path.read_text(encoding="utf-8")
        evidence = EvidenceAnchor.anchor(
            snapshot, exact, min_chars, media_fragment=media_fragment
        )
        metadata, _ = FrontMatter.parse(source_path.read_text(encoding="utf-8"))
        if metadata.get("snapshot_sha256") != evidence["snapshot_sha256"]:
            raise ValueError("stale")
        return EvidenceAnchor.apply_evidence(source_path, evidence)


def _batch_main(args: argparse.Namespace) -> int:
    """批量锚定（AC-F001-012 --from-jsonl）：不降低唯一性与长度标准，未解析行进 unresolved。"""
    report: dict[str, list[dict]] = {"ok": [], "unresolved": []}
    with args.from_jsonl.open(encoding="utf-8") as handle:
        for line_no, raw_line in enumerate(handle, 1):
            line = raw_line.strip()
            if not line:
                continue
            try:
                item = json.loads(line)
                source = Path(item["source"])
                snapshot = Path(item["snapshot"])
                exact = item["exact"]
                min_chars = int(item.get("min_chars", args.min_chars))
                if not source.is_absolute():
                    source = args.root / source
                if not snapshot.is_absolute():
                    snapshot = args.root / snapshot
                evidence = EvidenceAnchor.anchor_evidence(
                    source,
                    snapshot,
                    exact,
                    min_chars,
                    item.get("media_fragment"),
                )
                report["ok"].append(
                    {"line": line_no, "evidence_id": evidence["evidence_id"]}
                )
            except (
                ValueError,
                OSError,
                KeyError,
                TypeError,
                json.JSONDecodeError,
            ) as exc:
                report["unresolved"].append(
                    {
                        "line": line_no,
                        "error_code": (
                            str(exc)
                            if isinstance(exc, ValueError)
                            else type(exc).__name__
                        ),
                    }
                )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if not report["unresolved"] else 2


def main(argv: list[str] | None = None) -> int:
    """evidence_anchor CLI：定位引文并直接写入 source（单条或 --from-jsonl 批量）。

    不带 ``--source`` 时只做定位计算并打印 evidence（dry run，不落盘）。
    """
    parser = argparse.ArgumentParser(description="Anchor evidence in a source snapshot")
    parser.add_argument("snapshot", type=Path, nargs="?")
    parser.add_argument("exact", nargs="?")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--min-chars", type=int, default=12)
    parser.add_argument(
        "--media-fragment", help="W3C Media Fragments time range, e.g. #t=1450,1520"
    )
    parser.add_argument("--source", type=Path)
    parser.add_argument("--from-jsonl", type=Path, metavar="PATH")
    args = parser.parse_args(argv)
    if args.from_jsonl:
        return _batch_main(args)

    if not args.snapshot or args.exact is None:
        parser.error("snapshot and exact are required")
    try:
        if args.source:
            evidence = EvidenceAnchor.anchor_evidence(
                args.source,
                args.snapshot,
                args.exact,
                args.min_chars,
                args.media_fragment,
            )
            print(
                json.dumps(
                    {"state": "applied", "evidence": evidence},
                    ensure_ascii=False,
                    indent=2,
                )
            )
        else:
            evidence = EvidenceAnchor.anchor(
                args.snapshot.read_text(encoding="utf-8"),
                args.exact,
                args.min_chars,
                media_fragment=args.media_fragment,
            )
            print(json.dumps(evidence, ensure_ascii=False, indent=2))
    except ValueError as exc:
        print(json.dumps({"state": "blocked", "error_code": str(exc)}))
        return 2
    except OSError:
        print(json.dumps({"state": "blocked", "error_code": "path_unresolved"}))
        return 2
    return 0
