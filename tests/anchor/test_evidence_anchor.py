"""F001 Evidence 锚定（anchor 域）。

锚定是幂等派生、直接落盘（ADR-0019），所以本文件只覆盖两类东西：
selector/hash 的**纯计算**契约（不落盘、不依赖任何服务）与**直接写 + 幂等**
的落盘契约。原先覆盖 preview/apply 两阶段、per-vault 锁、TTL、commit-intent
恢复与崩溃注入的用例已随审批外壳一并删除。
"""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from tools.common import sha256_text, strip_sha256_prefix
from tools.evidence_anchor import EvidenceAnchor
from tools.front_matter import FrontMatter
from tools.ingest.source_ingestor import SourceIngestor


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
        source_dir = root / "content" / "sources" / "tools" / source_id
        source_dir.mkdir(parents=True, exist_ok=True)
        service = SourceIngestor(root)
        applied = service.ingest(
            {
                "source_type": "personal-note",
                "domain": "tools",
                "origin": "personal",
                "body": body,
                "source_id": source_id,
            }
        )
        assert applied["state"] == "applied", applied
        snapshot_path = (
            root / "archive" / "text" / f"{strip_sha256_prefix(sha256_text(body))}.md"
        )
        return source_dir / f"{source_id}.md", snapshot_path

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


if __name__ == "__main__":
    unittest.main()
