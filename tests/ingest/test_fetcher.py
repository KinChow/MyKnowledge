"""F001 F001 URL 抓取策略（ingest 域）。"""

from __future__ import annotations

import gzip
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tools.ingest.fetcher import URLFetcher, _bounded_decompress
from tools.ingest.source_ingestor import SourceIngestor


class FetcherTests(unittest.TestCase):
    def test_redirect_is_rechecked_and_response_limit_is_enforced(self):
        class Response:
            def __init__(self, status, body=b"", location=None):
                self.status, self.body, self.location = status, body, location

            def getheader(self, name):
                return self.location if name == "Location" else "identity"

            def read(self, size=-1):
                return self.body[:size]

        class Connection:
            responses = [
                Response(302, location="http://example.com/next"),
                Response(200, b"too-large"),
            ]

            def __init__(self, *args, **kwargs):
                pass

            def request(self, *args, **kwargs):
                pass

            def getresponse(self):
                return self.responses.pop(0)

            def close(self):
                pass

        fetcher = URLFetcher(max_bytes=3)
        with (
            mock.patch("tools.ingest.fetcher.http.client.HTTPConnection", Connection),
            mock.patch.object(
                URLFetcher, "_resolve_public_ip", return_value="93.184.216.34"
            ),
            self.assertRaisesRegex(RuntimeError, "response_limit"),
        ):
            fetcher.fetch("http://example.com/start")

    def test_redirect_limit_is_explicit(self):
        class Response:
            status = 302

            def getheader(self, name):
                return "http://example.com/next"

            def read(self, size=-1):
                return b""

        class Connection:
            def __init__(self, *args, **kwargs):
                pass

            def request(self, *args, **kwargs):
                pass

            def getresponse(self):
                return Response()

            def close(self):
                pass

        with (
            mock.patch("tools.ingest.fetcher.http.client.HTTPConnection", Connection),
            mock.patch.object(
                URLFetcher, "_resolve_public_ip", return_value="93.184.216.34"
            ),
            self.assertRaisesRegex(RuntimeError, "redirect_limit"),
        ):
            URLFetcher(max_redirects=1).fetch("http://example.com/start")

    def test_request_timeout_is_structured_and_connection_is_closed(self):
        class Connection:
            closed = False

            def __init__(self, *args, **kwargs):
                pass

            def request(self, *args, **kwargs):
                raise TimeoutError("deadline")

            def close(self):
                self.closed = True

        with (
            mock.patch("tools.ingest.fetcher.http.client.HTTPConnection", Connection),
            mock.patch.object(
                URLFetcher, "_resolve_public_ip", return_value="93.184.216.34"
            ),
            self.assertRaisesRegex(RuntimeError, "fetch_blocked:request_failed"),
        ):
            URLFetcher(timeout=0.01).fetch("http://example.com/start")

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

    def test_userinfo_url_is_blocked(self):
        with self.assertRaisesRegex(RuntimeError, "fetch_blocked:url_policy"):
            URLFetcher().fetch("http://user:pass@example.com/")

    def test_local_domain_suffix_is_blocked_before_dns_resolution(self):
        fetcher = URLFetcher()
        with mock.patch.object(URLFetcher, "_resolve_public_ip") as resolve:
            with self.assertRaisesRegex(RuntimeError, "fetch_blocked:host_policy"):
                fetcher.fetch("http://service.internal/")
            resolve.assert_not_called()
        with self.assertRaisesRegex(RuntimeError, "fetch_blocked:host_policy"):
            fetcher.fetch("http://printer.local/")

    def test_dns_rebinding_is_reported_separately(self):
        class Response:
            status = 302

            def getheader(self, name):
                return "http://example.com/next"

            def read(self, size=-1):
                return b""

        class Connection:
            def __init__(self, *args, **kwargs):
                pass

            def request(self, *args, **kwargs):
                pass

            def getresponse(self):
                return Response()

            def close(self):
                pass

        with (
            mock.patch("tools.ingest.fetcher.http.client.HTTPConnection", Connection),
            mock.patch.object(
                URLFetcher,
                "_resolve_public_ip",
                side_effect=["93.184.216.34", "93.184.216.35"],
            ),
            self.assertRaisesRegex(RuntimeError, "dns_rebinding_blocked"),
        ):
            URLFetcher().fetch("http://example.com/start")
