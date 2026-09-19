"""Read-only W3C-style citation replay for F006."""

from __future__ import annotations

from typing import Any

from .common import sha256_text
from .contract import ok


def replay(citation: dict[str, Any], snapshot: str) -> dict[str, Any]:
    """Verify snapshot hash and TextQuote/TextPosition 逐字命中。

    回放操作本身总能得出结论，故信封 ``status`` 恒为 ``ok``；命中与否是**校验结论**，
    落在 ``report.valid`` 而非 status 轴（TD §14：领域结果不进 status）。
    """
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
        # ADR-0019 §5：不再比对落盘的 `quote_sha256` / `selector_sha256`——校验值不
        # 落盘。命中判定完全由上一行的 position↔exact 逐字比对承担；指纹自证是冗余
        # 的（指纹可由 exact/selector 现算，canonical 被篡改由 git 暴露）。
        return ok(
            "citation-replay/v1",
            report={"valid": True},
            snapshot_sha256=expected_snapshot,
            start=start,
            end=end,
            exact=exact,
        )
    except (KeyError, TypeError, ValueError) as exc:
        return ok("citation-replay/v1", report={"valid": False, "reason": str(exc)})
