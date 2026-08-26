"""URL 抓取器：防 SSRF/DNS rebinding/解压炸弹的 HTTP(S) 抓取。

对应 AC-F001-007/010：逐跳检查 scheme/端口/主机与解析 IP，连接 pin 已检查 IP。
"""

from __future__ import annotations

import http.client
import ipaddress
import socket
import ssl
import urllib.parse
import zlib


class _PinnedHTTPSConnection(http.client.HTTPSConnection):
    """HTTPS 连接：TCP 连已校验的 IP，TLS 使用原始主机名做 SNI/证书校验。"""

    def __init__(self, ip: str, hostname: str, port: int, timeout: float) -> None:
        super().__init__(
            ip, port=port, timeout=timeout, context=ssl.create_default_context()
        )
        self._verified_hostname = hostname

    def connect(self) -> None:
        raw = socket.create_connection((self.host, self.port), self.timeout)
        try:
            self.sock = self._context.wrap_socket(
                raw, server_hostname=self._verified_hostname
            )
        except Exception:
            raw.close()  # 握手失败时显式释放 fd，避免依赖 GC 回收
            raise


def _bounded_decompress(data: bytes, encoding: str, max_bytes: int) -> bytes:
    """有界解压：输出超过 max_bytes 或流未消费完时抛 decompression_limit_exceeded。"""
    if encoding == "identity":
        result = data
    else:
        window = 16 + zlib.MAX_WBITS if encoding == "gzip" else zlib.MAX_WBITS
        decompressor = zlib.decompressobj(window)
        result = decompressor.decompress(data, max_bytes + 1)
        if len(result) > max_bytes or decompressor.unconsumed_tail:
            raise RuntimeError("decompression_limit_exceeded")
        result += decompressor.flush(max_bytes + 1 - len(result))
    if len(result) > max_bytes:
        raise RuntimeError("decompression_limit_exceeded")
    return result


class URLFetcher:
    """防 SSRF/DNS rebinding/解压炸弹的 URL 抓取器。"""

    def __init__(
        self,
        timeout: float = 30,
        max_bytes: int = 10_000_000,
        max_redirects: int = 5,
        max_ratio: int = 100,
    ) -> None:
        self.timeout = timeout
        self.max_bytes = max_bytes
        self.max_redirects = max_redirects
        self.max_ratio = max_ratio

    def fetch(self, url: str) -> tuple[bytes, str, str]:
        """按策略抓取 URL，返回 (响应字节, 最终 URL, Content-Type)。

        逐跳检查 scheme/端口/主机与解析 IP，连接 pin 已检查 IP；失败抛带
        ``fetch_blocked:*`` 错误码的 RuntimeError，损坏压缩数据与未知 charset 一并归一。
        """
        current = url
        for _ in range(self.max_redirects + 1):
            parsed = urllib.parse.urlparse(current)
            try:
                port = parsed.port
            except ValueError as exc:
                raise RuntimeError("fetch_blocked:url_policy") from exc
            if (
                parsed.scheme not in {"http", "https"}
                or parsed.username
                or parsed.password
                or port not in (None, 80, 443)
            ):
                raise RuntimeError("fetch_blocked:url_policy")
            host = parsed.hostname
            if not host or host.endswith((".local", ".internal")):
                raise RuntimeError("fetch_blocked:host_policy")
            ip = self._resolve_public_ip(host)
            port = port or (443 if parsed.scheme == "https" else 80)
            connection = (
                _PinnedHTTPSConnection(ip, host, port, self.timeout)
                if parsed.scheme == "https"
                else http.client.HTTPConnection(ip, port=port, timeout=self.timeout)
            )
            target = urllib.parse.urlunsplit(
                ("", "", parsed.path or "/", parsed.query, "")
            )
            host_header = host if port in (80, 443) else f"{host}:{port}"
            try:
                connection.request(
                    "GET",
                    target,
                    headers={
                        "Host": host_header,
                        "User-Agent": "MyKnowledge/1.0",
                        "Accept-Encoding": "gzip, deflate",
                        "Connection": "close",
                    },
                )
                response = connection.getresponse()
                if response.status in {301, 302, 303, 307, 308}:
                    location = response.getheader("Location")
                    if not location:
                        raise RuntimeError("fetch_blocked:redirect_without_location")
                    current = urllib.parse.urljoin(current, location)
                    continue
                if response.status < 200 or response.status >= 300:
                    raise RuntimeError(f"fetch_blocked:http_{response.status}")
                compressed = response.read(self.max_bytes + 1)
                if len(compressed) > self.max_bytes:
                    raise RuntimeError("fetch_blocked:response_limit")
                encoding = (
                    response.getheader("Content-Encoding") or "identity"
                ).lower()
                if encoding not in {"gzip", "deflate", "identity"}:
                    raise RuntimeError("decompression_limit_exceeded:invalid_encoding")
                data = _bounded_decompress(compressed, encoding, self.max_bytes)
                if compressed and len(data) / len(compressed) > self.max_ratio:
                    raise RuntimeError("decompression_limit_exceeded")
                content_type = (
                    response.getheader("Content-Type") or "application/octet-stream"
                ).split(";")[0].strip().lower()
                return data, current, content_type
            except zlib.error as exc:
                raise RuntimeError("fetch_blocked:decompression_error") from exc
            except LookupError as exc:
                raise RuntimeError("fetch_blocked:unknown_charset") from exc
            except (OSError, http.client.HTTPException, TimeoutError) as exc:
                raise RuntimeError("fetch_blocked:request_failed") from exc
            finally:
                connection.close()
        raise RuntimeError("fetch_blocked:redirect_limit")

    @staticmethod
    def _resolve_public_ip(host: str) -> str:
        """解析主机为公网 IP；任一地址命中私网/回环/保留段即拒绝（防 SSRF）。"""
        try:
            infos = socket.getaddrinfo(host, None, type=socket.SOCK_STREAM)
        except OSError as exc:
            raise RuntimeError("fetch_blocked:dns_failure") from exc
        addresses = []
        for info in infos:
            address = ipaddress.ip_address(info[4][0])
            if (
                address.is_private
                or address.is_loopback
                or address.is_link_local
                or address.is_reserved
                or address.is_multicast
            ):
                raise RuntimeError("fetch_blocked:private_network")
            addresses.append(str(address))
        if not addresses:
            raise RuntimeError("fetch_blocked:dns_failure")
        return addresses[0]
