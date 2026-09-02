"""tools/matrix_sync.py：追踪矩阵完成度机器派生的解析、派生、check/sync 契约。

对应「完成度列由机器派生、不人工维护」这条约束：引用悬空（矩阵承诺的文件
不存在）是硬错误而不是降档；完成度 = 状态列 × 引用存在性的纯函数，任何
人工改写都会在下次 check/sync 被纠正。

fixture 用 tmp_path 构造最小矩阵与假测试文件，不依赖真实仓库矩阵（避免
测试随内容演进而漂移）。
"""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from tools import matrix_sync as ms

MINIMAL_MATRIX = """\
| 规范 ID | Feature | ADR | 实现设计 | 验收 | 测试 | 状态 | 完成度 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SRC-001 | F001 | ADR-0001 | source-ingestion | AC-F001-001 | tests/ingest/test_source_ingestor.py | Implemented（部分） | 主体完成 |
| WIKI-001 | F002 | ADR-0001 | wiki-claim-validation | AC-F002-001 | test_wiki_schema.py + test_wiki_rules.py | Implemented | 完成 |
| LAY-004 | F013 | ADR-0014 | layers-and-channels | AC-F013-003 | 待实现 | Designed | 未开始 |
| WEB-001 | F007 | ADR-0009 | static-wiki-publishing | AC-F007-001 | frontend 工程骨架 | Implemented（部分） | 主体完成 |
"""


MINIMAL_FEATURE_LIST = """\
| ID | Feature | 分类 | 优先级 | 依赖 | 验收 |
| --- | --- | --- | --- | --- | --- |
| F001 | Source 导入 | 核心链路 | P0 | 规范 | link |
| F002 | Wiki 契约 | 核心链路 | P0 | F001 | link |
| F003 | 证据验证 | 核心链路 | P0 | F001, F002 | link |
| F004 | 写操作 | 核心链路 | P0 | F001-F003 | link |
| F005 | 索引检索 | 核心链路 | P1 | F001-F004 | link |
| F006 | FastAPI | 消费端 | P1 | F005 | link |
| F007 | 静态 Wiki | 消费端 | P1 | F005 | link |
| F008 | 练习 | 消费端 | P1 | F002, F003 | link |
| F009 | Agent Skill | 消费端 | P1 | F004-F006 | link |
| F010 | 迁移 | 消费端 | P1 | F001-F004 | link |
| F011 | Private Vaults | 横向基础 | P1 | F001-F004 | link |
| F012 | 备份 | 横向基础 | P1 | 核心模块 | link |
| F013 | 布局 | 演进/独立域 | P0 | F002, F004 | link |
| F014 | 音视频 | 演进/独立域 | P2 | F001, F013 | link |
"""


def _write_fake_tests(root: Path) -> None:
    """创建解析规则引用的假测试文件。"""
    for rel in (
        "tests/ingest/test_source_ingestor.py",
        "tests/validation/test_wiki_schema.py",
        "tests/validation/test_wiki_rules.py",
    ):
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("# fixture\n", encoding="utf-8")


def _write_doc_indexes(root: Path) -> None:
    """创建三个索引 README（含状态列表格）+ 各自目录内带状态行的文档。

    表格列数与 tools.matrix_sync._DOC_INDEXES 的 table 配置一致：
    adr 为 4 列（名称|状态|决策|链接），td/acceptance 为 3 列（名称|状态|链接）。
    """
    specs = {
        "adr": {
            "header": "| 名称 | 状态 | 决策 | 链接 |",
            "docs": [("0001-source-first.md", "Accepted")],
        },
        "technical-design": {
            "header": "| 名称 | 状态 | 链接 |",
            "docs": [("source-ingestion.md", "Implemented")],
        },
        "acceptance": {
            "header": "| 名称 | 状态 | 链接 |",
            "docs": [("F001-source-ingestion.md", "Implemented")],
        },
    }
    for dirname, spec in specs.items():
        d = root / "docs" / dirname
        d.mkdir(parents=True, exist_ok=True)
        for doc, status in spec["docs"]:
            (d / doc).write_text(f"# {doc}\n\n- 状态：{status}\n", encoding="utf-8")
        if dirname == "adr":
            rows = "\n".join(
                f"| {doc.removesuffix('.md')} | {status} | 决策说明 | [正文](./{doc}) |"
                for doc, status in spec["docs"]
            )
        else:
            rows = "\n".join(
                f"| {doc.removesuffix('.md')} | {status} | [正文](./{doc}) |"
                for doc, status in spec["docs"]
            )
        (d / "README.md").write_text(
            "## 索引\n\n" + spec["header"] + "\n| --- | --- | --- | --- |\n" + rows,
            encoding="utf-8",
        )


