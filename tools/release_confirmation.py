"""Historical validator and retired writer for public-release-confirmation/v1 events."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from .common import hash_canonical, safe_id, safe_operation_id
from .contract import blocked

SCHEMA = "public-release-confirmation/v1"
WRITE_SCHEMA = "public-release-confirmation-write/v1"
REQUIRED = {
    "event_id",
    "operation_id",
    "target_ref",
    "target_vault",
    "actor_type",
    "actor_id",
    "decision",
    "release_input_sha256",
    "reviewed_content_sha256",
    "reviewed_evidence_sha256",
    "leak_gate_report_sha256",
    "leak_gate_report_scope",
    "reason",
    "confirmation_nonce",
}


def validate_event(event: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(event, dict) or event.get("schema_version") != SCHEMA:
        return {"valid": False, "error_code": "event_schema_invalid"}
    missing = sorted(REQUIRED - set(event))
    if missing:
        return {
            "valid": False,
            "error_code": "event_fields_missing",
            "missing": missing,
        }
    try:
        safe_id(str(event["event_id"]))
        safe_id(str(event["actor_id"]))
    except ValueError:
        return {"valid": False, "error_code": "event_id_invalid"}
    try:
        safe_operation_id(str(event["operation_id"]))
    except ValueError:
        return {"valid": False, "error_code": "operation_id_invalid"}
    ref = event["target_ref"]
    if (
        not isinstance(ref, dict)
        or ref.get("vault_id") != "public"
        or ref.get("object_type") != "wiki"
    ):
        return {"valid": False, "error_code": "target_not_public"}
    try:
        safe_id(str(ref["object_id"]))
    except (KeyError, ValueError):
        return {"valid": False, "error_code": "target_ref_invalid"}
    if (
        event["target_vault"] != "public"
        or event["actor_type"] != "human"
        or event["decision"] != "approve"
    ):
        return {"valid": False, "error_code": "event_authority_invalid"}
    reason = event["reason"]
    if (
        not isinstance(reason, str)
        or not reason.strip()
        or len(reason) > 240
        or re.search(r"(?:https?://|/|\\|private|internal)", reason, re.I)
    ):
        return {"valid": False, "error_code": "reason_not_public_safe"}
    if event["leak_gate_report_scope"] != "input-tree":
        return {"valid": False, "error_code": "leak_gate_scope_invalid"}
    expected = hash_canonical({k: v for k, v in event.items() if k != "event_sha256"})
    if event.get("event_sha256") and event["event_sha256"] != expected:
        return {"valid": False, "error_code": "event_hash_mismatch"}
    return {"valid": True, "event_sha256": expected}


def write_event(_root: Path, _event: dict[str, Any]) -> dict[str, Any]:
    """Compatibility tombstone: approval is Git; historical events remain readable."""
    return blocked(
        WRITE_SCHEMA,
        "release_confirmation_retired",
        next_action="review and commit content, then build the public release",
    )
