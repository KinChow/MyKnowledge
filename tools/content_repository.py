"""managed 内容对象（`source`/`wiki`）的共享定位（实现 ADR-0017 的 R 能力起点）。

设计见 `docs/technical-design/content-crud-repository.md`。本模块只放**当前有
消费者**的那一份共享逻辑——按 object_ref 在 owner vault 内定位对象文件；读取、
列举、删除、更新等能力按 ADR-0017 的分阶段计划在 P2/P3 与其首个真实调用点一起
落地（避免提前引入无消费者的抽象，cosmicpython《Repository》与 Zen“practicality
beats purity”）。

P1 收敛目标：`backend.services.resolve_object_path` 与 `validation.resolution.
resolve_source` 两处重复的“按 id 定位”统一到 `locate_managed_object`；各调用点在
边界把结构化 `ObjectResolutionError.code` 适配回其既有契约错误码（外部契约不变）。

managed 类型与其物理根的**唯一枚举口径**是 `RepoPaths.object_roots`（见 paths.py
的“枚举口径必须集中”注释），本模块不再另存一份类型集合。
"""

from __future__ import annotations

from pathlib import Path

from .common import safe_id
from .contract import require_error_code
from .paths import RepoPaths


class ObjectResolutionError(ValueError):
    """结构化定位失败。

    ``code ∈ {invalid_object_ref, object_type_not_found, object_not_found,
    object_id_ambiguous}``。不映射到任何具体契约错误码——由各调用点在边界适配
    （后端映射到 HTTP 码、``resolution`` 映射到 wiki 校验码），保证同一定位逻辑
    服务于互不相同的既有契约。
    """

    def __init__(self, code: str, *, matches: list[Path] | None = None) -> None:
        # 定位失败码纳入 contract 单一词表治理（TD §14.3）：未登记即 fail-closed。
        super().__init__(require_error_code(code))
        self.code = code
        self.matches = matches or []


def locate_managed_object(owner_root: Path, object_type: str, object_id: str) -> Path:
    """在 owner vault 内按 id 唯一定位 managed 对象文件（单份实现）。

    只做“定位”：不解析 vault（调用方先给 owner_root），不读取正文。语义与原
    ``backend.services.resolve_object_path`` 逐字对齐：``safe_id`` 拒非法 id、非
    managed 类型拒绝、``rglob(f"{id}.md")`` 只收普通文件且拒符号链接、零命中与多命中
    分别结构化报错。类型→物理根经 ``RepoPaths.object_roots`` 派生（单一枚举口径）。
    """
    try:
        safe_id(object_id)
    except ValueError as exc:
        raise ObjectResolutionError("invalid_object_ref") from exc
    base = dict(RepoPaths(owner_root).object_roots).get(object_type)
    if base is None:
        raise ObjectResolutionError("object_type_not_found")
    matches = [
        p for p in base.rglob(f"{object_id}.md") if p.is_file() and not p.is_symlink()
    ]
    if not matches:
        raise ObjectResolutionError("object_not_found")
    if len(matches) > 1:
        raise ObjectResolutionError("object_id_ambiguous", matches=matches)
    return matches[0]