def _write_fixtures(root: Path) -> None:
    """创建矩阵 + feature-list + 三个索引的最小 fixture（check 综合门禁依赖）。"""
    (root / "docs").mkdir(parents=True, exist_ok=True)
    (root / "docs" / "traceability-matrix.md").write_text(
        MINIMAL_MATRIX, encoding="utf-8"
    )
    (root / "docs" / "feature-list.md").write_text(
        MINIMAL_FEATURE_LIST, encoding="utf-8"
    )
    _write_fake_tests(root)
    _write_doc_indexes(root)


class ParseAndResolveTests(unittest.TestCase):
    def test_parse_rows_extracts_eight_columns(self):
        rows, skipped = ms.parse_rows(MINIMAL_MATRIX)
        self.assertEqual(len(rows), 4)
        self.assertEqual(skipped, 0)
        self.assertEqual(rows[0]["id"], "SRC-001")
        self.assertEqual(rows[0]["completion"], "主体完成")
        self.assertEqual(rows[2]["status"], "Designed")
        self.assertEqual(rows[3]["test"], "frontend 工程骨架")

    def test_parse_rows_counts_skipped_bad_rows(self):
        """列数不符或 ID 非法的行计入 skipped（格式漂移信号），不静默吞掉。"""
        text = (
            "| 规范 ID | Feature | ADR | 实现设计 | 验收 | 测试 | 状态 | 完成度 |\n"
            "| --- | --- | --- | --- | --- | --- | --- | --- |\n"
            "| BAD-ROW | 只有两列 |\n"
            "| SRC-001 | F001 | ADR-0001 | source-ingestion | AC | tests/a.py | Implemented（部分） | 主体完成 |\n"
        )
        rows, skipped = ms.parse_rows(text)
        self.assertEqual(len(rows), 1)
        self.assertEqual(skipped, 1)

    def test_parse_rows_accepts_long_prefix_and_resets_at_section(self):
        """SKILL 5 字母前缀必须匹配；`## ` 章节标题退出矩阵状态（后面 2 列表不误计）。"""
        text = (
            "| 规范 ID | Feature | ADR | 实现设计 | 验收 | 测试 | 状态 | 完成度 |\n"
            "| --- | --- | --- | --- | --- | --- | --- | --- |\n"
            "| SKILL-001 | F009 | ADR-0006 | agent-skill | AC-F009-001 | tests/test_skill_runtime.py | Implemented（部分） | 主体完成 |\n"
            "## 验收场景完整覆盖\n"
            "| Feature | 全部验收场景 |\n"
            "| --- | --- |\n"
            "| F001 | AC-F001-001 |\n"
        )
        rows, skipped = ms.parse_rows(text)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["id"], "SKILL-001")
        self.assertEqual(skipped, 0)

    def test_parse_rows_ignores_non_spec_rows(self):
        text = "| 前缀 | 范围 |\n| --- | --- |\n" + MINIMAL_MATRIX
        rows, skipped = ms.parse_rows(text)
        self.assertEqual(len(rows), 4)
        self.assertEqual(skipped, 0)

    def test_extract_refs_splits_merged_and_dedups(self):
        cell = "tools/inventory_legacy.py + test_a.py/test_b.py + test_a.py"
        refs = ms.extract_refs(cell)
        self.assertEqual(refs, ["tools/inventory_legacy.py", "test_a.py", "test_b.py"])

    def test_resolve_full_path(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            _write_fake_tests(root)
            self.assertEqual(
                ms.resolve_ref("tests/ingest/test_source_ingestor.py", root),
                "tests/ingest/test_source_ingestor.py",
            )
            self.assertIsNone(ms.resolve_ref("tests/ingest/missing.py", root))

    def test_resolve_bare_filename_finds_unique_prefix(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            _write_fake_tests(root)
            self.assertEqual(
                ms.resolve_ref("test_wiki_schema.py", root),
                "tests/validation/test_wiki_schema.py",
            )


class DeriveCompletionTests(unittest.TestCase):
    def test_designed_maps_to_not_started(self):
        self.assertEqual(ms.derive_completion("Designed", []), ms.NOT_STARTED)

    def test_implemented_with_all_refs_maps_to_done(self):
        self.assertEqual(ms.derive_completion("Implemented", []), ms.DONE)

    def test_implemented_partial_with_all_refs_maps_to_mostly(self):
        self.assertEqual(ms.derive_completion("Implemented（部分）", []), ms.MOSTLY)

    def test_missing_refs_never_derives_to_partial(self):
        """引用缺失是悬空（由 check 报错），不是降档。"""
        self.assertIsNone(ms.derive_completion("Implemented（部分）", ["a.py"]))
        self.assertIsNone(ms.derive_completion("Implemented", ["a.py"]))

    def test_unknown_status_returns_none(self):
        self.assertIsNone(ms.derive_completion("Bogus", []))


class CheckTests(unittest.TestCase):
    def setUp(self) -> None:
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        _write_fixtures(self.root)

    def _matrix_checks(self, result: dict) -> dict:
        """从 check() 嵌套报告取矩阵子检查详情。"""
        return result.get("checks", {}).get("matrix", result)

    def test_consistent_matrix_is_ok(self):
        result = ms.check(self.root)
        self.assertEqual(result["state"], "ok")
        self.assertEqual(result["rows"], 4)
        self.assertIn("WEB-001", result.get("no_refs", []))

    def test_stale_completion_is_error(self):
        text = (self.root / "docs" / "traceability-matrix.md").read_text(
            encoding="utf-8"
        )
        # WIKI-001 状态是 Implemented 且引用全在 → 应为"完成"，手改成"主体完成"
        text = text.replace("| Implemented | 完成 |", "| Implemented | 主体完成 |")
        (self.root / "docs" / "traceability-matrix.md").write_text(
            text, encoding="utf-8"
        )
        result = ms.check(self.root)
        self.assertEqual(result["state"], "error")
        stale = self._matrix_checks(result)["stale"]
        self.assertEqual(stale[0]["id"], "WIKI-001")
        self.assertEqual(stale[0]["matrix"], "主体完成")
        self.assertEqual(stale[0]["derived"], "完成")

    def test_dangling_ref_is_hard_error_not_downgrade(self):
        text = (self.root / "docs" / "traceability-matrix.md").read_text(
            encoding="utf-8"
        )
        # 引用一个不存在的文件
        text = text.replace(
            "tests/ingest/test_source_ingestor.py",
            "tests/ingest/ghost.py",
        )
        (self.root / "docs" / "traceability-matrix.md").write_text(
            text, encoding="utf-8"
        )
        result = ms.check(self.root)
        self.assertEqual(result["state"], "error")
        matrix = self._matrix_checks(result)
        self.assertIn("dangling_refs", matrix)
        self.assertEqual(matrix["dangling_refs"][0]["id"], "SRC-001")

    def test_designed_with_resolved_refs_reports_drift_warning(self):
        text = (self.root / "docs" / "traceability-matrix.md").read_text(
            encoding="utf-8"
        )
        # LAY-004 改为引用存在的文件但保持 Designed → 状态滞后警示
        text = text.replace(
            "| 待实现 | Designed | 未开始 |",
            "| tests/ingest/test_source_ingestor.py | Designed | 未开始 |",
        )
        (self.root / "docs" / "traceability-matrix.md").write_text(
            text, encoding="utf-8"
        )
        result = ms.check(self.root)
        self.assertEqual(result["state"], "ok")
        drift = result.get("status_drift", [])
        self.assertTrue(any(d["id"] == "LAY-004" for d in drift))

    def test_designed_completion_hand_edit_is_stale(self):
        """Designed 行恒派生「未开始」，与引用无关：手改完成度必须被检出不静默跳过。"""
        text = (self.root / "docs" / "traceability-matrix.md").read_text(
            encoding="utf-8"
        )
        text = text.replace(
            "| 待实现 | Designed | 未开始 |",
            "| 待实现 | Designed | 完成 |",
        )
        (self.root / "docs" / "traceability-matrix.md").write_text(
            text, encoding="utf-8"
        )
        result = ms.check(self.root)
        self.assertEqual(result["state"], "error")
        stale = self._matrix_checks(result)["stale"]
        self.assertEqual(stale[0]["id"], "LAY-004")
        self.assertEqual(stale[0]["derived"], "未开始")

    def test_check_unreadable_encoding_is_structured_error(self):
        """非 UTF-8 矩阵 → matrix_unreadable 结构化错误，不抛 UnicodeDecodeError。"""
        (self.root / "docs" / "traceability-matrix.md").write_bytes(b"\xff\xfe\x00\x01")
        result = ms.check(self.root)
        self.assertEqual(result["state"], "error")
        self.assertIn("matrix_unreadable", self._matrix_checks(result)["reason"])

    def test_check_missing_matrix_is_structured_error(self):
        (self.root / "docs" / "traceability-matrix.md").unlink()
        result = ms.check(self.root)
        self.assertEqual(result["state"], "error")
        self.assertIn("matrix_unreadable", self._matrix_checks(result)["reason"])

    def test_check_unknown_status_is_reported_not_silent(self):
        """状态列拼写漂移（如半角括号）计入 unknown_status，不静默跳过。"""
        text = (self.root / "docs" / "traceability-matrix.md").read_text(
            encoding="utf-8"
        )
        text = text.replace(
            "| Implemented（部分） | 主体完成 |",
            "| Implemented (部分) | 主体完成 |",
            1,
        )
        (self.root / "docs" / "traceability-matrix.md").write_text(
            text, encoding="utf-8"
        )
        result = ms.check(self.root)
        self.assertEqual(result["state"], "ok")
        unknown = result.get("unknown_status", [])
        self.assertTrue(any(u["status"] == "Implemented (部分)" for u in unknown))


class SyncTests(unittest.TestCase):
    def setUp(self) -> None:
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        (self.root / "docs").mkdir(parents=True)
        self.matrix_path = self.root / "docs" / "traceability-matrix.md"
        self.matrix_path.write_text(MINIMAL_MATRIX, encoding="utf-8")
        _write_fake_tests(self.root)

    def test_sync_rewrites_stale_completion_and_reports_changed(self):
        text = self.matrix_path.read_text(encoding="utf-8")
        text = text.replace("| Implemented | 完成 |", "| Implemented | 主体完成 |")
        self.matrix_path.write_text(text, encoding="utf-8")

        result = ms.sync(self.root)
        self.assertEqual(result["state"], "ok")
        self.assertEqual(len(result["changed"]), 1)
        self.assertEqual(result["changed"][0]["id"], "WIKI-001")
        self.assertEqual(result["changed"][0]["completion"], "完成")

        after = self.matrix_path.read_text(encoding="utf-8")
        self.assertIn("| Implemented | 完成 |", after)
        self.assertNotIn("| Implemented | 主体完成 |", after)

    def test_sync_dry_run_does_not_write(self):
        text = self.matrix_path.read_text(encoding="utf-8")
        text = text.replace("| Implemented | 完成 |", "| Implemented | 主体完成 |")
        self.matrix_path.write_text(text, encoding="utf-8")

        result = ms.sync(self.root, dry_run=True)
        self.assertTrue(result["dry_run"])
        self.assertEqual(len(result["changed"]), 1)
        after = self.matrix_path.read_text(encoding="utf-8")
        self.assertIn("| Implemented | 主体完成 |", after)  # 未写盘

    def test_sync_skips_dangling_refs(self):
        text = self.matrix_path.read_text(encoding="utf-8")
        text = text.replace(
            "tests/ingest/test_source_ingestor.py",
            "tests/ingest/ghost.py",
        )
        self.matrix_path.write_text(text, encoding="utf-8")
        result = ms.sync(self.root)
        self.assertEqual(result["changed"], [])  # 悬空不掩盖，留给 check 报错

    def test_sync_missing_matrix_returns_structured_error(self):
        """矩阵缺失时 sync 返回结构化 error，不抛 FileNotFoundError 崩溃。"""
        self.matrix_path.unlink()
        result = ms.sync(self.root)
        self.assertEqual(result["state"], "error")
        self.assertIn("matrix_unreadable", result["reason"])

    def test_sync_designed_hand_edit_is_fixed(self):
        """Designed 行完成度被手改后 sync 应纠正为「未开始」。"""
        text = self.matrix_path.read_text(encoding="utf-8")
        text = text.replace(
            "| 待实现 | Designed | 未开始 |",
            "| 待实现 | Designed | 完成 |",
        )
        self.matrix_path.write_text(text, encoding="utf-8")
        result = ms.sync(self.root)
        self.assertEqual(len(result["changed"]), 1)
        self.assertEqual(result["changed"][0]["id"], "LAY-004")
        after = self.matrix_path.read_text(encoding="utf-8")
        self.assertIn("| 待实现 | Designed | 未开始 |", after)

    def test_sync_preserves_trailing_newline(self):
        """sync 写盘后文件末尾必须保留换行（splitlines keepends）。"""
        text = self.matrix_path.read_text(encoding="utf-8")
        text = text.replace("| Implemented | 完成 |", "| Implemented | 主体完成 |")
        self.matrix_path.write_text(text, encoding="utf-8")
        ms.sync(self.root)
        after = self.matrix_path.read_bytes()
        self.assertTrue(after.endswith(b"\n"))


class FeatureListCheckTests(unittest.TestCase):
    def setUp(self) -> None:
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        _write_fixtures(self.root)

    def test_valid_feature_list_is_ok(self):
        result = ms.check_feature_list(self.root)
        self.assertEqual(result["state"], "ok")
        self.assertEqual(result["features"], 14)

    def test_invalid_category_is_error(self):
        text = (self.root / "docs" / "feature-list.md").read_text(encoding="utf-8")
        text = text.replace(
            "| F001 | Source 导入 | 核心链路 |", "| F001 | Source 导入 | 随便分类 |"
        )
        (self.root / "docs" / "feature-list.md").write_text(text, encoding="utf-8")
        result = ms.check_feature_list(self.root)
        self.assertEqual(result["state"], "error")
        self.assertEqual(result["invalid_categories"][0]["id"], "F001")
        self.assertEqual(result["invalid_categories"][0]["category"], "随便分类")

    def test_duplicate_id_is_error(self):
        text = (self.root / "docs" / "feature-list.md").read_text(encoding="utf-8")
        text = text.replace("| F014 | 音视频 |", "| F001 | 音视频 |", 1)
        (self.root / "docs" / "feature-list.md").write_text(text, encoding="utf-8")
        result = ms.check_feature_list(self.root)
        self.assertEqual(result["state"], "error")
        self.assertIn("F001", result["duplicate_ids"])

    def test_matrix_referenced_feature_missing_from_list_is_error(self):
        """矩阵引用 F013 但 feature-list 缺该行 → 交叉一致失败。"""
        text = (self.root / "docs" / "feature-list.md").read_text(encoding="utf-8")
        text = text.replace("| F013 | 布局 |", "| F900 | 布局 |", 1)
        (self.root / "docs" / "feature-list.md").write_text(text, encoding="utf-8")
        result = ms.check_feature_list(self.root)
        self.assertEqual(result["state"], "error")
        self.assertIn("F013", result["missing_in_feature_list"])

    def test_check_aggregates_feature_list_error(self):
        """综合 check 同时暴露矩阵与 feature-list 的错误。"""
        text = (self.root / "docs" / "feature-list.md").read_text(encoding="utf-8")
        text = text.replace(
            "| F001 | Source 导入 | 核心链路 |", "| F001 | Source 导入 | 随便分类 |"
        )
        (self.root / "docs" / "feature-list.md").write_text(text, encoding="utf-8")
        result = ms.check(self.root)
        self.assertEqual(result["state"], "error")
        self.assertIn("feature_list", result["checks"])


class DocIndexCheckTests(unittest.TestCase):
    def setUp(self) -> None:
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        _write_doc_indexes(self.root)

    def test_symmetric_indexes_are_ok(self):
        result = ms.check_doc_indexes(self.root)
        self.assertEqual(result["state"], "ok")
        for name in ("adr", "technical-design", "acceptance"):
            self.assertEqual(result[name]["state"], "ok")
            self.assertEqual(result[name]["links"], result[name]["docs"])

    def test_missing_index_entries_are_error(self):
        """目录内新增文档但 README 未登记 → unindexed_docs error。"""
        extra = self.root / "docs" / "acceptance" / "F999-new.md"
        extra.write_text("# F999\n", encoding="utf-8")
        result = ms.check_doc_indexes(self.root)
        self.assertEqual(result["state"], "error")
        self.assertIn("F999-new.md", result["checks"]["acceptance"]["unindexed_docs"])

    def test_broken_link_is_error(self):
        """README 引用不存在的文档 → broken_links error。"""
        readme = self.root / "docs" / "adr" / "README.md"
        readme.write_text(
            "## 索引\n\n| 名称 | 状态 | 链接 |\n| --- | --- | --- |\n"
            "| ADR-9999 | Accepted | [正文](./9999-ghost.md) |\n",
            encoding="utf-8",
        )
        result = ms.check_doc_indexes(self.root)
        self.assertEqual(result["state"], "error")
        self.assertIn("9999-ghost.md", result["checks"]["adr"]["broken_links"])

    def test_status_mismatch_is_error(self):
        """README 状态列与正文状态不一致 → status_mismatches error。"""
        readme = self.root / "docs" / "adr" / "README.md"
        text = readme.read_text(encoding="utf-8")
        text = text.replace("| Accepted |", "| Proposed |", 1)
        readme.write_text(text, encoding="utf-8")
        result = ms.check_doc_indexes(self.root)
        self.assertEqual(result["state"], "error")
        mismatch = result["checks"]["adr"]["status_mismatches"]
        self.assertEqual(mismatch[0]["file"], "0001-source-first.md")
        self.assertEqual(mismatch[0]["readme"], "Proposed")
        self.assertEqual(mismatch[0]["doc"], "Accepted")

    def test_status_doc_has_but_readme_marks_missing(self):
        """正文有状态但 README 标「无状态行」→ error。"""
        readme = self.root / "docs" / "acceptance" / "README.md"
        text = readme.read_text(encoding="utf-8")
        text = text.replace("| Implemented |", "| （正文无状态行） |", 1)
        readme.write_text(text, encoding="utf-8")
        result = ms.check_doc_indexes(self.root)
        self.assertEqual(result["state"], "error")
        mismatch = result["checks"]["acceptance"]["status_mismatches"]
        self.assertEqual(
            mismatch[0]["reason"], "doc_has_status_but_readme_marks_missing"
        )

    def test_status_both_none_is_ok(self):
        """README 标「无状态行」且正文确无状态行 → 一致 ok。"""
        doc = self.root / "docs" / "acceptance" / "F001-source-ingestion.md"
        doc.write_text("# F001\n", encoding="utf-8")  # 移除状态行
        readme = self.root / "docs" / "acceptance" / "README.md"
        text = readme.read_text(encoding="utf-8")
        text = text.replace("| Implemented |", "| （正文无状态行） |", 1)
        readme.write_text(text, encoding="utf-8")
        result = ms.check_doc_indexes(self.root)
        self.assertEqual(result["state"], "ok")

    def test_check_aggregates_doc_index_error(self):
        """综合 check 同时暴露文档索引漂移。"""
        extra = self.root / "docs" / "technical-design" / "new-design.md"
        extra.write_text("# new\n", encoding="utf-8")
        result = ms.check(self.root)
        self.assertEqual(result["state"], "error")
        self.assertIn("doc_index:technical-design", result["checks"])


class MainExitCodeTests(unittest.TestCase):
    def test_check_ok_exits_zero(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            _write_fixtures(root)
            self.assertEqual(ms.main(["check", "--root", str(root)]), 0)

    def test_check_stale_exits_two(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            text = MINIMAL_MATRIX.replace(
                "| Implemented | 完成 |", "| Implemented | 主体完成 |"
            )
            (root / "docs").mkdir(parents=True)
            (root / "docs" / "traceability-matrix.md").write_text(
                text, encoding="utf-8"
            )
            (root / "docs" / "feature-list.md").write_text(
                MINIMAL_FEATURE_LIST, encoding="utf-8"
            )
            _write_fake_tests(root)
            _write_doc_indexes(root)
            self.assertEqual(ms.main(["check", "--root", str(root)]), 2)


if __name__ == "__main__":
    unittest.main()
