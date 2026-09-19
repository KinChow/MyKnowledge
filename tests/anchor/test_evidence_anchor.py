"""F001 Evidence 锚定（anchor 域）。

锚定是幂等派生、直接落盘（ADR-0019），所以本文件只覆盖两类东西：
selector/hash 的**纯计算**契约（不落盘、不依赖任何服务）与**直接写 + 幂等**
的落盘契约。原先覆盖 preview/apply 两阶段、per-vault 锁、TTL、commit-intent
恢复与崩溃注入的用例已随审批外壳一并删除。
"""

from __future__ import annotations

import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from tools import contract, evidence_anchor
from tools.common import sha256_text, strip_sha256_prefix
from tools.evidence_anchor import EvidenceAnchor
from tools.front_matter import FrontMatter
from tools.ingest.source_ingestor import SourceIngestor


def _run_main(argv: list[str]) -> tuple[int, dict]:
    """跑 CLI 入口，返回 (exit_code, 解析后的信封)。"""
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        code = evidence_anchor.main(argv)
    return code, json.loads(buffer.getvalue())


def _ingest_source(root: Path, source_id: str, body: str) -> tuple[Path, Path]:
    source_dir = root / "content" / "sources" / "tools" / source_id
    source_dir.mkdir(parents=True, exist_ok=True)
    applied = SourceIngestor(root).ingest(
        {
            "source_type": "personal-note",
            "domain": "tools",
            "origin": "personal",
            "body": body,
            "source_id": source_id,
        }
    )
    assert applied["status"] == "ok", applied
    snapshot_path = (
        root / "archive" / "text" / f"{strip_sha256_prefix(sha256_text(body))}.md"
    )
    return source_dir / f"{source_id}.md", snapshot_path


class AnchorComputationTests(unittest.TestCase):
    """纯计算：不落盘、不依赖服务。"""

    def test_media_fragment_is_locator_only(self):
        snapshot = "这是一个足够长的课程转录片段，用于测试时间定位。"
        exact = "课程转录片段，用于测试时间定位"
        plain = EvidenceAnchor.anchor(snapshot, exact, min_chars=6)
        media = EvidenceAnchor.anchor(
            snapshot, exact, min_chars=6, media_fragment="#t=1450,1520"
        )
        # ADR-0019 §5：校验值不落盘，改断言 selector/position 本身相同 ——
        # media_fragment 只进 locator，不得影响锚定结果。
        self.assertEqual(plain["selector"], media["selector"])
        self.assertEqual(plain["position"], media["position"])
        self.assertEqual(media["locator"], {"media_fragment": "#t=1450,1520"})

    def test_media_fragment_is_strictly_validated(self):
        with self.assertRaisesRegex(ValueError, "media_fragment_invalid"):
            EvidenceAnchor.anchor(
                "足够长的课程转录片段，用于测试时间定位。",
                "课程转录片段，用于测试时间定位",
                min_chars=6,
                media_fragment="#t=20,10",
            )

    def test_ambiguous_and_short_quotes(self):
        """AC-F001-012：短引文与歧义引文被拒绝。"""
        with self.assertRaisesRegex(ValueError, "ambiguous_selector"):
            EvidenceAnchor.anchor("重复内容，重复内容。", "重复内容", min_chars=2)
        with self.assertRaisesRegex(ValueError, "quote_too_short"):
            EvidenceAnchor.anchor("足够长的文本", "短", min_chars=2)

    def test_anchor_selector_unresolved(self):
        """AC-F001-012：exact 未出现在 snapshot 中 → selector_unresolved。"""
        with self.assertRaisesRegex(ValueError, "selector_unresolved"):
            EvidenceAnchor.anchor("足够长的正文内容", "未出现的引文内容", min_chars=2)

    def test_anchor_does_not_touch_disk(self):
        """纯计算不得产生任何文件副作用。"""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            EvidenceAnchor.anchor(
                "足够长的正文内容用于计算", "足够长的正文", min_chars=4
            )
            self.assertEqual(list(root.iterdir()), [])


