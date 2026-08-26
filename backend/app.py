"""FastAPI local adapter (F006)."""
from __future__ import annotations
import secrets
from pathlib import Path
from typing import Any
from fastapi import FastAPI, Header, HTTPException, Query
from pydantic import BaseModel, ConfigDict, Field
from tools.indexing import Retriever

class RetrieveRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    query: str = Field(min_length=1, max_length=4096)
    scope: str = "public"
    vault_ids: list[str] | None = None
    top_k: int = Field(default=8, ge=1, le=100)
    include_sources: bool = False
    include_archive: bool = False

def create_app(root: Path | None = None, *, items: list[dict] | None = None, capability_token: str | None = None) -> FastAPI:
    app = FastAPI(title="MyKnowledge Local API", version="v1")
    app.state.retriever = Retriever(items or [])
    app.state.capability_token = capability_token or secrets.token_urlsafe(32)

    def require_capability(token: str | None, scope: str) -> None:
        if scope == "public":
            return
        if not token:
            raise HTTPException(status_code=401, detail={"code": "capability_token_required", "stage": "auth", "retryable": False, "next_action": "provide capability token"})
        if not secrets.compare_digest(token, app.state.capability_token):
            raise HTTPException(status_code=403, detail={"code": "capability_token_invalid", "stage": "auth", "retryable": False, "next_action": "request a fresh local token"})

    def retrieve(req: RetrieveRequest, token: str | None = None) -> dict:
        if req.scope not in {"public", "local", "private"}:
            raise HTTPException(status_code=400, detail={"code": "scope_invalid", "stage": "request", "retryable": False, "next_action": "use public/local/private"})
        require_capability(token, req.scope)
        result = app.state.retriever.search(req.query, req.scope, req.top_k)
        if req.vault_ids:
            allowed = set(req.vault_ids)
            result["items"] = [x for x in result["items"] if x["object_ref"]["vault_id"] in allowed]
        return result

    @app.get("/api/health")
    def health() -> dict:
        return {"schema_version": "health/v1", "status": "ok", "api": "local"}

    @app.post("/api/retrieve")
    def retrieve_post(req: RetrieveRequest, x_myknowledge_capability: str | None = Header(default=None)) -> dict:
        return retrieve(req, x_myknowledge_capability)

    @app.get("/api/query")
    def query_get(q: str = Query(min_length=1, max_length=4096), scope: str = "public", vault_ids: str | None = None, top_k: int = Query(default=8, ge=1, le=100), x_myknowledge_capability: str | None = Header(default=None)) -> dict:
        ids = [x for x in vault_ids.split(",") if x] if vault_ids else None
        return retrieve(RetrieveRequest(query=q, scope=scope, vault_ids=ids, top_k=top_k), x_myknowledge_capability)

    @app.post("/api/ask")
    def ask(req: RetrieveRequest, x_myknowledge_capability: str | None = Header(default=None)) -> dict:
        retrieval = retrieve(req, x_myknowledge_capability)
        return {"schema_version": "ask-result/v1", "answer": None, "citations": [], "retrieval": retrieval, "availability": "unavailable", "availability_reason": "provider_unavailable", "confidentiality": retrieval["confidentiality_max"], "limits": ["llm_unavailable"], "warnings": ["No LLM provider configured"]}

    return app

app = create_app()
