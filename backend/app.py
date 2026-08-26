"""FastAPI local adapter (F006)."""
from __future__ import annotations
import os
import time
import secrets
from pathlib import Path
from typing import Any
from fastapi import Body, FastAPI, Header, HTTPException, Query, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict, Field
from tools.indexing import Retriever
from tools.common import atomic_write, safe_id
from tools.question import QuestionStore
from tools.write_operation import WriteOperation
from tools.vault_registry import VaultRegistry
from tools.validation.validator import WikiValidator

class RetrieveRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    query: str = Field(min_length=1, max_length=4000)
    scope: str = "public"
    vault_ids: list[str] | None = None
    top_k: int = Field(default=8, ge=1, le=50)
    include_sources: bool = False
    include_archive: bool = False


class WritePreviewRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    files: dict[str, str] = Field(min_length=1)
    vault_id: str = "public"


class ApplyRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    confirmed: bool = False
    actor_id: str = Field(default="local-user", min_length=1, max_length=128)

def create_app(root: Path | None = None, *, items: list[dict] | None = None, capability_token: str | None = None) -> FastAPI:
    app = FastAPI(title="MyKnowledge Local API", version="v1")
    app.state.root = Path(root or ".").resolve()
    app.state.retriever = Retriever(items or [])
    app.state.capability_token = capability_token or secrets.token_urlsafe(32)
    app.state.capability_token_created_at = time.time()
    app.state.capability_token_ttl_seconds = 3600
    app.state.capability_token_path = None
    if capability_token is None and root is not None:
        state_dir = app.state.root / "state"
        state_dir.mkdir(parents=True, exist_ok=True)
        os.chmod(state_dir, 0o700)
        token_path = state_dir / "capability-token"
        atomic_write(token_path, app.state.capability_token.encode("ascii") + b"\n", 0o600)
        app.state.capability_token_path = token_path
    app.state.practice = QuestionStore(app.state.root)
    app.state.writer = WriteOperation(app.state.root)
    app.state.max_request_body_bytes = 1_048_576

    @app.middleware("http")
    async def local_origin_guard(request: Request, call_next):
        content_length = request.headers.get("content-length")
        if content_length:
            try:
                oversized = int(content_length) > app.state.max_request_body_bytes
            except ValueError:
                oversized = True
            if oversized:
                return JSONResponse(status_code=413, content={"detail": {"code": "request_too_large", "stage": "request", "retryable": False, "next_action": "reduce request body"}})
        # Content-Length is optional for chunked requests. Buffer only up to the
        # configured cap, then expose the validated body to downstream handlers.
        if request.method in {"POST", "PUT", "PATCH", "DELETE"} and not content_length:
            chunks: list[bytes] = []
            total = 0
            async for chunk in request.stream():
                total += len(chunk)
                if total > app.state.max_request_body_bytes:
                    return JSONResponse(status_code=413, content={"detail": {"code": "request_too_large", "stage": "request", "retryable": False, "next_action": "reduce request body"}})
                chunks.append(chunk)
            request._body = b"".join(chunks)
        if request.method in {"POST", "PUT", "PATCH", "DELETE"}:
            host = (request.headers.get("host") or "").split(":", 1)[0].lower()
            origin = request.headers.get("origin")
            allowed_hosts = {"127.0.0.1", "localhost", "testserver"}
            if host and host not in allowed_hosts:
                return JSONResponse(status_code=403, content={"detail": {"code": "host_not_allowed", "stage": "auth", "retryable": False, "next_action": "use loopback host"}})
            if origin and not (origin.startswith("http://127.0.0.1") or origin.startswith("http://localhost") or origin.startswith("http://testserver")):
                return JSONResponse(status_code=403, content={"detail": {"code": "origin_not_allowed", "stage": "auth", "retryable": False, "next_action": "use loopback origin"}})
        return await call_next(request)

    def require_capability(token: str | None, scope: str, audience: str | None = None) -> None:
        if scope == "public":
            return
        if not token:
            raise HTTPException(status_code=401, detail={"code": "capability_token_required", "stage": "auth", "retryable": False, "next_action": "provide capability token"})
        if not secrets.compare_digest(token, app.state.capability_token):
            raise HTTPException(status_code=403, detail={"code": "capability_token_invalid", "stage": "auth", "retryable": False, "next_action": "request a fresh local token"})
        if time.time() - app.state.capability_token_created_at > app.state.capability_token_ttl_seconds:
            raise HTTPException(status_code=403, detail={"code": "capability_token_expired", "stage": "auth", "retryable": True, "next_action": "restart the local API for a fresh token"})
        if audience is not None and audience != "myknowledge-local-api":
            raise HTTPException(status_code=403, detail={"code": "capability_audience_invalid", "stage": "auth", "retryable": False, "next_action": "use the MyKnowledge local API audience"})

    def retrieve(req: RetrieveRequest, token: str | None = None, audience: str | None = None) -> dict:
        if req.scope not in {"public", "local", "private"}:
            raise HTTPException(status_code=400, detail={"code": "scope_invalid", "stage": "request", "retryable": False, "next_action": "use public/local/private"})
        require_capability(token, req.scope, audience)
        if len(req.vault_ids or []) > 16:
            raise HTTPException(status_code=400, detail={"code": "query_limit_exceeded", "stage": "request", "retryable": False, "next_action": "reduce vault_ids"})
        result = app.state.retriever.search(req.query, req.scope, req.top_k)
        if req.vault_ids:
            allowed = set(req.vault_ids)
            result["items"] = [x for x in result["items"] if x["object_ref"]["vault_id"] in allowed]
        return result

    @app.get("/api/health")
    def health() -> dict:
        return {"schema_version": "health/v1", "status": "ok", "api": "local"}

    @app.post("/api/retrieve")
    def retrieve_post(req: RetrieveRequest, x_myknowledge_capability: str | None = Header(default=None), x_myknowledge_audience: str | None = Header(default=None)) -> dict:
        return retrieve(req, x_myknowledge_capability, x_myknowledge_audience)

    @app.get("/api/query")
    def query_get(q: str = Query(min_length=1, max_length=4000), scope: str = "public", vault_ids: str | None = None, top_k: int = Query(default=8, ge=1, le=50), x_myknowledge_capability: str | None = Header(default=None), x_myknowledge_audience: str | None = Header(default=None)) -> dict:
        ids = [x for x in vault_ids.split(",") if x] if vault_ids else None
        return retrieve(RetrieveRequest(query=q, scope=scope, vault_ids=ids, top_k=top_k), x_myknowledge_capability, x_myknowledge_audience)

    @app.post("/api/ask")
    def ask(req: RetrieveRequest, x_myknowledge_capability: str | None = Header(default=None), x_myknowledge_audience: str | None = Header(default=None)) -> dict:
        retrieval = retrieve(req, x_myknowledge_capability, x_myknowledge_audience)
        return {"schema_version": "ask-result/v1", "answer": None, "citations": [], "retrieval": retrieval, "availability": "unavailable", "availability_reason": "provider_unavailable", "confidentiality": retrieval["confidentiality_max"], "limits": ["llm_unavailable"], "warnings": ["No LLM provider configured"]}

    def require_write_capability(token: str | None, audience: str | None = None) -> None:
        if not token:
            raise HTTPException(status_code=401, detail={"code": "capability_token_required", "stage": "auth", "retryable": False, "next_action": "provide capability token"})
        if not secrets.compare_digest(token, app.state.capability_token):
            raise HTTPException(status_code=403, detail={"code": "capability_token_invalid", "stage": "auth", "retryable": False, "next_action": "request a fresh local token"})
        if time.time() - app.state.capability_token_created_at > app.state.capability_token_ttl_seconds:
            raise HTTPException(status_code=403, detail={"code": "capability_token_expired", "stage": "auth", "retryable": True, "next_action": "restart the local API for a fresh token"})
        if audience is not None and audience != "myknowledge-local-api":
            raise HTTPException(status_code=403, detail={"code": "capability_audience_invalid", "stage": "auth", "retryable": False, "next_action": "use the MyKnowledge local API audience"})

    @app.post("/api/source/preview")
    def source_preview(req: WritePreviewRequest, x_myknowledge_capability: str | None = Header(default=None), x_myknowledge_audience: str | None = Header(default=None)) -> dict:
        require_write_capability(x_myknowledge_capability, x_myknowledge_audience)
        return {"schema_version": "operation-preview/v1", **app.state.writer.preview(req.files, operation_type="source", vault_id=req.vault_id)}

    @app.post("/api/wiki/preview")
    def wiki_preview(req: WritePreviewRequest, x_myknowledge_capability: str | None = Header(default=None), x_myknowledge_audience: str | None = Header(default=None)) -> dict:
        require_write_capability(x_myknowledge_capability, x_myknowledge_audience)
        return {"schema_version": "operation-preview/v1", **app.state.writer.preview(req.files, operation_type="wiki", vault_id=req.vault_id)}

    @app.post("/api/operation/{operation_id}/apply")
    def operation_apply(operation_id: str, req: ApplyRequest, x_myknowledge_capability: str | None = Header(default=None), x_myknowledge_audience: str | None = Header(default=None)) -> dict:
        require_write_capability(x_myknowledge_capability, x_myknowledge_audience)
        return {"schema_version": "operation-result/v1", **app.state.writer.apply(operation_id, confirmed=req.confirmed, actor_id=req.actor_id)}

    @app.get("/api/vault/check")
    def vault_check(x_myknowledge_capability: str | None = Header(default=None), x_myknowledge_audience: str | None = Header(default=None)) -> dict:
        require_write_capability(x_myknowledge_capability, x_myknowledge_audience)
        return VaultRegistry(app.state.root).check()

    @app.post("/api/validate/{vault_id}/{object_type}/{object_id}")
    def validate_object(vault_id: str, object_type: str, object_id: str, scope: str = "local", x_myknowledge_capability: str | None = Header(default=None)) -> dict:
        require_write_capability(x_myknowledge_capability)
        if object_type != "wiki":
            raise HTTPException(status_code=404, detail={"code": "object_type_not_supported", "stage": "validate", "retryable": False, "next_action": "validate a wiki object"})
        path = object_path(vault_id, object_type, object_id)
        report = WikiValidator(VaultRegistry(app.state.root).resolve_vault_path(vault_id)).validate(path)
        return {"schema_version": "validation-result/v1", "object_ref": {"vault_id": vault_id, "object_type": object_type, "object_id": object_id}, "report": report}

    def object_path(vault_id: str, object_type: str, object_id: str) -> Path:
        try:
            safe_id(vault_id); safe_id(object_id)
        except ValueError:
            raise HTTPException(status_code=422, detail={"code": "invalid_object_ref", "stage": "request", "retryable": False, "next_action": "use a safe vault_id/object_id"})
        if object_type not in {"wiki", "source"}:
            raise HTTPException(status_code=404, detail={"code": "object_type_not_found", "stage": "read", "retryable": False, "next_action": "use wiki or source"})
        try:
            owner_root = VaultRegistry(app.state.root).resolve_vault_path(vault_id)
        except (OSError, ValueError):
            raise HTTPException(status_code=404, detail={"code": "vault_unavailable", "stage": "read", "retryable": False, "next_action": "check vault registry"})
        base = owner_root / ("wiki" if object_type == "wiki" else "sources")
        matches = [p for p in base.rglob(f"{object_id}.md") if p.is_file() and not p.is_symlink()]
        if not matches: raise HTTPException(status_code=404, detail={"code": "object_not_found", "stage": "read", "retryable": False, "next_action": "check object_ref"})
        return matches[0]

    @app.get("/api/read/{vault_id}/{object_type}/{object_id}")
    def read_object(vault_id: str, object_type: str, object_id: str, scope: str = "public", x_myknowledge_capability: str | None = Header(default=None)) -> dict:
        require_capability(x_myknowledge_capability, scope)
        path = object_path(vault_id, object_type, object_id)
        owner_root = VaultRegistry(app.state.root).resolve_vault_path(vault_id)
        return {"schema_version": "read-result/v1", "object_ref": {"vault_id": vault_id, "object_type": object_type, "object_id": object_id}, "path": str(path.relative_to(owner_root)), "body": path.read_text(encoding="utf-8")}

    @app.get("/api/backlinks/{vault_id}/{object_type}/{object_id}")
    def backlinks(vault_id: str, object_type: str, object_id: str, scope: str = "public", x_myknowledge_capability: str | None = Header(default=None)) -> dict:
        require_capability(x_myknowledge_capability, scope)
        object_path(vault_id, object_type, object_id)
        owner_root = VaultRegistry(app.state.root).resolve_vault_path(vault_id)
        base = owner_root / "wiki"; results = []
        needle = f"{object_id}.md"
        for path in base.rglob("*.md"):
            if path.is_file() and needle in path.read_text(encoding="utf-8", errors="ignore"):
                results.append({"vault_id": vault_id, "object_type": "wiki", "object_id": path.stem})
        return {"schema_version": "backlinks-result/v1", "target": {"vault_id": vault_id, "object_type": object_type, "object_id": object_id}, "items": results}

    @app.post("/api/practice/{question_id}/answer")
    def practice_answer(question_id: str, response: Any = Body(...), scoring_mode: str = Query(default="manual", pattern="^(manual|deterministic|llm)$"), scope: str = "local", x_myknowledge_capability: str | None = Header(default=None)) -> dict:
        require_capability(x_myknowledge_capability, scope)
        try:
            return {"schema_version": "practice-answer/v1", **app.state.practice.answer(question_id, response, scoring_mode=scoring_mode)}
        except (OSError, ValueError):
            raise HTTPException(status_code=404, detail={"code": "question_not_found", "stage": "practice", "retryable": False, "next_action": "check question_id"})

    @app.post("/api/practice/{question_id}/review")
    def practice_review(question_id: str, rating: int, scope: str = "local", x_myknowledge_capability: str | None = Header(default=None)) -> dict:
        require_capability(x_myknowledge_capability, scope)
        try:
            return {"schema_version": "practice-review/v1", **app.state.practice.review(question_id, rating)}
        except (OSError, ValueError):
            raise HTTPException(status_code=404, detail={"code": "question_not_found", "stage": "practice", "retryable": False, "next_action": "check question_id"})

    return app

app = create_app()
