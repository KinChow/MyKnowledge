"""F010 deterministic Source-first migration preview (no canonical writes)."""
from __future__ import annotations

import hashlib
import re
from pathlib import Path
from typing import Any

from .common import canonical_json
from .inventory_legacy import inventory
from .ingest.source_ingestor import SourceIngestor
from .write_operation import WriteOperation
from .front_matter import FrontMatter
from .ingest.extractor import TextExtractor

MIGRATION_VERSION = "legacy-migration/v1"


def _slug(value: str) -> str:
    value = re.sub(r"[^a-zA-Z0-9]+", "-", value).strip("-").lower()
    return value or "untitled"


def _repair_links(body: str, legacy_path: str, plan: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    """Rewrite only links with a deterministic inventory mapping."""
    route_by_path = {item["legacy_path"]: item["route"] for item in plan["items"]}
    unresolved: list[str] = []
    repaired: list[dict[str, str]] = []
    pattern = re.compile(r"(\[[^\]]+\]\()([^)#]+)(#[^)]+)?(\))")
    parent = Path(legacy_path).parent

    def replace(match: re.Match[str]) -> str:
        prefix, target, anchor, suffix = match.groups()
        if re.match(r"(?:[a-zA-Z][a-zA-Z0-9+.-]*:|//|/)", target):
            return match.group(0)
        candidate = (parent / target).as_posix()
        if candidate in route_by_path:
            new_target = route_by_path[candidate] + (anchor or "")
            repaired.append({"from": target, "to": new_target})
            return prefix + new_target + suffix
        unresolved.append(target)
        return match.group(0)

    return pattern.sub(replace, body), {"repaired": repaired, "unresolved": unresolved}


def preview(root: Path, docs_dir: Path | None = None) -> dict[str, Any]:
    root = Path(root).resolve()
    report = inventory(root, docs_dir)
    drafts: list[dict[str, Any]] = []
    route_map: list[dict[str, str | None]] = []
    seen_ids: dict[str, str] = {}
    conflicts: list[dict[str, str]] = []
    for item in report["items"]:
        slug = _slug(Path(item["legacy_path"]).with_suffix("").as_posix())
        wiki_id = f"legacy-{slug}"
        source_id = f"legacy-{slug}-source"
        route = "/legacy/" + slug
        target = root / item["legacy_path"]
        # Every draft remains pending until source/evidence and human review pass.
        collision = seen_ids.get(wiki_id)
        if collision is not None:
            conflicts.append({"code": "stable_id_collision", "object_id": wiki_id, "first_legacy_path": collision, "legacy_path": item["legacy_path"]})
        else:
            seen_ids[wiki_id] = item["legacy_path"]
        drafts.append({
            "legacy_path": item["legacy_path"],
            "source_target": {"vault_id": "public", "object_type": "source", "object_id": source_id},
            "wiki_target": {"vault_id": "public", "object_type": "wiki", "object_id": wiki_id},
            "route": route,
            "status": "blocked" if collision is not None else "pending",
            "blocking_reason": "stable_id_collision" if collision is not None else None,
            "evidence_state": "pending",
            "publication_scope": "none",
            "content_verdict": "pending_manual_review",
            "body_sha256": item["body_sha256"],
            "extractor": "markdown-pass-through",
            "extractor_version": MIGRATION_VERSION,
            "input_exists": target.is_file(),
            "media_type": item.get("media_type", "text/markdown"),
        })
        route_map.append({"legacy_route": item["route"], "new_route": route, "status": "pending", "reason": "requires_link_repair_review"})
    result: dict[str, Any] = {
        "schema_version": MIGRATION_VERSION,
        "input_tree_sha256": report["input_tree_sha256"],
        "inventory_sha256": report["inventory_sha256"],
        "classifier_version": report["classifier_version"],
        "items": drafts,
        "route_map": route_map,
        "conflicts": conflicts,
        "completed": 0,
        "pending": len(drafts),
        "writes_applied": False,
    }
    result["preview_sha256"] = "sha256:" + hashlib.sha256(canonical_json(result)).hexdigest()
    return result


def apply_sample(root: Path, legacy_path: str, *, confirmed: bool = False, docs_dir: Path | None = None) -> dict[str, Any]:
    """Migrate one Markdown sample through the real Source-first write gates."""
    root = Path(root).resolve()
    plan = preview(root, docs_dir)
    item = next((x for x in plan["items"] if x["legacy_path"] == legacy_path), None)
    if item is None:
        return {"state": "blocked", "error_code": "legacy_item_not_found", "writes_applied": False}
    migration_key = hashlib.sha256(canonical_json({"legacy_path": legacy_path, "body_sha256": item["body_sha256"], "migration_version": MIGRATION_VERSION})).hexdigest()
    record_path = root / "audit" / "migrations" / f"{migration_key}.json"
    if record_path.is_file():
        try:
            record = __import__("json").loads(record_path.read_text(encoding="utf-8"))
            if record.get("schema_version") == "migration-record/v1" and record.get("migration_key") == migration_key:
                return {**record.get("result", {}), "replayed": True}
        except (OSError, ValueError, TypeError):
            pass
    if not confirmed:
            return {"state": "awaiting_confirmation", "writes_applied": False, "preview_sha256": plan["preview_sha256"], "item": item}
    if item.get("status") == "blocked":
        return {"state": "blocked", "error_code": item.get("blocking_reason", "migration_item_blocked"), "writes_applied": False, "item": item}
    source_id = item["source_target"]["object_id"]
    media_type = next((x.get("media_type", "text/markdown") for x in plan["items"] if x["legacy_path"] == legacy_path), "text/markdown")
    source_request = {"source_type": "local-file", "input_path": str(root / legacy_path), "domain": "tools", "source_id": source_id, "media_type": media_type}
    source_preview = SourceIngestor(root).preview(source_request)
    if source_preview.get("state") != "previewed":
        return {"state": "blocked", "stage": "source_preview", "source": source_preview, "writes_applied": False}
    source_result = SourceIngestor(root).apply(source_preview["operation_id"], confirmed=True, actor_id="migration")
    source_result = {key: value for key, value in source_result.items() if key != "source_path"}
    if source_result.get("state") != "applied":
        return {"state": "blocked", "stage": "source_apply", "source": source_result, "writes_applied": False}
    wiki_id = item["wiki_target"]["object_id"]
    wiki_path = f"wiki/tools/{wiki_id}.md"
    metadata = {"schema_version": "wiki/v1", "id": wiki_id, "title": Path(legacy_path).stem, "domain": "tools", "kind": "reference", "status": "draft", "publication_scope": "none", "confidentiality": "public", "tags": ["legacy-migration"], "aliases": [], "related": [], "sources": [source_id], "updated_at": "2026-08-27"}
    raw = (root / legacy_path).read_bytes()
    if media_type == "application/pdf":
        extracted_body, _ = TextExtractor().extract(raw, media_type)
    else:
        extracted_body = raw.decode("utf-8", errors="replace")
    repaired_body, link_report = _repair_links(extracted_body, legacy_path, plan)
    wiki_preview = WriteOperation(root).preview({wiki_path: FrontMatter.render(metadata, "# " + Path(legacy_path).stem + "\n\n" + repaired_body)}, operation_type="wiki", vault_id="public")
    if wiki_preview.get("state") != "previewed":
        return {"state": "blocked", "stage": "wiki_preview", "source": source_result, "wiki": wiki_preview, "writes_applied": True}
    wiki_result = WriteOperation(root).apply(wiki_preview["operation_id"], confirmed=True, actor_id="migration")
    result = {"state": "applied" if wiki_result.get("state") == "applied" else "blocked", "writes_applied": wiki_result.get("state") == "applied", "source": source_result, "wiki": wiki_result, "legacy_path": legacy_path, "wiki_path": wiki_path, "link_repair": link_report}
    if result["state"] == "applied":
        record = {"schema_version": "migration-record/v1", "migration_key": migration_key, "legacy_path": legacy_path, "body_sha256": item["body_sha256"], "result": result}
        record_path.parent.mkdir(parents=True, exist_ok=True)
        record_path.write_bytes(canonical_json(record) + b"\n")
    return result


def main(argv: list[str] | None = None) -> int:
    import argparse, json
    parser = argparse.ArgumentParser(description="Preview legacy Source-first migration")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--docs", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--apply-sample", metavar="LEGACY_PATH", help="apply one representative sample through Source/Wiki gates")
    parser.add_argument("--confirm", action="store_true", help="confirm the selected sample apply")
    args = parser.parse_args(argv)
    result = apply_sample(args.root, args.apply_sample, confirmed=args.confirm, docs_dir=args.docs) if args.apply_sample else preview(args.root, args.docs)
    data = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(data, encoding="utf-8")
    else:
        print(data, end="")
    return 0
