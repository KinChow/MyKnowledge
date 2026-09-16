"""unmanaged 层（`content/working|journal|decisions`）的枚举与 TTL/复习报告口径。

这三层没有 object 身份、没有 schema、没有出口。**入口无约束**（A1-深，2026-09-15）：
working 层曾要求 `source_ref` 或 `legacy_path` 非空，但实测 20/20 文件均不满足、该约束
从未生效（ADR-0019），且把出处门放在"进暂存"而非"晋升"与该层"低摩擦"的目的相悖。
出处校验统一归晋升关口——`content/wiki/` 的确定性校验与 LLM 审计（通道 A）。本模块
因此只保留两件事：滞留/复习到期的报告口径，与 unmanaged 文件的枚举口径。被消费于：

- `tools/doctor.py` 的 TTL / `review_by` 到期报告（report-only，工具永不自动删除）；
- unmanaged 层文本检索命令。

阈值默认值写在代码里：`config/policy.yaml` 缺失不得改变报告口径（fail-closed）。
"""

from __future__ import annotations

from pathlib import Path

from .paths import RepoPaths
from .policy import policy_value

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


def iter_unmanaged_files(root: Path) -> list[Path]:
    """三层下的全部 Markdown（枚举口径经 `RepoPaths.unmanaged_roots`）。"""
    files: list[Path] = []
    for base in RepoPaths(root).unmanaged_roots:
        if base.is_dir():
            files.extend(sorted(p for p in base.rglob("*.md") if p.is_file()))
    return files
