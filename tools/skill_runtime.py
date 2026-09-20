"""受控 Agent Skill 运行适配器（F009）。

只接受结构化 action 白名单，并把实际工作委托给现有领域服务；不执行
任意 shell，不接受物理路径写入，也不暴露 capability token。

写入是**直接落盘**（ADR-0019）：``write`` / ``source_ingest`` 一次调用完成，
不经 operation 状态机、不取 per-vault 锁、不产生人工确认事件；``write`` 同时是
通用文件写入的唯一收口（写前只剩越界与 `content/working/` 回指两条约束）。

结构：``dispatch`` 只做通道级门禁（白名单 / 禁用键 / 未知字段），每个 action
一个 ``_handle_*`` 函数，映射表 ``_HANDLERS`` 是唯一的 action 事实来源
（``ALLOWED_ACTIONS`` 由它派生）。字段级非法一律 ``raise ValueError("<error_code>")``，
由 ``dispatch`` 统一收敛成 ``{"state": "blocked", "error_code": ...}``。
"""

from __future__ import annotations

from collections.abc import Callable, Mapping
from pathlib import Path
from typing import Any

from . import contract
from .backup import BackupManager
from .common import atomic_write, safe_id
from .content_registry import ContentRegistry
from .indexing import Retriever
from .ingest.source_ingestor import SourceIngestor
from .projection import PublicProjectionStore
from .question import QuestionStore
from .release_confirmation import write_event
from .validation.validator import WikiValidator
from .vault_registry import VaultRegistry

FORBIDDEN_KEYS = frozenset(
    {
        "shell",
        "command",
        "exec",
        "git",
        "path",
        "absolute_path",
        "capability_token",
        "api_key",
    }
)
ACTION_FIELDS = {
    "skill_status": set(),
    "query": {"query", "scope", "top_k"},
    "retrieve": {"query", "scope", "top_k"},
    "ask": {"query", "scope", "top_k"},
    "read": {"vault_id", "object_id"},
    "backlinks": {"vault_id", "object_id"},
    "write": {"files", "vault_id"},
    "source_ingest": {"request"},
    "wiki_validate": {"wiki_path"},
    "publish_preview": {"wiki_path"},
    "publish_confirm": {"event"},
    "vault_check": set(),
    "backup_status": set(),
    "backup_manifest": {"vault_id"},
    "question_create": {"spec", "wiki_path"},
    "question_list": {"domain", "topic", "skill", "status"},
    "question_session": {"size", "domain", "topic", "concept_id", "skill"},
    "question_errors": {"limit", "domain", "topic", "concept_id", "skill"},
    "question_queue": {"size", "domain", "topic", "concept_id", "skill", "only_due"},
    "question_disable": {"question_id", "reason"},
    "question_enable": {"question_id"},
    "question_delete": {"question_id"},
    "question_answer": {"question_id", "response", "scoring_mode"},
    "question_review": {"question_id", "rating"},
    "list": {"object_type", "vault_id", "domain", "topic", "skill", "status"},
    "delete": {"object_type", "vault_id", "object_id"},
    "purge": {"object_type", "vault_id", "object_id"},
    "source_update": {"request"},
}


def _public_projection_items(root: Path) -> list[dict[str, Any]]:
    """严格版 public projection 加载，单实现见 projection.PublicProjectionStore。"""
    return PublicProjectionStore(root).public_items(with_body=True)


def _public_object_ref(object_id: str) -> dict[str, str]:
    return {"vault_id": "public", "object_type": "wiki", "object_id": object_id}


def _public_object_id(payload: dict[str, Any]) -> str:
    """Agent 通道只读 public vault；private/local 必须走带 capability 的 API。"""
    if payload.get("vault_id", "public") != "public":
        raise ValueError("skill_private_read_requires_api")
    return safe_id(str(payload.get("object_id", "")))


def _repo_relative_path(root: Path, payload: dict[str, Any]) -> Path:
    """把 payload 里的 wiki_path 解析成仓库内路径；越界或缺失都是结构化错误。"""
    wiki_path = payload.get("wiki_path")
    if not isinstance(wiki_path, str) or not wiki_path:
        raise ValueError("wiki_path_required")
    candidate = (root / wiki_path).resolve()
    try:
        candidate.relative_to(root)
    except ValueError:
        raise ValueError("path_invalid") from None
    return candidate


