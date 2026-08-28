"""正文提取器：按媒体类型从原始字节提取纯文本。

HTML 提取使用 trafilatura（网页正文提取专用，剔除导航/页脚/侧栏、自动检测
charset）；PDF 走 pypdf。注册表分派（match/handler）保持开闭原则。

异常策略：提取失败不降级、不回退——异常归一到结构化错误码
（extractor_unavailable:*/extract_failed:*）暴露给调用方转 blocked，
修复问题优于规避问题；非文章页返回空文本由调用方 source_empty 拒绝。
"""

from __future__ import annotations

import io
from collections.abc import Callable

# 媒体类型 → (match, handler) 注册表类型
MatchFn = Callable[[bytes, str], bool]
ExtractFn = Callable[[bytes, str], tuple[str, str]]


class TextExtractor:
    """按媒体类型从原始字节提取正文的提取器（注册表分派，开闭原则）。

    新增提取器通过 :meth:`register` 注册 match/handler，不修改 extract 本体。
    """

    def __init__(self) -> None:
        self._handlers: list[tuple[MatchFn, ExtractFn]] = []
        self._register_defaults()

    def _register_defaults(self) -> None:
        """注册内置 HTML/PDF 提取器（可按媒体类型或内容嗅探匹配）。"""
        self.register(
            lambda data, media_type: (
                "html" in media_type
                or data.lstrip().lower().startswith((b"<!doctype html", b"<html"))
            ),
            self._extract_html,
        )
        self.register(
            lambda data, media_type: "pdf" in media_type or data.startswith(b"%PDF"),
            self._extract_pdf,
        )
        self.register(
            lambda data, media_type: (
                "wordprocessingml.document" in media_type
                or data.startswith(b"PK\x03\x04")
                and "docx" in media_type
            ),
            self._extract_docx,
        )

    def register(self, match: MatchFn, handler: ExtractFn) -> None:
        """注册提取器：match 判定 (data, media_type) 是否命中，handler 执行提取。"""
        self._handlers.append((match, handler))

    def extract(self, data: bytes, media_type: str) -> tuple[str, str]:
        """按媒体类型提取正文，返回 (文本, extractor 版本)；无命中时按 UTF-8 文本处理。"""
        for match, handler in self._handlers:
            if match(data, media_type):
                return handler(data, media_type)
        return data.decode("utf-8", errors="replace"), "utf8/1"

    def _extract_html(self, data: bytes, media_type: str) -> tuple[str, str]:  # noqa: ARG002 - handler 表统一签名
        """HTML 正文提取：trafilatura 剔除导航/脚本并自动检测编码。

        来源：https://github.com/adbar/trafilatura（Apache-2.0）
        未安装 → extractor_unavailable:trafilatura；提取异常 → extract_failed:trafilatura。
        """
        try:
            from importlib.metadata import version

            import trafilatura
        except ImportError as exc:
            raise RuntimeError("extractor_unavailable:trafilatura") from exc
        try:
            text = trafilatura.extract(
                data,
                include_comments=False,
                include_tables=False,
                favor_precision=True,
                output_format="txt",
            )
        except Exception as exc:
            raise RuntimeError("extract_failed:trafilatura") from exc
        return (text or "").strip(), "trafilatura/" + version("trafilatura")

    def _extract_pdf(self, data: bytes, media_type: str) -> tuple[str, str]:  # noqa: ARG002 - handler 表统一签名
        """PDF 提取：pypdf 逐页抽取文本。

        未安装 → extractor_unavailable:pypdf；解析异常 → extract_failed:pypdf。
        """
        try:
            from pypdf import PdfReader, __version__
        except ImportError as exc:
            raise RuntimeError("extractor_unavailable:pypdf") from exc
        try:
            text = "\n".join(
                page.extract_text() or "" for page in PdfReader(io.BytesIO(data)).pages
            ).strip()
        except Exception as exc:
            raise RuntimeError("extract_failed:pypdf") from exc
        return text, "pypdf/" + __version__

    def _extract_docx(self, data: bytes, media_type: str) -> tuple[str, str]:  # noqa: ARG002 - handler 表统一签名
        """DOCX extraction via Docling; absence is an explicit blocked boundary."""
        try:
            from importlib.metadata import version

            from docling.document_converter import DocumentConverter
        except ImportError as exc:
            raise RuntimeError("extractor_unavailable:docling") from exc
        try:
            import tempfile
            from pathlib import Path

            with tempfile.NamedTemporaryFile(suffix=".docx") as handle:
                handle.write(data)
                handle.flush()
                document = DocumentConverter().convert(Path(handle.name)).document
                text = document.export_to_markdown()
        except Exception as exc:
            raise RuntimeError("extract_failed:docling") from exc
        return text.strip(), "docling/" + version("docling")
