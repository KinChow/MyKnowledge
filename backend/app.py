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
from tools.content_registry import ContentRegistry
from tools.indexing import Retriever, default_public_index_path
from tools.paths import RepoPaths
from tools.projection import PublicProjectionStore
from tools.question import QuestionStore
from tools.question_quality import QuestionQualityService
from tools.skill_runtime import dispatch
from tools.validation.validator import WikiValidator
from tools.vault_registry import VaultRegistry

from .errors import api_error
from .schemas import (
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
    state.question_quality = QuestionQualityService(state.root)
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
                "schema_invalid", "request", "remove unknown query parameters"
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
            "status": "ok",
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
        # replay 现在直接返回统一信封（citation-replay/v1, status=ok, report.valid）。
        return replay_citation(req.citation, req.snapshot)

    @app.post("/api/write")
    def write_object(
        req: WritePreviewRequest,
        x_myknowledge_capability: str | None = Header(default=None),
        x_myknowledge_audience: str | None = Header(default=None),
    ) -> dict:
        """一次落盘（ADR-0019）：无 operation_id、无 confirmation、无恢复态。

        与 Skill 通道共用同一实现（`skill_runtime` 的 write action），只在 HTTP 层
        保留写能力门禁——审批由 `git diff` + `git commit` 承担。
        """
        authorize_write(x_myknowledge_capability, x_myknowledge_audience)
        result = dispatch(
            "write", {"files": req.files, "vault_id": req.vault_id}, root=state.root
        )
        if result.get("status") != "ok":
            # 越界/非法写入是调用方错误：按 status 轴判据映射到 422，透出结构化码。
            raise api_error(result["error_code"], "write", "check write request")
        return {**result, "schema_version": "write-result/v1"}

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
                "object_type_not_supported", "validate", "validate a wiki object"
            )
        path = object_path(vault_id, object_type, object_id)
        report = WikiValidator(
            VaultRegistry(state.root).resolve_vault_path(vault_id)
        ).validate(path)
        return {
            "schema_version": "validation-result/v1",
            "status": "ok",
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
            "status": "ok",
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
                "invalid_object_ref", "request", "use a safe vault_id/object_id"
            ) from exc
        result = dispatch(
            "read", {"vault_id": "public", "object_id": object_id}, root=state.root
        )
        if result.get("status") != "ok":
            raise api_error("object_not_found", "read", "check object_ref")
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
            if result.get("status") != "ok":
                raise api_error("object_not_found", "read", "check object_ref")
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
            "status": "ok",
            "target": _object_ref(vault_id, object_type, object_id),
            "items": items,
        }

    @app.get("/api/list/{vault_id}/{object_type}")
    def list_objects(
        vault_id: str,
        object_type: str,
        scope: str = "public",
        x_myknowledge_capability: str | None = Header(default=None),
        x_myknowledge_audience: str | None = Header(default=None),
    ) -> dict:
        """统一列举：经 ContentRegistry 路由（public wiki→projection，其余→repository）。"""
        authorize(
            x_myknowledge_capability,
            "private" if vault_id != "public" else scope,
            x_myknowledge_audience,
        )
        result = ContentRegistry(state.root).list(object_type, vault_id=vault_id)
        if result.get("status") != "ok":
            raise api_error(result["error_code"], "list", "check object_type/vault")
        return result

    @app.delete("/api/object/{vault_id}/{object_type}/{object_id}")
    def delete_object(
        vault_id: str,
        object_type: str,
        object_id: str,
        x_myknowledge_capability: str | None = Header(default=None),
        x_myknowledge_audience: str | None = Header(default=None),
    ) -> dict:
        """统一软删/退休：source=RESTRICT、wiki=CASCADE+CDR、question=有历史降 disable。"""
        authorize_write(x_myknowledge_capability, x_myknowledge_audience)
        try:
            result = ContentRegistry(state.root).delete(
                object_type, vault_id=vault_id, object_id=object_id
            )
        except (OSError, ValueError) as exc:
            # question 域的严格加载对缺失/损坏抛异常；边界归一为 404，不泄漏内部文本。
            raise api_error("object_not_found", "delete", "check object_ref") from exc
        if result.get("status") != "ok":
            raise api_error(
                result["error_code"], "delete", "check object_ref / references"
            )
        return result

    @app.post("/api/object/{vault_id}/{object_type}/{object_id}/purge")
    def purge_object(
        vault_id: str,
        object_type: str,
        object_id: str,
        x_myknowledge_capability: str | None = Header(default=None),
        x_myknowledge_audience: str | None = Header(default=None),
    ) -> dict:
        """永久硬删（两阶段）：须先 DELETE（软删）且过宽限期，再物理回收（source/wiki）。"""
        authorize_write(x_myknowledge_capability, x_myknowledge_audience)
        try:
            result = ContentRegistry(state.root).purge(
                object_type, vault_id=vault_id, object_id=object_id
            )
        except (OSError, ValueError) as exc:
            raise api_error("object_not_found", "purge", "check object_ref") from exc
        if result.get("status") != "ok":
            raise api_error(
                result["error_code"],
                "purge",
                "soft-delete first and wait out retention",
            )
        return result

    @app.post("/api/source/update")
    def update_source(
        request: Any = Body(...),  # noqa: B008 - FastAPI 依赖注入的既定写法
        x_myknowledge_capability: str | None = Header(default=None),
        x_myknowledge_audience: str | None = Header(default=None),
    ) -> dict:
        """source 重导入更新（幂等 + 保留 evidence_items）经 ContentRegistry 路由。"""
        from tools.ingest.source_request import (
            LocatorError,
            normalize_source_request,
        )

        authorize_write(x_myknowledge_capability, x_myknowledge_audience)
        if not isinstance(request, dict):
            raise api_error(
                "source_request_required", "update", "send a source ingest request"
            )
        # 与 create_source 一致的 scheme 门禁：拒 file://、legacy input_path，
        # 堵住经 update 用 file:// 重导入读取本地盘（网络侧本地文件泄露）。
        try:
            request = normalize_source_request(
                request, allowed_schemes={"http", "https", "data"}
            )
        except LocatorError as exc:
            raise api_error(
                exc.code, "update", "use an http(s)/data locator or inline content"
            ) from exc
        result = ContentRegistry(state.root).update("source", request=request)
        if result.get("status") != "ok":
            raise api_error(result["error_code"], "update", "check source request")
        return result

    @app.post("/api/source")
    def create_source(
        request: Any = Body(...),  # noqa: B008 - FastAPI 依赖注入的既定写法
        x_myknowledge_capability: str | None = Header(default=None),
        x_myknowledge_audience: str | None = Header(default=None),
    ) -> dict:
        """统一创建：接受 {locator|content, kind, domain, …} 契约（仅远程/内联，拒 file://）。"""
        from tools.ingest.source_request import (
            LocatorError,
            normalize_source_request,
        )

        authorize_write(x_myknowledge_capability, x_myknowledge_audience)
        if not isinstance(request, dict):
            raise api_error(
                "source_request_required", "create", "send a source create request"
            )
        try:
            internal = normalize_source_request(
                request, allowed_schemes={"http", "https", "data"}
            )
        except LocatorError as exc:
            raise api_error(
                exc.code, "create", "use an http(s)/data locator or inline content"
            ) from exc
        result = ContentRegistry(state.root).create("source", request=internal)
        if result.get("status") != "ok":
            raise api_error(result["error_code"], "create", "check source request")
        return result

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
            # 成功体透传领域信封的 status（含判分 unavailable/blocked 均为 200），
            # 仅在题目缺失/损坏（load 抛错）时映射到结构化 404。
            return {
                **state.practice.answer(
                    question_id, response, scoring_mode=scoring_mode
                ),
                "schema_version": "practice-answer/v1",
            }
        except (OSError, ValueError) as exc:
            raise api_error(
                "question_not_found", "practice", "check question_id"
            ) from exc

    @app.get("/api/practice/questions")
    def practice_questions(
        domain: str | None = Query(default=None, max_length=128),
        topic: str | None = Query(default=None, max_length=128),
        skill: str | None = Query(default=None, max_length=128),
        status: str = Query(default="enabled", pattern="^(enabled|disabled|all)$"),
        scope: str = "local",
        x_myknowledge_capability: str | None = Header(default=None),
        x_myknowledge_audience: str | None = Header(default=None),
    ) -> dict:
        authorize(x_myknowledge_capability, scope, x_myknowledge_audience)
        return {
            **state.practice.list(
                domain=domain, topic=topic, skill=skill, status=status
            ),
            "schema_version": "practice-question-catalog/v1",
        }

    @app.post("/api/practice/import")
    def practice_import(
        spec: Any = Body(...),  # noqa: B008 - FastAPI 依赖注入的既定写法
        x_myknowledge_capability: str | None = Header(default=None),
        x_myknowledge_audience: str | None = Header(default=None),
    ) -> dict:
        authorize_write(x_myknowledge_capability, x_myknowledge_audience)
        if not isinstance(spec, dict):
            raise api_error(
                "question_spec_invalid",
                "practice",
                "send one question JSON object",
            )
        # 导入效果（新写入 vs 幂等）在 changed 布尔，字段级失败在 blocked+errors；
        # 两者都是 200 成功体，透传领域信封 status，仅覆盖对外 schema_version。
        return {
            **state.practice.import_spec(spec),
            "schema_version": "practice-import/v1",
        }

    @app.post("/api/practice/sessions")
    def practice_session_create(
        size: int = Query(default=6),
        domain: str | None = Query(default=None, max_length=128),
        topic: str | None = Query(default=None, max_length=128),
        concept_id: str | None = Query(default=None, max_length=128),
        skill: str | None = Query(default=None, max_length=128),
        scope: str = "local",
        x_myknowledge_capability: str | None = Header(default=None),
        x_myknowledge_audience: str | None = Header(default=None),
    ) -> dict:
        authorize(x_myknowledge_capability, scope, x_myknowledge_audience)
        result = state.practice.create_session(
            size=size,
            domain=domain,
            topic=topic,
            concept_id=concept_id,
            skill=skill,
        )
        return {**result, "schema_version": "practice-session/v1"}

    @app.post("/api/practice/sessions/{session_id}/progress")
    def practice_session_progress(
        session_id: str,
        current_index: int = Query(..., ge=0),
        completed: bool = False,
        scope: str = "local",
        x_myknowledge_capability: str | None = Header(default=None),
        x_myknowledge_audience: str | None = Header(default=None),
    ) -> dict:
        authorize(x_myknowledge_capability, scope, x_myknowledge_audience)
        try:
            return {
                **state.practice.update_session(
                    session_id,
                    current_index=current_index,
                    completed=completed,
                ),
                "schema_version": "practice-session-progress/v1",
            }
        except OSError as exc:
            raise api_error(
                "session_not_found", "practice", "check session_id"
            ) from exc
        except ValueError as exc:
            code = str(exc)
            if code in {"session_index_invalid", "session_completion_invalid"}:
                raise api_error(code, "practice", "check session progress") from exc
            raise api_error(
                "session_not_found", "practice", "check session_id"
            ) from exc

    @app.get("/api/practice/sessions/{session_id}")
    def practice_session_get(
        session_id: str,
        scope: str = "local",
        x_myknowledge_capability: str | None = Header(default=None),
        x_myknowledge_audience: str | None = Header(default=None),
    ) -> dict:
        authorize(x_myknowledge_capability, scope, x_myknowledge_audience)
        try:
            return {
                **state.practice.get_session(session_id),
                "schema_version": "practice-session/v1",
            }
        except (OSError, ValueError) as exc:
            raise api_error(
                "session_not_found", "practice", "check session_id"
            ) from exc

    @app.get("/api/practice/errors")
    def practice_errors(
        limit: int = Query(default=10, ge=1, le=50),
        domain: str | None = Query(default=None, max_length=128),
        topic: str | None = Query(default=None, max_length=128),
        concept_id: str | None = Query(default=None, max_length=128),
        skill: str | None = Query(default=None, max_length=128),
        scope: str = "local",
        x_myknowledge_capability: str | None = Header(default=None),
        x_myknowledge_audience: str | None = Header(default=None),
    ) -> dict:
        authorize(x_myknowledge_capability, scope, x_myknowledge_audience)
        return {
            **state.practice.error_queue(
                limit=limit,
                domain=domain,
                topic=topic,
                concept_id=concept_id,
                skill=skill,
            ),
            "schema_version": "practice-error-queue/v1",
        }

    @app.get("/api/practice/queue")
    def practice_queue(
        size: int = Query(default=6),
        domain: str | None = Query(default=None, max_length=128),
        topic: str | None = Query(default=None, max_length=128),
        concept_id: str | None = Query(default=None, max_length=128),
        skill: str | None = Query(default=None, max_length=128),
        only_due: bool = False,
        scope: str = "local",
        x_myknowledge_capability: str | None = Header(default=None),
        x_myknowledge_audience: str | None = Header(default=None),
    ) -> dict:
        authorize(x_myknowledge_capability, scope, x_myknowledge_audience)
        return {
            **state.practice.review_queue(
                size=size,
                domain=domain,
                topic=topic,
                concept_id=concept_id,
                skill=skill,
                include_new=not only_due,
            ),
            "schema_version": "practice-review-queue/v1",
        }

    @app.post("/api/practice/{question_id}/disable")
    def practice_disable(
        question_id: str,
        reason: str = Query(default="manual", max_length=128),
        scope: str = "local",
        x_myknowledge_capability: str | None = Header(default=None),
        x_myknowledge_audience: str | None = Header(default=None),
    ) -> dict:
        authorize(x_myknowledge_capability, scope, x_myknowledge_audience)
        try:
            return {
                **state.practice.disable(question_id, reason=reason),
                "schema_version": "practice-question-lifecycle/v1",
            }
        except (OSError, ValueError) as exc:
            raise api_error(
                "question_not_found", "practice", "check question_id"
            ) from exc

    @app.post("/api/practice/{question_id}/enable")
    def practice_enable(
        question_id: str,
        scope: str = "local",
        x_myknowledge_capability: str | None = Header(default=None),
        x_myknowledge_audience: str | None = Header(default=None),
    ) -> dict:
        authorize(x_myknowledge_capability, scope, x_myknowledge_audience)
        try:
            return {
                **state.practice.enable(question_id),
                "schema_version": "practice-question-lifecycle/v1",
            }
        except (OSError, ValueError) as exc:
            raise api_error(
                "question_not_found", "practice", "check question_id"
            ) from exc

    @app.delete("/api/practice/{question_id}")
    def practice_delete(
        question_id: str,
        scope: str = "local",
        x_myknowledge_capability: str | None = Header(default=None),
        x_myknowledge_audience: str | None = Header(default=None),
    ) -> dict:
        authorize(x_myknowledge_capability, scope, x_myknowledge_audience)
        try:
            return {
                **ContentRegistry(state.root).delete("question", object_id=question_id),
                "schema_version": "practice-question-lifecycle/v1",
            }
        except (OSError, ValueError) as exc:
            raise api_error(
                "question_not_found", "practice", "check question_id"
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
                **state.practice.review(question_id, rating),
                "schema_version": "practice-review/v1",
            }
        except (OSError, ValueError) as exc:
            raise api_error(
                "question_not_found", "practice", "check question_id"
            ) from exc

    @app.post("/api/practice/{question_id}/quality")
    def practice_quality(
        question_id: str,
        mode: str = Query(default="deterministic", pattern="^(deterministic|llm)$"),
        scope: str = "local",
        x_myknowledge_capability: str | None = Header(default=None),
        x_myknowledge_audience: str | None = Header(default=None),
    ) -> dict:
        authorize(x_myknowledge_capability, scope, x_myknowledge_audience)
        result = state.question_quality.validate(question_id, mode=mode)
        if result.get("status") == "blocked":
            if result.get("error_code") == "question_not_found":
                raise api_error("question_not_found", "practice", "check question_id")
            raise api_error(result["error_code"], "practice", "check quality mode")
        return result

    return app


app = create_app()
