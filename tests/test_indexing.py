import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tools.indexing import IndexBuilder, Retriever, SQLiteIndex
from tools.vault_registry import VaultRegistry

ITEMS = [
    {
        "vault_id": "public",
        "object_id": "pub",
        "title": "公开知识",
        "body": "SQLite 检索",
        "public_publishable": True,
        "public_release": True,
        "status": "published",
        "effective_confidentiality": "public",
        "content_sha256": "sha256:p",
    },
    {
        "vault_id": "private",
        "object_id": "priv",
        "title": "私有知识",
        "body": "SQLite 检索",
        "confidentiality": "internal",
        "public_publishable": False,
        "content_sha256": "sha256:i",
    },
    {
        "vault_id": "private",
        "object_id": "down",
        "title": "不可用",
        "body": "secret",
        "availability": "unavailable",
        "availability_reason": "vault_unavailable",
        "confidentiality": "internal",
    },
]


class IndexingTests(unittest.TestCase):
    def test_public_projection_filters_private(self):
        result = IndexBuilder(None).build(ITEMS, "public")
        self.assertEqual(
            [x["object_ref"]["object_id"] for x in result["items"]], ["pub"]
        )

    def test_registry_projection_feeds_owner_aware_index(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            public = root / "public"
            private = root / "private"
            for vault, title in ((public, "Public"), (private, "Private")):
                (vault / "wiki").mkdir(parents=True)
                (vault / "wiki" / "same.md").write_text(
                    f"# {title}\nSQLite", encoding="utf-8"
                )
                subprocess.run(["git", "init", "-q", str(vault)], check=True)
            manifest = root / "manifest.yaml"
            manifest.write_text(
                f"schema_version: 1\nlayout: superproject\nworkspace_root: {root}\nvaults:\n  - {{id: public, path: public}}\n  - {{id: private, path: private, confidentiality: internal}}\n",
                encoding="utf-8",
            )
            result = IndexBuilder(root).build_from_registry(
                VaultRegistry(public, manifest)
            )
            self.assertEqual(
                {x["object_ref"]["vault_id"] for x in result["items"]},
                {"public", "private"},
            )
            self.assertTrue(result["projection_sha256"].startswith("sha256:"))

    def test_public_projection_requires_complete_release_allowlist(self):
        draft = {**ITEMS[0], "object_id": "draft", "status": "draft"}
        unreleased = {**ITEMS[0], "object_id": "unreleased", "public_release": False}
        internal = {
            **ITEMS[0],
            "object_id": "internal",
            "effective_confidentiality": "internal",
        }
        result = IndexBuilder(None).build(
            [ITEMS[0], draft, unreleased, internal], "public"
        )
        self.assertEqual(
            [x["object_ref"]["object_id"] for x in result["items"]], ["pub"]
        )

    def test_private_scope_excludes_public_owner(self):
        result = IndexBuilder(None).build(ITEMS, "private")
        self.assertEqual(
            {x["object_ref"]["vault_id"] for x in result["items"]}, {"private"}
        )

    def test_vault_allowlist_is_applied_before_retrieval_result_generation(self):
        result = Retriever(ITEMS).search("SQLite", "local", vault_ids=["public"])
        self.assertEqual(
            {x["object_ref"]["vault_id"] for x in result["items"]}, {"public"}
        )
        result = Retriever(ITEMS).search("SQLite", "private")
        self.assertEqual(
            {x["object_ref"]["vault_id"] for x in result["items"]}, {"private"}
        )

    def test_local_keeps_owner_and_hides_unavailable_body(self):
        result = IndexBuilder(None).build(ITEMS)
        down = next(
            x for x in result["items"] if x["object_ref"]["object_id"] == "down"
        )
        self.assertIsNone(down["body"])
        self.assertEqual(down["object_ref"]["vault_id"], "private")

    def test_fallback_search_and_limits(self):
        retriever = Retriever(ITEMS)
        self.assertEqual(
            retriever.search("SQLite", "public")["items"][0]["object_ref"]["object_id"],
            "pub",
        )
        self.assertEqual(
            retriever.search("x", top_k=101)["availability_reason"],
            "query_limit_exceeded",
        )

    def test_retriever_enforces_vault_id_limit_before_provider(self):
        retriever = Retriever(ITEMS)
        result = retriever.search(
            "SQLite", "local", vault_ids=[f"vault-{i}" for i in range(17)]
        )
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
            self.assertEqual(result["warnings"], [])  # fts5 是主路径，非降级
            self.assertFalse(result["degraded"])

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
            index = SQLiteIndex(path)
            index.rebuild(ITEMS, "public")
            result = index.recover(ITEMS, "public")
            self.assertEqual(result["state"], "valid")
            self.assertFalse(result["recovered"])

    def test_index_cli_rebuild_and_recover_use_public_projection(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "wiki").mkdir()
            (root / "wiki" / "pub.md").write_text("SQLite", encoding="utf-8")
            (root / "queries" / "public").mkdir(parents=True)
            (root / "queries" / "public" / "manifest.json").write_text(
                __import__("json").dumps(
                    {
                        "schema_version": "public-projection/v1",
                        "projection": "public",
                        "items": [
                            {**ITEMS[0], "id": "pub", "body_path": "wiki/pub.md"}
                        ],
                    }
                ),
                encoding="utf-8",
            )
            path = root / "state" / "index.sqlite3"
            first = subprocess.run(
                [
                    __import__("sys").executable,
                    "-m",
                    "tools.cli",
                    "index",
                    "rebuild",
                    "--root",
                    str(root),
                    "--scope",
                    "public",
                    "--index",
                    str(path),
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(first.returncode, 0)
            second = subprocess.run(
                [
                    __import__("sys").executable,
                    "-m",
                    "tools.cli",
                    "index",
                    "recover",
                    "--root",
                    str(root),
                    "--scope",
                    "public",
                    "--index",
                    str(path),
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(second.returncode, 0)
            self.assertEqual(__import__("json").loads(second.stdout)["state"], "valid")


if __name__ == "__main__":
    unittest.main()


class F005WiringTests(unittest.TestCase):
    """F005 review（2026-08-28）：FTS5 默认接线与特殊字符查询。"""

    def test_default_index_path_is_wired_into_query_cli(self):
        import subprocess
        import sys
        import tempfile
        from pathlib import Path

        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "wiki").mkdir()
            (root / "wiki" / "pub.md").write_text("SQLite 检索", encoding="utf-8")
            (root / "queries" / "public").mkdir(parents=True)
            (root / "queries" / "public" / "manifest.json").write_text(
                __import__("json").dumps(
                    {
                        "schema_version": "public-projection/v1",
                        "projection": "public",
                        "items": [
                            {**ITEMS[0], "id": "pub", "body_path": "wiki/pub.md"}
                        ],
                    }
                ),
                encoding="utf-8",
            )
            repo = Path(__file__).resolve().parents[1]
            index = root / "state" / "index" / "public.sqlite3"
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "tools.cli",
                    "index",
                    "rebuild",
                    "--root",
                    str(root),
                    "--scope",
                    "public",
                    "--index",
                    str(index),
                ],
                cwd=repo,
                capture_output=True,
                check=True,
            )
            out = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "tools.cli",
                    "query",
                    "SQLite",
                    "--root",
                    str(root),
                ],
                cwd=repo,
                capture_output=True,
                text=True,
            )
            result = __import__("json").loads(out.stdout)
            self.assertEqual(
                result["method"], "fts5"
            )  # 默认接线：query CLI 自动使用约定索引

    def test_fts5_phrase_query_survives_special_characters(self):
        with tempfile.TemporaryDirectory() as d:
            from tools.indexing import Retriever, SQLiteIndex

            root = Path(d)
            idx = SQLiteIndex(root / "i.sqlite3")
            idx.rebuild(ITEMS, "public")
            for nasty in ("c++", 'quote"inside', "a-b", "NEAR(x, y)"):
                result = Retriever(ITEMS, index_path=idx.path).search(
                    nasty, "public", 5
                )
                self.assertEqual(
                    result["schema_version"], "query-result/v1"
                )  # 不抛 FTS5 语法错误
            hit = Retriever(ITEMS, index_path=idx.path).search(
                "SQLite 检索", "public", 5
            )
            self.assertEqual(hit["method"], "fts5")


