from pathlib import Path

from tools.migrate_legacy import preview


def test_migration_preview_is_source_first_and_does_not_write(tmp_path: Path):
    docs = tmp_path / "docs"
    docs.mkdir()
    source = docs / "guide.md"
    source.write_text("# Guide\n\nSee [other](other.md).\n", encoding="utf-8")
    before = source.read_bytes()
    result = preview(tmp_path)
    assert result["schema_version"] == "legacy-migration/v1"
    assert result["writes_applied"] is False
    assert result["pending"] == 1 and result["completed"] == 0
    item = result["items"][0]
    assert item["source_target"]["object_type"] == "source"
    assert item["wiki_target"]["object_type"] == "wiki"
    assert item["status"] == "pending"
    assert source.read_bytes() == before


def test_migration_preview_changes_with_input_tree(tmp_path: Path):
    docs = tmp_path / "docs"
    docs.mkdir()
    path = docs / "a.md"
    path.write_text("# A\n", encoding="utf-8")
    first = preview(tmp_path)["preview_sha256"]
    path.write_text("# B\n", encoding="utf-8")
    assert preview(tmp_path)["preview_sha256"] != first
