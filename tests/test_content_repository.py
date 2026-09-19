"""locate_managed_object 的共享定位契约测试（P1）。"""

from __future__ import annotations

from pathlib import Path

import pytest

from tools.content_repository import ObjectResolutionError, locate_managed_object


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_locate_finds_unique_managed_object(tmp_path: Path):
    target = tmp_path / "content" / "wiki" / "cs" / "transformer.md"
    _write(target, "---\nschema_version: wiki/v1\n---\nbody\n")
    assert locate_managed_object(tmp_path, "wiki", "transformer") == target


def test_locate_missing_is_object_not_found(tmp_path: Path):
    with pytest.raises(ObjectResolutionError) as exc:
        locate_managed_object(tmp_path, "wiki", "missing")
    assert exc.value.code == "object_not_found"


def test_locate_invalid_id_is_invalid_object_ref(tmp_path: Path):
    with pytest.raises(ObjectResolutionError) as exc:
        locate_managed_object(tmp_path, "wiki", "../etc")
    assert exc.value.code == "invalid_object_ref"


def test_locate_unknown_type_is_object_type_not_found(tmp_path: Path):
    with pytest.raises(ObjectResolutionError) as exc:
        locate_managed_object(tmp_path, "question", "anything")
    assert exc.value.code == "object_type_not_found"


def test_locate_ambiguous_reports_matches(tmp_path: Path):
    _write(tmp_path / "content" / "sources" / "cs" / "dup" / "dup.md", "x\n")
    _write(tmp_path / "content" / "sources" / "cs" / "other" / "dup.md", "y\n")
    with pytest.raises(ObjectResolutionError) as exc:
        locate_managed_object(tmp_path, "source", "dup")
    assert exc.value.code == "object_id_ambiguous"
    assert len(exc.value.matches) == 2


def test_locate_rejects_symlinked_object(tmp_path: Path):
    outside = tmp_path / "outside.md"
    _write(outside, "x\n")
    link_dir = tmp_path / "content" / "wiki" / "cs"
    link_dir.mkdir(parents=True, exist_ok=True)
    (link_dir / "linky.md").symlink_to(outside)
    with pytest.raises(ObjectResolutionError) as exc:
        locate_managed_object(tmp_path, "wiki", "linky")
    assert exc.value.code == "object_not_found"
