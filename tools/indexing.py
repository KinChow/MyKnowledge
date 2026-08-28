"""Projection index and deterministic retrieval (F005)."""
from __future__ import annotations
import json, sqlite3, os, tempfile, shutil, subprocess
from pathlib import Path
from .common import canonical_json, hash_canonical
from .projection import public_allowlisted as _public_allowlisted  # 单份过滤谓词（Step0-1）


def _infer_index_root(index_path: Path) -> Path | None:
    """默认索引约定 state/index/<name>.sqlite3 → root = 上三级。"""
    parts = Path(index_path).resolve().parts
    if len(parts) >= 3 and parts[-3:-1] == ("state", "index"):
        return Path(*parts[:-3])
    return None


def default_public_index_path(root: Path) -> Path:
    """约定默认 public FTS5 索引位置（state/ 属运行缓存，gitignored）。

    F005 review（2026-08-28）：此前 CLI query / API / Skill 构造 Retriever 时
    均未传 index_path，FTS5 索引可构建但无消费者，真实查询永远走 LIKE。
    """
    return Path(root) / "state" / "index" / "public.sqlite3"


def rebuild_default_public_index(root: Path) -> dict:
    """按当前 public projection 重建默认索引（供 write 后的自动接线复用）。"""
    from .projection import PublicProjectionStore

    items = PublicProjectionStore(root).public_items(with_body=True)
    return SQLiteIndex(default_public_index_path(root), root=root).rebuild(items, "public")

def _scope_items(items: list[dict], scope: str) -> list[dict]:
    """Apply scope filtering before any index/provider can see candidates."""
    if scope == "public":
        return [item for item in items if _public_allowlisted(item)]
    if scope == "private":
        return [item for item in items if item.get("vault_id") != "public"]
    return list(items)


class IndexBuilder:
    def __init__(self, root: Path | None): self.root = Path(root or ".").resolve()

    def build_from_registry(self, registry, scope: str = "local") -> dict:
        """Build the index contract from an owner-aware Vault projection."""
        projection = registry.local_projection(scope)
        result = self.build(projection["items"], scope)
        unavailable = projection.get("unavailable_vaults", [])
        if unavailable:
            result["degraded"] = True
            result["warnings"] = [
                "vault_unavailable:" + str(item["vault_id"]) + ":" + str(item["reason"])
                for item in unavailable
            ]
        result["generated_from"] = projection["generated_from"]
        result["projection_sha256"] = projection["projection_sha256"]
        return result

    def build(self, items: list[dict], scope: str = "local") -> dict:
        allowed = _scope_items(items, scope)
        records = []
        for x in allowed:
            rec = {"object_ref": {"vault_id": x.get("vault_id"), "object_type": x.get("object_type", "wiki"), "object_id": x.get("object_id")}, "title": x.get("title"), "body": x.get("body") if x.get("availability", "available") == "available" else None, "snippet": None, "score": None, "availability": x.get("availability", "available"), "availability_reason": x.get("availability_reason", "none"), "confidentiality": x.get("confidentiality", "public"), "content_sha256": x.get("content_sha256"), "source_ref": x.get("source_ref")}
            records.append(rec)
        return {"schema_version": "query-result/v1", "items": records, "scope": scope, "method": "fts5", "index_version": "fts5/v1", "generated_from": hash_canonical(allowed), "availability": "available", "availability_reason": "none", "degraded": False, "confidentiality_max": "internal" if any(x["confidentiality"] == "internal" for x in records) else "public", "limits": [], "warnings": []}

