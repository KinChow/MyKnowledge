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
from typing import Any, Protocol, runtime_checkable

from . import contract
from .common import safe_id
from .contract import require_error_code
from .front_matter import FrontMatter
from .paths import RepoPaths


# 能力 Protocol（对标 K8s apiserver ``registry/rest`` 的 Getter/Lister/Creater/
# Updater/GracefulDeleter 小接口）：结构化 + ``@runtime_checkable``，由 ContentRegistry
# 用 ``isinstance`` 探测某实体支持哪些动词（PEP 544），据此决定暴露面——不给不支持的
# 动词写硬编码分支。``runtime_checkable`` 只校验方法名存在，签名差异由适配层归一。
@runtime_checkable
class Readable(Protocol):
    def read(self, *args: Any, **kwargs: Any) -> dict: ...


@runtime_checkable
class Listable(Protocol):
    def list(self, *args: Any, **kwargs: Any) -> dict: ...  # noqa: A003


@runtime_checkable
class Creatable(Protocol):
    def create(self, *args: Any, **kwargs: Any) -> dict: ...


@runtime_checkable
class Updatable(Protocol):
    def update(self, *args: Any, **kwargs: Any) -> dict: ...


@runtime_checkable
class Deletable(Protocol):
    def delete(self, *args: Any, **kwargs: Any) -> dict: ...


@runtime_checkable
class Purgeable(Protocol):
    def purge(self, *args: Any, **kwargs: Any) -> dict: ...


# 两阶段硬删（purge）的宽限期：软删（delete）后需过 N 天才允许物理回收。
# 默认 14 天，对齐 git gc 的 prune 宽限期（``gc.pruneExpire="2 weeks ago"``）。
DEFAULT_PURGE_GRACE_DAYS = 14


def purge_grace_days(root: Path) -> int:
    from .policy import policy_value

    value = policy_value(
        root, "delete", "purge_grace_days", default=DEFAULT_PURGE_GRACE_DAYS
    )
    try:
        return int(value)
    except (TypeError, ValueError):
        return DEFAULT_PURGE_GRACE_DAYS


def purge_precondition(
    paths: RepoPaths,
    object_type: str,
    object_id: str,
    root: Path,
    *,
    grace_days: int | None = None,
) -> str | None:
    """两阶段硬删前置门禁（Azure soft-delete→purge / IMAP \\Deleted→EXPUNGE 语义）。

    返回 ``None``=可 purge；``"already"``=已 purge（幂等 noop）；否则为 error_code：
    ``not_deleted``（未先软删）/ ``retention_not_elapsed``（未过宽限期或删除时间不可判定）。
    """
    import time

    from . import retire_ledger

    if retire_ledger.is_purged(paths, object_type, object_id):
        return "already"
    if not retire_ledger.is_retired(paths, object_type, object_id):
        return "not_deleted"
    at = retire_ledger.deleted_at(paths, object_type, object_id)
    grace = purge_grace_days(root) if grace_days is None else grace_days
    if at is None or (time.time() - at) < grace * 86400:
        return "retention_not_elapsed"
    return None


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


def resolve_owner_root(root: Path, vault_id: str) -> Path:
    """把 vault_id 解析为 owner 检出根（复用 VaultRegistry，只读）。

    失败归一为 :class:`ObjectResolutionError`（与定位同一异常类型，调用方一处
    catch）：``vault_unavailable``（可重试）保留原码，其余（vault 不存在/路径非法）
    归为 ``invalid_object_ref``（引用本身不合法）。延迟导入 VaultRegistry 避免环。
    """
    from .vault_registry import VaultRegistry

    try:
        return VaultRegistry(Path(root).resolve()).resolve_vault_path(vault_id)
    except (OSError, ValueError) as exc:
        code = (
            "vault_unavailable"
            if str(exc) == "vault_unavailable"
            else "invalid_object_ref"
        )
        raise ObjectResolutionError(code) from exc


class ManagedObjectRepository:
    """source/wiki 共享的读/列举/owner 解析/错误映射（各 repo 只加各自的 CRUD）。

    高内聚：managed 对象“怎么定位/读/列举/把定位错误映射成统一信封”只此一份；
    低耦合：``SourceRepository``/``WikiRepository`` 经继承复用，退休墓碑走
    ``retire_ledger``，互不借对方私有 API。
    """

    object_type: str
    read_schema: str
    list_schema: str

    def __init__(self, root: Path) -> None:
        self.root = Path(root)

    def _owner(self, vault_id: str) -> Path:
        return resolve_owner_root(self.root, vault_id)

    @staticmethod
    def _error(schema: str, exc: ObjectResolutionError) -> dict[str, Any]:
        # vault_unavailable 是环境不可用（可重试）→ unavailable；其余是调用方错误 → blocked。
        status = "unavailable" if exc.code == "vault_unavailable" else "blocked"
        return contract.result(schema, status, error_code=exc.code)

    def _ref(self, vault_id: str, object_id: str) -> dict[str, str]:
        return {
            "vault_id": vault_id,
            "object_type": self.object_type,
            "object_id": object_id,
        }

    def read(self, vault_id: str, object_id: str) -> dict[str, Any]:
        try:
            path = locate_managed_object(
                self._owner(vault_id), self.object_type, object_id
            )
        except ObjectResolutionError as exc:
            return self._error(self.read_schema, exc)
        try:
            metadata, body = FrontMatter.parse(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, ValueError, TypeError) as exc:
            return contract.blocked(
                self.read_schema, "object_unreadable", reason=str(exc)
            )
        return contract.ok(
            self.read_schema,
            object_ref=self._ref(vault_id, object_id),
            metadata=metadata,
            body=body,
        )

    def list(self, vault_id: str = "public") -> dict[str, Any]:  # noqa: A003 - Repository 契约方法名
        try:
            owner = self._owner(vault_id)
        except ObjectResolutionError as exc:
            return self._error(self.list_schema, exc)
        base = dict(RepoPaths(owner).object_roots)[self.object_type]
        object_ids = (
            sorted(
                p.stem for p in base.rglob("*.md") if p.is_file() and not p.is_symlink()
            )
            if base.is_dir()
            else []
        )
        return contract.ok(
            self.list_schema,
            items=[{"object_ref": self._ref(vault_id, oid)} for oid in object_ids],
        )
