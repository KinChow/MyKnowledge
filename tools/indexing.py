"""Projection index and deterministic retrieval (F005)."""
from __future__ import annotations
import json, sqlite3, os, tempfile, shutil, subprocess
from pathlib import Path
from .common import canonical_json, hash_canonical


class QMDAdapter:
    """Read-only QMD capability probe; never downloads or executes network work."""
    def __init__(self, cache_dir: Path | None = None, command: str = "qmd"):
        self.cache_dir = Path(cache_dir).resolve() if cache_dir else None
        self.command = command

    def unavailable_reason(self) -> str | None:
        if shutil.which(self.command) is None:
            return "provider_unavailable"
        if self.cache_dir is None:
            return "cache_unconfigured"
        if not self.cache_dir.is_dir():
            return "cache_unavailable"
        if (self.cache_dir.stat().st_mode & 0o777) != 0o700:
            return "cache_permissions"
        if any(part == ".git" for part in self.cache_dir.parts):
            return "cache_in_git"
        return None

    @property
    def available(self) -> bool:
        return self.unavailable_reason() is None

    def search(self, query: str, top_k: int = 8) -> list[dict]:
        """Run an installed QMD CLI in its isolated cache and parse JSON output."""
        reason = self.unavailable_reason()
        if reason:
            raise RuntimeError(reason)
        completed = subprocess.run(
            [self.command, "search", query, "--json", "-n", str(top_k)],
            cwd=self.cache_dir, capture_output=True, text=True, timeout=10, check=False,
        )
        if completed.returncode != 0:
            raise RuntimeError("provider_error")
        data = json.loads(completed.stdout or "[]")
        if isinstance(data, dict):
            data = data.get("results", data.get("items", []))
        if not isinstance(data, list) or any(not isinstance(item, dict) for item in data):
            raise ValueError("provider_schema_invalid")
        return data[:top_k]

