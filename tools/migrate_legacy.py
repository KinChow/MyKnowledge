"""F010 deterministic Source-first migration preview (no canonical writes)."""
from __future__ import annotations

import hashlib
import re
from pathlib import Path
from typing import Any

from .common import canonical_json
from .inventory_legacy import inventory

MIGRATION_VERSION = "legacy-migration/v1"


def _slug(value: str) -> str:
    value = re.sub(r"[^a-zA-Z0-9]+", "-", value).strip("-").lower()
    return value or "untitled"


def preview(root: Path, docs_dir: Path | None = None) -> dict[str, Any]:
    root = Path(root).resolve()
    report = inventory(root, docs_dir)
    drafts: list[dict[str, Any]] = []
    route_map: list[dict[str, str | None]] = []
    for item in report["items"]:
        slug = _slug(Path(item["legacy_path"]).with_suffix("").as_posix())
        wiki_id = f"legacy-{slug}"
        source_id = f"legacy-{slug}-source"
        route = "/legacy/" + slug
        target = root / item["legacy_path"]
        # Every draft remains pending until source/evidence and human review pass.
        drafts.append({
            "legacy_path": item["legacy_path"],
            "source_target": {"vault_id": "public", "object_type": "source", "object_id": source_id},
            "wiki_target": {"vault_id": "public", "object_type": "wiki", "object_id": wiki_id},
            "route": route,
            "status": "pending",
            "evidence_state": "pending",
            "publication_scope": "none",
            "content_verdict": "pending_manual_review",
            "body_sha256": item["body_sha256"],
            "extractor": "markdown-pass-through",
            "extractor_version": MIGRATION_VERSION,
            "input_exists": target.is_file(),
        })
        route_map.append({"legacy_route": item["route"], "new_route": route, "status": "pending", "reason": "requires_link_repair_review"})
    result: dict[str, Any] = {
        "schema_version": MIGRATION_VERSION,
        "input_tree_sha256": report["input_tree_sha256"],
        "inventory_sha256": report["inventory_sha256"],
        "classifier_version": report["classifier_version"],
        "items": drafts,
        "route_map": route_map,
        "completed": 0,
        "pending": len(drafts),
        "writes_applied": False,
    }
    result["preview_sha256"] = "sha256:" + hashlib.sha256(canonical_json(result)).hexdigest()
    return result


def main(argv: list[str] | None = None) -> int:
    import argparse, json
    parser = argparse.ArgumentParser(description="Preview legacy Source-first migration")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--docs", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    data = json.dumps(preview(args.root, args.docs), ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(data, encoding="utf-8")
    else:
        print(data, end="")
    return 0

