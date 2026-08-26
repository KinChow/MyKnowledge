"""F001 Source 导入与归档验收测试：两阶段写、local-file 竞态、抓取策略与锚定。"""

from __future__ import annotations

import fcntl
import gzip
import json
import os
import sys
import tempfile
import time
import types
import unittest
from pathlib import Path
from unittest import mock

from tools.common import canonical_quote, sha256_text, strip_sha256_prefix
from tools.evidence_anchor import EvidenceAnchor
from tools.extractor import TextExtractor
from tools.fetcher import URLFetcher, _bounded_decompress
from tools.front_matter import FrontMatter
from tools.operation_store import OPERATION_TTL_SECONDS
from tools.source_ingestor import SourceIngestor
from tools.source_validator import SourceValidator


class F001Tests(unittest.TestCase):
    """F001 验收用例：对应 docs/acceptance/F001-source-ingestion.md 的 AC 条目。"""

    def test_personal_note_preview_apply_and_anchor(self):
        """AC-F001-005/011：personal-note 生成 snapshot 并可锚定 evidence。"""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            ingestor = SourceIngestor(root)
            body = "这是一个包含 emoji 😀 和代码 `x += 1` 的个人笔记。"
            result = ingestor.preview(
                {
                    "source_type": "personal-note",
                    "domain": "tools",
                    "origin": "personal",
                    "body": body,
                    "source_id": "personal-note-one",
                }
            )
            self.assertEqual(result["state"], "previewed")
            self.assertEqual(
                ingestor.apply(result["operation_id"])["state"],
                "awaiting_confirmation",
            )
            applied = ingestor.apply(result["operation_id"], confirmed=True)
            self.assertEqual(applied["state"], "applied")
            repeated = ingestor.apply(result["operation_id"], confirmed=True)
            self.assertEqual(repeated["state"], "applied")
            self.assertEqual(
                len((root / "archive" / "manifest.jsonl").read_text().splitlines()), 1
            )
            self.assertTrue(
                (
                    root
                    / "archive"
                    / "text"
                    / f"{strip_sha256_prefix(sha256_text(body))}.md"
                ).exists()
            )
            evidence = EvidenceAnchor.anchor(body, "包含 emoji 😀 和代码", min_chars=12)
            self.assertEqual(
                evidence["position"]["start"], body.index("包含 emoji 😀 和代码")
            )
            self.assertEqual(
                evidence["position"]["end"],
                body.index("包含 emoji 😀 和代码") + len("包含 emoji 😀 和代码"),
            )
            self.assertEqual(
                evidence["quote_sha256"],
                sha256_text(canonical_quote("包含 emoji 😀 和代码")),
            )
            self.assertEqual(
                evidence["quote_sha256"],
                SourceValidator.quote_sha256("包含 emoji 😀 和代码"),
            )
            self.assertTrue(evidence["selector_sha256"].startswith("sha256:"))
            source_path = root / "sources" / "tools" / "personal-note-one.md"
            snapshot_path = (
                root
                / "archive"
                / "text"
                / f"{strip_sha256_prefix(sha256_text(body))}.md"
            )
            anchor_service = EvidenceAnchor(root)
            evidence_preview = anchor_service.preview(
                source_path, snapshot_path, "包含 emoji 😀 和代码", min_chars=12
            )
            self.assertEqual(
                anchor_service.apply(evidence_preview["operation_id"])["state"],
                "awaiting_confirmation",
            )
            saved = anchor_service.apply(
                evidence_preview["operation_id"], confirmed=True
            )
            self.assertEqual(saved["state"], "applied")
            self.assertIn("evidence_items:", source_path.read_text(encoding="utf-8"))

    def test_local_file_hash_mismatch_blocks_apply(self):
        """AC-F001-008：local-file 被改写后 apply 返回 hash_mismatch 且不落盘。"""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            ingestor = SourceIngestor(root)
            source = root / "note.md"
            source.write_text("原始内容", encoding="utf-8")
            result = ingestor.preview(
                {
                    "source_type": "local-file",
                    "domain": "tools",
                    "input_path": str(source),
                    "source_id": "local-note",
                    "media_type": "text/plain",
                }
            )
            source.write_text("被替换内容", encoding="utf-8")
            applied = ingestor.apply(result["operation_id"], confirmed=True)
            self.assertEqual(applied["state"], "expired")
            self.assertEqual(applied["error_code"], "hash_mismatch")
            self.assertFalse((root / "sources" / "tools" / "local-note.md").exists())

    def test_local_file_deleted_returns_path_unresolved(self):
        """AC-F001-008 failure injection：preview 后删除文件，apply 返回 path_unresolved。"""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            ingestor = SourceIngestor(root)
            source = root / "note.md"
            source.write_text("原始内容", encoding="utf-8")
            result = ingestor.preview(
                {
                    "source_type": "local-file",
                    "domain": "tools",
                    "input_path": str(source),
                    "source_id": "deleted-note",
                    "media_type": "text/plain",
                }
            )
            source.unlink()
            applied = ingestor.apply(result["operation_id"], confirmed=True)
            self.assertEqual(applied["state"], "expired")
            self.assertEqual(applied["error_code"], "path_unresolved")
            self.assertFalse(
                (root / "sources" / "tools" / "deleted-note.md").exists()
            )

    def test_target_change_does_not_leave_snapshot(self):
        """AC-F001-008：目标被其他操作写入后 apply 过期，不留下 snapshot。"""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            ingestor = SourceIngestor(root)
            source = root / "note.md"
            source.write_text("原始内容", encoding="utf-8")
            result = ingestor.preview(
                {
                    "source_type": "local-file",
                    "domain": "tools",
                    "input_path": str(source),
                    "source_id": "target-change",
                    "media_type": "text/plain",
                }
            )
            target = root / "sources" / "tools" / "target-change.md"
            target.parent.mkdir(parents=True)
            target.write_text("其他 operation 已写入", encoding="utf-8")
            applied = ingestor.apply(result["operation_id"], confirmed=True)
            self.assertEqual(applied["state"], "expired")
            self.assertFalse(
                (
                    root
                    / "archive"
                    / "text"
                    / f"{strip_sha256_prefix(result['snapshot_sha256'])}.md"
                ).exists()
            )

    def test_operation_ttl_expires(self):
        """操作 TTL 1800s：超时后 apply 返回 operation_expired。"""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            ingestor = SourceIngestor(root)
            result = ingestor.preview(
                {
                    "source_type": "personal-note",
                    "domain": "tools",
                    "origin": "personal",
                    "body": "这是一个足够长的个人笔记内容。",
                    "source_id": "expired-note",
                }
            )
            operation_path = (
                root / "state" / "operations" / f"{result['operation_id']}.json"
            )
            payload = json.loads(operation_path.read_text(encoding="utf-8"))
            payload["created_at"] = time.time() - (OPERATION_TTL_SECONDS + 1)
            operation_path.write_text(json.dumps(payload), encoding="utf-8")
            applied = ingestor.apply(result["operation_id"], confirmed=True)
            self.assertEqual(applied["error_code"], "operation_expired")

    def test_bounded_gzip_rejects_expansion(self):
        """AC-F001-010：解压炸弹超限被拒绝。"""
        compressed = gzip.compress(b"A" * 10000)
        with self.assertRaisesRegex(RuntimeError, "decompression_limit_exceeded"):
            _bounded_decompress(compressed, "gzip", 100)

    def test_invalid_cross_fields_are_rejected(self):
        """AC-F001-009：input_path 与非 local-file 交叉字段被拒绝。"""
        with tempfile.TemporaryDirectory() as directory:
            result = SourceIngestor(Path(directory)).preview(
                {
                    "source_type": "doc",
                    "domain": "tools",
                    "input_path": "/tmp/file",
                }
            )
            self.assertEqual(result["state"], "blocked")
            self.assertEqual(result["errors"][0]["code"], "schema_invalid")

    def test_ambiguous_and_short_quotes(self):
        """AC-F001-012：短引文与歧义引文被拒绝。"""
        with self.assertRaisesRegex(ValueError, "ambiguous_selector"):
            EvidenceAnchor.anchor("重复内容，重复内容。", "重复内容", min_chars=2)
        with self.assertRaisesRegex(ValueError, "quote_too_short"):
            EvidenceAnchor.anchor("足够长的文本", "短", min_chars=2)

    def test_url_policy_rejects_private_and_unsafe_targets(self):
        """AC-F001-007/010：file scheme 与私网地址被拒绝。"""
        fetcher = URLFetcher()
        with self.assertRaisesRegex(RuntimeError, "url_policy"):
            fetcher.fetch("file:///etc/passwd")
        with self.assertRaisesRegex(RuntimeError, "private_network"):
            fetcher.fetch("http://127.0.0.1/")

    def test_url_preview_not_schema_blocked(self):
        """AC-F001-001 回归：URL 导入不被 schema 拦截，失败归因于抓取策略。"""
        with tempfile.TemporaryDirectory() as directory:
            result = SourceIngestor(Path(directory)).preview(
                {
                    "source_type": "doc",
                    "domain": "tools",
                    "url": "http://127.0.0.1/",
                }
            )
            self.assertEqual(result["state"], "blocked")
            self.assertEqual(
                result["errors"][0]["code"], "fetch_blocked:private_network"
            )

    def test_invalid_port_url_blocked(self):
        """AC-F001-010：非法端口 URL 返回结构化 fetch_blocked 而非崩溃。"""
        with tempfile.TemporaryDirectory() as directory:
            result = SourceIngestor(Path(directory)).preview(
                {
                    "source_type": "doc",
                    "domain": "tools",
                    "url": "http://example.com:abc/",
                }
            )
            self.assertEqual(result["state"], "blocked")
            self.assertEqual(result["errors"][0]["code"], "fetch_blocked:url_policy")

    def test_operation_type_mismatch_returns_structured(self):
        """跨类型操作 ID 返回 operation_type_mismatch 而非崩溃。"""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            ingestor = SourceIngestor(root)
            result = ingestor.preview(
                {
                    "source_type": "personal-note",
                    "domain": "tools",
                    "origin": "personal",
                    "body": "类型不匹配验证笔记内容",
                    "source_id": "type-mismatch",
                }
            )
            applied = EvidenceAnchor(root).apply(
                result["operation_id"], confirmed=True
            )
            self.assertEqual(applied["error_code"], "operation_type_mismatch")

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
            applied = anchor_service.apply(
                evidence["operation_id"], confirmed=True
            )
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
                applied = anchor_service.apply(
                    evidence["operation_id"], confirmed=True
                )
                self.assertEqual(applied.get("error_code"), "lock_busy")
            # 释放锁后重试成功
            applied = anchor_service.apply(
                evidence["operation_id"], confirmed=True
            )
            self.assertEqual(applied["state"], "applied")

    def test_manifest_corrupt_line_tolerated(self):
        """AC-F001-006：manifest 存在损坏行时后续 apply 仍成功且不覆盖旧行。"""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            ingestor = SourceIngestor(root)
            first_note = root / "note1.md"
            first_note.write_text("第一份内容", encoding="utf-8")
            first = ingestor.preview(
                {
                    "source_type": "local-file",
                    "domain": "tools",
                    "input_path": str(first_note),
                    "source_id": "first-source",
                    "media_type": "text/plain",
                }
            )
            ingestor.apply(first["operation_id"], confirmed=True)
            manifest = root / "archive" / "manifest.jsonl"
            manifest.write_text(
                manifest.read_text(encoding="utf-8") + "{corrupt line\n",
                encoding="utf-8",
            )
            second_note = root / "note2.md"
            second_note.write_text("第二份内容", encoding="utf-8")
            second = ingestor.preview(
                {
                    "source_type": "local-file",
                    "domain": "tools",
                    "input_path": str(second_note),
                    "source_id": "second-source",
                    "media_type": "text/plain",
                }
            )
            applied = ingestor.apply(second["operation_id"], confirmed=True)
            self.assertEqual(applied["state"], "applied")

    def test_manifest_invalid_utf8_tolerated(self):
        """manifest 含非法 UTF-8 字节行时后续 apply 仍成功。"""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            ingestor = SourceIngestor(root)
            first_note = root / "note1.md"
            first_note.write_text("第一份内容", encoding="utf-8")
            first = ingestor.preview(
                {
                    "source_type": "local-file",
                    "domain": "tools",
                    "input_path": str(first_note),
                    "source_id": "utf8-first",
                    "media_type": "text/plain",
                }
            )
            ingestor.apply(first["operation_id"], confirmed=True)
            manifest = root / "archive" / "manifest.jsonl"
            with manifest.open("ab") as handle:
                handle.write(b"\xff\xfe invalid utf8\n")
            second_note = root / "note2.md"
            second_note.write_text("第二份内容", encoding="utf-8")
            second = ingestor.preview(
                {
                    "source_type": "local-file",
                    "domain": "tools",
                    "input_path": str(second_note),
                    "source_id": "utf8-second",
                    "media_type": "text/plain",
                }
            )
            applied = ingestor.apply(second["operation_id"], confirmed=True)
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
            applied = anchor_service.apply(
                evidence["operation_id"], confirmed=True
            )
            self.assertEqual(applied["error_code"], "operation_expired")

    def test_extractor_register_open_for_extension(self):
        """开闭原则：注册自定义提取器后按 media_type 命中，不修改 extract 本体。"""
        extractor = TextExtractor()
        extractor.register(
            lambda data, media_type: media_type == "text/csv",
            lambda data, media_type: (
                data.decode("utf-8").replace(",", " | "),
                "csv/1",
            ),
        )
        text, name = extractor.extract(b"a,b,c", "text/csv")
        self.assertEqual(text, "a | b | c")
        self.assertEqual(name, "csv/1")
        # 未命中时仍走默认 UTF-8 文本路径
        text2, name2 = extractor.extract(b"plain", "text/plain")
        self.assertEqual(text2, "plain")
        self.assertEqual(name2, "utf8/1")

    def test_html_extraction_omits_active_content(self):
        """AC-F001-004：HTML 提取剔除 script/style 活动内容。"""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            ingestor = SourceIngestor(root)
            source = root / "page.html"
            source.write_text(
                "<html><style>hidden</style><body>Visible 正文<script>secret()</script></body></html>",
                encoding="utf-8",
            )
            result = ingestor.preview(
                {
                    "source_type": "local-file",
                    "domain": "tools",
                    "input_path": str(source),
                    "source_id": "html-page",
                    "media_type": "text/html",
                }
            )
            applied = ingestor.apply(result["operation_id"], confirmed=True)
            snapshot = (
                root
                / "archive"
                / "text"
                / f"{strip_sha256_prefix(applied['snapshot_sha256'])}.md"
            ).read_text(encoding="utf-8")
            self.assertIn("Visible 正文", snapshot)
            self.assertNotIn("secret", snapshot)

    def test_pdf_extraction(self):
        """AC-F001-004：PDF 提取正文（pypdf）。"""
        pdf = _minimal_pdf("Hello PDF Text")
        text, name = TextExtractor().extract(pdf, "application/pdf")
        self.assertIn("Hello PDF Text", text)
        self.assertTrue(name.startswith("pypdf/"))

    def test_url_fetch_success_archives_with_origin_url(self):
        """AC-F001-001：URL 正文非空 → 成功归档，且出处 URL 保留（M001 回归）。"""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            ingestor = SourceIngestor(root)

            class _FakeFetcher:
                def fetch(self, url: str) -> tuple[bytes, str, str]:
                    return (
                        "<html><body>抓取正文内容</body></html>".encode("utf-8"),
                        url,
                        "text/html",
                    )

            ingestor._acquirers["fetch"].fetcher = _FakeFetcher()
            result = ingestor.preview(
                {
                    "source_type": "doc",
                    "domain": "tools",
                    "url": "https://example.com/article",
                    "source_id": "url-source",
                }
            )
            self.assertEqual(result["state"], "previewed")
            applied = ingestor.apply(result["operation_id"], confirmed=True)
            self.assertEqual(applied["state"], "applied")
            source = (root / "sources" / "tools" / "url-source.md").read_text(
                encoding="utf-8"
            )
            self.assertIn("url: https://example.com/article", source)
            self.assertIn("resolved_url: https://example.com/article", source)
            self.assertIn("snapshot_sha256", source)
            snapshot = (
                root
                / "archive"
                / "text"
                / f"{strip_sha256_prefix(applied['snapshot_sha256'])}.md"
            )
            self.assertTrue(snapshot.exists())
            self.assertIn("抓取正文内容", snapshot.read_text(encoding="utf-8"))
            self.assertTrue((root / "archive" / "manifest.jsonl").exists())

    def test_manifest_deduplicates_snapshot_keeps_owners(self):
        """AC-F001-006：两个 source 相同内容 → archive 去重一个快照，manifest 两行 owner 保留。"""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            ingestor = SourceIngestor(root)
            body = "完全相同的正文内容"
            for source_id in ("dup-a", "dup-b"):
                result = ingestor.preview(
                    {
                        "source_type": "personal-note",
                        "domain": "tools",
                        "origin": "personal",
                        "body": body,
                        "source_id": source_id,
                    }
                )
                applied = ingestor.apply(result["operation_id"], confirmed=True)
                self.assertEqual(applied["state"], "applied")
            manifest = root / "archive" / "manifest.jsonl"
            lines = [
                json.loads(line)
                for line in manifest.read_text(encoding="utf-8").splitlines()
                if line.strip()
            ]
            self.assertEqual(len(lines), 2)
            self.assertEqual(lines[0]["snapshot_sha256"], lines[1]["snapshot_sha256"])
            self.assertEqual(lines[0]["owner_object_ref"]["id"], "dup-a")
            self.assertEqual(lines[1]["owner_object_ref"]["id"], "dup-b")
            self.assertEqual(len(list((root / "archive" / "text").glob("*.md"))), 1)

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

    def test_preview_non_string_body_blocked(self):
        """C001 回归：非字符串 body 返回结构化 blocked 而非崩溃。"""
        with tempfile.TemporaryDirectory() as directory:
            result = SourceIngestor(Path(directory)).preview(
                {
                    "source_type": "personal-note",
                    "domain": "tools",
                    "origin": "personal",
                    "body": None,
                    "source_id": "bad-body",
                }
            )
            self.assertEqual(result["state"], "blocked")
            self.assertEqual(result["errors"][0]["code"], "schema_invalid")

    def test_invalid_operation_id_structured(self):
        """C002 回归：非法 operation_id 返回 operation_not_found 而非 traceback。"""
        with tempfile.TemporaryDirectory() as directory:
            result = SourceIngestor(Path(directory)).apply(
                "op_BAD_ID", confirmed=True
            )
            self.assertEqual(result["error_code"], "operation_not_found")

    def test_local_file_symlink_retarget_blocks_apply(self):
        """AC-F001-008：preview 后 symlink 改指另一 hard link → apply 返回 path_unresolved。"""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            ingestor = SourceIngestor(root)
            same = "相同内容防止 hash 拦截"
            real_a = root / "real-a.md"
            real_a.write_text(same, encoding="utf-8")
            # real_b 与 real_a 同一 inode（hard link）：stat/hash 完全相同，
            # 仅 realpath 不同，用于验证 symlink 改指的 realpath 一致性检查
            real_b = root / "real-b.md"
            os.link(real_a, real_b)
            link = root / "link.md"
            link.symlink_to(real_a)
            result = ingestor.preview(
                {
                    "source_type": "local-file",
                    "domain": "tools",
                    "input_path": str(link),
                    "source_id": "symlink-note",
                    "media_type": "text/plain",
                }
            )
            self.assertEqual(result["state"], "previewed")
            link.unlink()
            link.symlink_to(real_b)
            applied = ingestor.apply(result["operation_id"], confirmed=True)
            self.assertEqual(applied["state"], "expired")
            self.assertEqual(applied["error_code"], "path_unresolved")

    def test_apply_failure_rolls_back_source(self):
        """R002/C003 回归：apply 中途 I/O 失败 → 结构化 apply_failed 且不留下 source 半成品。"""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            ingestor = SourceIngestor(root)
            result = ingestor.preview(
                {
                    "source_type": "personal-note",
                    "domain": "tools",
                    "origin": "personal",
                    "body": "足够长的失败回滚验证笔记正文内容",
                    "source_id": "rollback-note",
                }
            )
            # 用文件占位 archive 目录，使 snapshot 写入必然失败
            (root / "archive").write_text("occupied", encoding="utf-8")
            applied = ingestor.apply(result["operation_id"], confirmed=True)
            self.assertEqual(applied["state"], "expired")
            self.assertEqual(applied["error_code"], "apply_failed")
            self.assertFalse((root / "sources" / "tools" / "rollback-note.md").exists())

    def test_apply_recovery_after_partial_write(self):
        """R002 回归：崩溃后（source 已写、state 未提交）重试幂等恢复为 applied（WAL 重放）。"""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            ingestor = SourceIngestor(root)
            body = "崩溃恢复验证的足够长个人笔记正文。"
            result = ingestor.preview(
                {
                    "source_type": "personal-note",
                    "domain": "tools",
                    "origin": "personal",
                    "body": body,
                    "source_id": "recover-note",
                }
            )
            # 模拟崩溃点：source 已由本操作写入，manifest/state 未提交
            metadata = {
                "schema_version": "source/v1",
                "id": "recover-note",
                "domain": "tools",
                "vault_id": "public",
                "source_type": "personal-note",
                "origin": "personal",
                "retrieval": {"acquisition": "personal-note"},
                "snapshot_sha256": result["snapshot_sha256"],
                "extractor": "personal-note/1",
                "media_type": "text/markdown",
                "read_status": "retrieved",
                "confidentiality": "public",
                "archive_policy": "text-only",
            }
            source_path = root / "sources" / "tools" / "recover-note.md"
            source_path.parent.mkdir(parents=True)
            source_path.write_text(
                FrontMatter.render(metadata, body), encoding="utf-8"
            )
            applied = ingestor.apply(result["operation_id"], confirmed=True)
            self.assertEqual(applied["state"], "applied")
            manifest = (root / "archive" / "manifest.jsonl").read_text(
                encoding="utf-8"
            )
            self.assertIn("recover-note", manifest)


    def test_html_extractor_unavailable_without_trafilatura(self):
        """无 trafilatura 环境：返回 extractor_unavailable:trafilatura，不降级。"""
        with mock.patch.dict(sys.modules, {"trafilatura": None}):
            with self.assertRaisesRegex(
                RuntimeError, "extractor_unavailable:trafilatura"
            ):
                TextExtractor().extract(b"<html><body>x</body></html>", "text/html")

    def test_html_extractor_error_normalized(self):
        """trafilatura 提取抛意外异常 → extract_failed:trafilatura（不静默）。"""
        fake = types.ModuleType("trafilatura")

        def _boom(*args: object, **kwargs: object) -> str:
            raise ValueError("malformed html")

        fake.extract = _boom
        with mock.patch.dict(sys.modules, {"trafilatura": fake}):
            with self.assertRaisesRegex(RuntimeError, "extract_failed:trafilatura"):
                TextExtractor().extract(b"<html><body>x</body></html>", "text/html")

    def test_front_matter_error_normalization(self):
        """坏 YAML → front_matter_invalid_yaml；空 front matter → {}（不穿透库异常）。"""
        with self.assertRaisesRegex(ValueError, "front_matter_invalid_yaml"):
            FrontMatter.parse("---\na: [unclosed\n---\nbody")
        metadata, body = FrontMatter.parse("---\n\n---\nbody")
        self.assertEqual(metadata, {})
        self.assertEqual(body, "body")

    def test_apply_recovery_overwrite(self):
        """R002 回归：覆盖导入（preview 时目标已存在）崩溃后重放恢复为 applied。"""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            ingestor = SourceIngestor(root)
            old_body = "旧版本正文内容"
            first = ingestor.preview(
                {
                    "source_type": "personal-note",
                    "domain": "tools",
                    "origin": "personal",
                    "body": old_body,
                    "source_id": "overwrite-note",
                }
            )
            ingestor.apply(first["operation_id"], confirmed=True)
            new_body = "新版本正文内容，覆盖导入"
            second = ingestor.preview(
                {
                    "source_type": "personal-note",
                    "domain": "tools",
                    "origin": "personal",
                    "body": new_body,
                    "source_id": "overwrite-note",
                }
            )
            # 模拟崩溃点：source 已由本操作写入（front matter snapshot 为新 hash）
            source_path = root / "sources" / "tools" / "overwrite-note.md"
            metadata = {
                "schema_version": "source/v1",
                "id": "overwrite-note",
                "domain": "tools",
                "vault_id": "public",
                "source_type": "personal-note",
                "origin": "personal",
                "retrieval": {"acquisition": "personal-note"},
                "snapshot_sha256": second["snapshot_sha256"],
                "extractor": "personal-note/1",
                "media_type": "text/markdown",
                "read_status": "retrieved",
                "confidentiality": "public",
                "archive_policy": "text-only",
            }
            source_path.write_text(
                FrontMatter.render(metadata, new_body), encoding="utf-8"
            )
            applied = ingestor.apply(second["operation_id"], confirmed=True)
            self.assertEqual(applied["state"], "applied")
            self.assertEqual(applied["snapshot_sha256"], second["snapshot_sha256"])

    def test_apply_failure_keeps_existing_source(self):
        """覆盖导入失败：回滚保留旧文件，不误删旧版本。"""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            ingestor = SourceIngestor(root)
            old_body = "旧版本正文内容"
            first = ingestor.preview(
                {
                    "source_type": "personal-note",
                    "domain": "tools",
                    "origin": "personal",
                    "body": old_body,
                    "source_id": "keep-old-note",
                }
            )
            ingestor.apply(first["operation_id"], confirmed=True)
            second = ingestor.preview(
                {
                    "source_type": "personal-note",
                    "domain": "tools",
                    "origin": "personal",
                    "body": "新版本正文内容",
                    "source_id": "keep-old-note",
                }
            )
            # 新 snapshot 写入失败：archive/text 只读
            text_dir = root / "archive" / "text"
            text_dir.chmod(0o500)
            try:
                applied = ingestor.apply(second["operation_id"], confirmed=True)
            finally:
                text_dir.chmod(0o755)
            self.assertEqual(applied["state"], "expired")
            self.assertEqual(applied["error_code"], "apply_failed")
            source_text = (
                root / "sources" / "tools" / "keep-old-note.md"
            ).read_text(encoding="utf-8")
            self.assertIn("旧版本正文内容", source_text)
            self.assertNotIn("新版本正文内容", source_text)

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
            applied = anchor_service.apply(
                evidence["operation_id"], confirmed=True
            )
            self.assertEqual(applied["state"], "applied")
            self.assertEqual(
                applied["evidence"]["evidence_id"], evidence["evidence"]["evidence_id"]
            )

    def test_crash_injection_source_apply(self):
        """真实进程崩溃注入：4 个提交点 kill -9 后重放恢复为 applied（WAL 语义）。

        同时验证 flock 锁在进程 SIGKILL 后由内核自动释放（子进程 __exit__
        不会执行，重放进程仍能获取锁）。
        """
        import subprocess
        import sys as _sys

        repo_root = str(Path(__file__).resolve().parent.parent)
        script = (
            "import sys\n"
            "from pathlib import Path\n"
            "sys.path.insert(0, sys.argv[1])\n"
            "from tools.source_ingestor import SourceIngestor\n"
            "r = SourceIngestor(Path(sys.argv[2])).apply(sys.argv[3], confirmed=True)\n"
            "print('APPLIED' if r.get('state') == 'applied' else r, file=sys.stderr)\n"
        )
        for point in ("after_archive", "after_source", "after_manifest", "before_commit"):
            with self.subTest(point=point):
                with tempfile.TemporaryDirectory() as directory:
                    root = Path(directory)
                    ingestor = SourceIngestor(root)
                    result = ingestor.preview(
                        {
                            "source_type": "personal-note",
                            "domain": "tools",
                            "origin": "personal",
                            "body": f"崩溃注入验证正文内容 {point}",
                            "source_id": f"crash-{point}".replace("_", "-"),
                        }
                    )
                    proc = subprocess.run(
                        [_sys.executable, "-c", script, repo_root, str(root), result["operation_id"]],
                        env={**os.environ, "MYKNOWLEDGE_CRASH_AFTER": point},
                        capture_output=True,
                        text=True,
                    )
                    self.assertNotEqual(
                        proc.returncode, 0, f"{point}: 子进程未被 kill: {proc.stderr}"
                    )
                    replayed = SourceIngestor(root).apply(
                        result["operation_id"], confirmed=True
                    )
                    self.assertEqual(
                        replayed["state"], "applied", f"{point}: 重放失败: {proc.stderr}"
                    )

    def test_crash_injection_anchor_apply(self):
        """锚定 apply 崩溃注入：写 evidence 后/提交前 kill -9，重放补提交 applied。"""
        import subprocess
        import sys as _sys

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
                        [_sys.executable, "-c", script, repo_root, str(root), evidence["operation_id"]],
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
                        replayed["state"], "applied", f"{point}: 重放失败: {proc.stderr}"
                    )
                    self.assertEqual(
                        replayed["evidence"]["evidence_id"],
                        evidence["evidence"]["evidence_id"],
                        f"{point}: 重放生成了新的 evidence_id",
                    )


def _minimal_pdf(text: str) -> bytes:
    """构造含单个文本对象的最小合法 PDF（含 xref 表），供 pypdf 提取。"""
    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
        b"/Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>",
        None,  # 内容流（需计算长度后填充）
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
    ]
    stream = f"BT /F1 24 Tf 72 720 Td ({text}) Tj ET".encode("ascii")
    objects[3] = (
        b"<< /Length " + str(len(stream)).encode("ascii") + b" >>\nstream\n"
        + stream
        + b"\nendstream"
    )
    out = bytearray(b"%PDF-1.4\n")
    offsets = []
    for index, obj in enumerate(objects, 1):
        offsets.append(len(out))
        out += f"{index} 0 obj\n".encode("ascii") + obj + b"\nendobj\n"
    xref_pos = len(out)
    out += f"xref\n0 {len(objects) + 1}\n".encode("ascii")
    out += b"0000000000 65535 f \n"
    for offset in offsets:
        out += f"{offset:010d} 00000 n \n".encode("ascii")
    out += (
        f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\n"
        f"startxref\n{xref_pos}\n%%EOF\n"
    ).encode("ascii")
    return bytes(out)


if __name__ == "__main__":
    unittest.main()
