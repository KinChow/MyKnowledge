import tempfile
from pathlib import Path

from tools.inventory_legacy import inventory


def test_inventory_has_tree_hash_and_pending_boundaries():
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        docs = root / "docs"
        docs.mkdir()
        (docs / "a.md").write_text(
            "# Article\n\nSee [source](https://example.com).\n", encoding="utf-8"
        )
        (docs / "index.md").write_text("# Index\n", encoding="utf-8")
        result = inventory(root)
        assert result["schema_version"] == "migration-inventory/v1"
        assert result["input_tree_sha256"].startswith("sha256:")
        assert all(item["status"] == "pending" for item in result["items"])
        assert result["items"][0]["external_urls"] == ["https://example.com"]


def test_inventory_hash_changes_when_input_changes():
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        (root / "docs").mkdir()
        p = root / "docs" / "a.md"
        p.write_text("# A\n", encoding="utf-8")
        first = inventory(root)["input_tree_sha256"]
        p.write_text("# B\n", encoding="utf-8")
        assert inventory(root)["input_tree_sha256"] != first
