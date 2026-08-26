import json
import subprocess
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "frontend" / "scripts" / "validate-projection.mjs"
FRONTEND = Path(__file__).parents[1] / "frontend"


def run_manifest(tmp_path: Path, manifest: dict) -> subprocess.CompletedProcess:
    path = tmp_path / "manifest.json"
    path.write_text(json.dumps(manifest), encoding="utf-8")
    return subprocess.run(["node", str(SCRIPT), str(path)], capture_output=True, text=True, check=False)


def test_empty_public_projection_is_valid(tmp_path: Path):
    result = run_manifest(tmp_path, {"schema_version": "public-projection/v1", "projection": "public", "items": []})
    assert result.returncode == 0


def test_projection_rejects_practice_and_encoded_traversal(tmp_path: Path):
    base = {"id": "q", "vault_id": "public", "public_publishable": True, "public_release": True, "status": "published", "effective_confidentiality": "public"}
    for body_path in ("practice/questions/q.json", "%2e%2e/wiki/q.md"):
        result = run_manifest(tmp_path, {"schema_version": "public-projection/v1", "projection": "public", "items": [{**base, "body_path": body_path}]})
        assert result.returncode != 0


def test_projection_rejects_duplicate_ids(tmp_path: Path):
    item = {"id": "same", "vault_id": "public", "public_publishable": True, "public_release": True, "status": "published", "effective_confidentiality": "public", "body_path": "wiki/same.md"}
    result = run_manifest(tmp_path, {"schema_version": "public-projection/v1", "projection": "public", "items": [item, item]})
    assert result.returncode != 0


def test_release_lock_blocks_concurrent_build():
    lock = FRONTEND.parent / "state" / "public-release.lock"
    lock.parent.mkdir(parents=True, exist_ok=True)
    lock.write_text("held", encoding="utf-8")
    try:
        result = subprocess.run(["node", "scripts/build-release.mjs"], cwd=FRONTEND, capture_output=True, text=True, check=False)
        assert result.returncode == 2
        assert "release_lock_held" in result.stderr
    finally:
        lock.unlink(missing_ok=True)
