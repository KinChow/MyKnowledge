"""F001 F001 URL 抓取策略（ingest 域）。"""

from __future__ import annotations

import unittest
from pathlib import Path

import gzip
import tempfile
from pathlib import Path

from tools.ingest.fetcher import URLFetcher, _bounded_decompress
from tools.ingest.source_ingestor import SourceIngestor

class FetcherTests(unittest.TestCase):
    def test_bounded_gzip_rejects_expansion(self):
        """AC-F001-010：解压炸弹超限被拒绝。"""
        compressed = gzip.compress(b"A" * 10000)
        with self.assertRaisesRegex(RuntimeError, "decompression_limit_exceeded"):
            _bounded_decompress(compressed, "gzip", 100)

    def test_url_policy_rejects_private_and_unsafe_targets(self):
        """AC-F001-007/010：file scheme 与私网地址被拒绝。"""
        fetcher = URLFetcher()
        with self.assertRaisesRegex(RuntimeError, "url_policy"):
            fetcher.fetch("file:///etc/passwd")
        with self.assertRaisesRegex(RuntimeError, "private_network"):
            fetcher.fetch("http://127.0.0.1/")

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

