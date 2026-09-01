"""`config/schemas.yaml` 的唯一加载入口（fail-closed，与 `tools/policy.py` 同形）。

实测动机（2026-09-01）：全库**没有任何代码读取过 `config/schemas.yaml`**。这份 822 行的
契约声明（`required_item_fields`、`release_input_fields`、`required_match_fields`、
`excluded_from_content_hash` …）因此只是文档，不是门禁——声明与实现之间没有任何机制
保证一致。本模块把它变成可消费的事实源，让"声明了就必须被执行"。

语义与 policy 加载一致：文件缺失返回空（调用方持默认值），文件损坏抛
``ValueError("schemas_invalid")``，不静默降级。
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .common import config_value, load_config_yaml
from .paths import RepoPaths

SCHEMAS_FILENAME = "schemas.yaml"


def schemas_path(root: Path) -> Path:
    return RepoPaths(root).config_dir / SCHEMAS_FILENAME


def load_schemas(root: Path) -> dict[str, Any]:
    """读取整份 schemas 契约；文件缺失返回 {}，损坏抛 ValueError("schemas_invalid")。"""
    return load_config_yaml(schemas_path(root), "schemas_invalid")


def schemas_value(root: Path, *keys: str, default: Any = None) -> Any:
    """按键路径取值；中途遇到非映射节点视为未声明（返回 default）。"""
    return config_value(load_schemas(root), *keys, default=default)