def _require_mapping(
    payload: dict[str, Any], key: str, error_code: str
) -> dict[str, Any]:
    value = payload.get(key)
    if not isinstance(value, dict):
        raise ValueError(error_code)
    return value


def _handle_skill_status(root: Path, _payload: dict[str, Any]) -> dict[str, Any]:
    skill = root / "skills" / "myknowledge" / "SKILL.md"
    if not skill.is_file() or skill.is_symlink():
        return contract.unavailable(
            "skill-status/v1", "skill_unavailable", reason="canonical_skill_missing"
        )
    text = skill.read_text(encoding="utf-8")
    required = ("name: myknowledge", "tools.cli", "explicit human confirmation")
    if any(marker not in text for marker in required):
        return contract.unavailable(
            "skill-status/v1", "skill_unavailable", reason="canonical_skill_invalid"
        )
    return contract.ok("skill-status/v1", skill="myknowledge")


def _handle_query(root: Path, payload: dict[str, Any]) -> dict[str, Any]:
    if str(payload.get("scope", "public")) != "public" or not isinstance(
        payload.get("query"), str
    ):
        raise ValueError("skill_public_query_only")
    from .indexing import default_public_index_path

    index_path = default_public_index_path(root)
    return Retriever(
        _public_projection_items(root),
        index_path=index_path if index_path.exists() else None,
    ).search(payload["query"], "public", int(payload.get("top_k", 8)))


def _handle_ask(root: Path, payload: dict[str, Any]) -> dict[str, Any]:
    """Agent 通道没有 LLM provider，只回检索结果 + 不可用理由，绝不编造答案。"""
    retrieval = _handle_query(root, payload)
    # 离线通道没有 LLM provider：这是**定义好的成功回退**（status=ok），
    # provider 缺失作为 availability 领域字段暴露，绝不编造答案。
    return contract.ok(
        "ask-result/v1",
        answer=None,
        citations=[],
        retrieval=retrieval,
        availability="unavailable",
        availability_reason="provider_unavailable",
        confidentiality=retrieval.get("confidentiality_max", "public"),
        limits=["llm_unavailable"],
        warnings=["No LLM provider configured"],
    )


def _handle_read(root: Path, payload: dict[str, Any]) -> dict[str, Any]:
    # 公共 wiki 读经统领入口 ContentRegistry（单份 projection 读实现），此处只保留
    # Skill 通道的 public-only 门禁与既有返回契约（read-result/v1，raise 由 dispatch 收敛）。
    object_id = _public_object_id(payload)
    result = ContentRegistry(root).read("wiki", object_id=object_id)
    if result["status"] != "ok":
        raise ValueError(result["error_code"])
    return contract.ok(
        "read-result/v1",
        object_ref=_public_object_ref(object_id),
        path=result["path"],
        body=result["body"],
    )


def _handle_backlinks(root: Path, payload: dict[str, Any]) -> dict[str, Any]:
    object_id = _public_object_id(payload)
    items = _public_projection_items(root)
    if not any(item["object_id"] == object_id for item in items):
        raise ValueError("object_not_found")
    needle = f"/wiki/{object_id}"
    results = [
        _public_object_ref(item["object_id"])
        for item in items
        if item["object_id"] != object_id
        and (
            needle in item["body"]
            or object_id
            in {str(link).strip("/").split("/")[-1] for link in item.get("links", [])}
        )
    ]
    return contract.ok(
        "backlinks-result/v1",
        target=_public_object_ref(object_id),
        items=results,
    )


def _vault_root(root: Path, vault_id: str) -> Path:
    """写入目标的 Vault 根：public 即 checkout 根，其余走 Registry 的 owner checkout。"""
    if vault_id == "public":
        return root
    return VaultRegistry(root).resolve_vault_path(vault_id)


