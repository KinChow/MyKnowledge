"""Generate the public projection from validated public Wiki objects (F007)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from . import retire_ledger
from .common import atomic_write, canonical_json, hash_canonical
from .contract import blocked, ok
from .front_matter import FrontMatter
from .paths import RepoPaths
from .validation.validator import WikiValidator


class PublicProjectionGenerator:
    """Public-only manifest generator with an explicit allowlist boundary."""

    def __init__(self, root: Path, validator: Any | None = None) -> None:
        self.root = Path(root).resolve()
        self.paths = RepoPaths(self.root)
        self.validator = validator or WikiValidator(self.root, vault_id="public")

    def _item(
        self,
        object_id: str,
        relative: str,
        metadata: dict,
        derived: dict,
        hashes: dict,
        links: Any,
    ) -> dict[str, Any]:
        """Materialize deterministic public metadata; never copy approval events."""
        return {
            "id": object_id,
            "object_type": "wiki",
            "vault_id": "public",
            "title": metadata.get("title", object_id),
            "domain": metadata.get("domain"),
            "kind": metadata.get("kind"),
            "tags": [
                str(tag) for tag in (metadata.get("tags") or []) if isinstance(tag, str)
            ],
            "strength": derived.get("strength"),
            "route": "/wiki/" + object_id,
            "body_path": relative,
            "attachments": [],
            "status": "published",
            "publication_scope": metadata.get("publication_scope"),
            "public_publishable": True,
            "public_release": True,
            "effective_confidentiality": derived.get(
                "effective_confidentiality", "public"
            ),
            "validation_state": derived.get("validation_state"),
            "evidence_state": derived.get("evidence_state"),
            "links": links if isinstance(links, list) else [],
            "content_sha256": hashes.get("content_sha256"),
            "evidence_sha256": hashes.get("evidence_sha256"),
        }

    def release_candidate(
        self, object_id: str
    ) -> tuple[dict[str, Any] | None, str | None]:
        """Deterministic material for the historical ``release input`` command."""
        wiki_root = self.paths.wiki_root
        paths = sorted(wiki_root.rglob("*.md")) if wiki_root.is_dir() else []
        for path in paths:
            if retire_ledger.is_retired(self.paths, "wiki", path.stem):
                continue
            if path.is_symlink() or not path.is_file():
                continue
            try:
                report = self.validator.validate(path)
            except (OSError, UnicodeError, ValueError):
                continue
            current = str(
                (report.get("object_ref") or {}).get("object_id") or path.stem
            )
            if current != object_id:
                continue
            derived = report.get("derived") or {}
            hashes = report.get("hashes") or {}
            if not report.get("valid") or not derived.get("public_release_ready"):
                return None, "not_public_publishable"
            metadata: dict = {}
            try:
                metadata, _ = FrontMatter.parse(path.read_text(encoding="utf-8"))
            except (OSError, ValueError, UnicodeError):
                metadata = {}
            links = metadata.get("related", []) if isinstance(metadata, dict) else []
            return {
                "item": self._item(
                    object_id,
                    str(path.relative_to(self.root)),
                    metadata,
                    derived,
                    hashes,
                    links,
                ),
                "content_sha256": hashes.get("content_sha256"),
                "evidence_sha256": hashes.get("evidence_sha256"),
            }, None
        return None, "object_not_found"

    @staticmethod
    def _failed_candidates(skipped: list[dict], paths: list[Path]) -> list[dict]:
        failed = []
        for entry in skipped:
            oid = entry.get("object_id")
            candidates = [p for p in paths if p.stem == oid] if oid else paths
            for candidate in candidates:
                try:
                    meta, _ = FrontMatter.parse(candidate.read_text(encoding="utf-8"))
                except (OSError, ValueError):
                    failed.append(entry)
                    break
                if (
                    meta.get("status") == "published"
                    and meta.get("publication_scope") == "public"
                ):
                    failed.append(entry)
                    break
        return failed

    def generate(
        self, output: Path | None = None, *, strict: bool = False
    ) -> dict[str, Any]:
        output = (
            Path(output)
            if output is not None
            else self.paths.queries_public / "manifest.json"
        )
        if not output.is_absolute():
            output = self.root / output
        items: list[dict[str, Any]] = []
        skipped: list[dict[str, str]] = []
        wiki_root = self.paths.wiki_root
        paths = sorted(wiki_root.rglob("*.md")) if wiki_root.is_dir() else []
        for path in paths:
            if retire_ledger.is_retired(self.paths, "wiki", path.stem):
                continue
            if path.is_symlink() or not path.is_file():
                continue
            try:
                report = self.validator.validate(path)
            except (OSError, UnicodeError, ValueError) as exc:
                # 读文件/front matter 层面的失败是对象级阻断；validator 自身的
                # 编程错误不在此吞掉，否则未发布会被伪装成"跳过一篇"
                skipped.append(
                    {
                        "path": str(path.relative_to(self.root)),
                        "reason": type(exc).__name__,
                    }
                )
                continue
            object_id = str(
                (report.get("object_ref") or {}).get("object_id") or path.stem
            )
            derived = report.get("derived") or {}
            hashes = report.get("hashes") or {}
            if not report.get("valid") or not derived.get("public_publishable"):
                skipped.append(
                    {"object_id": object_id, "reason": "not_public_publishable"}
                )
                continue
            relative = str(path.relative_to(self.root))
            metadata = {}
            try:
                metadata, _ = FrontMatter.parse(path.read_text(encoding="utf-8"))
            except (OSError, ValueError, UnicodeError):
                metadata = {}
            links = metadata.get("related", []) if isinstance(metadata, dict) else []
            candidate = self._item(
                object_id, relative, metadata, derived, hashes, links
            )
            items.append(candidate)
        if strict:
            failed = self._failed_candidates(skipped, paths)
            if failed:
                return blocked(
                    "public-projection-result/v1", "projection_invalid", errors=failed
                )
        if len({item["id"] for item in items}) != len(items):
            return blocked("public-projection-result/v1", "projection_invalid")
        items.sort(key=lambda item: item["id"])
        manifest = {
            "schema_version": "public-projection/v1",
            "projection": "public",
            "generated_from": hash_canonical(items),
            "items": items,
        }
        encoded = canonical_json(manifest) + b"\n"
        changed = not output.exists() or output.read_bytes() != encoded
        if changed and output == self.paths.queries_public / "manifest.json":
            from .indexing import mark_public_index_stale

            mark_public_index_stale(self.root)
        atomic_write(output, encoded, 0o600)
        return ok(
            "public-projection-result/v1",
            path=str(output.relative_to(self.root))
            if output.is_relative_to(self.root)
            else str(output),
            item_count=len(items),
            skipped=skipped,
            manifest_sha256=hash_canonical(manifest),
        )
