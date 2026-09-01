"""FastAPI local adapter (F006)。

分层：``schemas``（请求模型）/``errors``（错误契约）/``security``（回环防护与
capability 门禁）/``services``（检索与对象定位）。本模块只是组合根：装配
app.state、注册中间件、声明端点，不再承载协议细节与领域编排。
"""

from __future__ import annotations

import os
import secrets
import time
from contextlib import asynccontextmanager, suppress
from functools import partial
from pathlib import Path
from typing import Any

from fastapi import Body, FastAPI, Header, Query, Request

from tools.citation import replay as replay_citation
from tools.common import atomic_write, safe_id
from tools.indexing import Retriever, default_public_index_path
from tools.paths import RepoPaths
from tools.projection import PublicProjectionStore
from tools.question import QuestionStore
from tools.skill_runtime import dispatch
from tools.validation.validator import WikiValidator
from tools.vault_registry import VaultRegistry
from tools.write_operation import WriteOperation

from .errors import api_error
from .schemas import (
    ApplyRequest,
    CitationReplayRequest,
    RetrieveRequest,
    WritePreviewRequest,
)
from .security import local_origin_guard, require_capability, require_write_capability
from .services import require_scope, resolve_object_path, run_retrieve

QUERY_PARAMS = frozenset(
    {"q", "scope", "vault_ids", "top_k", "include_sources", "include_archive"}
)


def _load_public_projection(root: Path) -> list[dict]:
    """Strict allowlist + body loading via the single PublicProjectionStore.

    缺失/非法 manifest 降级为空检索（F006 离线设计），不扫描 canonical 内容。
    """
    return PublicProjectionStore(root).degraded_items()


def _object_ref(vault_id: str, object_type: str, object_id: str) -> dict[str, str]:
    return {
        "vault_id": vault_id,
        "object_type": object_type,
        "object_id": object_id,
    }


def _issue_capability_token(state: Any, capability_token: str | None) -> None:
    """装配 capability token 与作用域；未显式传 token 时落一份 0600 的本地凭据。"""
    state.capability_token = capability_token or secrets.token_urlsafe(32)
    state.capability_token_created_at = time.time()
    state.capability_token_ttl_seconds = 3600
    state.capability_scopes = {"local-read", "private-read", "vault-check", "write"}
    state.capability_token_path = None


def _persist_capability_token(state: Any) -> None:
    state_dir = RepoPaths(state.root).var_root / "state"
    state_dir.mkdir(parents=True, exist_ok=True)
    os.chmod(state_dir, 0o700)
    token_path = state_dir / "capability-token"
    atomic_write(token_path, state.capability_token.encode("ascii") + b"\n", 0o600)
    state.capability_token_path = token_path


@asynccontextmanager
async def _lifespan(application: FastAPI):
    yield
    token_path = getattr(application.state, "capability_token_path", None)
    if token_path is not None:
        with suppress(OSError):
            token_path.unlink(missing_ok=True)


