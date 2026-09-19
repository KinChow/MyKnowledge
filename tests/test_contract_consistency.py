"""A 线收尾：结果信封防回潮一致性测试（TD §16 步骤 7）。

contract 的构造器已在**构造时** fail-closed（未知 status / 未登记 error_code 直接
ValueError），所以凡经 `tools.contract` 产出的信封天然合规。本测试再加两道守护：
1) 词表/状态轴结构不变（STATUSES 恰 3 值、ERROR_CODES = 各域子集并集、无空码）；
2) 跑一组有代表性的真实入口（question/source/wiki repo + skill dispatch），断言其
   返回信封满足统一不变量：`status ∈ STATUSES`，且 `status != ok ⇒ error_code ∈ ERROR_CODES`。
"""

from __future__ import annotations

from pathlib import Path

from tools import contract
from tools.backup import BackupManager
from tools.doctor import run_doctor
from tools.skill_runtime import dispatch
from tools.source_repository import SourceRepository
from tools.wiki_repository import WikiRepository


def _assert_envelope(result: dict) -> None:
    assert isinstance(result, dict), result
    assert result.get("status") in contract.STATUSES, result
    # 防回潮：顶层不得再出现与 status 并列的第二根状态轴 `state`
    # （历史双轴：backup/doctor/video 的 state / review 的 fsrs state 均已下沉/改名）。
    assert "state" not in result, result
    if result["status"] != "ok":
        assert result.get("error_code") in contract.ERROR_CODES, result


def test_statuses_are_exactly_three():
    expected = {"ok", "blocked", "unavailable"}
    assert expected == set(contract.STATUSES)


def test_error_codes_is_union_of_domain_subsets_and_wellformed():
    subsets = [
        contract._LOCATE_CODES,
        contract._QUESTION_CODES,
        contract._SOURCE_CODES,
        contract._ENTRY_CODES,
        contract._MISC_CODES,
        contract._CRUD_CODES,
        contract._BACKUP_CODES,
        contract._VALIDATION_CODES,
        contract._INGEST_CODES,
        contract._DOCTOR_CODES,
    ]
    union: set[str] = set()
    for block in subsets:
        union |= set(block)
    assert union == set(contract.ERROR_CODES)
    for code in contract.ERROR_CODES:
        assert isinstance(code, str) and code == code.strip() and code, repr(code)


def test_representative_envelopes_conform(tmp_path: Path):
    # blocked 路径（各实体定位失败）
    _assert_envelope(SourceRepository(tmp_path).read("public", "missing"))
    _assert_envelope(WikiRepository(tmp_path).read("public", "missing"))
    _assert_envelope(SourceRepository(tmp_path).list("public"))
    _assert_envelope(WikiRepository(tmp_path).list("public"))
    # skill dispatch：未知 action → blocked；skill_status → ok/unavailable
    _assert_envelope(dispatch("definitely_not_an_action", {}, root=tmp_path))
    _assert_envelope(dispatch("skill_status", {}, root=tmp_path))
    # 非法 payload 字段 → blocked
    _assert_envelope(dispatch("read", {"bogus": 1}, root=tmp_path))
    # 曾经的双轴重灾区：doctor（health 非 state）、backup（status 非 state）
    _assert_envelope(run_doctor(tmp_path))
    _assert_envelope(BackupManager(tmp_path).status())


def test_construction_is_fail_closed():
    import pytest

    with pytest.raises(ValueError, match="status_not_controlled"):
        contract.result("x/v1", "scheduled")
    with pytest.raises(ValueError, match="error_code_not_registered"):
        contract.blocked("x/v1", "not_a_registered_code")
