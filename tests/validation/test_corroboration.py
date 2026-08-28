"""F003 corroboration-v1：多 source 一致性/冲突的确定性检查。

对应 docs/acceptance/F003-evidence-validation.md AC-F003-004/005/012：
- 相同范围的一致支持才派生 corroborated；相交范围冲突 → conflicting + review；
- 转载链（同 independence_group/derived_from）不贡献独立佐证；
- 版本不相交只标记 version_scoped；未知/单位无法转换标记 unresolved；
- 不能通过增加转载数量、隐含数值容差或多数票把冲突变 corroborated。
"""

from __future__ import annotations

import unittest

from tools.validation.corroboration import (
    compute_corroboration,
    normalize_observation,
    pair_compare,
)


def _obs(**overrides: object):
    base = {
        "subject": "命题",
        "predicate": "等于",
        "object": "值",
        "qualifiers": {},
    }
    base.update(overrides)
    return normalize_observation(base)


class NormalizeTests(unittest.TestCase):
    def test_identical_observation_hashes_stable(self):
        """observation_sha256 可重放：相同输入恒同。"""
        a = _obs(
            subject="CPU 频率",
            predicate="等于",
            object="3.5 GHz",
            qualifiers={"version_range": ["v2.0", "v3.0"]},
        )
        b = _obs(
            subject="CPU 频率",
            predicate="等于",
            object="3.5 GHz",
            qualifiers={"version_range": ["v2.0", "v3.0"]},
        )
        self.assertEqual(a.observation_sha256, b.observation_sha256)

    def test_nfc_normalization(self):
        """Unicode NFC 归一：组合字符序列统一（TD 第 3 步，NFC 而非 NFKC——
        保留代码标识符与标点，全角字母不做兼容分解）。"""
        # "café" 预组合 vs "cafe\u0301" 分解形式 → NFC 归一后相等
        a = _obs(subject="café", predicate="等于", object="1")
        b = _obs(subject="cafe\u0301", predicate="等于", object="1")
        self.assertEqual(a.subject, b.subject)

    def test_unconvertible_unit_not_unresolved(self):
        """未知单位只记 note 不置 unresolved（文本全等命题仍可比较）。"""
        obs = _obs(subject="CPU 频率", predicate="等于", object="3.5 GHz")
        self.assertFalse(obs.unresolved)
        self.assertEqual(obs.note, "unit_unconvertible")

    def test_explicit_number_unparseable_is_unresolved(self):
        """显式声明数值但无法解析 → unresolved（fail-closed）。"""
        obs = _obs(
            subject="命题",
            predicate="等于",
            object="abc",
            qualifiers={"number": "not-a-number"},
        )
        self.assertTrue(obs.unresolved)
        self.assertEqual(obs.note, "number_unparseable")


class PairCompareTests(unittest.TestCase):
    def test_same_proposition_supports_same(self):
        a = _obs(
            subject="CPU 频率",
            predicate="等于",
            object="3.5 GHz",
            qualifiers={"version_range": ["v2.0", "v3.0"]},
        )
        b = _obs(
            subject="CPU 频率",
            predicate="等于",
            object="3.5 GHz",
            qualifiers={"version_range": ["v2.0", "v3.0"]},
        )
        self.assertEqual(pair_compare(a, b)["result"], "supports_same")

    def test_opposite_predicate_conflicts(self):
        a = _obs(subject="CPU 频率", predicate="等于", object="3.5 GHz")
        b = _obs(subject="CPU 频率", predicate="不等于", object="3.5 GHz")
        self.assertEqual(pair_compare(a, b)["result"], "conflicts")

    def test_numeric_equal_across_units_supports(self):
        """ "2 GB" ≡ "2048 MB"：规范化后相等 → supports_same（无隐含容差，精确相等）。"""
        a = _obs(subject="内存大小", predicate="等于", object="2 GB")
        b = _obs(subject="内存大小", predicate="等于", object="2048 MB")
        self.assertEqual(pair_compare(a, b)["result"], "supports_same")

    def test_numeric_difference_conflicts(self):
        a = _obs(subject="内存大小", predicate="等于", object="2 GB")
        b = _obs(subject="内存大小", predicate="等于", object="4 GB")
        self.assertEqual(pair_compare(a, b)["result"], "conflicts")

    def test_disjoint_version_ranges_version_scoped(self):
        """版本半开区间不相交 → version_scoped（不算冲突）。"""
        a = _obs(
            subject="CPU 频率",
            predicate="等于",
            object="3.5 GHz",
            qualifiers={"version_range": ["v2.0", "v3.0"]},
        )
        b = _obs(
            subject="CPU 频率",
            predicate="等于",
            object="4.0 GHz",
            qualifiers={"version_range": ["v3.0", "v4.0"]},
        )
        self.assertEqual(pair_compare(a, b)["result"], "version_scoped")

    def test_different_proposition_unresolved(self):
        a = _obs(subject="A", predicate="等于", object="1")
        b = _obs(subject="B", predicate="等于", object="1")
        self.assertEqual(pair_compare(a, b)["result"], "unresolved")