def create_app(
    root: Path | None = None,
    *,
    items: list[dict] | None = None,
    capability_token: str | None = None,
) -> FastAPI:
    app = FastAPI(title="MyKnowledge Local API", version="v1", lifespan=_lifespan)
    state = app.state
    state.root = Path(root or ".").resolve()
    # F005：默认接线 var/state/index/public.sqlite3（存在即用；陈旧/损坏自动降级 LIKE）
    default_index = default_public_index_path(state.root)
    state.retriever = Retriever(
        list(items) if items is not None else _load_public_projection(state.root),
        index_path=default_index if default_index.exists() else None,
    )
    _issue_capability_token(state, capability_token)
    if capability_token is None and root is not None:
        _persist_capability_token(state)
    state.practice = QuestionStore(state.root)
    state.writer = WriteOperation(state.root)
    state.max_request_body_bytes = 1_048_576
    app.middleware("http")(local_origin_guard)

    # 端点内统一用这几个绑定好 state/root 的闭包，避免每处重复传状态
    authorize = partial(require_capability, state)
    authorize_write = partial(require_write_capability, state)
    retrieve = partial(run_retrieve, state)
    object_path = partial(resolve_object_path, state.root)

    @app.get("/api/health")
    def health() -> dict:
        return {"schema_version": "health/v1", "status": "ok", "api": "local"}

    @app.post("/api/retrieve")
    def retrieve_post(
        req: RetrieveRequest,
        x_myknowledge_capability: str | None = Header(default=None),
        x_myknowledge_audience: str | None = Header(default=None),
    ) -> dict:
        # 顺序与门禁语义绑定：force=True 的能力校验先行，scope 合法性由
        # run_retrieve 统一判定（未授权请求不应先泄露参数级错误）
        authorize(
            x_myknowledge_capability, req.scope, x_myknowledge_audience, force=True
        )
        return retrieve(req, x_myknowledge_capability, x_myknowledge_audience)

    @app.get("/api/query")
    def query_get(
        request: Request,
        q: str = Query(min_length=1, max_length=4000),
        scope: str = "public",
        vault_ids: str | None = None,
        top_k: int = Query(default=8, ge=1, le=50),
        include_sources: bool = False,
        include_archive: bool = False,
        x_myknowledge_capability: str | None = Header(default=None),
        x_myknowledge_audience: str | None = Header(default=None),
    ) -> dict:
        if set(request.query_params) - QUERY_PARAMS:
            raise api_error(
                400, "schema_invalid", "request", "remove unknown query parameters"
            )
        ids = [x for x in vault_ids.split(",") if x] if vault_ids else None
        return retrieve(
            RetrieveRequest(
                query=q,
                scope=scope,
                vault_ids=ids,
                top_k=top_k,
                include_sources=include_sources,
                include_archive=include_archive,
            ),
            x_myknowledge_capability,
            x_myknowledge_audience,
        )

    @app.post("/api/ask")
    def ask(
        req: RetrieveRequest,
        x_myknowledge_capability: str | None = Header(default=None),
        x_myknowledge_audience: str | None = Header(default=None),
    ) -> dict:
        authorize(
            x_myknowledge_capability, req.scope, x_myknowledge_audience, force=True
        )
        retrieval = retrieve(req, x_myknowledge_capability, x_myknowledge_audience)
        return {
            "schema_version": "ask-result/v1",
            "answer": None,
            "citations": [],
            "retrieval": retrieval,
            "availability": "unavailable",
            "availability_reason": "provider_unavailable",
            "confidentiality": retrieval["confidentiality_max"],
            "limits": ["llm_unavailable"],
            "warnings": ["No LLM provider configured"],
        }

    @app.post("/api/citation/replay")
    def citation_replay(
        req: CitationReplayRequest,
        scope: str = "local",
        x_myknowledge_capability: str | None = Header(default=None),
        x_myknowledge_audience: str | None = Header(default=None),
    ) -> dict:
        require_scope(scope)
        authorize(
            x_myknowledge_capability,
            scope,
            x_myknowledge_audience,
            force=scope != "public",
        )
        return {
            "schema_version": "citation-replay/v1",
            **replay_citation(req.citation, req.snapshot),
        }

    def _preview(req: WritePreviewRequest, operation_type: str) -> dict:
        return {
            "schema_version": "operation-preview/v1",
            **state.writer.preview(
                req.files, operation_type=operation_type, vault_id=req.vault_id
            ),
        }

    @app.post("/api/source/preview")
    def source_preview(
        req: WritePreviewRequest,
        x_myknowledge_capability: str | None = Header(default=None),
        x_myknowledge_audience: str | None = Header(default=None),
    ) -> dict:
        authorize_write(x_myknowledge_capability, x_myknowledge_audience)
        return _preview(req, "source")

    @app.post("/api/wiki/preview")
    def wiki_preview(
        req: WritePreviewRequest,
        x_myknowledge_capability: str | None = Header(default=None),
        x_myknowledge_audience: str | None = Header(default=None),
    ) -> dict:
        authorize_write(x_myknowledge_capability, x_myknowledge_audience)
        return _preview(req, "wiki")

    @app.post("/api/operation/{operation_id}/apply")
    def operation_apply(
        operation_id: str,
        req: ApplyRequest,
        x_myknowledge_capability: str | None = Header(default=None),
        x_myknowledge_audience: str | None = Header(default=None),
    ) -> dict:
        authorize_write(x_myknowledge_capability, x_myknowledge_audience)
        return {
            "schema_version": "operation-result/v1",
            **state.writer.apply(
                operation_id,
                confirmed=req.confirmed,
                actor_id=req.actor_id,
                confirmation=req.confirmation,
            ),
        }

    @app.get("/api/vault/check")
    def vault_check(
        x_myknowledge_capability: str | None = Header(default=None),
        x_myknowledge_audience: str | None = Header(default=None),
    ) -> dict:
        authorize_write(
            x_myknowledge_capability,
            x_myknowledge_audience,
            required_scope="vault-check",
        )
        return VaultRegistry(state.root).check()

    @app.post("/api/validate/{vault_id}/{object_type}/{object_id}")
    def validate_object(
        vault_id: str,
        object_type: str,
        object_id: str,
        x_myknowledge_capability: str | None = Header(default=None),
        x_myknowledge_audience: str | None = Header(default=None),
    ) -> dict:
        # 校验一律需要写能力（scope 在这里没有语义，不接受被忽略的入参）
        authorize_write(x_myknowledge_capability, x_myknowledge_audience)
        if object_type != "wiki":
            raise api_error(
                404, "object_type_not_supported", "validate", "validate a wiki object"
            )
        path = object_path(vault_id, object_type, object_id)
        report = WikiValidator(
            VaultRegistry(state.root).resolve_vault_path(vault_id)
        ).validate(path)
        return {
            "schema_version": "validation-result/v1",
            "object_ref": _object_ref(vault_id, object_type, object_id),
            "report": report,
        }

    @app.get("/api/read/{vault_id}/{object_type}/{object_id}")
    def read_object(
        vault_id: str,
        object_type: str,
        object_id: str,
        scope: str = "public",
        x_myknowledge_capability: str | None = Header(default=None),
        x_myknowledge_audience: str | None = Header(default=None),
    ) -> dict:
        authorize(
            x_myknowledge_capability,
            "private" if vault_id != "public" else scope,
            x_myknowledge_audience,
        )
        if vault_id == "public":
            return _read_public(object_id)
        path = object_path(vault_id, object_type, object_id)
        owner_root = VaultRegistry(state.root).resolve_vault_path(vault_id)
        return {
            "schema_version": "read-result/v1",
            "object_ref": _object_ref(vault_id, object_type, object_id),
            "path": str(path.relative_to(owner_root)),
            "body": path.read_text(encoding="utf-8"),
        }

    def _read_public(object_id: str) -> dict:
        """public 读只能来自 projection（与 Skill 同一实现）。

        不得 rglob canonical 内容，否则未发布 wiki 可被免 token 读取。
        """
        try:
            safe_id(object_id)
        except ValueError as exc:
            raise api_error(
                422, "invalid_object_ref", "request", "use a safe vault_id/object_id"
            ) from exc
        result = dispatch(
            "read", {"vault_id": "public", "object_id": object_id}, root=state.root
        )
        if result.get("state") != "ok" and "body" not in result:
            raise api_error(404, "object_not_found", "read", "check object_ref")
        return result

    @app.get("/api/backlinks/{vault_id}/{object_type}/{object_id}")
    def backlinks(
        vault_id: str,
        object_type: str,
        object_id: str,
        scope: str = "public",
        x_myknowledge_capability: str | None = Header(default=None),
        x_myknowledge_audience: str | None = Header(default=None),
    ) -> dict:
        authorize(
            x_myknowledge_capability,
            "private" if vault_id != "public" else scope,
            x_myknowledge_audience,
        )
        if vault_id == "public":
            # 同上：public 反链来自 projection，不扫 canonical
            result = dispatch(
                "backlinks",
                {"vault_id": "public", "object_id": object_id},
                root=state.root,
            )
            if result.get("target") is None:
                raise api_error(404, "object_not_found", "read", "check object_ref")
            return result
        object_path(vault_id, object_type, object_id)
        owner_root = VaultRegistry(state.root).resolve_vault_path(vault_id)
        needle = f"{object_id}.md"
        items = [
            _object_ref(vault_id, "wiki", path.stem)
            for path in RepoPaths(owner_root).wiki_root.rglob("*.md")
            if path.is_file()
            and needle in path.read_text(encoding="utf-8", errors="ignore")
        ]
        return {
            "schema_version": "backlinks-result/v1",
            "target": _object_ref(vault_id, object_type, object_id),
            "items": items,
        }

    @app.post("/api/practice/{question_id}/answer")
    def practice_answer(
        question_id: str,
        response: Any = Body(...),  # noqa: B008 - FastAPI 依赖注入的既定写法
        scoring_mode: str = Query(
            default="manual", pattern="^(manual|deterministic|llm)$"
        ),
        scope: str = "local",
        x_myknowledge_capability: str | None = Header(default=None),
        x_myknowledge_audience: str | None = Header(default=None),
    ) -> dict:
        authorize(x_myknowledge_capability, scope, x_myknowledge_audience)
        try:
            return {
                "schema_version": "practice-answer/v1",
                **state.practice.answer(
                    question_id, response, scoring_mode=scoring_mode
                ),
            }
        except (OSError, ValueError) as exc:
            raise api_error(
                404, "question_not_found", "practice", "check question_id"
            ) from exc

    @app.post("/api/practice/{question_id}/review")
    def practice_review(
        question_id: str,
        rating: int,
        scope: str = "local",
        x_myknowledge_capability: str | None = Header(default=None),
        x_myknowledge_audience: str | None = Header(default=None),
    ) -> dict:
        authorize(x_myknowledge_capability, scope, x_myknowledge_audience)
        try:
            return {
                "schema_version": "practice-review/v1",
                **state.practice.review(question_id, rating),
            }
        except (OSError, ValueError) as exc:
            raise api_error(
                404, "question_not_found", "practice", "check question_id"
            ) from exc

    return app


app = create_app()