class SQLiteIndex:
    """Rebuildable SQLite FTS5 index with metadata kept outside the FTS table.

    中文分词（§1808 修订，2026-08-28）：加载 libsimple（wangfenjin/simple，
    MIT，https://github.com/wangfenjin/simple）后建表用 ``tokenize='simple'``，
    查询用 ``jieba_query()``（词级分词 + AND）；扩展/词典缺失或加载失败一律
    fail-closed 回退 unicode61（引号短语查询），并在 index_info 记录 tokenizer
    供 doctor 显性化。扩展基名默认 ``state/lib/libsimple``（sqlite 自动追加
    平台后缀），可用 ``MYKNOWLEDGE_SIMPLE_LIB`` 覆盖；词典经 ``jieba_dict()``
    显式指定为 ``state/lib/dict/`` 绝对路径，不依赖 cwd。
    """
    def __init__(self, path: Path, *, root: Path | None = None): self.path = Path(path); self.root = Path(root) if root else None

    SIMPLE_ENV = "MYKNOWLEDGE_SIMPLE_LIB"

    @classmethod
    def _simple_paths(cls, root: Path | None) -> tuple[str, Path] | None:
        import os as _os
        lib = _os.environ.get(cls.SIMPLE_ENV) or (str(root / "state" / "lib" / "libsimple") if root else None)
        if not lib:
            return None
        dictionary = Path(lib).parent / "dict"
        return lib, dictionary

    @classmethod
    def _load_simple(cls, db, root: Path | None) -> bool:
        """加载 simple 扩展并显式配置词典；任何失败返回 False（不抛、不 abort）。"""
        import os as _os
        lib = _os.environ.get(cls.SIMPLE_ENV) or (str(root / "state" / "lib" / "libsimple") if root else None)
        if not lib:
            return False
        if not (Path(lib + ".dylib").exists() or Path(lib + ".so").exists()):
            return False
        try:
            db.enable_load_extension(True)
            db.load_extension(lib)
            dictionary = Path(lib).parent / "dict"
            if dictionary.is_dir():
                db.execute("SELECT jieba_dict(?)", (str(dictionary) + "/",))
            return True
        except (AttributeError, sqlite3.Error, OSError):
            return False

    def _infer_root(self) -> Path | None:
        return _infer_index_root(self.path)

    def rebuild(self, items: list[dict], scope: str = "local") -> dict:
        source_allowed = _scope_items(items, scope)
        allowed = IndexBuilder(self.path.parent).build(items, scope)["items"]
        self.path.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp = tempfile.mkstemp(prefix=".index.", suffix=".sqlite3", dir=self.path.parent); os.close(fd)
        try:
            db = sqlite3.connect(tmp)
            use_simple = self._load_simple(db, self.root or self._infer_root())
            tokenizer = "simple" if use_simple else "unicode61"
            generated_from = hash_canonical(source_allowed)
            db.execute("CREATE TABLE index_info (scope TEXT NOT NULL, generated_from TEXT NOT NULL, tokenizer TEXT NOT NULL)")
            db.execute("INSERT INTO index_info(scope,generated_from,tokenizer) VALUES(?,?,?)", (scope, generated_from, tokenizer))
            db.execute("CREATE TABLE metadata (rowid INTEGER PRIMARY KEY, object_ref TEXT, title TEXT, body TEXT, availability TEXT, availability_reason TEXT, confidentiality TEXT, content_sha256 TEXT, source_ref TEXT)")
            db.execute(f"CREATE VIRTUAL TABLE documents USING fts5(title, body, content='metadata', content_rowid='rowid', tokenize='{tokenizer}')")
            for row in allowed:
                ref = json.dumps(row["object_ref"], ensure_ascii=False, sort_keys=True)
                db.execute("INSERT INTO metadata(object_ref,title,body,availability,availability_reason,confidentiality,content_sha256,source_ref) VALUES(?,?,?,?,?,?,?,?)", (ref,row["title"],row["body"],row["availability"],row["availability_reason"],row["confidentiality"],row["content_sha256"],row["source_ref"]))
            db.execute("INSERT INTO documents(documents) VALUES('rebuild')"); db.commit(); db.close()
            previous = self.path.with_suffix(self.path.suffix + ".previous")
            old_moved = False
            try:
                if self.path.exists():
                    os.replace(self.path, previous)
                    old_moved = True
                os.replace(tmp, self.path)
            except OSError:
                # Restore the last known-good index if the final swap fails.
                if old_moved and not self.path.exists() and previous.exists():
                    os.replace(previous, self.path)
                raise
        finally:
            if os.path.exists(tmp): os.unlink(tmp)
        return {"schema_version":"index-manifest/v1", "scope":scope, "generated_from":generated_from, "item_count":len(allowed), "index_version":"fts5/v1", "previous_path": str(previous.name) if self.path.with_suffix(self.path.suffix + ".previous").exists() else None}

    def recover(self, items: list[dict], scope: str = "local") -> dict:
        """Validate the current index and atomically rebuild it when stale/corrupt."""
        expected = hash_canonical(_scope_items(items, scope))
        if self.path.exists():
            try:
                db = sqlite3.connect(self.path)
                row = db.execute("SELECT scope, generated_from FROM index_info LIMIT 1").fetchone()
                integrity = db.execute("PRAGMA quick_check").fetchone()
                db.close()
                if row and row[0] == scope and row[1] == expected and integrity and integrity[0] == "ok":
                    return {"state": "valid", "scope": scope, "generated_from": expected, "recovered": False}
            except (OSError, sqlite3.Error, TypeError):
                pass
        try:
            rebuilt = self.rebuild(items, scope)
            return {"state": "recovered", "scope": scope, "generated_from": rebuilt["generated_from"],
                    "previous_path": rebuilt.get("previous_path"), "recovered": True}
        except (OSError, sqlite3.Error, ValueError) as exc:
            return {"state": "failed", "scope": scope, "error_code": "index_recovery_failed", "detail": type(exc).__name__}
    def search(self, query: str, top_k: int = 8) -> list[dict]:
        db = sqlite3.connect(self.path)
        try:
            tokenizer = "unicode61"
            try:
                row = db.execute("SELECT tokenizer FROM index_info LIMIT 1").fetchone()
                if row: tokenizer = str(row[0])
            except sqlite3.Error:
                pass
            if tokenizer == "simple" and self._load_simple(db, self.root or self._infer_root()):
                # 词级分词 + AND：jieba_query 由 simple 扩展提供（加载失败不会走到这里）
                match_expr = db.execute("SELECT jieba_query(?)", (query,)).fetchone()[0]
            else:
                # 用户查询按 FTS5 短语字面量包裹（双引号转义）：裸 MATCH 语法会把
                # "c++"、"a-b"、引号等当作 FTS5 语法符号抛 OperationalError，
                # 曾导致含特殊字符的真实查询永远静默降级到 LIKE
                match_expr = '"' + query.replace('"', '""') + '"'
            rows = db.execute("SELECT m.object_ref,m.title,m.body,bm25(documents),m.availability,m.availability_reason,m.confidentiality,m.content_sha256,m.source_ref FROM documents JOIN metadata m ON documents.rowid=m.rowid WHERE documents MATCH ? ORDER BY bm25(documents) LIMIT ?", (match_expr, top_k)).fetchall()
        finally:
            db.close()
        return [{"object_ref":json.loads(r[0]),"title":r[1],"snippet":(r[2] or "")[:240],"score":float(r[3]),"availability":r[4],"availability_reason":r[5],"confidentiality":r[6],"content_sha256":r[7],"source_ref":r[8]} for r in rows]

    def tokenizer(self) -> str:
        db = sqlite3.connect(self.path)
        try:
            row = db.execute("SELECT tokenizer FROM index_info LIMIT 1").fetchone()
            return str(row[0]) if row else "unicode61"
        except sqlite3.Error:
            return "unknown"
        finally:
            db.close()

    def scope(self) -> str:
        db = sqlite3.connect(self.path)
        try:
            return str(db.execute("SELECT scope FROM index_info LIMIT 1").fetchone()[0])
        finally:
            db.close()

    def generated_from(self) -> str:
        db = sqlite3.connect(self.path)
        try:
            return str(db.execute("SELECT generated_from FROM index_info LIMIT 1").fetchone()[0])
        finally:
            db.close()

