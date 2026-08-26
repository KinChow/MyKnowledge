import unittest, tempfile
from pathlib import Path
from tools.indexing import IndexBuilder, QMDAdapter, Retriever, SQLiteIndex

ITEMS = [
    {"vault_id": "public", "object_id": "pub", "title": "公开知识", "body": "SQLite 检索", "public_publishable": True, "public_release": True, "status": "published", "effective_confidentiality": "public", "content_sha256": "sha256:p"},
    {"vault_id": "private", "object_id": "priv", "title": "私有知识", "body": "SQLite 检索", "confidentiality": "internal", "public_publishable": False, "content_sha256": "sha256:i"},
    {"vault_id": "private", "object_id": "down", "title": "不可用", "body": "secret", "availability": "unavailable", "availability_reason": "vault_unavailable", "confidentiality": "internal"},
]

class IndexingTests(unittest.TestCase):
    def test_public_projection_filters_private(self):
        result = IndexBuilder(None).build(ITEMS, "public")
        self.assertEqual([x["object_ref"]["object_id"] for x in result["items"]], ["pub"])

    def test_public_projection_requires_complete_release_allowlist(self):
        draft = {**ITEMS[0], "object_id": "draft", "status": "draft"}
        unreleased = {**ITEMS[0], "object_id": "unreleased", "public_release": False}
        internal = {**ITEMS[0], "object_id": "internal", "effective_confidentiality": "internal"}
        result = IndexBuilder(None).build([ITEMS[0], draft, unreleased, internal], "public")
        self.assertEqual([x["object_ref"]["object_id"] for x in result["items"]], ["pub"])

    def test_local_keeps_owner_and_hides_unavailable_body(self):
        result = IndexBuilder(None).build(ITEMS)
        down = next(x for x in result["items"] if x["object_ref"]["object_id"] == "down")
        self.assertIsNone(down["body"]); self.assertEqual(down["object_ref"]["vault_id"], "private")

    def test_fallback_search_and_limits(self):
        retriever = Retriever(ITEMS)
        self.assertEqual(retriever.search("SQLite", "public")["items"][0]["object_ref"]["object_id"], "pub")
        self.assertEqual(retriever.search("x", top_k=101)["availability_reason"], "query_limit_exceeded")

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

if __name__ == "__main__": unittest.main()
