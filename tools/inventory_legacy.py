"""Deterministic legacy docs inventory (F010)."""
from __future__ import annotations
import hashlib, json, re, time
import mimetypes
from pathlib import Path
from .common import canonical_json, sha256_bytes

CLASSIFIER_VERSION = "legacy-classifier/v1"

def _tree_hash(files: list[Path], root: Path) -> str:
    entries = [{"path": str(p.relative_to(root)), "sha256": sha256_bytes(p.read_bytes())} for p in files]
    return "sha256:" + hashlib.sha256(canonical_json(entries)).hexdigest()

def inventory(root: Path, docs_dir: Path | None = None) -> dict:
    root = Path(root).resolve(); source = (docs_dir or root / "docs").resolve()
    supported = {".md", ".html", ".htm", ".pdf", ".txt", ".docx"}
    files = sorted([p for p in source.rglob("*") if p.is_file() and not p.is_symlink() and p.suffix.lower() in supported], key=lambda p: str(p.relative_to(root)))
    items = []
    for path in files:
        is_binary = path.suffix.lower() in {".pdf", ".docx"}
        body = path.read_text(encoding="utf-8", errors="replace") if not is_binary else ""
        title = next((line.lstrip("# ").strip() for line in body.splitlines() if line.startswith("#")), None)
        links = re.findall(r"\[[^\]]+\]\(([^)]+)\)", body)
        urls = [x for x in links if re.match(r"https?://", x)]
        nonempty = bool(body.strip()); heading_count = sum(1 for line in body.splitlines() if line.startswith("#"))
        # contents.md 一律 index（R2 导航页语义）：富目录页 heading 多/超 500B，
        # 旧阈值把它们误判为 article，曾导致 69 篇导航页混入迁移并同名互撞
        shape = "empty" if not nonempty else ("index" if path.name == "contents.md" or (heading_count <= 1 and len(body) < 500) else "article")
        media_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        extractor = "docling" if path.suffix.lower() == ".docx" else ("pypdf" if path.suffix.lower() == ".pdf" else ("trafilatura" if "html" in media_type else "utf8"))
        items.append({"legacy_path": str(path.relative_to(root)), "body_sha256": sha256_bytes(path.read_bytes()), "byte_length": path.stat().st_size, "title": title, "shape": shape, "external_urls": urls, "media_type": media_type, "extractor": extractor, "route": "/" + str(path.relative_to(source)).rsplit(".", 1)[0], "source_target": None, "wiki_target": None, "evidence_state": "pending", "target_vault": "public", "status": "pending"})
    result = {"schema_version": "migration-inventory/v1", "generated_at": time.time(), "input_tree_sha256": _tree_hash(files, root), "classifier_version": CLASSIFIER_VERSION, "thresholds": {"index_max_bytes": 500}, "items": items}
    result["inventory_sha256"] = "sha256:" + hashlib.sha256(canonical_json({k:v for k,v in result.items() if k != "inventory_sha256"})).hexdigest()
    return result

def main(argv: list[str] | None = None) -> int:
    import argparse
    parser = argparse.ArgumentParser(description="Build legacy docs migration inventory")
    parser.add_argument("--root", type=Path, default=Path.cwd()); parser.add_argument("--docs", type=Path); parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv); result = inventory(args.root, args.docs)
    data = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output: args.output.write_text(data, encoding="utf-8")
    else: print(data, end="")
    return 0