def _write_target(vault_root: Path, name: str) -> Path:
    """解析写入目标：拒绝符号链接路径段、越界路径与共享 inode 的 hard-link。

    这三条是写前唯一与"谁批准"无关的检查（越界写入不可逆），不随 ADR-0019 退场。
    """
    current = vault_root
    for part in Path(name).parts:
        if part in {"", "."}:
            continue
        current = current / part
        if current.is_symlink():
            raise ValueError("path_symlink")
    path = (vault_root / name).resolve()
    try:
        path.relative_to(vault_root)
    except ValueError:
        raise ValueError("path_outside_repo") from None
    if path == vault_root:
        raise ValueError("invalid_target")
    if path.exists() and path.stat().st_nlink > 1:
        raise ValueError("path_hardlink")
    return path


def _write_files(root: Path, files: Mapping[str, str], vault_id: str) -> dict[str, Any]:
    """把 files 直接落盘（ADR-0019）：写前校验 → `atomic_write`，无 operation/锁/确认。

    保留的写前约束只有一条能捕获真实缺陷的：目标必须落在 Vault 根内且各段都不是
    符号链接（越界写不可逆）。`content/working/` 的出处门已删除（A1-深，2026-09-15）：
    出处校验统一归晋升关口（通道 A 的 wiki 校验/审计），不放在暂存入口。**不保留**
    before-hash 比对、多文件回滚与提交收尾状态机：半成品由 `git status` 可见、由
    git 回滚，这正是"审批 = git"的代价与收益。
    """
    if not files:
        raise ValueError("empty_write")
    vault_root = _vault_root(root, vault_id)
    targets: list[tuple[Path, str]] = []
    for name, content in sorted(files.items()):
        if not isinstance(content, str):
            raise ValueError("content_not_string")
        path = _write_target(vault_root, name)
        targets.append((path, content))
    applied_files: list[str] = []
    for path, content in targets:
        try:
            atomic_write(path, content.encode("utf-8"))
        except OSError:
            # 逐文件独立提交：已落盘的前几个不做回滚（ADR-0019 把事务边界缩到
            # "临时文件 + os.replace"，多文件的半成品交给 git 审核与回滚）。
            raise ValueError("apply_failed") from None
        applied_files.append(str(path.relative_to(vault_root)))
    return contract.ok(
        "write-result/v1",
        changed=True,
        vault_id=vault_id,
        applied_files=applied_files,
    )


def _handle_write(root: Path, payload: dict[str, Any]) -> dict[str, Any]:
    """通用写入：直接落盘（ADR-0019），无 preview/apply 两阶段、无人工确认事件。"""
    files = _require_mapping(payload, "files", "files_required")
    return _write_files(root, files, str(payload.get("vault_id", "public")))


def _handle_source_ingest(root: Path, payload: dict[str, Any]) -> dict[str, Any]:
    """Source 采集：直接写（ADR-0019），无 operation 记录、无确认事件。"""
    from .ingest.source_request import normalize_source_request

    request = _require_mapping(payload, "request", "source_request_required")
    # agent 面安全门禁：只允许远程/内联（http/https/data），拒 file:// 与本地 input_path。
    request = normalize_source_request(
        request, allowed_schemes={"http", "https", "data"}
    )
    return SourceIngestor(root).ingest(request)


def _handle_wiki_validate(root: Path, payload: dict[str, Any]) -> dict[str, Any]:
    return WikiValidator(root).validate(_repo_relative_path(root, payload))


def _handle_publish_preview(root: Path, payload: dict[str, Any]) -> dict[str, Any]:
    report = _handle_wiki_validate(root, payload)
    derived = report.get("derived") or {}
    # 校验结论（可否发布）是领域判定，进 report.* 领域字段，不进 status 轴：
    # 预览动作本身成功执行即 status=ok，wiki_report 透传底层校验器（未迁移）。
    return contract.ok(
        "publish-preview/v1",
        wiki_report=report,
        public_publishable=derived.get("public_publishable", False),
        private_publishable=derived.get("private_publishable", False),
        report={
            "valid": bool(report.get("valid")),
            "public_publishable": derived.get("public_publishable", False),
            "private_publishable": derived.get("private_publishable", False),
        },
    )


