from tools.citation import replay
from tools.evidence_anchor import EvidenceAnchor


def test_citation_replay_uses_unicode_codepoint_offsets():
    snapshot = "前缀😀 这是可验证的引文。 后缀"
    anchored = EvidenceAnchor.anchor(snapshot, "这是可验证的引文。", min_chars=1)
    result = replay(anchored, snapshot)
    assert result["status"] == "ok"
    assert result["report"]["valid"] is True


def test_citation_replay_rejects_snapshot_and_selector_drift():
    snapshot = "这是稳定的证据文本。"
    anchored = EvidenceAnchor.anchor(snapshot, snapshot, min_chars=1)
    drifted = replay(anchored, "文本已经变化。")
    assert drifted["status"] == "ok"
    assert drifted["report"] == {"valid": False, "reason": "snapshot_hash_mismatch"}
    anchored["selector"]["exact"] = "伪造文本"
    unresolved = replay(anchored, snapshot)
    assert unresolved["report"] == {"valid": False, "reason": "selector_unresolved"}
