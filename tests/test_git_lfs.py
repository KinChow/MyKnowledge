from __future__ import annotations

import subprocess
from pathlib import Path

from tools.git_lfs import (
    is_lfs_pointer,
    lfs_index_errors,
    require_pdf_lfs,
)
from tools.ingest.source_ingestor import SourceIngestor

POINTER = (
    b"version https://git-lfs.github.com/spec/v1\n"
    b"oid sha256:" + b"0" * 64 + b"\n"
    b"size 4\n"
)


def git(root: Path, *args: str) -> None:
    subprocess.run(["git", "-C", str(root), *args], check=True)


def add_raw_blob(root: Path, path: Path) -> None:
    blob = subprocess.check_output(
        ["git", "-C", str(root), "hash-object", "--no-filters", "-w", str(path)]
    )
    blob_id = blob.decode().strip()
    git(
        root,
        "update-index",
        "--add",
        "--cacheinfo",
        f"100644,{blob_id},{path.relative_to(root)}",
    )


def init_repo(tmp_path: Path) -> Path:
    root = tmp_path / "repo"
    root.mkdir()
    git(root, "init", "-q")
    git(root, "config", "user.name", "Fixture")
    git(root, "config", "user.email", "fixture@example.invalid")
    (root / ".gitattributes").write_text(
        "/content/sources/**/*.pdf filter=lfs diff=lfs merge=lfs -text\n",
        encoding="utf-8",
    )
    return root


def test_lfs_index_check_rejects_regular_blob_under_lfs_rule(tmp_path: Path):
    root = init_repo(tmp_path)
    path = root / "content/sources/tools/example/example.pdf"
    path.parent.mkdir(parents=True)
    path.write_bytes(b"%PDF-regular")
    git(root, "add", ".gitattributes")
    add_raw_blob(root, path)
    errors = lfs_index_errors(root)
    assert errors == [
        {
            "path": "content/sources/tools/example/example.pdf",
            "code": "lfs_pointer_required",
        }
    ]


def test_lfs_index_check_accepts_pointer_under_lfs_rule(tmp_path: Path):
    root = init_repo(tmp_path)
    path = root / "content/sources/tools/example/example.pdf"
    path.parent.mkdir(parents=True)
    path.write_bytes(POINTER)
    git(root, "add", ".")
    assert is_lfs_pointer(POINTER)
    assert lfs_index_errors(root) == []


def test_pdf_policy_requires_repository_lfs_attribute(tmp_path: Path):
    root = init_repo(tmp_path)
    (root / ".gitattributes").write_text("", encoding="utf-8")
    assert (
        require_pdf_lfs(root, "content/sources/tools/example/example.pdf")
        == "pdf_lfs_rule_missing"
    )


def test_pdf_import_is_blocked_before_parsing_without_lfs(tmp_path: Path):
    root = init_repo(tmp_path)
    (root / ".gitattributes").write_text("", encoding="utf-8")
    source = root / "input.pdf"
    source.write_bytes(b"%PDF-not-imported")
    result = SourceIngestor(root).ingest(
        {
            "source_type": "local-file",
            "domain": "tools",
            "input_path": str(source),
            "source_id": "pdf-without-lfs",
            "media_type": "application/pdf",
        }
    )
    assert result["status"] == "blocked"
    assert result["error_code"] == "source_ingest_failed"
    assert result["errors"][0]["code"] == "pdf_lfs_rule_missing"
