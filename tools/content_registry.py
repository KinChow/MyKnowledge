"""统领入口：按 ``object_type`` 路由到实体的读/列举能力（ADR-0017 P1）。

设计约束（KISS）：**只路由，不含领域逻辑**。此前每个入口（backend 端点、
skill dispatch、CLI）各自写一遍 ``if object_type == "wiki": ... else 404``，
同一句"某类型内容怎么读/怎么列举"散落多处、语义容易漂移。这里把"object_type →
能力"收敛成一张表：backend / skill 通道经 :class:`ContentRegistry` 取得能力，
具体的读/列举实现仍住在各自的领域模块里（本模块不复制任何一行领域逻辑，只做
查表分发 + 统一信封）。

未登记的 ``object_type`` 一律 fail-closed 为 ``blocked`` + ``object_type_not_found``
（词表已在 ``contract._LOCATE_CODES`` 登记），杜绝"未知类型被静默当成 wiki"。
"""

from __future__ import annotations

from collections.abc import Callable, Iterable, Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .contract import blocked
from .projection import PublicProjectionStore

READ_SCHEMA = "content-read/v1"
LIST_SCHEMA = "content-list/v1"

# 能力函数签名：``(root, **kwargs) -> 统一信封 dict``。领域实现自带 status，
# 本模块只在"路由未命中"时构造 blocked，不改写命中路径的返回。
CapabilityFn = Callable[..., dict[str, Any]]


@dataclass(frozen=True)
class ContentCapability:
    """一个 object_type 的读/列举能力。read/list 直接委托给领域实现。"""

    object_type: str
    read: CapabilityFn
    list: CapabilityFn


def _wiki_read(root: Path, *, object_id: str, **_ignored: Any) -> dict[str, Any]:
    """public wiki 读：从 projection 取正文（与 skill 只读通道同一数据源）。"""
    from .contract import ok

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


def _wiki_list(root: Path, **_ignored: Any) -> dict[str, Any]:
    """public wiki 列举：只回 object_ref，不含正文（列举≠读取）。"""
    from .contract import ok

    items = PublicProjectionStore(root).public_items(with_body=False)
    return ok(
        LIST_SCHEMA,
        object_type="wiki",
        items=[
            {"vault_id": "public", "object_type": "wiki", "object_id": item["id"]}
            for item in items
        ],
    )


def _default_capabilities() -> tuple[ContentCapability, ...]:
    return (ContentCapability("wiki", read=_wiki_read, list=_wiki_list),)


class ContentRegistry:
    """object_type → 能力 的唯一路由表。"""

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

    def read(self, object_type: str, **kwargs: Any) -> dict[str, Any]:
        cap = self._by_type.get(object_type)
        if cap is None:
            return blocked(
                READ_SCHEMA, "object_type_not_found", object_type=object_type
            )
        return cap.read(self.root, **kwargs)

    def list(self, object_type: str, **kwargs: Any) -> dict[str, Any]:
        cap = self._by_type.get(object_type)
        if cap is None:
            return blocked(
                LIST_SCHEMA, "object_type_not_found", object_type=object_type
            )
        return cap.list(self.root, **kwargs)
