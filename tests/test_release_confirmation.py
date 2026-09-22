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


def test_confirmation_writer_is_retired_without_touching_history(tmp_path):
    path = tmp_path / "release/public-confirmations/history.json"
    path.parent.mkdir(parents=True)
    path.write_text("historical bytes")
    before = path.read_bytes()
    result = write_event(tmp_path, event())
    assert result["error_code"] == "release_confirmation_retired"
    assert path.read_bytes() == before
    assert list(path.parent.iterdir()) == [path]


def test_history_validator_still_accepts_old_events():
    assert validate_event(event())["valid"]
    assert not validate_event({**event(), "target_vault": "private"})["valid"]


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
