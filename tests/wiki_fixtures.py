"""Wiki 测试共享 fixture（F002 各模块测试复用）。

从真实产物构造（F001 evidence_anchor 集成测试见 test_wiki_resolution），
避免手写键名与实现同源的自证陷阱。
"""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from tools.common import canonical_quote, sha256_text, strip_sha256_prefix
from tools.front_matter import FrontMatter
from tools.validation import WikiValidator

WIKI_BODY = """# 测试主题

## 一句话结论

结论内容。

## 核心概念

概念内容。

## 工作机制

机制内容。

## 示例或代码

示例内容。

## 常见误区

误区内容。

## 证据映射

映射内容。

## 待验证项

待验证内容。

## 关联知识

关联内容。
"""

# 引文 ≥ quote_min_chars(12)：规范化后 16 字符
QUOTE_EXACT = "用于引文匹配的原文片段，以及更多"

SOURCE_BODY = "这是一个足够长的 source 正文，包含" + QUOTE_EXACT + "填充内容。"


def _install_spec_doc(root: Path) -> None:
    """把仓库真实规范文档复制到测试 root（ruleset 抽取的 fixture 须来自真实产物）。

    F003：ruleset_sha256 依赖 docs/myknowledge-system-design.md 实时抽取；
    测试临时目录没有该文档时，pass 报告会被保守标 stale_ruleset。
    """
    repo_root = Path(__file__).resolve().parent.parent
    src = repo_root / "docs" / "myknowledge-system-design.md"
    target = root / "docs" / "myknowledge-system-design.md"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")


def _make_source(
    root: Path,
    source_id: str,
    domain: str = "tools",
    body: str = SOURCE_BODY,
    evidence_items: list[dict] | None = None,
    **metadata_overrides: object,
) -> str:
    """构造 source 文件 + archive snapshot，返回 snapshot_sha256。"""
    snapshot_sha = sha256_text(body)
    snapshot_path = root / "archive" / "text" / f"{strip_sha256_prefix(snapshot_sha)}.md"
    snapshot_path.parent.mkdir(parents=True, exist_ok=True)
    snapshot_path.write_text(body, encoding="utf-8")
    metadata = {
        "schema_version": "source/v1",
        "id": source_id,
        "domain": domain,
        "vault_id": "public",
        "source_type": "local-file",
        "origin": "external",
        "retrieval": {"acquisition": "local-file"},
        "snapshot_sha256": snapshot_sha,
        "extractor": "utf8/1",
        "media_type": "text/markdown",
        "read_status": "retrieved",
        "evidence_status": "source-reported",
        "confidentiality": "public",
        "archive_policy": "text-only",
        "evidence_items": evidence_items or [],
    }
    metadata.update(metadata_overrides)
    path = root / "sources" / domain / f"{source_id}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(FrontMatter.render(metadata, body), encoding="utf-8")
    return snapshot_sha


def _evidence_item(evidence_id: str, body: str, exact: str) -> dict:
    """在 body 中定位 exact 构造 evidence item（code-point 偏移）。"""
    start = body.index(exact)
    return {
        "id": evidence_id,
        "snapshot_sha256": sha256_text(body),
        "selector": {"type": "TextQuoteSelector", "exact": exact},
        "position": {"type": "TextPositionSelector", "start": start, "end": start + len(exact)},
        "selector_sha256": sha256_text(exact),
        "quote_sha256": sha256_text(canonical_quote(exact)),
    }


def _write_wiki(root: Path, metadata: dict, body: str = WIKI_BODY) -> Path:
    path = root / "wiki" / metadata["domain"] / f"{metadata['id']}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(FrontMatter.render(metadata, body), encoding="utf-8")
    return path


def _base_wiki(**overrides: object) -> dict:
    """合法 knowledge Wiki 的默认 front matter（覆盖项可改）。"""
    meta = {
        "id": "test-wiki",
        "title": "测试主题",
        "domain": "tools",
        "kind": "knowledge",
        "status": "draft",
        "publication_scope": "none",
        "confidentiality": "public",
        "tags": ["test"],
        "aliases": [],
        "related": [],
        "sources": ["test-source"],
        "evidence": [
            {
                "claim_id": "c1",
                "claim": "测试论断。",
                "targets": [{"source_id": "test-source", "evidence_id": "e1"}],
                "support": "direct",
                "supporting_quotes": [
                    {"evidence_id": "e1", "exact": QUOTE_EXACT}
                ],
            }
        ],
        "updated_at": "2026-08-26",
    }
    meta.update(overrides)
    return meta


def root_replace(path: Path, new_name: str) -> Path:
    """返回同目录下不同文件名的 Path（用于 planned 测试的独立文件）。"""
    return path.parent / f"{new_name}.md"


class WikiTestCase(unittest.TestCase):
    """构造 source + snapshot + wiki 的完整 fixture，返回 (wiki_path, validator)。"""

    def _fixture(self, wiki: dict) -> tuple[Path, WikiValidator]:
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        root = Path(directory.name)
        _make_source(
            root,
            "test-source",
            evidence_items=[
                _evidence_item("e1", SOURCE_BODY, QUOTE_EXACT)
            ],
        )
        wiki_path = _write_wiki(root, wiki)
        return wiki_path, WikiValidator(root)

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