class Retriever:
    def __init__(self, items: list[dict], index_path: Path | None = None):
        self.items = items
        self.index_path = Path(index_path) if index_path else None

    def search(self, query: str, scope: str = "local", top_k: int = 8, vault_ids: list[str] | None = None) -> dict:
        if (not isinstance(query, str) or len(query) > 4096 or top_k < 1 or top_k > 100
                or (vault_ids is not None and (len(vault_ids) > 16 or any(not isinstance(v, str) or not v for v in vault_ids)))):
            return {"schema_version": "query-result/v1", "items": [], "scope": scope, "method": "deterministic-fallback", "index_version": "none", "generated_from": "", "availability": "invalid", "availability_reason": "query_limit_exceeded", "degraded": True, "confidentiality_max": "public", "limits": ["query_limit_exceeded"], "warnings": []}
        public = _scope_items(self.items, scope)
        if vault_ids is not None:
            requested = set(vault_ids)
            public = [item for item in public if item.get("vault_id") in requested]
        # §1808 修订：qmd 不可得已被 simple 替代，QMD 适配器退役；
        # 降级链为 FTS5（simple/unicode61）→ LIKE
        if self.index_path and self.index_path.exists():
            try:
                index = SQLiteIndex(self.index_path, root=_infer_index_root(self.index_path))
                if index.scope() != scope:
                    raise ValueError("index_scope_mismatch")
                if index.generated_from() != hash_canonical(public):
                    raise ValueError("index_stale")
                indexed = index.search(query, top_k)
                return {"schema_version": "query-result/v1", "items": indexed, "scope": scope, "method": "fts5", "index_version": "fts5/v1", "generated_from": hash_canonical(public), "availability": "available", "availability_reason": "none", "degraded": False, "confidentiality_max": "internal" if any(x.get("confidentiality") == "internal" for x in indexed) else "public", "limits": [], "warnings": []}
            except (OSError, sqlite3.Error, ValueError):
                pass
        q = query.casefold()
        hits = [x for x in public if q in str(x.get("title", "")).casefold() or (x.get("availability", "available") == "available" and q in str(x.get("body", "")).casefold())]
        result_items = []
        for x in hits[:top_k]:
            available = x.get("availability", "available") == "available"
            result_items.append({"object_ref": {"vault_id": x.get("vault_id"), "object_type": x.get("object_type", "wiki"), "object_id": x.get("object_id")}, "title": x.get("title"), "snippet": str(x.get("body", ""))[:240] if available else None, "score": 1.0, "availability": "available" if available else "unavailable", "availability_reason": "none" if available else x.get("availability_reason", "unavailable"), "confidentiality": x.get("confidentiality", "public"), "content_sha256": x.get("content_sha256"), "source_ref": x.get("source_ref")})
        return {"schema_version": "query-result/v1", "items": result_items, "scope": scope, "method": "deterministic-fallback", "index_version": "fallback/v1", "generated_from": hash_canonical(public), "availability": "available", "availability_reason": "none", "degraded": True, "confidentiality_max": "internal" if any(x.get("confidentiality") == "internal" for x in public) else "public", "limits": [], "warnings": ["fts5_unavailable"]}
