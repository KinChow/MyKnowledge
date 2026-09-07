"""ASR strength gate tests."""

from tools.validation.derived import compute_strength


def _resolution(human_verified: bool) -> dict:
    return {
        "resolved_targets": [
            {
                "source_id": "asr-video",
                "evidence_id": "e1",
                "position": {"start": 20, "end": 40},
                "human_verified_segment": (
                    {"start": 0, "end": 100} if human_verified else None
                ),
            },
            {
                "source_id": "official-pdf",
                "evidence_id": "e2",
                "position": {"start": 0, "end": 30},
                "human_verified_segment": None,
            },
        ],
        "sources": {
            "asr-video": {
                "metadata": {
                    "source_type": "video",
                    "video": {"transcript_provenance": {"kind": "asr"}},
                }
            },
            "official-pdf": {"metadata": {"source_type": "doc"}},
        },
    }


def test_asr_target_caps_multi_source_verified_strength():
    assert (
        compute_strength(
            "knowledge",
            "supported",
            _resolution(human_verified=False),
            {"verdict": "pass"},
            "pass",
        )
        == "attested"
    )


def test_human_verified_segment_unlocks_asr_cap():
    assert (
        compute_strength(
            "knowledge",
            "supported",
            _resolution(human_verified=True),
            {"verdict": "pass"},
            "pass",
        )
        == "verified"
    )