def _handle_publish_confirm(root: Path, payload: dict[str, Any]) -> dict[str, Any]:
    return write_event(
        root, _require_mapping(payload, "event", "publish_event_required")
    )


def _handle_vault_check(root: Path, _payload: dict[str, Any]) -> dict[str, Any]:
    return VaultRegistry(root).check()


def _handle_backup_status(root: Path, _payload: dict[str, Any]) -> dict[str, Any]:
    return BackupManager(root).status()


def _handle_backup_manifest(root: Path, payload: dict[str, Any]) -> dict[str, Any]:
    return BackupManager(root).create_manifest(str(payload.get("vault_id", "public")))


def _handle_question_create(root: Path, payload: dict[str, Any]) -> dict[str, Any]:
    spec = _require_mapping(payload, "spec", "spec_required")
    candidate = _repo_relative_path(root, payload)
    if not candidate.is_file() or candidate.is_symlink():
        raise ValueError("wiki_not_found")
    report = WikiValidator(root).validate(candidate)
    # 经统领入口 ContentRegistry 路由（question create 能力）；wiki 校验编排仍在此。
    return ContentRegistry(root).create(
        "question", spec=spec, wiki_path=candidate, wiki_report=report
    )


def _handle_question_answer(root: Path, payload: dict[str, Any]) -> dict[str, Any]:
    scoring_mode = payload.get("scoring_mode", "manual")
    if scoring_mode not in {"manual", "deterministic", "llm"}:
        raise ValueError("scoring_mode_invalid")
    return QuestionStore(root).answer(
        str(payload.get("question_id", "")),
        payload.get("response"),
        scoring_mode=scoring_mode,
    )


def _handle_question_list(root: Path, payload: dict[str, Any]) -> dict[str, Any]:
    status = payload.get("status", "enabled")
    if status not in {"enabled", "disabled", "all"}:
        raise ValueError("question_status_invalid")
    return ContentRegistry(root).list(
        "question",
        domain=payload.get("domain"),
        topic=payload.get("topic"),
        skill=payload.get("skill"),
        status=status,
    )


def _handle_question_session(root: Path, payload: dict[str, Any]) -> dict[str, Any]:
    return QuestionStore(root).create_session(
        size=payload.get("size", 6),
        domain=payload.get("domain"),
        topic=payload.get("topic"),
        concept_id=payload.get("concept_id"),
        skill=payload.get("skill"),
    )


def _handle_question_errors(root: Path, payload: dict[str, Any]) -> dict[str, Any]:
    return QuestionStore(root).error_queue(
        limit=payload.get("limit", 10),
        domain=payload.get("domain"),
        topic=payload.get("topic"),
        concept_id=payload.get("concept_id"),
        skill=payload.get("skill"),
    )


def _handle_question_queue(root: Path, payload: dict[str, Any]) -> dict[str, Any]:
    return QuestionStore(root).review_queue(
        size=payload.get("size", 6),
        domain=payload.get("domain"),
        topic=payload.get("topic"),
        concept_id=payload.get("concept_id"),
        skill=payload.get("skill"),
        include_new=not payload.get("only_due", False),
    )


def _handle_question_disable(root: Path, payload: dict[str, Any]) -> dict[str, Any]:
    return QuestionStore(root).disable(
        str(payload.get("question_id", "")),
        reason=str(payload.get("reason", "manual")),
    )


def _handle_question_enable(root: Path, payload: dict[str, Any]) -> dict[str, Any]:
    return QuestionStore(root).enable(str(payload.get("question_id", "")))


def _handle_question_delete(root: Path, payload: dict[str, Any]) -> dict[str, Any]:
    return ContentRegistry(root).delete(
        "question", object_id=str(payload.get("question_id", ""))
    )


def _handle_list(root: Path, payload: dict[str, Any]) -> dict[str, Any]:
    """统一列举：object_type 经 ContentRegistry 路由（source/wiki 用 vault_id，question 用分类过滤）。"""
    return ContentRegistry(root).list(
        str(payload.get("object_type", "")),
        vault_id=payload.get("vault_id", "public"),
        domain=payload.get("domain"),
        topic=payload.get("topic"),
        skill=payload.get("skill"),
        status=payload.get("status", "enabled"),
    )


