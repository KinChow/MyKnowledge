"""Evidence 锚定：在 source 快照中定位引文并生成 W3C selector 与 hash。

对应 AC-F001-011/012：偏移量按 Unicode code point 计算，selector 可复现，
锚定写入必须经 preview/apply 两阶段与 per-vault 写锁。
经统一入口调用：``python -m tools.cli anchor ...``
"""

from __future__ import annotations

import argparse
import json
import time
import uuid
from pathlib import Path

from .common import (
    atomic_write,
    canonical_quote,
    hash_canonical,
    injection_point,
    sha256_bytes,
    sha256_text,
)
from .front_matter import FrontMatter
from .operation_store import OperationStore
from .vault_lock import LockBusyError, VaultLock


class EvidenceAnchor:
    """Evidence 锚定服务：定位唯一引文、生成 selector/hash，并两阶段写回 source。"""

    def __init__(self, root: Path) -> None:
        self.root = root
        self.store = OperationStore(root)

    @staticmethod
    def anchor(snapshot: str, exact: str, min_chars: int = 12) -> dict:
        """在快照文本中定位唯一引文，生成 selector 与 hash。

        引文过短、未命中或多处命中时分别抛 ValueError（quote_too_short、
        selector_unresolved、ambiguous_selector），不做自动选取。
        """
        if len(canonical_quote(exact)) < min_chars:
            raise ValueError("quote_too_short")
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
        selector_hash = hash_canonical(
            {
                "snapshot_sha256": snapshot_hash,
                "start": start,
                "end": end,
                "exact": exact,
                "prefix": selector["prefix"],
                "suffix": selector["suffix"],
            }
        )
        return {
            "evidence_id": "evidence-" + uuid.uuid4().hex[:12],
            "snapshot_sha256": snapshot_hash,
            "selector": selector,
            "position": position,
            "selector_sha256": selector_hash,
            "quote_sha256": sha256_text(canonical_quote(exact)),
        }

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

    def preview(
        self,
        source_path: Path,
        snapshot_path: Path,
        exact: str,
        min_chars: int = 12,
    ) -> dict:
        """生成锚定操作（previewed）；source 快照引用与快照不匹配时抛 stale。"""
        source_bytes = source_path.read_bytes()
        snapshot = snapshot_path.read_text(encoding="utf-8")
        evidence = self.anchor(snapshot, exact, min_chars)
        metadata, _ = FrontMatter.parse(source_bytes.decode("utf-8"))
        if metadata.get("snapshot_sha256") != evidence["snapshot_sha256"]:
            raise ValueError("stale")
        operation = self.store.new(
            {
                "operation_type": "anchor_evidence",
                "target_vault": "public",
                "source_path": str(source_path.resolve()),
                "snapshot_path": str(snapshot_path.resolve()),
                "source_hash": sha256_bytes(source_bytes),
                "snapshot_sha256": evidence["snapshot_sha256"],
                "evidence": evidence,
            }
        )
        return {
            "state": "previewed",
            "operation_id": operation["operation_id"],
            "evidence": evidence,
        }

    def apply(
        self,
        operation_id: str,
        confirmed: bool = False,
        actor_id: str = "local-user",
    ) -> dict:
        """确认并执行锚定操作：TTL/状态在锁内复查，快照漂移返回 stale。"""
        record, preflight_error = self.store.apply_preflight(
            operation_id, "anchor_evidence", confirmed
        )
        if preflight_error is not None:
            return preflight_error
        try:
            with VaultLock(self.root, "public", operation_id):
                record, begin_error = self.store.begin_locked(operation_id)
                if begin_error is not None:
                    return begin_error
                source_path = Path(record["source_path"])
                snapshot_path = Path(record["snapshot_path"])
                try:
                    source_bytes = source_path.read_bytes()
                    snapshot_text = snapshot_path.read_text(encoding="utf-8")
                except (OSError, UnicodeError):
                    self.store.update(record, "expired", error_code="path_unresolved")
                    return {
                        "state": "expired",
                        "operation_id": operation_id,
                        "error_code": "path_unresolved",
                    }
                if sha256_text(snapshot_text) != record["snapshot_sha256"]:
                    self.store.update(record, "expired", error_code="stale")
                    return {
                        "state": "expired",
                        "operation_id": operation_id,
                        "error_code": "stale",
                    }
                if sha256_bytes(source_bytes) != record["source_hash"]:
                    # 崩溃恢复：evidence 可能已由本操作写入但 state 未提交——
                    # 若 front matter 已含 (snapshot_sha256, position) 则视为
                    # 已应用并继续补提交（apply_evidence 幂等返回既有 item），
                    # 否则按 hash_mismatch 过期
                    already_written = False
                    try:
                        existing_meta, _ = FrontMatter.parse(
                            source_path.read_text(encoding="utf-8")
                        )
                        position = record["evidence"].get("position")
                        already_written = any(
                            item.get("snapshot_sha256") == record["snapshot_sha256"]
                            and item.get("position") == position
                            for item in existing_meta.get("evidence_items", [])
                        )
                    except (OSError, ValueError, UnicodeError, AttributeError):
                        already_written = False
                    if not already_written:
                        self.store.update(record, "expired", error_code="hash_mismatch")
                        return {
                            "state": "expired",
                            "operation_id": operation_id,
                            "error_code": "hash_mismatch",
                        }
                try:
                    evidence = self.apply_evidence(source_path, record["evidence"])
                    injection_point("after_evidence")
                except ValueError as exc:
                    self.store.update(record, "expired", error_code=str(exc))
                    return {
                        "state": "expired",
                        "operation_id": operation_id,
                        "error_code": str(exc),
                    }
                except (OSError, UnicodeError):
                    # 写路径 I/O 失败（C002）：与 source_ingestor 对齐为结构化错误
                    self.store.update(record, "expired", error_code="apply_failed")
                    return {
                        "state": "expired",
                        "operation_id": operation_id,
                        "error_code": "apply_failed",
                    }
                injection_point("before_commit")
                try:
                    applied_file = str(
                        source_path.resolve().relative_to(self.root.resolve())
                    )
                except ValueError:
                    applied_file = str(source_path.resolve())
                confirmation = {
                    "actor_type": "human",
                    "actor_id": actor_id,
                    "scope": "apply",
                    "confirmed_at": time.time(),
                }
                self.store.update(
                    record,
                    "applied",
                    confirmation=confirmation,
                    applied_files=[applied_file],
                )
                return {
                    "state": "applied",
                    "operation_id": operation_id,
                    "evidence": evidence,
                }
        except LockBusyError:
            return VaultLock.lock_busy_response(operation_id)