class SimpleTokenizerTests(unittest.TestCase):
    """§1808 修订：simple 中文分词集成（无扩展环境自动回退 unicode61）。"""

    def test_simple_index_matches_chinese_across_particles(self):
        from tools.indexing import Retriever, SQLiteIndex

        lib = Path(__file__).resolve().parents[1] / "state" / "lib" / "libsimple.dylib"
        if not lib.exists():
            self.skipTest("libsimple 未安装（bootstrap 可装），回退路径由其他测试覆盖")
        import os as _os

        repo = Path(__file__).resolve().parents[1]
        _os.environ["MYKNOWLEDGE_SIMPLE_LIB"] = str(
            repo / "state" / "lib" / "libsimple"
        )
        self.addCleanup(_os.environ.pop, "MYKNOWLEDGE_SIMPLE_LIB", None)
        root = repo
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / "state" / "index").mkdir(
                parents=True
            )  # 约定布局：Retriever 由此推断 root
            idx = SQLiteIndex(Path(d) / "state" / "index" / "public.sqlite3", root=root)
            idx.rebuild(
                [
                    {
                        **ITEMS[0],
                        "title": "结构化的讨论方法",
                        "body": "AAR 是一个结构化的讨论方法，事后回顾",
                    }
                ],
                "public",
            )
            db = __import__("sqlite3").connect(idx.path)
            tok = db.execute("SELECT tokenizer FROM index_info").fetchone()[0]
            db.close()
            self.assertEqual(tok, "simple")
            result = Retriever(
                [
                    {
                        **ITEMS[0],
                        "title": "结构化的讨论方法",
                        "body": "AAR 是一个结构化的讨论方法，事后回顾",
                    }
                ],
                index_path=idx.path,
            ).search("结构化讨论", "public", 5)
            self.assertEqual(result["method"], "fts5")
            self.assertEqual(
                [i["object_ref"]["object_id"] for i in result["items"]],
                [ITEMS[0]["object_id"]],
            )

    def test_fallback_to_unicode61_without_extension(self):
        import os as _os

        from tools.indexing import Retriever, SQLiteIndex

        _os.environ.pop("MYKNOWLEDGE_SIMPLE_LIB", None)
        with tempfile.TemporaryDirectory() as d:
            idx = SQLiteIndex(
                Path(d) / "i.sqlite3", root=Path(d)
            )  # root 下无 state/lib → 回退
            idx.rebuild(ITEMS, "public")
            db = __import__("sqlite3").connect(Path(d) / "i.sqlite3")
            tok = db.execute("SELECT tokenizer FROM index_info").fetchone()[0]
            db.close()
            self.assertEqual(tok, "unicode61")
            result = Retriever(ITEMS, index_path=idx.path).search(
                "SQLite 检索", "public", 5
            )
            self.assertEqual(result["method"], "fts5")  # 回退路径仍可用（短语语义）
