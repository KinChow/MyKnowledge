"""``config/policy.yaml`` 的唯一加载入口（fail-closed）。

此前 ruleset.py / audit.py 各自 `yaml.safe_load` 一遍，且都用
`except Exception: return 默认值` 兜底——策略文件写坏时会静默按默认值继续，
等于让配置错误改变审计语义而不告警。本模块把读取收敛为一处并区分两种情况：

- 文件不存在：合法状态，返回空策略（策略是可选覆盖层，默认值在调用方）；
- 文件存在但读不动/不是 YAML 映射：``ValueError("policy_invalid")``，
  由调用方转成结构化阻断（不写"已审"痕迹）。
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .common import config_value, load_config_yaml
from .paths import RepoPaths

POLICY_FILENAME = "policy.yaml"


def policy_path(root: Path) -> Path:
    return RepoPaths(root).config_dir / POLICY_FILENAME


def load_policy(root: Path) -> dict[str, Any]:
    """读取整份策略；文件缺失返回 {}，损坏抛 ValueError("policy_invalid")。"""
    return load_config_yaml(policy_path(root), "policy_invalid")


def policy_value(root: Path, *keys: str, default: Any = None) -> Any:
    """按键路径取值；中途遇到非映射节点视为未配置（返回 default）。"""
    node = config_value(load_policy(root), *keys, default=None)
    return default if node is None else node
