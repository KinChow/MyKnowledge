"""F001 F001 正文提取（ingest 域）。"""

from __future__ import annotations

import unittest
from pathlib import Path

import sys
import tempfile
import types
from pathlib import Path
from unittest import mock

from tools.common import strip_sha256_prefix
from tools.ingest.extractor import TextExtractor
from wiki_fixtures import _minimal_pdf
from tools.ingest.source_ingestor import SourceIngestor

class ExtractorTests(unittest.TestCase):
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

    def test_docx_extractor_does_not_fallback_to_binary_text(self):
        with mock.patch.dict(sys.modules, {"docling": None, "docling.document_converter": None}):
            with self.assertRaisesRegex(RuntimeError, "extractor_unavailable:docling"):
                TextExtractor().extract(b"PK\x03\x04not-a-docx", "application/vnd.openxmlformats-officedocument.wordprocessingml.document")
