"""F001 F001 Source 导入与归档（ingest 域）。"""

from __future__ import annotations

import json
import os
import signal as _signal
import subprocess
import sys as _sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tools.common import canonical_quote, sha256_text, strip_sha256_prefix
from tools.doctor import run_doctor
from tools.evidence_anchor import EvidenceAnchor
from tools.ingest.source_ingestor import SourceIngestor
from tools.ingest.source_validator import SourceValidator


class SourceIngestorTests(unittest.TestCase):
    def test_personal_note_ingest_and_anchor(self):
        """AC-F001-005/011：personal-note 生成 snapshot 并可锚定 evidence；重复 ingest 幂等。"""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            ingestor = SourceIngestor(root)
            body = "这是一个包含 emoji 😀 和代码 `x += 1` 的个人笔记。"
            request = {
                "source_type": "personal-note",
                "domain": "tools",
                "origin": "personal",
                "body": body,
                "source_id": "personal-note-one",
            }
            applied = ingestor.ingest(request)
            self.assertEqual(applied["status"], "ok")
            # 直接写下：重复 ingest 同一内容必须幂等（快照内容寻址 + manifest 按 record_id 去重）
            repeated = ingestor.ingest(request)
            self.assertEqual(repeated["status"], "ok")
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
            # AC-F001-013：锚定链与验证器必须共用同一 `canonical_quote` 实现。
            # 校验值不落盘（ADR-0019 §5）后，这条锁改成直接对两条重算路径比对 ——
            # 它要防的仍然是"有人另写第二份归一实现"，与是否落盘无关。
            self.assertEqual(
                sha256_text(canonical_quote("包含 emoji 😀 和代码")),
                SourceValidator.quote_sha256("包含 emoji 😀 和代码"),
            )
            # §5 的落盘契约：证据项不带校验值指纹
            self.assertNotIn("selector_sha256", evidence)
            self.assertNotIn("quote_sha256", evidence)
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
            EvidenceAnchor.anchor_evidence(
                source_path, snapshot_path, "包含 emoji 😀 和代码", min_chars=12
            )
            self.assertIn("evidence_items:", source_path.read_text(encoding="utf-8"))

    def test_invalid_cross_fields_are_rejected(self):
        """AC-F001-009：input_path 与非 local-file 交叉字段被拒绝。"""
        with tempfile.TemporaryDirectory() as directory:
            result = SourceIngestor(Path(directory)).ingest(
                {
                    "source_type": "doc",
                    "domain": "tools",
                    "input_path": "/tmp/file",
                }
            )
            self.assertEqual(result["status"], "blocked")
            self.assertEqual(result["error_code"], "schema_invalid")
            self.assertEqual(result["errors"][0]["code"], "schema_invalid")

    def test_url_ingest_not_schema_blocked(self):
        """AC-F001-001 回归：URL 导入不被 schema 拦截，失败归因于抓取策略。"""
        with tempfile.TemporaryDirectory() as directory:
            result = SourceIngestor(Path(directory)).ingest(
                {
                    "source_type": "doc",
                    "domain": "tools",
                    "url": "http://127.0.0.1/",
                }
            )
            # 采集阶段抓取失败（SSRF 策略拒绝等）属调用方输入问题：blocked + 伞码，
            # 动态明细码（fetch_blocked:private_network）留在 errors[]。
            self.assertEqual(result["status"], "blocked")
            self.assertEqual(result["error_code"], "source_ingest_failed")
            self.assertEqual(
                result["errors"][0]["code"], "fetch_blocked:private_network"
            )

    def test_manifest_corrupt_line_tolerated(self):
        """AC-F001-006：manifest 存在损坏行时后续 ingest 仍成功且不覆盖旧行。"""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            ingestor = SourceIngestor(root)
            first_note = root / "note1.md"
            first_note.write_text("第一份内容", encoding="utf-8")
            ingestor.ingest(
                {
                    "source_type": "local-file",
                    "domain": "tools",
                    "input_path": str(first_note),
                    "source_id": "first-source",
                    "media_type": "text/plain",
                }
            )
            manifest = root / "archive" / "manifest.jsonl"
            manifest.write_text(
                manifest.read_text(encoding="utf-8") + "{corrupt line\n",
                encoding="utf-8",
            )
            second_note = root / "note2.md"
            second_note.write_text("第二份内容", encoding="utf-8")
            applied = ingestor.ingest(
                {
                    "source_type": "local-file",
                    "domain": "tools",
                    "input_path": str(second_note),
                    "source_id": "second-source",
                    "media_type": "text/plain",
                }
            )
            self.assertEqual(applied["status"], "ok")

    def test_manifest_invalid_utf8_tolerated(self):
        """manifest 含非法 UTF-8 字节行时后续 ingest 仍成功。"""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            ingestor = SourceIngestor(root)
            first_note = root / "note1.md"
            first_note.write_text("第一份内容", encoding="utf-8")
            ingestor.ingest(
                {
                    "source_type": "local-file",
                    "domain": "tools",
                    "input_path": str(first_note),
                    "source_id": "utf8-first",
                    "media_type": "text/plain",
                }
            )
            manifest = root / "archive" / "manifest.jsonl"
            with manifest.open("ab") as handle:
                handle.write(b"\xff\xfe invalid utf8\n")
            second_note = root / "note2.md"
            second_note.write_text("第二份内容", encoding="utf-8")
            applied = ingestor.ingest(
                {
                    "source_type": "local-file",
                    "domain": "tools",
                    "input_path": str(second_note),
                    "source_id": "utf8-second",
                    "media_type": "text/plain",
                }
            )
            self.assertEqual(applied["status"], "ok")

    def test_manifest_deduplicates_snapshot_keeps_owners(self):
        """AC-F001-006：两个 source 相同内容 → archive 去重一个快照，manifest 两行 owner 保留。"""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            ingestor = SourceIngestor(root)
            body = "完全相同的正文内容"
            for source_id in ("dup-a", "dup-b"):
                applied = ingestor.ingest(
                    {
                        "source_type": "personal-note",
                        "domain": "tools",
                        "origin": "personal",
                        "body": body,
                        "source_id": source_id,
                    }
                )
                self.assertEqual(applied["status"], "ok")
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
            applied = ingestor.ingest(
                {
                    "source_type": "doc",
                    "domain": "tools",
                    "url": "https://example.com/article",
                    "source_id": "url-source",
                }
            )
            self.assertEqual(applied["status"], "ok")
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
            applied = json.loads(captured[-1])
            self.assertEqual(applied["status"], "ok", applied)
            snapshot = (
                root
                / "archive"
                / "text"
                / f"{strip_sha256_prefix(applied['snapshot_sha256'])}.md"
            )
            body = snapshot.read_text(encoding="utf-8")
            self.assertIn("本人综合改写的正文", body)
            self.assertNotIn(str(note), body)

    def test_non_string_body_blocked(self):
        """C001 回归：非字符串 body 返回结构化 blocked 而非崩溃。"""
        with tempfile.TemporaryDirectory() as directory:
            result = SourceIngestor(Path(directory)).ingest(
                {
                    "source_type": "personal-note",
                    "domain": "tools",
                    "origin": "personal",
                    "body": None,
                    "source_id": "bad-body",
                }
            )
            self.assertEqual(result["status"], "blocked")
            self.assertEqual(result["error_code"], "schema_invalid")
            self.assertEqual(result["errors"][0]["code"], "schema_invalid")

    def test_ingest_failure_rolls_back_source(self):
        """R002/C003 回归：ingest 中途 I/O 失败 → 结构化 apply_failed 且不留下 source 半成品。"""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            ingestor = SourceIngestor(root)
            # 用文件占位 archive 目录，使 snapshot 写入必然失败
            (root / "archive").write_text("occupied", encoding="utf-8")
            applied = ingestor.ingest(
                {
                    "source_type": "personal-note",
                    "domain": "tools",
                    "origin": "personal",
                    "body": "足够长的失败回滚验证笔记正文内容",
                    "source_id": "rollback-note",
                }
            )
            # 落盘 I/O 失败：blocked + 伞码（保持迁移前语义），明细码进 errors[]。
            self.assertEqual(applied["status"], "blocked")
            self.assertEqual(applied["error_code"], "source_ingest_failed")
            self.assertEqual(applied["errors"][0]["code"], "apply_failed")
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

    def test_ingest_failure_keeps_existing_source(self):
        """覆盖导入失败：回滚保留旧文件，不误删旧版本。"""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            ingestor = SourceIngestor(root)
            self._ingest_note(ingestor, "旧版本正文内容", "keep-old-note")
            # 新 snapshot 写入失败：archive/text 只读
            text_dir = root / "archive" / "text"
            text_dir.chmod(0o500)
            try:
                applied = self._ingest_note(ingestor, "新版本正文内容", "keep-old-note")
            finally:
                text_dir.chmod(0o755)
            self.assertEqual(applied["status"], "blocked")
            self.assertEqual(applied["error_code"], "source_ingest_failed")
            self.assertEqual(applied["errors"][0]["code"], "apply_failed")
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

    def _ingest_note(self, ingestor, body: str, source_id: str) -> dict:
        return ingestor.ingest(
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
            with mock.patch.dict(os.environ, {"MYKNOWLEDGE_FAIL_AT": "after_source"}):
                applied = self._ingest_note(ingestor, "新建正文内容", "fail-new-note")
            self.assertEqual(applied["status"], "blocked")
            self.assertEqual(applied["error_code"], "source_ingest_failed")
            self.assertEqual(applied["errors"][0]["code"], "apply_failed")
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
        **对应账目已入账**（manifest 先于 source 落盘）、doctor 双向检查全过。
        这是把不可逆的一步放到最后换来的：过去这里是永久账目缺口，只能人工重做。
        """
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            ingestor = SourceIngestor(root)
            self._ingest_note(ingestor, "旧版本正文内容", "fail-ovw-note")
            with mock.patch.dict(os.environ, {"MYKNOWLEDGE_FAIL_AT": "after_source"}):
                applied = self._ingest_note(ingestor, "新版本正文内容", "fail-ovw-note")
            self.assertEqual(applied["status"], "blocked")
            self.assertEqual(applied["error_code"], "source_ingest_failed")
            self.assertEqual(applied["errors"][0]["code"], "apply_failed")

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
            self.assertEqual(run_doctor(root)["errors"], 0)  # 无需人工修复

    def test_failure_before_source_write_leaves_only_a_harmless_extra_record(self):
        """注入点 after_manifest 抛 OSError：source 未被改写，只多一条账目。

        这是新顺序引入的唯一新失效面，钉住它的无害性：旧内容完好（覆盖导入未
        发生）、多出的 record 指向真实存在的快照，doctor 双向检查都过。
        """
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            ingestor = SourceIngestor(root)
            self._ingest_note(ingestor, "旧版本正文内容", "extra-rec-note")
            with mock.patch.dict(os.environ, {"MYKNOWLEDGE_FAIL_AT": "after_manifest"}):
                applied = self._ingest_note(
                    ingestor, "新版本正文内容", "extra-rec-note"
                )
            self.assertEqual(applied["status"], "blocked")
            self.assertEqual(applied["error_code"], "source_ingest_failed")
            self.assertEqual(applied["errors"][0]["code"], "apply_failed")
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

    def test_crash_injection_ingest_converges(self):
        """SIGKILL 注入：3 个落盘提交点被 kill -9 后重跑 ingest 必须自愈。

        与 ``MYKNOWLEDGE_FAIL_AT`` 的 OSError 注入是**两类不同的失败**
        （见 ``tools/common.py::injection_point`` 文档）：OSError 会走
        ``_rollback_uncommitted``，SIGKILL 下回滚根本不执行，中间态只能靠
        ``_write_artifacts`` 的落盘顺序（不可逆的 source 放最后）+ 快照内容寻址
        + manifest ``record_id`` 幂等去重来自愈。这正是该函数 docstring
        "顺序即恢复语义"所主张的东西，也是 OSError 用例覆盖不到的那一半。
        """

        repo_root = str(Path(__file__).resolve().parent.parent)
        script = (
            "import json, sys\n"
            "from pathlib import Path\n"
            "sys.path.insert(0, sys.argv[1])\n"
            "from tools.ingest.source_ingestor import SourceIngestor\n"
            "r = SourceIngestor(Path(sys.argv[2])).ingest(json.loads(sys.argv[3]))\n"
            "print(json.dumps(r, ensure_ascii=False), file=sys.stderr)\n"
        )
        for point in ("after_archive", "after_manifest", "after_source"):
            with self.subTest(point=point):
                with tempfile.TemporaryDirectory() as directory:
                    root = Path(directory)
                    request = {
                        "source_type": "personal-note",
                        "domain": "tools",
                        "origin": "personal",
                        "body": f"崩溃注入验证正文内容 {point}",
                        "source_id": f"crash-{point}".replace("_", "-"),
                    }
                    proc = subprocess.run(
                        [
                            _sys.executable,
                            "-c",
                            script,
                            repo_root,
                            str(root),
                            json.dumps(request),
                        ],
                        env={**os.environ, "MYKNOWLEDGE_CRASH_AFTER": point},
                        capture_output=True,
                        text=True,
                    )
                    # 必须是真被 SIGKILL 打断（-9 而非任意非零），否则子进程可能
                    # 因 import 等无关原因失败，用例会假绿
                    self.assertEqual(
                        proc.returncode,
                        -_signal.SIGKILL,
                        f"{point}: 子进程未被 kill -9: {proc.stderr}",
                    )
                    replayed = SourceIngestor(root).ingest(request)
                    self.assertEqual(
                        replayed["status"], "ok", f"{point}: 重跑未收敛: {replayed}"
                    )
                    # 单一账目：SIGKILL 没有回滚，重复记录只能靠 record_id 幂等去重
                    manifest = root / "archive" / "manifest.jsonl"
                    lines = [
                        line
                        for line in manifest.read_text(encoding="utf-8").splitlines()
                        if line.strip()
                    ]
                    self.assertEqual(len(lines), 1, f"{point}: manifest 未去重")
                    source_text = (
                        root
                        / "content"
                        / "sources"
                        / "tools"
                        / request["source_id"]
                        / f"{request['source_id']}.md"
                    ).read_text(encoding="utf-8")
                    self.assertIn(request["body"], source_text)
                    # 中间态不需要人工修：doctor 双向检查（archive ↔ manifest）都过
                    self.assertEqual(run_doctor(root)["errors"], 0)

    def test_unsupported_transcript_format_is_blocked_not_raised(self):
        """回归：采集阶段抛的 ValueError 必须转成结构化 blocked，不得逃逸成 traceback。

        `VideoAcquirer.acquire` 用 `raise ValueError("transcript_format_unsupported")`
        当错误码载体，而 `_prepare` 的 except 元组原先不含 `ValueError`——schema 合法
        的请求（合法视频 URL + 非 .vtt/.srt 的字幕文件）会让裸异常冒到 CLI，人被
        traceback 而不是结构化错误码。此用例钉住"ingest 对所有输入只返回结构化结果"。
        """
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            transcript = root / "subtitle.txt"
            transcript.write_text(
                "1\n00:00:00,000 --> 00:00:01,000\nhi\n", encoding="utf-8"
            )
            media = root / "clip.mp4"
            media.write_bytes(b"\x00")
            result = SourceIngestor(root).ingest(
                {
                    "source_type": "video",
                    "domain": "tools",
                    "source_id": "bad-transcript-format",
                    "url": "https://www.bilibili.com/video/BV1xx411c7mD",
                    "transcript_path": str(transcript),
                    "input_path": str(media),
                    "subtitle_mode": "manual",
                }
            )
            # 采集阶段抛的 ValueError 归一为结构化 blocked（不逃逸成 traceback），
            # 明细码 transcript_format_unsupported 留在 errors[]。
            self.assertEqual(result["status"], "blocked")
            self.assertEqual(result["error_code"], "source_ingest_failed")
            self.assertEqual(
                result["errors"][0]["code"], "transcript_format_unsupported"
            )
            self.assertEqual(run_doctor(root)["errors"], 0)
