"""文档解析器：按媒体类型把原始字节解析为结构化 Markdown + 附件清单。

多格式摄取架构（A3）：
- 原始字节 → 附件原件（`<id>.<ext>`）+ 证据链副本（`archive/raw/`）；
- 解析结果 = 结构化 Markdown（evidence 锚定基础）+ 衍生附件（图片等）+ 元数据。

分派沿用开闭原则注册表：PDF/PPT/DOCX 走 Marker（布局感知，标题/表格/列表保真）；
HTML 走 trafilatura（网页正文）；其余按 UTF-8 文本兜底。视频/音频/图片的 parser
预留注册位，后续按同一接口实现（转录文本 + 抽帧图 → 附件）。

Marker 实测（2026-09-03，Apple M3 / Python 3.14）：
- 多进程 worker 在 macOS spawn 下会崩（`A worker process died`），须用
  `workers=None` 单进程运行（MPS 加速在进程内生效，~0.7s/页）；
- 模型首次使用下载 ~2-4GB（HF cache），后续复用；
- 输出含 `**·**` 等加粗污染，需正则清理（见 _MARKER_BOLD_NOISE）。
"""

from __future__ import annotations

import re
from collections.abc import Callable
from dataclasses import dataclass, field

from .extractor import TextExtractor

# 媒体类型 → (match, handler) 注册表类型
MatchFn = Callable[[bytes, str], bool]
ParseFn = Callable[[bytes, str], "ParseResult"]


@dataclass
class Attachment:
    """source 目录内的附件：原始件（role=original）或衍生媒体（role=derived）。"""

    filename: str  # 相对 source 目录（如 `<id>.pdf`、`media/fig1.png`）
    media_type: str
    sha256: str
    role: str  # original | derived
    kind: str = "document"  # document | image | transcript | frame

    def to_dict(self) -> dict:
        return {
            "filename": self.filename,
            "media_type": self.media_type,
            "sha256": self.sha256,
            "role": self.role,
            "kind": self.kind,
        }

    @classmethod
    def from_dict(cls, data: dict) -> Attachment:
        return cls(
            filename=data["filename"],
            media_type=data.get("media_type", ""),
            sha256=data.get("sha256", ""),
            role=data.get("role", "derived"),
            kind=data.get("kind", "document"),
        )


def media_suffix(media_type: str) -> str:
    """media_type → 文件后缀（原件落位用；未知类型回退 .bin）。"""
    mt = (media_type or "").lower()
    if "pdf" in mt:
        return ".pdf"
    if "presentationml" in mt or "pptx" in mt:
        return ".pptx"
    if "wordprocessingml" in mt or "docx" in mt:
        return ".docx"
    if "html" in mt:
        return ".html"
    if mt.startswith("text/"):
        return ".txt"
    if "jpeg" in mt or "jpg" in mt:
        return ".jpg"
    if "png" in mt:
        return ".png"
    return ".bin"


@dataclass
class ParseResult:
    """文档解析结果：Markdown 正文 + 附件清单 + 元数据。"""

    markdown: str
    attachments: list[Attachment] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)
    extractor: str = "utf8/1"


def is_marker_type(data: bytes, media_type: str) -> bool:
    """Marker 支持的类型：PDF / PPTX / DOCX（按 media_type 或魔数嗅探）。"""
    mt = (media_type or "").lower()
    if "pdf" in mt or data.startswith(b"%PDF"):
        return True
    if "presentationml" in mt or "wordprocessingml" in mt:
        return True
    return data.startswith(b"PK\x03\x04") and ("pptx" in mt or "docx" in mt)


_MARKER_BOLD_NOISE = re.compile(r"\*\*([·•\-—])\*\*")


