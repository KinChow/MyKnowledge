"""config/*.yaml 的每个顶层段都必须有代码读取方（ADR-0019 反模式门禁）。

背景：本仓库反复出现同一个反模式——把"设计说明"塞进运行时配置，然后无人读。
已清理四批：vocab.yaml（整份 294 行零读者）、schemas.yaml 的 21 个对象契约副本、
policy.yaml 的 6 个顶层段、两阶段写入的 operation 声明。共性是"声明存在、代码
不读、且会悄悄漂移"（如 retrieval.default=qmd 而 QMD 早已退役）。

本测试把该反模式从"逐次人工 grep"升级为 CI 门禁：任何新增的 config 顶层段若
没有读取方，提交即红。这是 Knip 式可达性检测在"配置键"这一格的手写落地——
现成死代码工具（Knip/depcheck）只覆盖 JS/TS 代码与依赖，读不懂本仓库
`policy_value(root, "a", "b")` 这种字符串路径访问器。

**覆盖边界（有意划清，不假装更宽）**：
- 只判**顶层段**级"整段死"，不判段内死子键。段内子键的可达性需要键路径级的
  AST 比对（复杂度高一个量级），当前只有 `validation` 段一个已知实例，留待
  真出现第二例再上。
- 检测口径是 AST（取调用的字符串实参），不是 grep——grep 会因词形碰撞误判
  （source/archive 等），这正是本仓库栽过多次的坑。
"""

from __future__ import annotations

import ast
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
# 扫这些目录里对 config 的**值访问**：函数名 → 该调用读的是哪个 config 文件。
# 假阳性面：只认这两个访问器 + path_contract RULES。若将来有人换第四种方式读
# config（如 `load_policy(root)["x"]` 直接下标），其读的段会被漏进"死段"误判——
# 新增读取入口时必须同步 _VALUE_READERS，否则活段会被当死段报红。
_VALUE_READERS = {"policy_value": "policy", "schemas_value": "schemas"}
_SCAN_DIRS = ("tools", "backend", "tests", "scripts")
# 顶层段没有读取方但保留是合法的（列出理由）。当前为空——四批清理后无豁免。
_ALLOWLIST: dict[str, set[str]] = {"policy": set(), "schemas": set()}


def _value_reader_keys() -> dict[str, set[str]]:
    """AST 扫描：每个 `policy_value`/`schemas_value` 调用的首个字符串实参即顶层键。"""
    consumed: dict[str, set[str]] = {"policy": set(), "schemas": set()}
    for name in _SCAN_DIRS:
        for path in (ROOT / name).rglob("*.py"):
            try:
                tree = ast.parse(path.read_text(encoding="utf-8"))
            except (OSError, SyntaxError):  # noqa: PERF203 - 单文件损坏不该拖垮全扫描
                continue
            for node in ast.walk(tree):
                if not (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)):
                    continue
                source = _VALUE_READERS.get(node.func.id)
                if source is None or len(node.args) < 2:
                    continue
                first_key = node.args[1]
                if isinstance(first_key, ast.Constant) and isinstance(
                    first_key.value, str
                ):
                    consumed[source].add(first_key.value)
    return consumed


def _path_contract_keys() -> dict[str, set[str]]:
    """path_contract 的 RULES/MEMBER_RULES 也是读取方：(source, (top_key, ...))。"""
    from tools.path_contract import MEMBER_RULES, RULES

    consumed: dict[str, set[str]] = {"policy": set(), "schemas": set()}
    for source, keys, _ in list(RULES) + list(MEMBER_RULES):
        if source in consumed and keys:
            consumed[source].add(keys[0])
    return consumed


def _top_level_keys(config_name: str) -> set[str]:
    data = yaml.safe_load((ROOT / "config" / f"{config_name}.yaml").read_text("utf-8"))
    # schema_version / policy_version 是元数据，不是被消费的业务段。
    return {k for k in data if k not in ("schema_version", "policy_version")}


class ConfigNoDeadSectionsTests(unittest.TestCase):
    def test_every_top_level_section_has_a_reader(self):
        value_keys = _value_reader_keys()
        rule_keys = _path_contract_keys()
        for config_name in ("policy", "schemas"):
            consumed = value_keys[config_name] | rule_keys[config_name]
            declared = _top_level_keys(config_name)
            dead = declared - consumed - _ALLOWLIST[config_name]
            self.assertEqual(
                dead,
                set(),
                f"{config_name}.yaml 顶层段无读取方（ADR-0019 反模式）：{sorted(dead)}。"
                f"要么删除该段，要么让代码经 *_value / path_contract RULES 读它；"
                f"确有理由保留则加进本测试的 _ALLOWLIST 并注明原因。",
            )

    def test_detector_actually_finds_readers(self):
        """自证：检测器不是恒真——它必须真的抓到已知读取方。

        若某次改动让 AST 扫描静默失效（如函数改名后忘了同步），本断言先红，
        避免门禁变成"永远通过"的摆设。
        """
        value_keys = _value_reader_keys()
        self.assertIn("layers", value_keys["policy"])
        self.assertIn("public_projection", value_keys["schemas"])
        self.assertIn("field_contracts", _path_contract_keys()["schemas"])


if __name__ == "__main__":
    unittest.main()
