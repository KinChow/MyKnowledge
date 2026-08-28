"""F001 F001 Evidence 锚定（anchor 域）。"""

from __future__ import annotations

import fcntl
import json
import os
import subprocess
import sys as _sys
import tempfile
import time
import unittest
from pathlib import Path

from tools.common import sha256_text, strip_sha256_prefix
from tools.evidence_anchor import EvidenceAnchor
from tools.front_matter import FrontMatter
from tools.ingest.source_ingestor import SourceIngestor
from tools.operation_store import OPERATION_TTL_SECONDS


class EvidenceAnchorTests(unittest.TestCase):
    def test_ambiguous_and_short_quotes(self):
        """AC-F001-012：短引文与歧义引文被拒绝。"""
        with self.assertRaisesRegex(ValueError, "ambiguous_selector"):
            EvidenceAnchor.anchor("重复内容，重复内容。", "重复内容", min_chars=2)
        with self.assertRaisesRegex(ValueError, "quote_too_short"):
            EvidenceAnchor.anchor("足够长的文本", "短", min_chars=2)

    def test_anchor_stale_on_snapshot_change(self):
        """AC-F001-012：snapshot 重抓后锚定返回 stale 而非 hash_mismatch。"""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            ingestor = SourceIngestor(root)
            body = "这是用于 stale 验证的足够长个人笔记正文内容。"
            result = ingestor.preview(
                {
                    "source_type": "personal-note",
                    "domain": "tools",
                    "origin": "personal",
                    "body": body,
                    "source_id": "stale-note",
                }
            )
            ingestor.apply(result["operation_id"], confirmed=True)
            source_path = root / "sources" / "tools" / "stale-note.md"
            snapshot_path = (
                root
                / "archive"
                / "text"
                / f"{strip_sha256_prefix(sha256_text(body))}.md"
            )
            anchor_service = EvidenceAnchor(root)
            evidence = anchor_service.preview(
                source_path, snapshot_path, "stale 验证", min_chars=6
            )
            snapshot_path.write_text("重新抓取后的新内容", encoding="utf-8")
            applied = anchor_service.apply(evidence["operation_id"], confirmed=True)
            self.assertEqual(applied["error_code"], "stale")

    def test_anchor_lock_busy_returns_structured(self):
        """并发锚定时 lock_busy 返回结构化错误而非 traceback。"""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            ingestor = SourceIngestor(root)
            body = "用于 lock_busy 验证的足够长个人笔记正文。"
            result = ingestor.preview(
                {
                    "source_type": "personal-note",
                    "domain": "tools",
                    "origin": "personal",
                    "body": body,
                    "source_id": "lockbusy-note",
                }
            )
            ingestor.apply(result["operation_id"], confirmed=True)
            source_path = root / "sources" / "tools" / "lockbusy-note.md"
            snapshot_path = (
                root
                / "archive"
                / "text"
                / f"{strip_sha256_prefix(sha256_text(body))}.md"
            )
            anchor_service = EvidenceAnchor(root)
            evidence = anchor_service.preview(
                source_path, snapshot_path, "lock_busy 验证", min_chars=6
            )
            # 本进程先 flock 持锁，模拟其他进程占用（flock 按 fd 互斥）
            lock_path = root / "state" / "locks" / "public.lock"
            lock_path.parent.mkdir(parents=True, exist_ok=True)
            with lock_path.open("a+b") as handle:
                fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                applied = anchor_service.apply(evidence["operation_id"], confirmed=True)
                self.assertEqual(applied.get("error_code"), "lock_busy")
            # 释放锁后重试成功
            applied = anchor_service.apply(evidence["operation_id"], confirmed=True)
            self.assertEqual(applied["state"], "applied")

    def test_anchor_evidence_ttl_expires(self):
        """锚定操作同样受 TTL 1800s 约束：超时后返回 operation_expired。"""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            ingestor = SourceIngestor(root)
            body = "这是用于 TTL 过期验证的足够长个人笔记正文内容。"
            result = ingestor.preview(
                {
                    "source_type": "personal-note",
                    "domain": "tools",
                    "origin": "personal",
                    "body": body,
                    "source_id": "ttl-note",
                }
            )
            ingestor.apply(result["operation_id"], confirmed=True)
            source_path = root / "sources" / "tools" / "ttl-note.md"
            snapshot_path = (
                root
                / "archive"
                / "text"
                / f"{strip_sha256_prefix(sha256_text(body))}.md"
            )
            anchor_service = EvidenceAnchor(root)
            evidence = anchor_service.preview(
                source_path, snapshot_path, "TTL 过期验证", min_chars=6
            )
            operation_path = (
                root / "state" / "operations" / f"{evidence['operation_id']}.json"
            )
            payload = json.loads(operation_path.read_text(encoding="utf-8"))
            payload["created_at"] = time.time() - (OPERATION_TTL_SECONDS + 1)
            operation_path.write_text(json.dumps(payload), encoding="utf-8")
            applied = anchor_service.apply(evidence["operation_id"], confirmed=True)
            self.assertEqual(applied["error_code"], "operation_expired")

    def test_anchor_selector_unresolved(self):
        """AC-F001-012：exact 未出现在 snapshot 中 → selector_unresolved。"""
        with self.assertRaisesRegex(ValueError, "selector_unresolved"):
            EvidenceAnchor.anchor("足够长的正文内容", "未出现的引文内容", min_chars=2)

    def test_anchor_repeat_idempotent(self):
        """AC-F001-012：重复锚定同一 (snapshot, position) 返回既有 evidence_id。"""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            ingestor = SourceIngestor(root)
            body = "这是用于幂等验证的足够长个人笔记正文内容。"
            result = ingestor.preview(
                {
                    "source_type": "personal-note",
                    "domain": "tools",
                    "origin": "personal",
                    "body": body,
                    "source_id": "idem-note",
                }
            )
            ingestor.apply(result["operation_id"], confirmed=True)
            source_path = root / "sources" / "tools" / "idem-note.md"
            snapshot_path = (
                root
                / "archive"
                / "text"
                / f"{strip_sha256_prefix(sha256_text(body))}.md"
            )
            anchor_service = EvidenceAnchor(root)
            first = anchor_service.apply(
                anchor_service.preview(
                    source_path, snapshot_path, "用于幂等验证的足够长", min_chars=6
                )["operation_id"],
                confirmed=True,
            )
            second = anchor_service.apply(
                anchor_service.preview(
                    source_path, snapshot_path, "用于幂等验证的足够长", min_chars=6
                )["operation_id"],
                confirmed=True,
            )
            self.assertEqual(second["state"], "applied")
            self.assertEqual(
                second["evidence"]["evidence_id"], first["evidence"]["evidence_id"]
            )

    def test_anchor_recovery_already_written(self):
        """R004 回归：evidence 已写入但 state 未提交 → 重放补提交 applied。"""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            ingestor = SourceIngestor(root)
            body = "这是用于锚定崩溃恢复验证的足够长个人笔记正文。"
            result = ingestor.preview(
                {
                    "source_type": "personal-note",
                    "domain": "tools",
                    "origin": "personal",
                    "body": body,
                    "source_id": "anchor-recover-note",
                }
            )
            ingestor.apply(result["operation_id"], confirmed=True)
            source_path = root / "sources" / "tools" / "anchor-recover-note.md"
            snapshot_path = (
                root
                / "archive"
                / "text"
                / f"{strip_sha256_prefix(sha256_text(body))}.md"
            )
            anchor_service = EvidenceAnchor(root)
            evidence = anchor_service.preview(
                source_path, snapshot_path, "崩溃恢复验证", min_chars=6
            )
            # 模拟崩溃点：evidence 已写入 source 但 state 未提交
            metadata, existing_body = FrontMatter.parse(
                source_path.read_text(encoding="utf-8")
            )
            metadata.setdefault("evidence_items", []).append(evidence["evidence"])
            source_path.write_text(
                FrontMatter.render(metadata, existing_body), encoding="utf-8"
            )
            applied = anchor_service.apply(evidence["operation_id"], confirmed=True)
            self.assertEqual(applied["state"], "applied")
            self.assertEqual(
                applied["evidence"]["evidence_id"], evidence["evidence"]["evidence_id"]
            )

    def test_crash_injection_anchor_apply(self):
        """锚定 apply 崩溃注入：写 evidence 后/提交前 kill -9，重放补提交 applied。"""

        repo_root = str(Path(__file__).resolve().parent.parent)
        script = (
            "import sys\n"
            "from pathlib import Path\n"
            "sys.path.insert(0, sys.argv[1])\n"
            "from tools.evidence_anchor import EvidenceAnchor\n"
            "r = EvidenceAnchor(Path(sys.argv[2])).apply(sys.argv[3], confirmed=True)\n"
            "print('APPLIED' if r.get('state') == 'applied' else r, file=sys.stderr)\n"
        )
        for point in ("after_evidence", "before_commit"):
            with self.subTest(point=point):
                with tempfile.TemporaryDirectory() as directory:
                    root = Path(directory)
                    ingestor = SourceIngestor(root)
                    body = "用于锚定崩溃注入验证的足够长个人笔记正文。"
                    source_id = f"anchor-crash-{point}".replace("_", "-")
                    result = ingestor.preview(
                        {
                            "source_type": "personal-note",
                            "domain": "tools",
                            "origin": "personal",
                            "body": body,
                            "source_id": source_id,
                        }
                    )
                    ingestor.apply(result["operation_id"], confirmed=True)
                    source_path = root / "sources" / "tools" / f"{source_id}.md"
                    snapshot_path = (
                        root
                        / "archive"
                        / "text"
                        / f"{strip_sha256_prefix(sha256_text(body))}.md"
                    )
                    evidence = EvidenceAnchor(root).preview(
                        source_path, snapshot_path, "崩溃注入验证", min_chars=6
                    )
                    proc = subprocess.run(
                        [
                            _sys.executable,
                            "-c",
                            script,
                            repo_root,
                            str(root),
                            evidence["operation_id"],
                        ],
                        env={**os.environ, "MYKNOWLEDGE_CRASH_AFTER": point},
                        capture_output=True,
                        text=True,
                    )
                    self.assertNotEqual(
                        proc.returncode, 0, f"{point}: 子进程未被 kill: {proc.stderr}"
                    )
                    replayed = EvidenceAnchor(root).apply(
                        evidence["operation_id"], confirmed=True
                    )
                    self.assertEqual(
                        replayed["state"],
                        "applied",
                        f"{point}: 重放失败: {proc.stderr}",
                    )
                    self.assertEqual(
                        replayed["evidence"]["evidence_id"],
                        evidence["evidence"]["evidence_id"],
                        f"{point}: 重放生成了新的 evidence_id",
                    )
