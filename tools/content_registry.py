"""统领入口：``object_type`` → **全动词**内容能力（ADR-0017 P1/P5）。

设计移植 Kubernetes apiserver ``registry/rest`` 的能力发现：每个实体（Repository /
Store）实现哪些动词由其**结构**决定；注册表用 ``@runtime_checkable`` 能力 Protocol +
``issubclass`` 探测（见 ``content_repository.Readable`` 等），据此建能力表——只对探测到
的动词开放入口，不给不支持的动词写硬编码分支（对应 apiserver 里的
``if _, ok := storage.(rest.Lister); ok {…}``）。

**只路由 + 统一信封，零领域逻辑**：读/列举/增/改/删的实现全部住在
``source_repository`` / ``wiki_repository`` / ``question``。三个物理入口（backend HTTP /
skill dispatch / CLI）都经本注册表取能力，消除"各入口各写一遍 if object_type"的漂移。

失败语义：未知 ``object_type`` → ``blocked/object_type_not_found``；已知类型但该实体不
支持此动词 → ``blocked/capability_not_supported``（对应 HTTP 405）。两码均在
``contract._LOCATE_CODES`` 登记。
"""

from __future__ import annotations

from collections.abc import Callable, Iterable, Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .content_repository import (
    Creatable,
    Deletable,
    Listable,
    Purgeable,
    Readable,
    Updatable,
)
from .contract import blocked, ok
from .projection import PublicProjectionStore

# 复用既有读/列举信封名（skill/backend 现有公共读契约一致）；增/改/删的路由级信封仅在
# "路由失败"（未知类型/动词不支持）时出现，成功路径透传领域信封（source-create/v1 等）。
READ_SCHEMA = "read-result/v1"
LIST_SCHEMA = "object-list/v1"
CREATE_SCHEMA = "content-create/v1"
UPDATE_SCHEMA = "content-update/v1"
DELETE_SCHEMA = "content-delete/v1"
PURGE_SCHEMA = "content-purge/v1"

# 能力函数签名：``(root, **kwargs) -> 统一信封 dict``。领域实现自带 status，
# 本模块只在"路由未命中/动词不支持"时构造 blocked，不改写命中路径的返回。
CapabilityFn = Callable[..., dict[str, Any]]

# verb → (探测用 Protocol, 路由失败信封 schema)。这是"全动词"的唯一事实源。
_VERBS: dict[str, tuple[type, str]] = {
    "read": (Readable, READ_SCHEMA),
    "list": (Listable, LIST_SCHEMA),
    "create": (Creatable, CREATE_SCHEMA),
    "update": (Updatable, UPDATE_SCHEMA),
    "delete": (Deletable, DELETE_SCHEMA),
    "purge": (Purgeable, PURGE_SCHEMA),
}


@dataclass(frozen=True)
class ContentCapability:
    """一个 object_type 的动词能力集：每个动词委托给领域实现，未提供即 ``None``。"""

    object_type: str
    read: CapabilityFn | None = None
    list: CapabilityFn | None = None  # noqa: A003 - Repository 契约动词名
    create: CapabilityFn | None = None
    update: CapabilityFn | None = None
    delete: CapabilityFn | None = None
    purge: CapabilityFn | None = None

    def verb(self, name: str) -> CapabilityFn | None:
        return getattr(self, name)


# ---- source 适配器（委托 SourceRepository；延迟导入避免环、贴合既有惰性风格） ----
def _source_read(root: Path, *, vault_id: str = "public", object_id: str, **_: Any):
    from .source_repository import SourceRepository

    return SourceRepository(root).read(vault_id, object_id)


def _source_list(root: Path, *, vault_id: str = "public", **_: Any):
    from .source_repository import SourceRepository

    return SourceRepository(root).list(vault_id)


def _source_create(root: Path, *, request: dict | None = None, **kw: Any):
    from .source_repository import SourceRepository

    return SourceRepository(root).create(request if request is not None else kw)


def _source_update(root: Path, *, request: dict | None = None, **kw: Any):
    from .source_repository import SourceRepository

    return SourceRepository(root).update(request if request is not None else kw)


def _source_delete(root: Path, *, vault_id: str = "public", object_id: str, **_: Any):
    from .source_repository import SourceRepository

    return SourceRepository(root).delete(vault_id, object_id)


def _source_purge(root: Path, *, vault_id: str = "public", object_id: str, **_: Any):
    from .source_repository import SourceRepository

    return SourceRepository(root).purge(vault_id, object_id)


# ---- wiki 适配器：读/列举 scope 感知（public→projection，免 token；private→repo） ----
def _wiki_read(
    root: Path,
    *,
    vault_id: str = "public",
    object_id: str,
    **_: Any,
) -> dict[str, Any]:
    if vault_id == "public":
        items = PublicProjectionStore(root).public_items(with_body=True)
        item = next((x for x in items if x["object_id"] == object_id), None)
        if item is None:
            return blocked(READ_SCHEMA, "object_not_found", object_id=object_id)
        return ok(
            READ_SCHEMA,
            object_ref={
                "vault_id": "public",
                "object_type": "wiki",
                "object_id": object_id,
            },
            path=item["body_path"],
            body=item["body"],
        )
    from .wiki_repository import WikiRepository

    return WikiRepository(root).read(vault_id, object_id)