class MarkerExtractor:
    """PDF/PPT/DOCX → 结构化 Markdown（Marker 布局感知；workers=None 规避 macOS spawn 崩溃）。"""

    def __init__(self, workers: int | None = None) -> None:
        self.workers = workers

    def parse(self, data: bytes, media_type: str) -> ParseResult:
        try:
            from marker.converters.pdf import PdfConverter
            from marker.models import create_model_dict
        except ImportError as exc:  # pragma: no cover - 依赖缺失路径
            raise RuntimeError("extractor_unavailable:marker") from exc
        try:
            import tempfile
            from pathlib import Path

            with tempfile.NamedTemporaryFile(suffix=self._suffix(media_type)) as handle:
                handle.write(data)
                handle.flush()
                artifacts = create_model_dict()
                converter = PdfConverter(artifact_dict=artifacts)
                result = converter(Path(handle.name))
        except Exception as exc:
            raise RuntimeError("extract_failed:marker") from exc
        markdown = _MARKER_BOLD_NOISE.sub(r"\1", result.markdown or "")
        attachments = self._collect_attachments(result)
        metadata = {
            k: v
            for k, v in (result.metadata or {}).items()
            if isinstance(v, (str, int, float, bool, list))
        }
        return ParseResult(
            markdown=markdown.strip(),
            attachments=attachments,
            metadata=metadata,
            extractor="marker/" + _marker_version(),
        )

    def _suffix(self, media_type: str) -> str:
        mt = (media_type or "").lower()
        if "pdf" in mt or "%pdf" in mt:
            return ".pdf"
        if "presentationml" in mt:
            return ".pptx"
        if "wordprocessingml" in mt:
            return ".docx"
        return ".bin"

    def _collect_attachments(self, result) -> list[Attachment]:
        """把 Marker 抽取的图片登记为衍生附件（写盘由调用方按 filename 落位）。"""
        images = getattr(result, "images", None) or {}
        attachments: list[Attachment] = []
        for ref, image in images.items():
            if not isinstance(image, object):
                continue
            # 记录 filename（markdown 里的引用 ref）与媒介类型；写盘用 media/
            fmt = getattr(image, "format", None) or "PNG"
            ext = (fmt or "png").lower()
            attachments.append(
                Attachment(
                    filename=f"media/{ref}.{ext}",
                    media_type=f"image/{ext}",
                    sha256="",
                    role="derived",
                    kind="image",
                )
            )
        return attachments


def _marker_version() -> str:
    try:
        from importlib.metadata import PackageNotFoundError, version

        return version("marker-pdf")
    except PackageNotFoundError:
        return "unknown"


class DocumentParser:
    """多格式文档解析器（注册表分派，开闭原则）。

    Marker 类型（PDF/PPT/DOCX）→ 结构化 Markdown + 附件；
    其余 → TextExtractor 纯文本兜底（HTML/personal 行为不变）。
    视频/音频/图片 parser 后续按 ParseFn 注册，不修改 parse 本体。
    """

    def __init__(self) -> None:
        self._handlers: list[tuple[MatchFn, ParseFn]] = []
        self._text = TextExtractor()
        self._register_defaults()

    def _register_defaults(self) -> None:
        marker = MarkerExtractor()
        self.register(is_marker_type, marker.parse)
        # 非 Marker 类型委托旧 TextExtractor（HTML→trafilatura、纯文本兜底），行为不变
        self.register(lambda data, mt: not is_marker_type(data, mt), self._parse_text)

    def _parse_text(self, data: bytes, media_type: str) -> ParseResult:
        text, extractor = self._text.extract(data, media_type)
        return ParseResult(markdown=text, extractor=extractor)

    def register(self, match: MatchFn, handler: ParseFn) -> None:
        self._handlers.append((match, handler))

    def parse(self, data: bytes, media_type: str) -> ParseResult:
        """按媒体类型解析；无命中时回落 UTF-8 纯文本（与旧 TextExtractor 行为一致）。"""
        for match, handler in self._handlers:
            if match(data, media_type):
                return handler(data, media_type)
        return ParseResult(
            markdown=data.decode("utf-8", errors="replace").strip(),
            extractor="utf8/1",
        )
