from pathlib import Path

from tools.release_confirmation import validate_event, write_event


def event():
    return {"schema_version": "public-release-confirmation/v1", "event_id": "event-one", "operation_id": "op-one", "target_ref": {"vault_id": "public", "object_type": "wiki", "object_id": "wiki-one"}, "target_vault": "public", "actor_type": "human", "actor_id": "alice", "decision": "approve", "release_input_sha256": "sha256:input", "reviewed_content_sha256": "sha256:content", "reviewed_evidence_sha256": "sha256:evidence", "leak_gate_report_sha256": "sha256:leak", "leak_gate_report_scope": "input-tree", "reason": "Reviewed public knowledge release", "confirmation_nonce": "nonce-one"}


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
    masquerade = {"schema_version": "operation-confirmation/v1", "operation_id": "op-one",
                  "scope": "public_release", "actor_type": "human", "actor_id": "alice",
                  "input_hash": "sha256:input", "diff_hash": "sha256:diff"}
    assert validate_event(masquerade) == {"valid": False, "error_code": "event_schema_invalid"}
    assert write_event(tmp_path, masquerade)["state"] == "blocked"
