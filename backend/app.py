"""FastAPI local adapter (F006)."""
from __future__ import annotations
import os
import time
import secrets
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any
from fastapi import Body, FastAPI, Header, HTTPException, Query, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict, Field
from tools.indexing import Retriever
from tools.common import atomic_write, safe_id
from tools.projection import PublicProjectionStore
from tools.question import QuestionStore
from tools.write_operation import WriteOperation
from tools.vault_registry import VaultRegistry
from tools.validation.validator import WikiValidator
from tools.citation import replay as replay_citation
from tools.capability import check_capability, required_scope_for

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

class CitationReplayRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    citation: dict[str, Any]
    snapshot: str = Field(min_length=1, max_length=2_000_000)


def _load_public_projection(root: Path) -> list[dict]:
    """Strict allowlist + body loading via the single PublicProjectionStore.

    缺失/非法 manifest 降级为空检索（F006 离线设计），不扫描 canonical 内容。
    """
    return PublicProjectionStore(root).degraded_items()

def create_app(root: Path | None = None, *, items: list[dict] | None = None, capability_token: str | None = None) -> FastAPI:
    @asynccontextmanager
    async def lifespan(application: FastAPI):
        yield
        token_path = getattr(application.state, "capability_token_path", None)
        if token_path is not None:
            try:
                token_path.unlink(missing_ok=True)
            except OSError:
                pass

    app = FastAPI(title="MyKnowledge Local API", version="v1", lifespan=lifespan)
    app.state.root = Path(root or ".").resolve()
    app.state.retriever = Retriever(list(items) if items is not None else _load_public_projection(app.state.root))
    app.state.capability_token = capability_token or secrets.token_urlsafe(32)
    app.state.capability_token_created_at = time.time()
    app.state.capability_token_ttl_seconds = 3600
    app.state.capability_scopes = {"local-read", "private-read", "vault-check", "write"}
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

    def _capability_error(result: tuple[str, bool, str], status_code: int) -> HTTPException:
        code, retryable, next_action = result
        return HTTPException(status_code=status_code, detail={"code": code, "stage": "auth", "retryable": retryable, "next_action": next_action})

    def require_capability(token: str | None, scope: str, audience: str | None = None, *, force: bool = False, required_scope: str | None = None) -> None:
        """HTTP adapter over tools.capability.check_capability (single core)."""
        result = check_capability(
            token, app.state.capability_token,
            created_at=app.state.capability_token_created_at,
            ttl_seconds=app.state.capability_token_ttl_seconds,
            scopes=app.state.capability_scopes,
            required_scope=required_scope if required_scope is not None else required_scope_for(scope, force=force),
            audience=audience,
            skip=scope == "public" and not force,
        )
        if result is None:
            return
        # token 缺失是 401，其余校验失败是 403（与原实现一致）
        raise _capability_error(result, 401 if result[0] == "capability_token_required" else 403)

    def require_write_capability(token: str | None, audience: str | None = None, *, required_scope: str = "write") -> None:
        require_capability(token, "write", audience, force=True, required_scope=required_scope)

    def retrieve(req: RetrieveRequest, token: str | None = None, audience: str | None = None) -> dict:
        if req.scope not in {"public", "local", "private"}:
            raise HTTPException(status_code=400, detail={"code": "scope_invalid", "stage": "request", "retryable": False, "next_action": "use public/local/private"})
        require_capability(token, req.scope, audience)
        if req.scope == "private" and not req.vault_ids:
            raise HTTPException(status_code=400, detail={"code": "vault_ids_required", "stage": "request", "retryable": False, "next_action": "select one or more internal vault_ids"})
        if len(req.vault_ids or []) > 16:
            raise HTTPException(status_code=400, detail={"code": "query_limit_exceeded", "stage": "request", "retryable": False, "next_action": "reduce vault_ids"})
        return app.state.retriever.search(req.query, req.scope, req.top_k, req.vault_ids)

    @app.get("/api/health")
    def health() -> dict:
        return {"schema_version": "health/v1", "status": "ok", "api": "local"}

    @app.post("/api/retrieve")
    def retrieve_post(req: RetrieveRequest, x_myknowledge_capability: str | None = Header(default=None), x_myknowledge_audience: str | None = Header(default=None)) -> dict:
        require_capability(x_myknowledge_capability, req.scope, x_myknowledge_audience, force=True)
        return retrieve(req, x_myknowledge_capability, x_myknowledge_audience)

    @app.get("/api/query")
    def query_get(request: Request, q: str = Query(min_length=1, max_length=4000), scope: str = "public", vault_ids: str | None = None, top_k: int = Query(default=8, ge=1, le=50), include_sources: bool = False, include_archive: bool = False, x_myknowledge_capability: str | None = Header(default=None), x_myknowledge_audience: str | None = Header(default=None)) -> dict:
        unknown = set(request.query_params) - {"q", "scope", "vault_ids", "top_k", "include_sources", "include_archive"}
        if unknown:
            raise HTTPException(status_code=400, detail={"code": "schema_invalid", "stage": "request", "retryable": False, "next_action": "remove unknown query parameters"})
        ids = [x for x in vault_ids.split(",") if x] if vault_ids else None
        return retrieve(RetrieveRequest(query=q, scope=scope, vault_ids=ids, top_k=top_k, include_sources=include_sources, include_archive=include_archive), x_myknowledge_capability, x_myknowledge_audience)

    @app.post("/api/ask")
    def ask(req: RetrieveRequest, x_myknowledge_capability: str | None = Header(default=None), x_myknowledge_audience: str | None = Header(default=None)) -> dict:
        require_capability(x_myknowledge_capability, req.scope, x_myknowledge_audience, force=True)
        retrieval = retrieve(req, x_myknowledge_capability, x_myknowledge_audience)
        return {"schema_version": "ask-result/v1", "answer": None, "citations": [], "retrieval": retrieval, "availability": "unavailable", "availability_reason": "provider_unavailable", "confidentiality": retrieval["confidentiality_max"], "limits": ["llm_unavailable"], "warnings": ["No LLM provider configured"]}

    @app.post("/api/citation/replay")
    def citation_replay(req: CitationReplayRequest, scope: str = "local", x_myknowledge_capability: str | None = Header(default=None), x_myknowledge_audience: str | None = Header(default=None)) -> dict:
        if scope not in {"public", "local", "private"}:
            raise HTTPException(status_code=400, detail={"code": "scope_invalid", "stage": "request", "retryable": False, "next_action": "use public/local/private"})
        require_capability(x_myknowledge_capability, scope, x_myknowledge_audience, force=scope != "public")
        return {"schema_version": "citation-replay/v1", **replay_citation(req.citation, req.snapshot)}

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
        require_write_capability(x_myknowledge_capability, x_myknowledge_audience, required_scope="vault-check")
        return VaultRegistry(app.state.root).check()

    @app.post("/api/validate/{vault_id}/{object_type}/{object_id}")
    def validate_object(vault_id: str, object_type: str, object_id: str, scope: str = "local", x_myknowledge_capability: str | None = Header(default=None), x_myknowledge_audience: str | None = Header(default=None)) -> dict:
        require_write_capability(x_myknowledge_capability, x_myknowledge_audience)
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
    def read_object(vault_id: str, object_type: str, object_id: str, scope: str = "public", x_myknowledge_capability: str | None = Header(default=None), x_myknowledge_audience: str | None = Header(default=None)) -> dict:
        require_capability(x_myknowledge_capability, "private" if vault_id != "public" else scope, x_myknowledge_audience)
        if vault_id == "public":
            # public 读只能来自 projection（与 Skill 同一实现）；
            # 不得 rglob canonical 内容，否则未发布 wiki 可被免 token 读取
            try:
                safe_id(object_id)
            except ValueError:
                raise HTTPException(status_code=422, detail={"code": "invalid_object_ref", "stage": "request", "retryable": False, "next_action": "use a safe vault_id/object_id"})
            from tools.skill_runtime import dispatch
            result = dispatch("read", {"vault_id": "public", "object_id": object_id}, root=app.state.root)
            if result.get("state") != "ok" and "body" not in result:
                raise HTTPException(status_code=404, detail={"code": "object_not_found", "stage": "read", "retryable": False, "next_action": "check object_ref"})
            return result
        path = object_path(vault_id, object_type, object_id)
        owner_root = VaultRegistry(app.state.root).resolve_vault_path(vault_id)
        return {"schema_version": "read-result/v1", "object_ref": {"vault_id": vault_id, "object_type": object_type, "object_id": object_id}, "path": str(path.relative_to(owner_root)), "body": path.read_text(encoding="utf-8")}

    @app.get("/api/backlinks/{vault_id}/{object_type}/{object_id}")
    def backlinks(vault_id: str, object_type: str, object_id: str, scope: str = "public", x_myknowledge_capability: str | None = Header(default=None), x_myknowledge_audience: str | None = Header(default=None)) -> dict:
        require_capability(x_myknowledge_capability, "private" if vault_id != "public" else scope, x_myknowledge_audience)
        if vault_id == "public":
            # 同上：public 反链来自 projection，不扫 canonical
            from tools.skill_runtime import dispatch
            result = dispatch("backlinks", {"vault_id": "public", "object_id": object_id}, root=app.state.root)
            if result.get("target") is None:
                raise HTTPException(status_code=404, detail={"code": "object_not_found", "stage": "read", "retryable": False, "next_action": "check object_ref"})
            return result
        object_path(vault_id, object_type, object_id)
        owner_root = VaultRegistry(app.state.root).resolve_vault_path(vault_id)
        base = owner_root / "wiki"; results = []
        needle = f"{object_id}.md"
        for path in base.rglob("*.md"):
            if path.is_file() and needle in path.read_text(encoding="utf-8", errors="ignore"):
                results.append({"vault_id": vault_id, "object_type": "wiki", "object_id": path.stem})
        return {"schema_version": "backlinks-result/v1", "target": {"vault_id": vault_id, "object_type": object_type, "object_id": object_id}, "items": results}

    @app.post("/api/practice/{question_id}/answer")
    def practice_answer(question_id: str, response: Any = Body(...), scoring_mode: str = Query(default="manual", pattern="^(manual|deterministic|llm)$"), scope: str = "local", x_myknowledge_capability: str | None = Header(default=None), x_myknowledge_audience: str | None = Header(default=None)) -> dict:
        require_capability(x_myknowledge_capability, scope, x_myknowledge_audience)
        try:
            return {"schema_version": "practice-answer/v1", **app.state.practice.answer(question_id, response, scoring_mode=scoring_mode)}
        except (OSError, ValueError):
            raise HTTPException(status_code=404, detail={"code": "question_not_found", "stage": "practice", "retryable": False, "next_action": "check question_id"})

    @app.post("/api/practice/{question_id}/review")
    def practice_review(question_id: str, rating: int, scope: str = "local", x_myknowledge_capability: str | None = Header(default=None), x_myknowledge_audience: str | None = Header(default=None)) -> dict:
        require_capability(x_myknowledge_capability, scope, x_myknowledge_audience)
        try:
            return {"schema_version": "practice-review/v1", **app.state.practice.review(question_id, rating)}
        except (OSError, ValueError):
            raise HTTPException(status_code=404, detail={"code": "question_not_found", "stage": "practice", "retryable": False, "next_action": "check question_id"})

    return app

app = create_app()
