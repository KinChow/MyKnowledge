"""Git-approved release preparation; also the frontend's read-only Python bridge.

Release mode regenerates projection from committed canonical inputs; export mode
validates an existing manifest for local preview. Neither mode signs approvals or
calls an LLM. Frontend build must recheck the Git revision before promoting dist.
"""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

from .common import atomic_write, canonical_json
from .projection import PublicProjectionStore
from .public_projection import PublicProjectionGenerator
from .published_files import read_public_body

# Generated indexes/reports and local provider credentials are not release inputs.
# Include sources/evidence, retirement state, rules and generator code as well as UI.
RELEASE_INPUTS = (
    "content/wiki",
    "content/sources",
    "archive",
    "audit/retire",
    "audit/validation",
    "audit/overrides",
    "docs",
    "config/policy.yaml",
    "config/schemas.yaml",
    "config/json-schema",
    "tools",
    "backend",
    "frontend/src",
    "frontend/scripts",
    "frontend/astro.config.mjs",
    "frontend/package.json",
    "frontend/package-lock.json",
    "requirements-release.txt",
    ".github/workflows",
)


def committed_revision(root: Path) -> str:
    def git(*args: str) -> str:
        return subprocess.run(
            ["git", "-C", str(root), *args], check=True, capture_output=True, text=True
        ).stdout.strip()

    try:
        if Path(git("rev-parse", "--show-toplevel")).resolve() != root.resolve():
            raise ValueError("release_git_root_invalid")
        revision = git("rev-parse", "HEAD")
        if git("status", "--porcelain", "--untracked-files=all", "--", *RELEASE_INPUTS):
            raise ValueError("release_inputs_dirty")
        # Ignored files beneath canonical roots must not sneak into rglob inputs.
        if git(
            "ls-files",
            "--others",
            "--ignored",
            "--exclude-standard",
            "--",
            "content/wiki",
            "content/sources",
            "archive",
            "audit/retire",
            "audit/validation",
            "audit/overrides",
            "docs",
        ):
            raise ValueError("release_inputs_untracked")
        return revision
    except subprocess.CalledProcessError as exc:
        raise ValueError("release_git_unavailable") from exc


def export_projection(root: Path, manifest_path: Path | None = None) -> dict:
    store = PublicProjectionStore(root)
    if manifest_path is not None:
        store.manifest_path = lambda: manifest_path
    manifest = store.load_manifest()
    items = store.public_items(with_body=True)
    # Do not silently filter an invalid release input manifest.
    if len(items) != len(manifest["items"]):
        raise ValueError("projection_invalid")
    exported = []
    for item in items:
        meta, _body, _text = read_public_body(root, item)
        exported.append({**item, "aliases": meta.get("aliases") or []})
    return {**manifest, "items": exported}


def prepare_release(root: Path, output: Path) -> dict:
    revision = committed_revision(root)
    result = PublicProjectionGenerator(root).generate(output, strict=True)
    if result["status"] != "ok":
        raise ValueError("projection_invalid:" + json.dumps(result.get("errors", [])))
    manifest = json.loads(output.read_text(encoding="utf-8"))
    manifest["source_revision"] = revision
    manifest["approval"] = "git"
    atomic_write(output, canonical_json(manifest) + b"\n", 0o600)
    export_projection(root, output)
    if committed_revision(root) != revision:
        raise ValueError("release_revision_changed")
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["check", "prepare", "export"])
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--manifest", type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    try:
        if args.action == "check":
            result = {"source_revision": committed_revision(root)}
        elif args.action == "prepare":
            if args.manifest is None:
                parser.error("--manifest required")
            result = prepare_release(root, args.manifest)
        else:
            result = export_projection(root, args.manifest)
        print(json.dumps(result, ensure_ascii=False))
        return 0
    except (OSError, ValueError) as exc:
        print(json.dumps({"status": "blocked", "error_code": str(exc)}))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
