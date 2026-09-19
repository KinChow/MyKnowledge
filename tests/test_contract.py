"""统一结果信封（tools.contract, TD §14 · 单 status 轴）的 TDD 契约测试。"""

from __future__ import annotations

import pytest

from tools import contract


def test_statuses_are_the_three_controlled_values():
    expected = {"ok", "blocked", "unavailable"}
    assert expected == set(contract.STATUSES)


def test_ok_sets_schema_version_and_status_and_payload():
    r = contract.ok("read-result/v1", body="x")
    assert r == {"schema_version": "read-result/v1", "status": "ok", "body": "x"}


def test_result_rejects_uncontrolled_status():
    with pytest.raises(ValueError, match="status_not_controlled"):
        contract.result("x/v1", "created")


@pytest.mark.parametrize("bad", ["noversion", "a/b/c/v1", "Upper/v1", "name/v"])
def test_result_rejects_malformed_schema_version(bad: str):
    with pytest.raises(ValueError, match="schema_version_invalid"):
        contract.ok(bad)


def test_non_ok_requires_error_code():
    with pytest.raises(ValueError, match="error_code_required"):
        contract.result("x/v1", "blocked")


def test_non_ok_rejects_unregistered_error_code():
    with pytest.raises(ValueError, match="error_code_not_registered"):
        contract.blocked("x/v1", "totally_made_up_code")


def test_blocked_accepts_registered_code_with_field_errors():
    r = contract.blocked(
        "x/v1", "object_not_found", errors=[{"code": "object_not_found"}]
    )
    assert r["status"] == "blocked"
    assert r["error_code"] == "object_not_found"
    assert r["errors"] == [{"code": "object_not_found"}]


def test_unavailable_builder():
    with pytest.raises(ValueError, match="error_code_not_registered"):
        contract.unavailable("ask-result/v1", "provider_unavailable")
    r = contract.unavailable("x/v1", "vault_unavailable")
    assert r["status"] == "unavailable"
    assert r["error_code"] == "vault_unavailable"


def test_require_error_code_roundtrip():
    assert contract.require_error_code("object_id_ambiguous") == "object_id_ambiguous"