class AnchorDirectWriteTests(unittest.TestCase):
    """直接写 + 幂等：取代原 preview→apply 两阶段。"""

    def _ingest(self, root: Path, source_id: str, body: str) -> tuple[Path, Path]:
        return _ingest_source(root, source_id, body)

    def test_anchor_evidence_writes_directly_without_operation_record(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            body = "这是用于直接写验证的足够长个人笔记正文内容。"
            source_path, snapshot_path = self._ingest(root, "direct-note", body)
            evidence = EvidenceAnchor.anchor_evidence(
                source_path, snapshot_path, "足够长个人笔记正文", min_chars=6
            )
            self.assertTrue(evidence["evidence_id"].startswith("evidence-"))
            stored, _ = FrontMatter.parse(source_path.read_text(encoding="utf-8"))
            self.assertEqual(
                [item["evidence_id"] for item in stored["evidence_items"]],
                [evidence["evidence_id"]],
            )
            # 直接写：不产生 operation 记录（审批外壳已退场）
            self.assertEqual(list((root / "state").glob("operations/*"))[:1], [])

    def test_anchor_evidence_is_idempotent(self):
        """AC-F001-012：重复锚定同一 (snapshot, position) 返回既有 evidence_id。"""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            body = "这是用于幂等验证的足够长个人笔记正文内容。"
            source_path, snapshot_path = self._ingest(root, "idem-note", body)
            first = EvidenceAnchor.anchor_evidence(
                source_path, snapshot_path, "足够长个人笔记正文", min_chars=6
            )
            second = EvidenceAnchor.anchor_evidence(
                source_path, snapshot_path, "足够长个人笔记正文", min_chars=6
            )
            self.assertEqual(second["evidence_id"], first["evidence_id"])
            stored, _ = FrontMatter.parse(source_path.read_text(encoding="utf-8"))
            self.assertEqual(len(stored["evidence_items"]), 1)

    def test_anchor_evidence_stale_when_snapshot_mismatches_source(self):
        """快照内容与 source 声明的 snapshot_sha256 不符 → stale，且不落盘。"""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            body = "这是用于 stale 验证的足够长个人笔记正文内容。"
            source_path, snapshot_path = self._ingest(root, "stale-note", body)
            before = source_path.read_bytes()
            # 快照被换掉：引文仍在（anchor 能定位），但 hash 已不同
            snapshot_path.write_text(
                body + "\n追加一行，使快照 hash 与 source 声明不符。\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "stale"):
                EvidenceAnchor.anchor_evidence(
                    source_path, snapshot_path, "足够长个人笔记正文", min_chars=6
                )
            self.assertEqual(source_path.read_bytes(), before)


class MainEnvelopeTests(unittest.TestCase):
    """CLI 入口 main()/_batch_main() 归一到 tools.contract 单一 status 轴（无并列 state）。"""

    def test_dry_run_returns_ok_envelope_without_write(self):
        with tempfile.TemporaryDirectory() as directory:
            snapshot = Path(directory) / "snap.md"
            snapshot.write_text("足够长的正文内容用于纯定位计算。", encoding="utf-8")
            code, envelope = _run_main(
                [str(snapshot), "足够长的正文内容", "--min-chars", "6"]
            )
            self.assertEqual(code, 0)
            self.assertEqual(envelope["schema_version"], "evidence-anchor/v1")
            self.assertEqual(envelope["status"], "ok")
            self.assertFalse(envelope["applied"])
            self.assertTrue(envelope["evidence"]["evidence_id"].startswith("evidence-"))
            self.assertNotIn("state", envelope)

    def test_source_write_returns_ok_applied_envelope(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            body = "这是用于 CLI 直接写验证的足够长个人笔记正文内容。"
            source_path, snapshot_path = _ingest_source(root, "cli-note", body)
            code, envelope = _run_main(
                [
                    str(snapshot_path),
                    "足够长个人笔记正文",
                    "--source",
                    str(source_path),
                    "--min-chars",
                    "6",
                ]
            )
            self.assertEqual(code, 0)
            self.assertEqual(envelope["status"], "ok")
            self.assertTrue(envelope["applied"])
            evidence_id = envelope["evidence"]["evidence_id"]
            stored, _ = FrontMatter.parse(source_path.read_text(encoding="utf-8"))
            self.assertIn(
                evidence_id, [item["evidence_id"] for item in stored["evidence_items"]]
            )
            self.assertNotIn("state", envelope)

    def test_validation_failure_returns_blocked_registered_code(self):
        with tempfile.TemporaryDirectory() as directory:
            snapshot = Path(directory) / "snap.md"
            snapshot.write_text("足够长的正文内容用于校验失败测试。", encoding="utf-8")
            code, envelope = _run_main([str(snapshot), "短", "--min-chars", "12"])
            self.assertEqual(code, 2)
            self.assertEqual(envelope["status"], "blocked")
            self.assertEqual(envelope["error_code"], "quote_too_short")
            self.assertIn(envelope["error_code"], contract.ERROR_CODES)
            self.assertNotIn("state", envelope)

    def test_unresolved_selector_returns_blocked(self):
        with tempfile.TemporaryDirectory() as directory:
            snapshot = Path(directory) / "snap.md"
            snapshot.write_text("足够长的正文内容。", encoding="utf-8")
            code, envelope = _run_main(
                [str(snapshot), "未出现的引文内容", "--min-chars", "6"]
            )
            self.assertEqual(code, 2)
            self.assertEqual(envelope["status"], "blocked")
            self.assertEqual(envelope["error_code"], "selector_unresolved")

    def test_missing_path_returns_blocked_path_unresolved(self):
        with tempfile.TemporaryDirectory() as directory:
            missing = Path(directory) / "nope.md"
            code, envelope = _run_main(
                [str(missing), "任意引文内容", "--min-chars", "6"]
            )
            self.assertEqual(code, 2)
            self.assertEqual(envelope["status"], "blocked")
            self.assertEqual(envelope["error_code"], "path_unresolved")

    def test_batch_all_resolved_returns_ok(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            body = "这是用于批量锚定验证的足够长个人笔记正文内容。"
            source_path, snapshot_path = _ingest_source(root, "batch-ok", body)
            jsonl = root / "batch.jsonl"
            jsonl.write_text(
                json.dumps(
                    {
                        "source": str(source_path),
                        "snapshot": str(snapshot_path),
                        "exact": "足够长个人笔记正文",
                        "min_chars": 6,
                    },
                    ensure_ascii=False,
                )
                + "\n",
                encoding="utf-8",
            )
            code, envelope = _run_main(
                ["--from-jsonl", str(jsonl), "--root", str(root)]
            )
            self.assertEqual(code, 0)
            self.assertEqual(envelope["schema_version"], "evidence-anchor-batch/v1")
            self.assertEqual(envelope["status"], "ok")
            self.assertEqual(len(envelope["resolved"]), 1)
            self.assertEqual(envelope["unresolved"], [])

    def test_batch_partial_failure_returns_blocked_umbrella(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            body = "这是用于批量部分失败验证的足够长个人笔记正文内容。"
            source_path, snapshot_path = _ingest_source(root, "batch-mixed", body)
            good = json.dumps(
                {
                    "source": str(source_path),
                    "snapshot": str(snapshot_path),
                    "exact": "足够长个人笔记正文",
                    "min_chars": 6,
                },
                ensure_ascii=False,
            )
            # 缺 exact 字段 → KeyError，其类名是动态/明细码，不在统一词表。
            bad = json.dumps(
                {"source": str(source_path), "snapshot": str(snapshot_path)},
                ensure_ascii=False,
            )
            jsonl = root / "batch.jsonl"
            jsonl.write_text(good + "\n" + bad + "\n", encoding="utf-8")
            code, envelope = _run_main(
                ["--from-jsonl", str(jsonl), "--root", str(root)]
            )
            self.assertEqual(code, 2)
            self.assertEqual(envelope["status"], "blocked")
            self.assertEqual(envelope["error_code"], "anchor_batch_unresolved")
            self.assertEqual(len(envelope["resolved"]), 1)
            self.assertEqual(len(envelope["unresolved"]), 1)
            # 每行动态/明细码（此处异常类名）留在 payload，不进词表。
            self.assertEqual(envelope["unresolved"][0]["error_code"], "KeyError")
            self.assertNotIn(
                envelope["unresolved"][0]["error_code"], contract.ERROR_CODES
            )


class AnchorCodeRegistrationTests(unittest.TestCase):
    """本模块 blocked 顶层码必须登记进单一词表（fail-closed 前提）。"""

    def test_anchor_codes_registered(self):
        expected = {
            "quote_too_short",
            "selector_unresolved",
            "ambiguous_selector",
            "media_fragment_invalid",
            "stale",
            "path_unresolved",
            "anchor_batch_unresolved",
        }
        self.assertTrue(expected <= contract.ERROR_CODES)


if __name__ == "__main__":
    unittest.main()