def _public_allowlisted(item: dict) -> bool:
    """Require the complete public projection allowlist, not one derived flag."""
    return (
        item.get("vault_id") == "public"
        and item.get("public_publishable") is True
        and item.get("public_release") is True
        and item.get("status") == "published"
        and item.get("effective_confidentiality", item.get("confidentiality", "public")) == "public"
    )


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
    """Rebuildable SQLite FTS5 index with metadata kept outside the FTS table."""
    def __init__(self, path: Path): self.path = Path(path)
    def rebuild(self, items: list[dict], scope: str = "local") -> dict:
        source_allowed = _scope_items(items, scope)
        allowed = IndexBuilder(self.path.parent).build(items, scope)["items"]
        self.path.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp = tempfile.mkstemp(prefix=".index.", suffix=".sqlite3", dir=self.path.parent); os.close(fd)
        try:
            db = sqlite3.connect(tmp)
            generated_from = hash_canonical(source_allowed)
            db.execute("CREATE TABLE index_info (scope TEXT NOT NULL, generated_from TEXT NOT NULL)")
            db.execute("INSERT INTO index_info(scope,generated_from) VALUES(?,?)", (scope, generated_from))
            db.execute("CREATE TABLE metadata (rowid INTEGER PRIMARY KEY, object_ref TEXT, title TEXT, body TEXT, availability TEXT, availability_reason TEXT, confidentiality TEXT, content_sha256 TEXT, source_ref TEXT)")
            db.execute("CREATE VIRTUAL TABLE documents USING fts5(title, body, content='metadata', content_rowid='rowid')")
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
    def search(self, query: str, top_k: int = 8) -> list[dict]:
        db = sqlite3.connect(self.path); rows = db.execute("SELECT m.object_ref,m.title,m.body,bm25(documents),m.availability,m.availability_reason,m.confidentiality,m.content_sha256,m.source_ref FROM documents JOIN metadata m ON documents.rowid=m.rowid WHERE documents MATCH ? ORDER BY bm25(documents) LIMIT ?", (query, top_k)).fetchall(); db.close()
        return [{"object_ref":json.loads(r[0]),"title":r[1],"snippet":(r[2] or "")[:240],"score":float(r[3]),"availability":r[4],"availability_reason":r[5],"confidentiality":r[6],"content_sha256":r[7],"source_ref":r[8]} for r in rows]

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
    def __init__(self, items: list[dict], index_path: Path | None = None, qmd: QMDAdapter | None = None):
        self.items = items
        self.index_path = Path(index_path) if index_path else None
        self.qmd = qmd or QMDAdapter()

    def search(self, query: str, scope: str = "local", top_k: int = 8, vault_ids: list[str] | None = None) -> dict:
        if not isinstance(query, str) or len(query) > 4096 or top_k < 1 or top_k > 100: return {"schema_version": "query-result/v1", "items": [], "scope": scope, "method": "deterministic-fallback", "index_version": "none", "generated_from": "", "availability": "invalid", "availability_reason": "query_limit_exceeded", "degraded": True, "confidentiality_max": "public", "limits": ["query_limit_exceeded"], "warnings": []}
        public = _scope_items(self.items, scope)
        if vault_ids is not None:
            requested = set(vault_ids)
            public = [item for item in public if item.get("vault_id") in requested]
        if self.qmd.available:
            try:
                allowed_refs = {(x.get("vault_id"), x.get("object_type", "wiki"), x.get("object_id")): x for x in public}
                candidates = self.qmd.search(query, top_k)
                items = []
                for candidate in candidates:
                    ref = candidate.get("object_ref") or {"vault_id": candidate.get("vault_id"), "object_type": candidate.get("object_type", "wiki"), "object_id": candidate.get("object_id")}
                    source = allowed_refs.get((ref.get("vault_id"), ref.get("object_type", "wiki"), ref.get("object_id")))
                    if source is None:
                        continue
                    available = source.get("availability", "available") == "available"
                    items.append({"object_ref": {"vault_id": ref.get("vault_id"), "object_type": ref.get("object_type", "wiki"), "object_id": ref.get("object_id")}, "title": source.get("title"), "snippet": str(source.get("body", ""))[:240] if available else None, "score": candidate.get("score"), "availability": "available" if available else "unavailable", "availability_reason": "none" if available else source.get("availability_reason", "unavailable"), "confidentiality": source.get("confidentiality", "public"), "content_sha256": source.get("content_sha256"), "source_ref": source.get("source_ref")})
                return {"schema_version": "query-result/v1", "items": items, "scope": scope, "method": "qmd", "index_version": "qmd/v1", "generated_from": hash_canonical(public), "availability": "available", "availability_reason": "none", "degraded": False, "confidentiality_max": "internal" if any(x["confidentiality"] == "internal" for x in items) else "public", "limits": [], "warnings": []}
            except (OSError, RuntimeError, ValueError, json.JSONDecodeError):
                pass
        if self.index_path and self.index_path.exists():
            try:
                index = SQLiteIndex(self.index_path)
                if index.scope() != scope:
                    raise ValueError("index_scope_mismatch")
                if index.generated_from() != hash_canonical(public):
                    raise ValueError("index_stale")
                indexed = index.search(query, top_k)
                return {"schema_version": "query-result/v1", "items": indexed, "scope": scope, "method": "fts5", "index_version": "fts5/v1", "generated_from": hash_canonical(public), "availability": "available", "availability_reason": "none", "degraded": True, "confidentiality_max": "internal" if any(x.get("confidentiality") == "internal" for x in indexed) else "public", "limits": [], "warnings": ["qmd_unavailable", self.qmd.unavailable_reason() or "none"]}
            except (OSError, sqlite3.Error, ValueError):
                pass
        q = query.casefold()
        hits = [x for x in public if q in str(x.get("title", "")).casefold() or (x.get("availability", "available") == "available" and q in str(x.get("body", "")).casefold())]
        result_items = []
        for x in hits[:top_k]:
            available = x.get("availability", "available") == "available"
            result_items.append({"object_ref": {"vault_id": x.get("vault_id"), "object_type": x.get("object_type", "wiki"), "object_id": x.get("object_id")}, "title": x.get("title"), "snippet": str(x.get("body", ""))[:240] if available else None, "score": 1.0, "availability": "available" if available else "unavailable", "availability_reason": "none" if available else x.get("availability_reason", "unavailable"), "confidentiality": x.get("confidentiality", "public"), "content_sha256": x.get("content_sha256"), "source_ref": x.get("source_ref")})
        return {"schema_version": "query-result/v1", "items": result_items, "scope": scope, "method": "deterministic-fallback", "index_version": "fallback/v1", "generated_from": hash_canonical(public), "availability": "available", "availability_reason": "none", "degraded": True, "confidentiality_max": "internal" if any(x.get("confidentiality") == "internal" for x in public) else "public", "limits": [], "warnings": ["qmd_unavailable", "fts5_unavailable"]}
