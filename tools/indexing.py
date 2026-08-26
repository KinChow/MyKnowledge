"""Projection index and deterministic retrieval (F005)."""
from __future__ import annotations
import json, sqlite3
from pathlib import Path
from .common import canonical_json, hash_canonical

class IndexBuilder:
    def __init__(self, root: Path | None): self.root = Path(root or ".").resolve()
    def build(self, items: list[dict], scope: str = "local") -> dict:
        allowed = [x for x in items if scope != "public" or (x.get("vault_id") == "public" and x.get("public_publishable") is True)]
        records = []
        for x in allowed:
            rec = {"object_ref": {"vault_id": x.get("vault_id"), "object_type": x.get("object_type", "wiki"), "object_id": x.get("object_id")}, "title": x.get("title"), "body": x.get("body") if x.get("availability", "available") == "available" else None, "snippet": None, "score": None, "availability": x.get("availability", "available"), "availability_reason": x.get("availability_reason", "none"), "confidentiality": x.get("confidentiality", "public"), "content_sha256": x.get("content_sha256"), "source_ref": x.get("source_ref")}
            records.append(rec)
        return {"schema_version": "query-result/v1", "items": records, "scope": scope, "method": "fts5", "index_version": "fts5/v1", "generated_from": hash_canonical(allowed), "availability": "available", "availability_reason": "none", "degraded": False, "confidentiality_max": "internal" if any(x["confidentiality"] == "internal" for x in records) else "public", "limits": [], "warnings": []}

class Retriever:
    def __init__(self, items: list[dict]): self.items = items
    def search(self, query: str, scope: str = "local", top_k: int = 8) -> dict:
        if not isinstance(query, str) or len(query) > 4096 or top_k < 1 or top_k > 100: return {"schema_version": "query-result/v1", "items": [], "scope": scope, "method": "deterministic-fallback", "index_version": "none", "generated_from": "", "availability": "invalid", "availability_reason": "query_limit_exceeded", "degraded": True, "confidentiality_max": "public", "limits": ["query_limit_exceeded"], "warnings": []}
        public = [x for x in self.items if scope != "public" or (x.get("vault_id") == "public" and x.get("public_publishable") is True)]
        q = query.casefold(); hits = [x for x in public if x.get("availability", "available") == "available" and q in (str(x.get("title", "")) + "\n" + str(x.get("body", ""))).casefold()]
        return {"schema_version": "query-result/v1", "items": [{"object_ref": {"vault_id": x.get("vault_id"), "object_type": x.get("object_type", "wiki"), "object_id": x.get("object_id")}, "title": x.get("title"), "snippet": str(x.get("body", ""))[:240], "score": 1.0, "availability": "available", "availability_reason": "none", "confidentiality": x.get("confidentiality", "public"), "content_sha256": x.get("content_sha256"), "source_ref": x.get("source_ref")} for x in hits[:top_k]], "scope": scope, "method": "deterministic-fallback", "index_version": "fallback/v1", "generated_from": hash_canonical(public), "availability": "available", "availability_reason": "none", "degraded": True, "confidentiality_max": "internal" if any(x.get("confidentiality") == "internal" for x in public) else "public", "limits": [], "warnings": ["qmd_unavailable", "fts5_unavailable"]}