class AggregateTests(unittest.TestCase):
    def _targets_and_sources(self, groups: dict[str, str]) -> tuple[list, dict]:
        targets = []
        sources = {}
        for idx, (source_id, group) in enumerate(groups.items()):
            targets.append(
                {
                    "source_id": source_id,
                    "evidence_id": f"e{idx + 1}",
                    "resolved_object_ref": {"vault_id": "public"},
                    "snapshot_sha256": f"sha256:{idx}",
                    "selector": {},
                }
            )
            sources[source_id] = {
                "metadata": {"provenance": {"independence_group": group}}
            }
        return targets, sources

    def test_two_independent_groups_corroborated(self):
        """≥2 个不同独立组一致支持 → corroborated。"""
        targets, sources = self._targets_and_sources({"s1": "g1", "s2": "g2"})
        obs = _obs(subject="命题", predicate="等于", object="值")
        result = compute_corroboration(targets, sources, {"e1": obs, "e2": obs})
        self.assertEqual(result["evidence_state"], "corroborated")
        self.assertEqual(result["independent_groups"], ["g1", "g2"])

    def test_same_group_duplicate_does_not_corroborate(self):
        """AC-F003-005：转载链（同组）不贡献独立佐证 → 仍 supported。"""
        targets, sources = self._targets_and_sources({"s1": "g1", "s2": "g1"})
        obs = _obs(subject="命题", predicate="等于", object="值")
        result = compute_corroboration(targets, sources, {"e1": obs, "e2": obs})
        self.assertEqual(result["evidence_state"], "supported")
        self.assertEqual(result["independent_groups"], [])

    def test_conflict_sets_review(self):
        """AC-F003-004：相交范围冲突 → conflicting + review，不得自动发布。"""
        targets, sources = self._targets_and_sources({"s1": "g1", "s2": "g2"})
        result = compute_corroboration(
            targets,
            sources,
            {
                "e1": _obs(subject="命题", predicate="等于", object="值"),
                "e2": _obs(subject="命题", predicate="不等于", object="值"),
            },
        )
        self.assertEqual(result["evidence_state"], "conflicting")
        self.assertEqual(result["status"], "review")
        self.assertEqual(len(result["conflict_pairs"]), 1)

    def test_missing_independence_group_warns_unknown(self):
        """source 未声明 independence_group → independence_unknown（不凭域名推断）。"""
        targets = [
            {
                "source_id": "s1",
                "evidence_id": "e1",
                "resolved_object_ref": {"vault_id": "public"},
                "snapshot_sha256": "sha256:1",
                "selector": {},
            }
        ]
        sources = {"s1": {"metadata": {"provenance": {}}}}
        obs = _obs(subject="命题", predicate="等于", object="值")
        result = compute_corroboration(targets, sources, {"e1": obs})
        self.assertTrue(
            any(w["code"] == "independence_unknown" for w in result["warnings"])
        )

    def test_duplicate_target_dedup(self):
        """同一 (source, evidence, snapshot, selector) 重复 target 只保留一条。"""
        targets, sources = self._targets_and_sources({"s1": "g1"})
        targets = targets + [dict(targets[0])]
        obs = _obs(subject="命题", predicate="等于", object="值")
        result = compute_corroboration(targets, sources, {"e1": obs})
        self.assertTrue(
            any(w["code"] == "duplicate_target" for w in result["warnings"])
        )

    def test_same_group_conflict_not_supported(self):
        """④ 修复：同组内冲突命题不得落 supported（可进 publishable 的漏洞）。

        同源转载的两条相反命题 → same_group_conflicts → unresolved，
        不落入 supported 回退分支（AC-F003-012：不能把冲突变 publishable）。
        """
        targets, sources = self._targets_and_sources({"s1": "g1", "s2": "g1"})
        result = compute_corroboration(
            targets,
            sources,
            {
                "e1": _obs(subject="命题", predicate="等于", object="值"),
                "e2": _obs(subject="命题", predicate="不等于", object="值"),
            },
        )
        self.assertEqual(result["evidence_state"], "unresolved")
        self.assertTrue(result["same_group_conflicts"])

    def test_time_range_disjoint_is_version_scoped(self):
        """⑤ 修复：time_range 用日期解析，时间不相交 → version_scoped 而非 conflicts。"""
        a = _obs(
            subject="命题",
            predicate="等于",
            object="值",
            qualifiers={"time_range": ["2024-01-01", "2025-01-01"]},
        )
        b = _obs(
            subject="命题",
            predicate="等于",
            object="值2",
            qualifiers={"time_range": ["2025-01-01", "2026-01-01"]},
        )
        self.assertEqual(pair_compare(a, b)["result"], "version_scoped")

    def test_time_range_unparseable_unresolved(self):
        """⑤ 修复：时间边界无法解析 → unresolved（不得当作无边界放行）。"""
        a = _obs(
            subject="命题",
            predicate="等于",
            object="值",
            qualifiers={"time_range": ["not-a-date", "2025-01-01"]},
        )
        b = _obs(
            subject="命题",
            predicate="等于",
            object="值2",
            qualifiers={"time_range": ["2025-01-01", "2026-01-01"]},
        )
        self.assertEqual(pair_compare(a, b)["result"], "unresolved")

    def test_unitless_vs_unit_incomparable(self):
        """⑥ 修复：一侧无单位一侧带单位 → unresolved（不可按数值判等/判冲突）。"""
        a = _obs(subject="命题", predicate="等于", object="1.5")
        b = _obs(subject="命题", predicate="等于", object="1.5 s")
        self.assertEqual(pair_compare(a, b)["result"], "unresolved")

    def test_opposite_predicate_symmetric(self):
        """⑦ 修复：谓词取反双向判定，成对结果不依赖遍历顺序。"""
        a = _obs(subject="命题", predicate="等于", object="值")
        b = _obs(subject="命题", predicate="不等于", object="值")
        # 修复前 b vs a（"不等于" 在前）判 unresolved；修复后双向一致 conflicts
        self.assertEqual(pair_compare(b, a)["result"], "conflicts")

    def test_unstructurable_observation_unresolved(self):
        """无法结构化的引文不参与 corroboration → unresolved。"""
        targets, sources = self._targets_and_sources({"s1": "g1", "s2": "g2"})
        result = compute_corroboration(targets, sources, {"e1": None, "e2": None})
        self.assertEqual(result["evidence_state"], "unresolved")


if __name__ == "__main__":
    unittest.main()
