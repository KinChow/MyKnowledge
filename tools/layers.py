"""unmanaged 层（`content/working|journal|decisions`）的契约与枚举（LAY-003/CHN-001）。

这三层没有 object 身份、没有 schema、没有出口，因此**不存在领域服务**去承载它们
唯一的那条约束（§5.9/技术设计"失败流程"：`content/working/` 缺 `source_ref` 拒绝
写入）。本模块是该约束与枚举口径的单一实现，被三处消费：

- `tools/write_operation.py` 的 preview（唯一写入收口，返回 `schema_invalid`）；
- `tools/doctor.py` 的 TTL / `review_by` 到期报告（report-only）；
- unmanaged 层文本检索命令。

阈值默认值写在代码里：`config/policy.yaml` 缺失不得等于"约束消失"（fail-closed）。
"""

from __future__ import annotations

from pathlib import Path

from .front_matter import FrontMatter
from .paths import RepoPaths
from .policy import policy_value

# working 层的最小回指字段：任一存在即可（`legacy_path` 是存量 docs/ 迁移入口）
WORKING_REFERENCE_FIELDS = ("source_ref", "legacy_path")
# policy 缺失时的兜底阈值（技术设计 §数据模型 layers.working.ttl_days）
DEFAULT_WORKING_TTL_DAYS = 30
# 显式关闭滞留报告的取值。用哨兵字符串而不是 null：`policy_value` 把 null 当
# "未配置"回落默认值，那样"关闭"和"漏配"就无法区分（owner 2026-09-01 设为无限）
WORKING_TTL_UNLIMITED = "unlimited"
DEFAULT_REVIEW_FIELD = "review_by"


def working_ttl_days(root: Path) -> int | None:
    """working 层滞留阈值；`unlimited` 返回 None 表示显式关闭该报告。"""
    value = policy_value(
        root, "layers", "working", "ttl_days", default=DEFAULT_WORKING_TTL_DAYS
    )
    if isinstance(value, str) and value.strip().lower() == WORKING_TTL_UNLIMITED:
        return None
    return int(value) if isinstance(value, int | str) else DEFAULT_WORKING_TTL_DAYS


def review_field(root: Path) -> str:
    value = policy_value(root, "review", "field", default=DEFAULT_REVIEW_FIELD)
    return value if isinstance(value, str) and value else DEFAULT_REVIEW_FIELD


def require_source_ref(root: Path) -> bool:
    """working 层是否要求回指来源；policy 缺失时按 True（不允许"来源待补"）。"""
    return (
        policy_value(root, "layers", "working", "require_source_ref", default=True)
        is not False
    )


def _under(path: Path, base: Path) -> bool:
    return path == base or base in path.parents


def working_contract_error(root: Path, relative_path: str, content: str) -> str | None:
    """写入 `content/working/` 的最小契约校验；返回错误码或 None。

    只看回指字段，不看 schema：working 层的价值在于低摩擦，多一条规则就少一次
    使用。front matter 语法损坏同样阻断（沿用 `FrontMatter` 的错误码）。
    """
    paths = RepoPaths(root)
    target = (paths.root / relative_path).resolve()
    if not _under(target, paths.working_root) or target.suffix != ".md":
        return None
    if not require_source_ref(root):
        return None
    try:
        metadata, _ = FrontMatter.parse(content)
    except ValueError as exc:
        return str(exc)
    if any(metadata.get(field) for field in WORKING_REFERENCE_FIELDS):
        return None
    return "schema_invalid"


def iter_unmanaged_files(root: Path) -> list[Path]:
    """三层下的全部 Markdown（枚举口径经 `RepoPaths.unmanaged_roots`）。"""
    files: list[Path] = []
    for base in RepoPaths(root).unmanaged_roots:
        if base.is_dir():
            files.extend(sorted(p for p in base.rglob("*.md") if p.is_file()))
    return files