def _wiki_list(root: Path, *, vault_id: str = "public", **_: Any) -> dict[str, Any]:
    if vault_id == "public":
        items = PublicProjectionStore(root).public_items(with_body=False)
        return ok(
            LIST_SCHEMA,
            object_type="wiki",
            items=[
                {"vault_id": "public", "object_type": "wiki", "object_id": item["id"]}
                for item in items
            ],
        )
    from .wiki_repository import WikiRepository

    return WikiRepository(root).list(vault_id)


def _wiki_delete(root: Path, *, vault_id: str = "public", object_id: str, **_: Any):
    from .wiki_repository import WikiRepository

    return WikiRepository(root).delete(vault_id, object_id)


def _wiki_purge(root: Path, *, vault_id: str = "public", object_id: str, **_: Any):
    from .wiki_repository import WikiRepository

    return WikiRepository(root).purge(vault_id, object_id)


# ---- question 适配器：单一本地 practice 根（ObjectRef 约定 vault_id="local"） ----
def _question_read(root: Path, *, object_id: str, **_: Any):
    from .question import QuestionStore

    return QuestionStore(root).read(object_id)


def _question_list(
    root: Path,
    *,
    domain: str | None = None,
    topic: str | None = None,
    skill: str | None = None,
    status: str = "enabled",
    **_: Any,
):
    from .question import QuestionStore

    return QuestionStore(root).list(
        domain=domain, topic=topic, skill=skill, status=status
    )


def _question_create(
    root: Path,
    *,
    spec: dict,
    wiki_path: Any = None,
    wiki_report: dict | None = None,
    **_: Any,
):
    from .question import QuestionStore

    return QuestionStore(root).create(
        spec, wiki_path=wiki_path, wiki_report=wiki_report
    )


def _question_delete(root: Path, *, object_id: str, **_: Any):
    from .question import QuestionStore

    return QuestionStore(root).delete(object_id)


def _probe(object_type: str, repo_cls: type, adapters: dict[str, CapabilityFn]):
    """K8s 式能力发现：只保留 (提供了适配器) 且 (结构上实现该动词) 的动词。"""
    kept = {
        verb: fn
        for verb, (proto, _schema) in _VERBS.items()
        if (fn := adapters.get(verb)) is not None and issubclass(repo_cls, proto)
    }
    return ContentCapability(object_type, **kept)


def _default_capabilities() -> tuple[ContentCapability, ...]:
    """探测式构建三类实体的能力表（source/wiki/question）。

    只做 ``issubclass`` 探测（Protocol 仅方法、非数据，探测合法），不实例化领域对象。
    """
    from .question import QuestionStore
    from .source_repository import SourceRepository
    from .wiki_repository import WikiRepository

    return (
        _probe(
            "source",
            SourceRepository,
            {
                "read": _source_read,
                "list": _source_list,
                "create": _source_create,
                "update": _source_update,
                "delete": _source_delete,
                "purge": _source_purge,
            },
        ),
        _probe(
            "wiki",
            WikiRepository,
            {
                "read": _wiki_read,
                "list": _wiki_list,
                "delete": _wiki_delete,
                "purge": _wiki_purge,
            },
        ),
        _probe(
            "question",
            QuestionStore,
            {
                "read": _question_read,
                "list": _question_list,
                "create": _question_create,
                "delete": _question_delete,
            },
        ),
    )


class ContentRegistry:
    """object_type → 全动词能力 的唯一路由表。"""

    def __init__(
        self,
        root: Path,
        capabilities: Iterable[ContentCapability] | None = None,
    ) -> None:
        self.root = Path(root)
        caps = _default_capabilities() if capabilities is None else tuple(capabilities)
        self._by_type: Mapping[str, ContentCapability] = {
            cap.object_type: cap for cap in caps
        }

    def object_types(self) -> frozenset[str]:
        return frozenset(self._by_type)

    def capability(self, object_type: str) -> ContentCapability | None:
        return self._by_type.get(object_type)

    def verbs(self, object_type: str) -> frozenset[str]:
        """某 object_type 实际暴露的动词集合（探测结果，供入口/测试对账）。"""
        cap = self._by_type.get(object_type)
        if cap is None:
            return frozenset()
        return frozenset(v for v in _VERBS if cap.verb(v) is not None)

    def _route(
        self, verb: str, object_type: str, kwargs: dict[str, Any]
    ) -> dict[str, Any]:
        _proto, schema = _VERBS[verb]
        cap = self._by_type.get(object_type)
        if cap is None:
            return blocked(schema, "object_type_not_found", object_type=object_type)
        fn = cap.verb(verb)
        if fn is None:
            return blocked(
                schema,
                "capability_not_supported",
                object_type=object_type,
                verb=verb,
            )
        return fn(self.root, **kwargs)

    def read(self, object_type: str, **kwargs: Any) -> dict[str, Any]:
        return self._route("read", object_type, kwargs)

    def list(self, object_type: str, **kwargs: Any) -> dict[str, Any]:  # noqa: A003
        return self._route("list", object_type, kwargs)

    def create(self, object_type: str, **kwargs: Any) -> dict[str, Any]:
        return self._route("create", object_type, kwargs)

    def update(self, object_type: str, **kwargs: Any) -> dict[str, Any]:
        return self._route("update", object_type, kwargs)

    def delete(self, object_type: str, **kwargs: Any) -> dict[str, Any]:
        return self._route("delete", object_type, kwargs)

    def purge(self, object_type: str, **kwargs: Any) -> dict[str, Any]:
        return self._route("purge", object_type, kwargs)
