"""Safe file reads at the public boundary (shared by projection and staging)."""

from pathlib import Path

from .common import canonical_body, read_stable, sha256_text
from .front_matter import FrontMatter


def read_public_file(
    root: Path, relative: str, *, prefix: str = "content/wiki"
) -> bytes:
    root = root.resolve()
    rel = Path(relative)
    allowed = Path(prefix).parts
    if (
        not relative
        or rel.is_absolute()
        or ".." in rel.parts
        or "\\" in relative
        or rel.parts[: len(allowed)] != allowed
    ):
        raise ValueError("projection_path_invalid")
    path = root
    for part in rel.parts:
        path /= part
        if path.is_symlink():
            raise ValueError("projection_path_invalid")
    if not path.resolve().is_relative_to(root / prefix):
        raise ValueError("projection_path_invalid")
    if not path.is_file() or path.stat().st_nlink != 1:
        raise ValueError("projection_body_unavailable")
    try:
        data, stat = read_stable(path)
    except RuntimeError as exc:
        raise ValueError("projection_body_stale") from exc
    if stat.st_nlink != 1:
        raise ValueError("projection_body_unavailable")
    return data


def read_public_body(root: Path, item: dict) -> tuple[dict, str, str]:
    text = read_public_file(root, str(item.get("body_path", ""))).decode("utf-8")
    metadata, body = FrontMatter.parse(text)
    if sha256_text(canonical_body(body)) != item.get("content_sha256"):
        raise ValueError("projection_body_stale")
    if metadata and (
        metadata.get("status") != "published"
        or metadata.get("publication_scope") != "public"
        or metadata.get("confidentiality") != "public"
    ):
        raise ValueError("projection_body_stale")
    return metadata, body, text