def _batch_main(args: argparse.Namespace) -> int:
    """批量锚定（AC-F001-012 --from-jsonl）：不降低唯一性与长度标准，未解析行进 unresolved。"""
    anchor_service = EvidenceAnchor(args.root)
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
                result = anchor_service.preview(source, snapshot, exact, min_chars)
                report["ok"].append(
                    {
                        "line": line_no,
                        "operation_id": result["operation_id"],
                        "evidence_id": result["evidence"]["evidence_id"],
                    }
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
    """evidence_anchor CLI：预览/应用锚定操作（单条或 --from-jsonl 批量）。"""
    parser = argparse.ArgumentParser(description="Anchor evidence in a source snapshot")
    parser.add_argument("snapshot", type=Path, nargs="?")
    parser.add_argument("exact", nargs="?")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--min-chars", type=int, default=12)
    parser.add_argument("--apply", metavar="OPERATION_ID")
    parser.add_argument("--source", type=Path)
    parser.add_argument("--from-jsonl", type=Path, metavar="PATH")
    parser.add_argument(
        "--confirm",
        action="store_true",
        help="confirm the operation as the invoking human",
    )
    parser.add_argument("--actor-id", default="local-user")
    args = parser.parse_args(argv)
    anchor_service = EvidenceAnchor(args.root)
    if args.from_jsonl:
        return _batch_main(args)
    if args.apply:
        print(
            json.dumps(
                anchor_service.apply(
                    args.apply,
                    confirmed=args.confirm,
                    actor_id=args.actor_id,
                ),
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0
    if not args.snapshot or args.exact is None:
        parser.error("snapshot and exact are required for preview")
    try:
        if args.source:
            result = anchor_service.preview(
                args.source, args.snapshot, args.exact, args.min_chars
            )
        else:
            result = EvidenceAnchor.anchor(
                args.snapshot.read_text(encoding="utf-8"),
                args.exact,
                args.min_chars,
            )
    except ValueError as exc:
        print(json.dumps({"state": "blocked", "error_code": str(exc)}))
        return 2
    except OSError:
        print(json.dumps({"state": "blocked", "error_code": "path_unresolved"}))
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0
