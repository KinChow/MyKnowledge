"""结构守卫：把 review 结论机器化，防止布局硬编码/已删除 API 回潮。

覆盖（来自 F001 二次 review 的 reuse 维度结论）：
- 布局路径必须收敛到 RepoPaths（paths.py），业务代码不得 self.root 直拼
- sha256_hex 已删除（并入 strip_sha256_prefix/hash_canonical）
- extractor 的 stdlib-html fallback 已删除（trafilatura 是唯一 HTML 实现）
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent.parent / "tools"


class LayoutGuardTests(unittest.TestCase):
    """机器强制：路径收口 RepoPaths、sha256_hex/fallback 零残留。"""

    def _tool_sources(self) -> list[tuple[str, str]]:
        # 递归 glob：tools/validation/ 包（F002 拆分后）同样受守卫约束
        return [
            (str(path.relative_to(TOOLS_DIR)), path.read_text(encoding="utf-8"))
            for path in sorted(TOOLS_DIR.glob("**/*.py"))
            if path.name not in {"__init__.py", "paths.py"}
        ]

    def test_no_hardcoded_root_paths_outside_paths(self):
        """paths.py 之外不得出现 ``self.root / "xxx"`` 布局硬编码。"""
        violations = []
        for name, text in self._tool_sources():
            for line_no, line in enumerate(text.splitlines(), 1):
                if re.search(r'self\.root\s*/\s*"', line):
                    violations.append(f"{name}:{line_no}: {line.strip()}")
        self.assertEqual(violations, [])

    def test_no_sha256_hex_residue(self):
        """sha256_hex 已删除（合并入 hash_canonical/strip 组合），不得回潮。"""
        for name, text in self._tool_sources():
            self.assertNotIn("sha256_hex", text, name)

    def test_no_html_fallback_residue(self):
        """extractor 的 stdlib-html fallback 已删除，不得回潮。"""
        for name, text in self._tool_sources():
            self.assertNotIn("stdlib-html", text, name)
            self.assertNotIn("_fallback_html", text, name)


if __name__ == "__main__":
    unittest.main()
