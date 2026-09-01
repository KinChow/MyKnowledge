from pathlib import Path

import pytest

from tools.common import new_operation_id, safe_operation_id
from tools.release_confirmation import validate_event, write_event


def event():
    return {
        "schema_version": "public-release-confirmation/v1",
        "event_id": "event-one",
        "operation_id": "op-one",
        "target_ref": {
            "vault_id": "public",
            "object_type": "wiki",
            "object_id": "wiki-one",
        },
        "target_vault": "public",
        "actor_type": "human",
        "actor_id": "alice",
        "decision": "approve",
        "release_input_sha256": "sha256:input",
        "reviewed_content_sha256": "sha256:content",
        "reviewed_evidence_sha256": "sha256:evidence",
        "leak_gate_report_sha256": "sha256:leak",
        "leak_gate_report_scope": "input-tree",
        "reason": "Reviewed public knowledge release",
        "confirmation_nonce": "nonce-one",
    }


def test_public_release_event_is_hashed_and_written(tmp_path: Path):
    result = write_event(tmp_path, event())
    assert result["state"] == "created"
    assert validate_event({**event(), "event_sha256": result["event_sha256"]})["valid"]


def test_public_release_event_rejects_private_reason_or_target(tmp_path: Path):
    bad = {**event(), "reason": "see https://internal.example/private"}
    assert validate_event(bad)["error_code"] == "reason_not_public_safe"
    bad = {**event(), "target_vault": "private"}
    assert validate_event(bad)["error_code"] == "event_authority_invalid"


def test_public_release_nonce_cannot_be_reused_by_another_event(tmp_path: Path):
    assert write_event(tmp_path, event())["state"] == "created"
    replay = {**event(), "event_id": "event-two", "operation_id": "op-two"}
    result = write_event(tmp_path, replay)
    assert result == {"state": "blocked", "error_code": "confirmation_nonce_reused"}


def test_public_release_rejects_operation_confirmation_masquerade(tmp_path: Path):
    """AC-F004-011：public release 只接受 public-release-confirmation/v1。"""
    masquerade = {
        "schema_version": "operation-confirmation/v1",
        "operation_id": "op-one",
        "scope": "public_release",
        "actor_type": "human",
        "actor_id": "alice",
        "input_hash": "sha256:input",
        "diff_hash": "sha256:diff",
    }
    assert validate_event(masquerade) == {
        "valid": False,
        "error_code": "event_schema_invalid",
    }
    assert write_event(tmp_path, masquerade)["state"] == "blocked"


def test_relative_root_still_reports_a_repo_relative_path(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    """`--root .` 必须能正常返回：事件已落盘却以 traceback 收尾时，人只看到
    "报错了"，无法判断确认到底有没有生效（实测就是这样丢掉一次人工确认的）。"""
    monkeypatch.chdir(tmp_path)
    created = write_event(Path("."), event())
    assert created["state"] == "created"
    assert created["path"] == "release/public-confirmations/event-one.json"
    assert write_event(Path("."), event())["state"] == "already_applied"


def test_repeating_the_same_confirmation_is_already_applied(tmp_path: Path):
    """重复执行同一条确认不是失败：报 already_applied 并回带已存记录的 hash。

    原来返回 blocked/event_exists，人会以为签名失败而去删 append-only 记录重签。
    """
    created = write_event(tmp_path, event())
    repeated = write_event(tmp_path, event())
    assert repeated == {
        "state": "already_applied",
        "event_sha256": created["event_sha256"],
        "path": created["path"],
    }


def test_same_event_id_with_different_content_is_a_conflict(tmp_path: Path):
    """同 event_id、不同内容必须 fail-closed，不得混进 already_applied。"""
    assert write_event(tmp_path, event())["state"] == "created"
    result = write_event(tmp_path, {**event(), "reason": "Reviewed again later"})
    assert result == {"state": "blocked", "error_code": "event_id_conflict"}


def test_real_generated_operation_id_passes_validation(tmp_path: Path):
    """生产形态 op_<hex> 必须被校验端接受（生成端与校验端同源）。"""
    real = new_operation_id()
    assert safe_operation_id(real) == real
    assert validate_event({**event(), "operation_id": real})["valid"] is True


@pytest.mark.parametrize(
    "bad", ["op_", "op_ABC", "../op-one", "op_one/two", "one", "op_一", "op__x"]
)
def test_operation_id_rejects_unsafe_forms(bad: str):
    """非法 operation_id 必须在生成端/校验端同时拒绝（路径穿越与注入防护）。"""
    with pytest.raises(ValueError):
        safe_operation_id(bad)
    assert validate_event({**event(), "operation_id": bad}) == {
        "valid": False,
        "error_code": "operation_id_invalid",
    }
