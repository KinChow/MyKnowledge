from pathlib import Path

from tools.migrate_legacy import apply_sample, preview


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


def test_representative_sample_applies_source_then_draft_wiki(tmp_path: Path):
    docs = tmp_path / "docs"; docs.mkdir()
    source = docs / "guide.md"; source.write_text("# Guide\n\nA migrated note.\n", encoding="utf-8")
    pending = apply_sample(tmp_path, "docs/guide.md")
    assert pending["state"] == "awaiting_confirmation"
    applied = apply_sample(tmp_path, "docs/guide.md", confirmed=True)
    assert applied["state"] == "applied"
    assert applied["writes_applied"] is True
    assert source.exists()
    source_file = tmp_path / "sources" / "tools" / "legacy-docs-guide-source.md"
    wiki_file = tmp_path / "wiki" / "tools" / "legacy-docs-guide.md"
    assert source_file.exists() and wiki_file.exists()
    assert "status: draft" in wiki_file.read_text(encoding="utf-8")
    assert "A migrated note." in source_file.read_text(encoding="utf-8")


def test_sample_apply_missing_item_is_fail_closed(tmp_path: Path):
    (tmp_path / "docs").mkdir()
    result = apply_sample(tmp_path, "docs/missing.md", confirmed=True)
    assert result["state"] == "blocked"
    assert result["writes_applied"] is False


def test_sample_apply_repairs_only_inventory_links_and_reports_unresolved(tmp_path: Path):
    docs = tmp_path / "docs"; docs.mkdir()
    (docs / "target.md").write_text("# Target\n", encoding="utf-8")
    (docs / "guide.md").write_text("# Guide\n\n[Target](target.md) [Missing](missing.md) [Web](https://example.com)\n", encoding="utf-8")
    result = apply_sample(tmp_path, "docs/guide.md", confirmed=True)
    assert result["state"] == "applied"
    assert result["link_repair"]["repaired"] == [{"from": "target.md", "to": "/legacy/docs-target"}]
    assert result["link_repair"]["unresolved"] == ["missing.md"]
    body = (tmp_path / "wiki" / "tools" / "legacy-docs-guide.md").read_text(encoding="utf-8")
    assert "](/legacy/docs-target)" in body
    assert "](missing.md)" in body


def test_migrate_cli_applies_confirmed_sample(tmp_path: Path):
    import json, subprocess, sys
    docs = tmp_path / "docs"; docs.mkdir(); (docs / "cli.md").write_text("# CLI\n", encoding="utf-8")
    result = subprocess.run([sys.executable, "-m", "tools.cli", "migrate", "--root", str(tmp_path), "--apply-sample", "docs/cli.md", "--confirm"], capture_output=True, text=True, check=False)
    assert result.returncode == 0
    assert json.loads(result.stdout)["state"] == "applied"


def test_reapplying_sample_is_idempotent_and_does_not_duplicate_objects(tmp_path: Path):
    docs = tmp_path / "docs"; docs.mkdir()
    (docs / "guide.md").write_text("# Guide\n\nStable content.\n", encoding="utf-8")
    first = apply_sample(tmp_path, "docs/guide.md", confirmed=True)
    source = tmp_path / "sources" / "tools" / "legacy-docs-guide-source.md"
    wiki = tmp_path / "wiki" / "tools" / "legacy-docs-guide.md"
    first_bytes = (source.read_bytes(), wiki.read_bytes())
    second = apply_sample(tmp_path, "docs/guide.md", confirmed=True)
    assert first["state"] == second["state"] == "applied"
    assert second.get("replayed") is True
    assert (source.read_bytes(), wiki.read_bytes()) == first_bytes
    assert len(list((tmp_path / "sources").rglob("legacy-docs-guide-source.md"))) == 1
    assert len(list((tmp_path / "wiki").rglob("legacy-docs-guide.md"))) == 1
    assert len(list((tmp_path / "audit" / "migrations").glob("*.json"))) == 1

def test_tampered_migration_record_is_not_replayed(tmp_path: Path):
    docs = tmp_path / "docs"; docs.mkdir()
    (docs / "guide.md").write_text("# Guide\n\nStable content.\n", encoding="utf-8")
    first = apply_sample(tmp_path, "docs/guide.md", confirmed=True)
    record_path = next((tmp_path / "audit" / "migrations").glob("*.json"))
    record = __import__("json").loads(record_path.read_text(encoding="utf-8"))
    record["result"]["state"] = "forged"
    record_path.write_text(__import__("json").dumps(record), encoding="utf-8")
    replay = apply_sample(tmp_path, "docs/guide.md", confirmed=True)
    assert first["state"] == "applied"
    assert replay["state"] == "applied"
    assert replay.get("replayed") is not True


def test_migration_preview_blocks_normalized_id_collision_before_writes(tmp_path: Path):
    docs = tmp_path / "docs"; docs.mkdir()
    (docs / "a").mkdir()
    (docs / "a" / "one.md").write_text("# A\n", encoding="utf-8")
    (docs / "a-one.md").write_text("# a\n", encoding="utf-8")
    plan = preview(tmp_path)
    assert plan["conflicts"][0]["code"] == "stable_id_collision"
    blocked = [item for item in plan["items"] if item["status"] == "blocked"]
    assert len(blocked) == 1
    result = apply_sample(tmp_path, blocked[0]["legacy_path"], confirmed=True)
    assert result == {"state": "blocked", "error_code": "stable_id_collision", "writes_applied": False, "item": blocked[0]}