def _handle_delete(root: Path, payload: dict[str, Any]) -> dict[str, Any]:
    """统一软删（可恢复）：source=RESTRICT、wiki=CASCADE+CDR、question=有历史降 disable。"""
    return ContentRegistry(root).delete(
        str(payload.get("object_type", "")),
        vault_id=payload.get("vault_id", "public"),
        object_id=str(payload.get("object_id", "")),
    )


def _handle_purge(root: Path, payload: dict[str, Any]) -> dict[str, Any]:
    """统一硬删（永久）：必须先 delete 且过宽限期，再物理回收（source/wiki）。"""
    return ContentRegistry(root).purge(
        str(payload.get("object_type", "")),
        vault_id=payload.get("vault_id", "public"),
        object_id=str(payload.get("object_id", "")),
    )


def _handle_source_update(root: Path, payload: dict[str, Any]) -> dict[str, Any]:
    """source 重导入更新（幂等 + 保留 evidence_items）经注册表路由。"""
    request = _require_mapping(payload, "request", "source_request_required")
    return ContentRegistry(root).update("source", request=request)


def _handle_question_review(root: Path, payload: dict[str, Any]) -> dict[str, Any]:
    return QuestionStore(root).review(
        str(payload.get("question_id", "")), payload.get("rating")
    )


# action → handler 是 action 的唯一事实来源；ALLOWED_ACTIONS 由它派生，
# ACTION_FIELDS 必须与它键一致（tests/test_skill_runtime.py 有对账断言）。
_HANDLERS: dict[str, Callable[[Path, dict[str, Any]], dict[str, Any]]] = {
    "skill_status": _handle_skill_status,
    "query": _handle_query,
    "retrieve": _handle_query,
    "ask": _handle_ask,
    "read": _handle_read,
    "backlinks": _handle_backlinks,
    "write": _handle_write,
    "source_ingest": _handle_source_ingest,
    "wiki_validate": _handle_wiki_validate,
    "publish_preview": _handle_publish_preview,
    "publish_confirm": _handle_publish_confirm,
    "vault_check": _handle_vault_check,
    "backup_status": _handle_backup_status,
    "backup_manifest": _handle_backup_manifest,
    "question_create": _handle_question_create,
    "question_list": _handle_question_list,
    "question_session": _handle_question_session,
    "question_errors": _handle_question_errors,
    "question_queue": _handle_question_queue,
    "question_disable": _handle_question_disable,
    "question_enable": _handle_question_enable,
    "question_delete": _handle_question_delete,
    "question_answer": _handle_question_answer,
    "question_review": _handle_question_review,
    "list": _handle_list,
    "delete": _handle_delete,
    "purge": _handle_purge,
    "source_update": _handle_source_update,
}
ALLOWED_ACTIONS = frozenset(_HANDLERS)


def dispatch(
    action: str, payload: dict[str, Any] | None = None, *, root: Path
) -> dict[str, Any]:
    payload = payload or {}
    handler = _HANDLERS.get(action)
    if handler is None:
        return contract.blocked(
            "skill-dispatch/v1", "skill_action_not_allowed", action=action
        )
    if not isinstance(payload, dict) or any(key in FORBIDDEN_KEYS for key in payload):
        return contract.blocked("skill-dispatch/v1", "skill_payload_forbidden")
    unknown = sorted(set(payload) - ACTION_FIELDS[action])
    if unknown:
        return contract.blocked(
            "skill-dispatch/v1", "skill_payload_unknown_field", fields=unknown
        )
    try:
        return handler(Path(root).resolve(), payload)
    except (OSError, ValueError, TypeError) as exc:
        # handler 以 ``raise ValueError("<error_code>")`` 表达字段级失败；已登记的码
        # 直接作为 blocked 的 error_code，未登记（含 OSError 文本）归一到伞码
        # ``skill_action_failed`` 并把原始文本留在 reason（fail-closed，不漂移词表）。
        code = str(exc)
        if code in contract.ERROR_CODES:
            return contract.blocked("skill-dispatch/v1", code)
        return contract.blocked("skill-dispatch/v1", "skill_action_failed", reason=code)
