"""F001 F001 Source 导入与归档（ingest 域）。"""

from __future__ import annotations

import json
import os
import subprocess
import sys as _sys
import tempfile
import time
import unittest
from pathlib import Path
from unittest import mock

from tools.common import canonical_quote, sha256_text, strip_sha256_prefix
from tools.doctor import run_doctor
from tools.evidence_anchor import EvidenceAnchor
from tools.front_matter import FrontMatter
from tools.ingest.source_ingestor import SourceIngestor
from tools.ingest.source_validator import SourceValidator
from tools.operation_store import OPERATION_TTL_SECONDS


class SourceIngestorTests(unittest.TestCase):
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
            entry = json.loads(
                (root / "archive" / "manifest.jsonl").read_text().splitlines()[0]
            )
            for field in (
                "record_id",
                "vault_id",
                "owner_object_ref",
                "snapshot_sha256",
                "archive_path",
                "extractor",
                "normalization_version",
                "canonical_byte_length",
                "record_sha256",
            ):
                self.assertIn(field, entry)
            self.assertEqual(entry["vault_id"], "public")
            self.assertEqual(
                entry["owner_object_ref"], {"type": "source", "id": "personal-note-one"}
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
            source_path = (
                root
                / "content"
                / "sources"
                / "tools"
                / "personal-note-one"
                / "personal-note-one.md"
            )
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
            self.assertFalse(
                (
                    root
                    / "content"
                    / "sources"
                    / "tools"
                    / "local-note"
                    / "local-note.md"
                ).exists()
            )

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
                (
                    root
                    / "content"
                    / "sources"
                    / "tools"
                    / "deleted-note"
                    / "deleted-note.md"
                ).exists()
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
            target = (
                root
                / "content"
                / "sources"
                / "tools"
                / "target-change"
                / "target-change.md"
            )
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
                root / "var" / "state" / "operations" / f"{result['operation_id']}.json"
            )
            payload = json.loads(operation_path.read_text(encoding="utf-8"))
            payload["created_at"] = time.time() - (OPERATION_TTL_SECONDS + 1)
            operation_path.write_text(json.dumps(payload), encoding="utf-8")
            applied = ingestor.apply(result["operation_id"], confirmed=True)
            self.assertEqual(applied["error_code"], "operation_expired")

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
            applied = EvidenceAnchor(root).apply(result["operation_id"], confirmed=True)
            self.assertEqual(applied["error_code"], "operation_type_mismatch")

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

    def test_url_fetch_success_archives_with_origin_url(self):
        """AC-F001-001：URL 正文非空 → 成功归档，且出处 URL 保留（M001 回归）。"""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            ingestor = SourceIngestor(root)

            class _FakeFetcher:
                def fetch(self, url: str) -> tuple[bytes, str, str]:
                    return (
                        "<html><body>抓取正文内容</body></html>".encode(),
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
            source = (
                root / "content" / "sources" / "tools" / "url-source" / "url-source.md"
            ).read_text(encoding="utf-8")
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

    def test_personal_note_at_path_reads_the_file_as_body(self):
        """`--personal-note @path` 必须把文件正文当 body，而不是把路径当正文。

        实测过的失败：融合型内容（来源已融进作者表达）本来就以文件形式存在，
        只能走 personal-note 通道（`--from-file` 会写 `origin: external`，正是
        要消除的失真登记）；此前把路径传给 `--personal-note`，导入的快照是那串
        路径字符串本身（83 字节假快照）。
        """
        from tools.ingest.source_ingestor import main as source_main

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            note = root / "note.md"
            note.write_text(
                "# 融合型笔记\n\n这是本人综合改写的正文。\n", encoding="utf-8"
            )
            captured: list[str] = []
            with mock.patch("builtins.print", side_effect=captured.append):
                code = source_main(
                    [
                        "--root",
                        str(root),
                        "--personal-note",
                        f"@{note}",
                        "--source-id",
                        "fused-note",
                        "--domain",
                        "tools",
                    ]
                )
            self.assertEqual(code, 0)
            preview = json.loads(captured[-1])
            self.assertEqual(preview["state"], "previewed")
            applied = SourceIngestor(root).apply(
                preview["operation_id"], confirmed=True
            )
            self.assertEqual(applied["state"], "applied", applied)
            snapshot = (
                root
                / "archive"
                / "text"
                / f"{strip_sha256_prefix(applied['snapshot_sha256'])}.md"
            )
            body = snapshot.read_text(encoding="utf-8")
            self.assertIn("本人综合改写的正文", body)
            self.assertNotIn(str(note), body)

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
            result = SourceIngestor(Path(directory)).apply("op_BAD_ID", confirmed=True)
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
            self.assertFalse(
                (
                    root
                    / "content"
                    / "sources"
                    / "tools"
                    / "rollback-note"
                    / "rollback-note.md"
                ).exists()
            )

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
            source_path = (
                root
                / "content"
                / "sources"
                / "tools"
                / "recover-note"
                / "recover-note.md"
            )
            source_path.parent.mkdir(parents=True)
            source_path.write_text(FrontMatter.render(metadata, body), encoding="utf-8")
            applied = ingestor.apply(result["operation_id"], confirmed=True)
            self.assertEqual(applied["state"], "applied")
            manifest = (root / "archive" / "manifest.jsonl").read_text(encoding="utf-8")
            self.assertIn("recover-note", manifest)

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
            source_path = (
                root
                / "content"
                / "sources"
                / "tools"
                / "overwrite-note"
                / "overwrite-note.md"
            )
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
                root
                / "content"
                / "sources"
                / "tools"
                / "keep-old-note"
                / "keep-old-note.md"
            ).read_text(encoding="utf-8")
            self.assertIn("旧版本正文内容", source_text)
            self.assertNotIn("新版本正文内容", source_text)

    def _preview_note(self, ingestor, body: str, source_id: str) -> dict:
        return ingestor.preview(
            {
                "source_type": "personal-note",
                "domain": "tools",
                "origin": "personal",
                "body": body,
                "source_id": source_id,
            }
        )

    def test_failure_at_the_last_write_rolls_back_the_new_source(self):
        """注入点 after_source（最后一步之后）抛 OSError：新建导入删掉刚写的 source。

        既有两个回滚用例都让 archive 写入失败——那时 source 还没写，unlink 是
        空操作。这里覆盖真正会删文件的分支。account 侧的实测语义：账目已在
        source 之前入账，所以留下的是"多一条指向已存在快照的记录"（无害），
        而不是缺口——doctor 依然干净。
        """
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            ingestor = SourceIngestor(root)
            operation = self._preview_note(ingestor, "新建正文内容", "fail-new-note")
            with mock.patch.dict(os.environ, {"MYKNOWLEDGE_FAIL_AT": "after_source"}):
                applied = ingestor.apply(operation["operation_id"], confirmed=True)
            self.assertEqual(applied["state"], "expired")
            self.assertEqual(applied["error_code"], "apply_failed")
            self.assertFalse(
                (
                    root
                    / "content"
                    / "sources"
                    / "tools"
                    / "fail-new-note"
                    / "fail-new-note.md"
                ).exists()
            )
            manifest = root / "archive" / "manifest.jsonl"
            self.assertEqual(
                len(manifest.read_text(encoding="utf-8").strip().splitlines()), 1
            )
            # archive 是内容寻址的不可变快照，保留无害（重放会命中同一文件）
            self.assertEqual(len(list((root / "archive" / "text").glob("*.md"))), 1)
            self.assertEqual(run_doctor(root)["errors"], 0)  # 多一条账目不是缺口

    def test_overwrite_failure_keeps_content_and_ledger_consistent(self):
        """注入点 after_source 抛 OSError：覆盖导入失败后内容与账目仍然自洽。

        实测语义（不是设计意图的复述）：新内容留在 source 里（原子替换不可回退）、
        **对应账目已入账**（manifest 先于 source 落盘）、失败的 operation 是
        expired 不可重放——但也不需要重放，doctor 双向检查全过。这是把不可逆
        的一步放到最后换来的：过去这里是永久账目缺口，只能人工重做。
        """
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            ingestor = SourceIngestor(root)
            first = self._preview_note(ingestor, "旧版本正文内容", "fail-ovw-note")
            ingestor.apply(first["operation_id"], confirmed=True)
            second = self._preview_note(ingestor, "新版本正文内容", "fail-ovw-note")
            with mock.patch.dict(os.environ, {"MYKNOWLEDGE_FAIL_AT": "after_source"}):
                applied = ingestor.apply(second["operation_id"], confirmed=True)
            self.assertEqual(applied["error_code"], "apply_failed")

            source_path = (
                root
                / "content"
                / "sources"
                / "tools"
                / "fail-ovw-note"
                / "fail-ovw-note.md"
            )
            body = source_path.read_text(encoding="utf-8")
            self.assertIn("新版本正文内容", body)  # 旧内容已被原子替换，不可恢复
            manifest = root / "archive" / "manifest.jsonl"
            self.assertEqual(
                len(manifest.read_text(encoding="utf-8").strip().splitlines()),
                2,  # 旧+新两条 owner record：新 snapshot 已入账
            )
            self.assertEqual(
                ingestor.apply(second["operation_id"], confirmed=True)["state"],
                "expired",  # 同一 operation 不可重放（apply_preflight 只接受 previewed）
            )
            self.assertEqual(run_doctor(root)["errors"], 0)  # 无需人工修复

    def test_failure_before_source_write_leaves_only_a_harmless_extra_record(self):
        """注入点 after_manifest 抛 OSError：source 未被改写，只多一条账目。

        这是新顺序引入的唯一新失效面，钉住它的无害性：旧内容完好（覆盖导入未
        发生）、多出的 record 指向真实存在的快照，doctor 双向检查都过。
        """
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            ingestor = SourceIngestor(root)
            first = self._preview_note(ingestor, "旧版本正文内容", "extra-rec-note")
            ingestor.apply(first["operation_id"], confirmed=True)
            second = self._preview_note(ingestor, "新版本正文内容", "extra-rec-note")
            with mock.patch.dict(os.environ, {"MYKNOWLEDGE_FAIL_AT": "after_manifest"}):
                applied = ingestor.apply(second["operation_id"], confirmed=True)
            self.assertEqual(applied["error_code"], "apply_failed")
            source_text = (
                root
                / "content"
                / "sources"
                / "tools"
                / "extra-rec-note"
                / "extra-rec-note.md"
            ).read_text(encoding="utf-8")
            self.assertIn("旧版本正文内容", source_text)  # 不可逆的一步没有发生
            self.assertNotIn("新版本正文内容", source_text)
            manifest = root / "archive" / "manifest.jsonl"
            self.assertEqual(
                len(manifest.read_text(encoding="utf-8").strip().splitlines()), 2
            )
            self.assertEqual(run_doctor(root)["errors"], 0)

    def test_crash_injection_source_apply(self):
        """真实进程崩溃注入：4 个提交点 kill -9 后重放恢复为 applied（WAL 语义）。

        同时验证 flock 锁在进程 SIGKILL 后由内核自动释放（子进程 __exit__
        不会执行，重放进程仍能获取锁）。
        """

        repo_root = str(Path(__file__).resolve().parent.parent)
        script = (
            "import sys\n"
            "from pathlib import Path\n"
            "sys.path.insert(0, sys.argv[1])\n"
            "from tools.ingest.source_ingestor import SourceIngestor\n"
            "r = SourceIngestor(Path(sys.argv[2])).apply(sys.argv[3], confirmed=True)\n"
            "print('APPLIED' if r.get('state') == 'applied' else r, file=sys.stderr)\n"
        )
        for point in (
            "after_archive",
            "after_source",
            "after_manifest",
            "before_commit",
        ):
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
                        [
                            _sys.executable,
                            "-c",
                            script,
                            repo_root,
                            str(root),
                            result["operation_id"],
                        ],
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
                        replayed["state"],
                        "applied",
                        f"{point}: 重放失败: {proc.stderr}",
                    )
