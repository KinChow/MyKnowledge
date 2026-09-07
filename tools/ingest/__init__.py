"""导入与归档职责域（F001；F010 存量迁移归入本包）。

命名对齐 kernelwiki-kunlun/scripts 的职责域组织方式（validation/ingest/gates）。
对外接口：``SourceIngestor``（两阶段写入口）、``URLFetcher``（防 SSRF 抓取）、
``TextExtractor``（正文提取）、``SourceValidator``（source 请求/文件校验）。
"""

from .extractor import TextExtractor
from .fetcher import URLFetcher
from .source_ingestor import SourceIngestor
from .source_validator import SourceValidator
from .video_asr import transcribe_openai_whisper, transcribe_whisper_cpp
from .video_frames import VideoFrameService, extract_keyframes
from .video_inventory import build_inventory, classify_language, validate_video_url
from .video_subtitles import acquire_subtitles
from .video_transcript import normalize_file, parse_subtitles, render_transcript

__all__ = [
    "SourceIngestor",
    "URLFetcher",
    "TextExtractor",
    "SourceValidator",
    "build_inventory",
    "classify_language",
    "validate_video_url",
    "acquire_subtitles",
    "transcribe_whisper_cpp",
    "transcribe_openai_whisper",
    "VideoFrameService",
    "extract_keyframes",
    "normalize_file",
    "parse_subtitles",
    "render_transcript",
]
