import unittest, tempfile
import subprocess
from pathlib import Path
from unittest import mock
from tools.indexing import IndexBuilder, QMDAdapter, Retriever, SQLiteIndex
from tools.vault_registry import VaultRegistry

ITEMS = [
    {"vault_id": "public", "object_id": "pub", "title": "公开知识", "body": "SQLite 检索", "public_publishable": True, "public_release": True, "status": "published", "effective_confidentiality": "public", "content_sha256": "sha256:p"},
    {"vault_id": "private", "object_id": "priv", "title": "私有知识", "body": "SQLite 检索", "confidentiality": "internal", "public_publishable": False, "content_sha256": "sha256:i"},
    {"vault_id": "private", "object_id": "down", "title": "不可用", "body": "secret", "availability": "unavailable", "availability_reason": "vault_unavailable", "confidentiality": "internal"},
]

class IndexingTests(unittest.TestCase):
    def test_public_projection_filters_private(self):
        result = IndexBuilder(None).build(ITEMS, "public")
        self.assertEqual([x["object_ref"]["object_id"] for x in result["items"]], ["pub"])

    def test_registry_projection_feeds_owner_aware_index(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); public = root / "public"; private = root / "private"
            for vault, title in ((public, "Public"), (private, "Private")):
                (vault / "wiki").mkdir(parents=True)
                (vault / "wiki" / "same.md").write_text(f"# {title}\nSQLite", encoding="utf-8")
                subprocess.run(["git", "init", "-q", str(vault)], check=True)
            manifest = root / "manifest.yaml"
            manifest.write_text(f"schema_version: 1\nlayout: superproject\nworkspace_root: {root}\nvaults:\n  - {{id: public, path: public}}\n  - {{id: private, path: private, confidentiality: internal}}\n", encoding="utf-8")
            result = IndexBuilder(root).build_from_registry(VaultRegistry(public, manifest))
            self.assertEqual({x["object_ref"]["vault_id"] for x in result["items"]}, {"public", "private"})
            self.assertTrue(result["projection_sha256"].startswith("sha256:"))

    def test_public_projection_requires_complete_release_allowlist(self):
        draft = {**ITEMS[0], "object_id": "draft", "status": "draft"}
        unreleased = {**ITEMS[0], "object_id": "unreleased", "public_release": False}
        internal = {**ITEMS[0], "object_id": "internal", "effective_confidentiality": "internal"}
        result = IndexBuilder(None).build([ITEMS[0], draft, unreleased, internal], "public")
        self.assertEqual([x["object_ref"]["object_id"] for x in result["items"]], ["pub"])

    def test_private_scope_excludes_public_owner(self):
        result = IndexBuilder(None).build(ITEMS, "private")
        self.assertEqual({x["object_ref"]["vault_id"] for x in result["items"]}, {"private"})

    def test_vault_allowlist_is_applied_before_retrieval_result_generation(self):
        result = Retriever(ITEMS).search("SQLite", "local", vault_ids=["public"])
        self.assertEqual({x["object_ref"]["vault_id"] for x in result["items"]}, {"public"})
        result = Retriever(ITEMS).search("SQLite", "private")
        self.assertEqual({x["object_ref"]["vault_id"] for x in result["items"]}, {"private"})

    def test_local_keeps_owner_and_hides_unavailable_body(self):
        result = IndexBuilder(None).build(ITEMS)
        down = next(x for x in result["items"] if x["object_ref"]["object_id"] == "down")
        self.assertIsNone(down["body"]); self.assertEqual(down["object_ref"]["vault_id"], "private")

    def test_fallback_search_and_limits(self):
        retriever = Retriever(ITEMS)
        self.assertEqual(retriever.search("SQLite", "public")["items"][0]["object_ref"]["object_id"], "pub")
        self.assertEqual(retriever.search("x", top_k=101)["availability_reason"], "query_limit_exceeded")

    def test_retriever_enforces_vault_id_limit_before_provider(self):
        retriever = Retriever(ITEMS)
        result = retriever.search("SQLite", "local", vault_ids=[f"vault-{i}" for i in range(17)])
        self.assertEqual(result["availability_reason"], "query_limit_exceeded")
        self.assertEqual(result["items"], [])

    def test_unavailable_metadata_is_searchable_without_body(self):
        result = Retriever(ITEMS).search("不可用", "local")
        self.assertEqual(result["items"][0]["availability"], "unavailable")
        self.assertEqual(result["items"][0]["availability_reason"], "vault_unavailable")
        self.assertIsNone(result["items"][0]["snippet"])

    def test_sqlite_fts5_rebuild_and_search(self):
        with tempfile.TemporaryDirectory() as d:
            idx = SQLiteIndex(Path(d) / "index.sqlite3")
            manifest = idx.rebuild(ITEMS, "public")
            self.assertEqual(manifest["item_count"], 1)
            self.assertEqual(idx.search("SQLite")[0]["object_ref"]["object_id"], "pub")

    def test_retriever_prefers_persistent_fts5_when_available(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "index.sqlite3"
            SQLiteIndex(path).rebuild(ITEMS, "public")
            result = Retriever(ITEMS, path).search("SQLite", "public")
            self.assertEqual(result["method"], "fts5")
            self.assertIn("qmd_unavailable", result["warnings"])

    def test_retriever_rejects_stale_fts5_index(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "index.sqlite3"
            SQLiteIndex(path).rebuild(ITEMS, "public")
            changed = [dict(item) for item in ITEMS]
            changed[0]["title"] = "changed"
            result = Retriever(changed, path).search("SQLite", "public")
            self.assertEqual(result["method"], "deterministic-fallback")
            self.assertIn("fts5_unavailable", result["warnings"])

    def test_rebuild_retains_previous_index(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "index.sqlite3"
            SQLiteIndex(path).rebuild(ITEMS, "public")
            SQLiteIndex(path).rebuild([ITEMS[0]], "public")
            previous = path.with_suffix(".sqlite3.previous")
            self.assertTrue(previous.exists())
            self.assertEqual(SQLiteIndex(previous).scope(), "public")

    def test_rebuild_swap_failure_restores_previous_index(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "index.sqlite3"
            index = SQLiteIndex(path)
            index.rebuild(ITEMS, "public")
            original = path.read_bytes()
            real_replace = __import__("os").replace
            calls = {"count": 0}

            def fail_new(source, destination):
                calls["count"] += 1
                if calls["count"] == 2:
                    raise OSError("injected index swap failure")
                return real_replace(source, destination)

            with mock.patch("tools.indexing.os.replace", side_effect=fail_new):
                with self.assertRaisesRegex(OSError, "injected index swap failure"):
                    index.rebuild([ITEMS[0]], "public")
            self.assertTrue(path.exists())
            self.assertEqual(path.read_bytes(), original)
            self.assertEqual(SQLiteIndex(path).scope(), "public")

    def test_qmd_cache_probe_is_fail_closed(self):
        with tempfile.TemporaryDirectory() as d:
            cache = Path(d) / "cache"; cache.mkdir(mode=0o755)
            adapter = QMDAdapter(cache, command="missing-qmd")
            self.assertFalse(adapter.available)
            self.assertEqual(adapter.unavailable_reason(), "provider_unavailable")
            adapter = QMDAdapter(cache, command="sh")
            self.assertEqual(adapter.unavailable_reason(), "cache_permissions")

    def test_qmd_results_are_normalized_and_projection_allowlisted(self):
        class FakeQMD:
            available = True
            def search(self, query, top_k=8):
                return [
                    {"object_ref": {"vault_id": "public", "object_type": "wiki", "object_id": "pub"}, "score": 0.9},
                    {"object_ref": {"vault_id": "private", "object_type": "wiki", "object_id": "priv"}, "score": 1.0},
                ]
            def unavailable_reason(self):
                return None
        result = Retriever(ITEMS, qmd=FakeQMD()).search("SQLite", "public")
        self.assertEqual(result["method"], "qmd")
        self.assertEqual([x["object_ref"]["object_id"] for x in result["items"]], ["pub"])

    def test_sqlite_index_recover_rebuilds_corrupt_index_and_keeps_previous(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "index.sqlite3"
            index = SQLiteIndex(path)
            first = index.rebuild(ITEMS, "public")
            path.write_bytes(b"corrupt")
            recovered = index.recover(ITEMS, "public")
            self.assertEqual(recovered["state"], "recovered")
            self.assertTrue((path.parent / "index.sqlite3.previous").exists())
            self.assertEqual(index.generated_from(), first["generated_from"])

    def test_sqlite_index_recover_reports_valid_without_rebuild(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "index.sqlite3"
            index = SQLiteIndex(path); index.rebuild(ITEMS, "public")
            result = index.recover(ITEMS, "public")
            self.assertEqual(result["state"], "valid")
            self.assertFalse(result["recovered"])

if __name__ == "__main__": unittest.main()
