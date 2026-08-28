"""Read-only W3C-style citation replay for F006."""

from __future__ import annotations

from typing import Any

from .common import canonical_quote, hash_canonical, sha256_text


def replay(citation: dict[str, Any], snapshot: str) -> dict[str, Any]:
    """Verify snapshot hash, TextQuote/TextPosition and selector hash."""
    try:
        expected_snapshot = citation["snapshot_sha256"]
        if sha256_text(snapshot) != expected_snapshot:
            raise ValueError("snapshot_hash_mismatch")
        selector = citation["selector"]
        position = citation.get("position") or citation.get("text_position")
        if (
            selector.get("type") != "TextQuoteSelector"
            or not isinstance(position, dict)
            or position.get("type") != "TextPositionSelector"
        ):
            raise ValueError("selector_unresolved")
        start, end = position.get("start"), position.get("end")
        if (
            not isinstance(start, int)
            or not isinstance(end, int)
            or start < 0
            or end <= start
            or end > len(snapshot)
        ):
            raise ValueError("selector_unresolved")
        exact = selector.get("exact")
        if not isinstance(exact, str) or snapshot[start:end] != exact:
            raise ValueError("selector_unresolved")
        if citation.get("quote_sha256") and citation["quote_sha256"] != sha256_text(
            canonical_quote(exact)
        ):
            raise ValueError("selector_hash_mismatch")
        computed = hash_canonical(
            {
                "snapshot_sha256": expected_snapshot,
                "start": start,
                "end": end,
                "exact": exact,
                "prefix": selector.get("prefix", ""),
                "suffix": selector.get("suffix", ""),
            }
        )
        if citation.get("selector_sha256") and citation["selector_sha256"] != computed:
            raise ValueError("selector_hash_mismatch")
        return {
            "state": "valid",
            "snapshot_sha256": expected_snapshot,
            "start": start,
            "end": end,
            "exact": exact,
        }
    except (KeyError, TypeError, ValueError) as exc:
        return {"state": "unavailable", "reason": str(exc)}
