import json
import os
import subprocess

import pytest

from tools.common import canonical_body, sha256_text
from tools.projection import PublicProjectionStore
from tools.release_build import committed_revision


def manifest_fixture(root):
    path = root / "content/wiki/one.md"
    path.parent.mkdir(parents=True)
    path.write_text("# One\n")
    item = {
        "id": "one",
        "vault_id": "public",
        "public_publishable": True,
        "public_release": True,
        "status": "published",
        "effective_confidentiality": "public",
        "body_path": "content/wiki/one.md",
        "content_sha256": sha256_text(canonical_body("# One\n")),
    }
    manifest = root / "var/queries/public/manifest.json"
    manifest.parent.mkdir(parents=True)
    manifest.write_text(
        json.dumps(
            {
                "schema_version": "public-projection/v1",
                "projection": "public",
                "items": [item],
            }
        )
    )
    return path


def test_changed_body_is_never_public(tmp_path):
    path = manifest_fixture(tmp_path)
    store = PublicProjectionStore(tmp_path)
    assert store.public_items(with_body=True)[0]["body"] == "# One\n"
    path.write_text("# Unapproved\n")
    with pytest.raises(ValueError, match="projection_body_stale"):
        store.public_items(with_body=True)
    with pytest.raises(ValueError, match="projection_body_stale"):
        store.public_items(with_body=False)
    assert store.degraded_items() == []


def test_http_and_cli_reject_stale_body_after_startup(tmp_path):
    from fastapi.testclient import TestClient

    from backend.app import create_app
    from tools.skill_runtime import dispatch

    path = manifest_fixture(tmp_path)
    client = TestClient(create_app(root=tmp_path, capability_token="secret"))
    assert client.get("/api/read/public/wiki/one").status_code == 200
    path.write_text("# Unapproved\n")
    for route in [
        "/api/read/public/wiki/one",
        "/api/list/public/wiki",
        "/api/query?q=One",
        "/api/backlinks/public/wiki/one",
    ]:
        response = client.get(route)
        assert response.status_code == 409, response.text
        assert response.json()["detail"]["code"] == "projection_body_stale"
        assert "Unapproved" not in response.text
    assert (
        dispatch("read", {"object_id": "one"}, root=tmp_path)["error_code"]
        == "projection_body_stale"
    )


@pytest.mark.parametrize(
    "relative", ["../one.md", "/etc/passwd", "content/wiki/../../one.md"]
)
def test_projection_rejects_outside_paths(tmp_path, relative):
    from tools.published_files import read_public_file

    with pytest.raises(ValueError, match="projection_path_invalid"):
        read_public_file(tmp_path, relative)


def test_index_invalidation_is_explicit_and_rebuild_clears_it(tmp_path):
    from tools.indexing import (
        SQLiteIndex,
        default_public_index_path,
        mark_public_index_stale,
    )

    path = default_public_index_path(tmp_path)
    index = SQLiteIndex(path, root=tmp_path)
    index.rebuild([], "public")
    mark_public_index_stale(tmp_path)
    marker = path.with_suffix(".sqlite3.stale")
    assert marker.exists()
    index.rebuild([], "public")
    assert not marker.exists()


@pytest.mark.parametrize("mode", ["parent", "file", "hardlink"])
def test_projection_refuses_link_paths(tmp_path, mode):
    root = tmp_path / "repo"
    root.mkdir()
    path = manifest_fixture(root)
    outside = tmp_path / "outside"
    outside.mkdir()
    target = outside / "one.md"
    target.write_text("# One\n")
    path.unlink()
    if mode == "file":
        path.symlink_to(target)
    elif mode == "hardlink":
        os.link(target, path)
    else:
        path.parent.rmdir()
        path.parent.symlink_to(outside, target_is_directory=True)
    with pytest.raises(ValueError):
        PublicProjectionStore(root).public_items(with_body=True)


def test_release_rejects_dirty_staged_untracked_and_non_git_root(tmp_path):
    def git(*args):
        subprocess.run(
            ["git", "-C", str(tmp_path), *args], check=True, capture_output=True
        )

    git("init")
    git("config", "user.name", "Fixture")
    git("config", "user.email", "fixture@example.invalid")
    p = tmp_path / "content/wiki/one.md"
    p.parent.mkdir(parents=True)
    p.write_text("one")
    git("add", ".")
    git("commit", "-m", "fixture")
    assert len(committed_revision(tmp_path)) == 40
    p.write_text("two")
    with pytest.raises(ValueError, match="release_inputs_dirty"):
        committed_revision(tmp_path)
    git("add", ".")
    with pytest.raises(ValueError, match="release_inputs_dirty"):
        committed_revision(tmp_path)
    git("commit", "-m", "fixture two")
    p.with_name("untracked.md").write_text("new")
    with pytest.raises(ValueError, match="release_inputs_dirty"):
        committed_revision(tmp_path)
