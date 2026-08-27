"""Generate the public projection from validated public Wiki objects (F007)."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .common import atomic_write, canonical_json, hash_canonical
from .release_confirmation import validate_event
from .front_matter import FrontMatter
from .validation.validator import WikiValidator
from .paths import RepoPaths


class PublicProjectionGenerator:
    """Public-only manifest generator with an explicit allowlist boundary."""

    def __init__(self, root: Path, validator: Any | None = None) -> None:
        self.root = Path(root).resolve()
        self.paths = RepoPaths(self.root)
        self.validator = validator or WikiValidator(self.root, vault_id="public")

    def _confirmation(self, object_id: str, content_hash: str, evidence_hash: str) -> tuple[dict | None, str | None]:
        directory = self.paths.release_confirmations
        if not directory.is_dir():
            return None, "confirmation_missing"
        for path in sorted(directory.glob("*.json"), reverse=True):
            try:
                event = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, ValueError, json.JSONDecodeError):
                continue
            result = validate_event(event)
            ref = event.get("target_ref") or {}
            if not result.get("valid") or ref.get("object_id") != object_id:
                continue
            if event.get("reviewed_content_sha256") != content_hash or event.get("reviewed_evidence_sha256") != evidence_hash:
                continue
            return {"event": event, "path": str(path.relative_to(self.root)), "event_sha256": result["event_sha256"]}, None
        return None, "confirmation_mismatch"

    def generate(self, output: Path | None = None) -> dict[str, Any]:
        output = Path(output) if output is not None else self.paths.queries_public / "manifest.json"
        if not output.is_absolute():
            output = self.root / output
        items: list[dict[str, Any]] = []
        skipped: list[dict[str, str]] = []
        wiki_root = self.paths.wiki_root
        paths = sorted(wiki_root.rglob("*.md")) if wiki_root.is_dir() else []
        for path in paths:
            if path.is_symlink() or not path.is_file():
                continue
            try:
                report = self.validator.validate(path)
            except Exception as exc:  # validator failure is an object-level block
                skipped.append({"path": str(path.relative_to(self.root)), "reason": type(exc).__name__})
                continue
            object_id = str((report.get("object_ref") or {}).get("object_id") or path.stem)
            derived = report.get("derived") or {}
            hashes = report.get("hashes") or {}
            if not report.get("valid") or not derived.get("public_publishable"):
                skipped.append({"object_id": object_id, "reason": "not_public_publishable"})
                continue
            confirmation, reason = self._confirmation(object_id, hashes.get("content_sha256"), hashes.get("evidence_sha256"))
            if confirmation is None:
                skipped.append({"object_id": object_id, "reason": reason or "confirmation_missing"})
                continue
            relative = str(path.relative_to(self.root))
            metadata = {}
            try:
                metadata, _ = FrontMatter.parse(path.read_text(encoding="utf-8"))
            except (OSError, ValueError, UnicodeError):
                metadata = {}
            links = metadata.get("related", []) if isinstance(metadata, dict) else []
            items.append({
                "id": object_id, "title": metadata.get("title", object_id), "route": "/wiki/" + object_id,
                "body_path": relative, "vault_id": "public", "status": "published",
                "public_publishable": True, "public_release": True, "effective_confidentiality": "public",
                "content_sha256": hashes.get("content_sha256"), "evidence_sha256": hashes.get("evidence_sha256"),
                "release_input_sha256": confirmation["event"].get("release_input_sha256"),
                "public_confirmation_path": confirmation["path"], "public_confirmation_sha256": confirmation["event_sha256"],
                "links": links if isinstance(links, list) else [],
            })
        items.sort(key=lambda item: item["id"])
        manifest = {"schema_version": "public-projection/v1", "projection": "public", "generated_from": hash_canonical(items), "items": items}
        atomic_write(output, canonical_json(manifest) + b"\n", 0o600)
        return {"state": "generated", "path": str(output.relative_to(self.root)) if output.is_relative_to(self.root) else str(output),
                "item_count": len(items), "skipped": skipped, "manifest_sha256": hash_canonical(manifest)}
