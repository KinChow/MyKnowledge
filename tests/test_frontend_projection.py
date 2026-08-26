import json
import subprocess
import shutil
import hashlib
import os
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


def test_prepare_content_requires_matching_confirmation(tmp_path: Path):
    root = tmp_path / "repo"; frontend = tmp_path / "frontend"; frontend.mkdir()
    script = frontend / "prepare-content.mjs"; shutil.copy(Path(__file__).parents[1] / "frontend/scripts/prepare-content.mjs", script)
    body = root / "wiki" / "item.md"; body.parent.mkdir(parents=True); body.write_text("# Item\n", encoding="utf-8")
    manifest = {"schema_version":"public-projection/v1","projection":"public","items":[{"id":"item","vault_id":"public","public_publishable":True,"public_release":True,"status":"published","effective_confidentiality":"public","body_path":"wiki/item.md","public_confirmation_path":"release/public-confirmations/event-one.json"}]}
    (root / "queries" / "public").mkdir(parents=True); (root / "queries" / "public" / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    result = subprocess.run(["node", str(script)], cwd=frontend, env={**__import__("os").environ, "MYKNOWLEDGE_ROOT": str(root), "MYKNOWLEDGE_CONTENT_MODE":"projection"}, capture_output=True, text=True, check=False)
    assert result.returncode != 0 and "confirmation_missing" in result.stderr


def test_projection_prepare_and_graph_build_multi_page_fixture(tmp_path: Path):
    root = tmp_path / "repo"; frontend = tmp_path / "frontend"; frontend.mkdir()
    for name in ("prepare-content.mjs", "build-graph.mjs"):
        target = frontend / "scripts" / name; target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(Path(__file__).parents[1] / "frontend/scripts" / name, target)
    wiki = root / "wiki"; wiki.mkdir(parents=True)
    (wiki / "one.md").write_text("# One\n\n中文 attention\n", encoding="utf-8")
    (wiki / "two.md").write_text("# Two\n\nEnglish transformer\n", encoding="utf-8")
    from tools.release_confirmation import write_event
    (root / "queries" / "public").mkdir(parents=True)
    (root / "release" / "public-confirmations").mkdir(parents=True)
    items = []
    for ident, title, links in (("one", "One", ["two"]), ("two", "Two", [])):
        event = {"schema_version":"public-release-confirmation/v1", "event_id":f"event-{ident}", "operation_id":f"op-{ident}", "target_ref":{"vault_id":"public","object_type":"wiki","object_id":ident}, "target_vault":"public", "actor_type":"human", "actor_id":"alice", "decision":"approve", "release_input_sha256":"sha256:input", "reviewed_content_sha256":"sha256:content", "reviewed_evidence_sha256":"sha256:evidence", "leak_gate_report_sha256":"sha256:leak", "leak_gate_report_scope":"input-tree", "reason":"Reviewed public release", "confirmation_nonce":f"nonce-{ident}"}
        written = write_event(root, event)
        body = (wiki / f"{ident}.md").read_bytes()
        items.append({"id":ident,"vault_id":"public","public_publishable":True,"public_release":True,"status":"published","effective_confidentiality":"public","body_path":f"wiki/{ident}.md","public_confirmation_path":f"release/public-confirmations/event-{ident}.json","content_sha256":"sha256:" + hashlib.sha256(body).hexdigest(),"title":title,"route":ident,"links":links})
    (root / "queries" / "public" / "manifest.json").write_text(json.dumps({"schema_version":"public-projection/v1","projection":"public","generated_from":"fixture","items":items}), encoding="utf-8")
    env = {**os.environ, "MYKNOWLEDGE_ROOT": str(root), "MYKNOWLEDGE_CONTENT_MODE":"projection"}
    prepared = subprocess.run(["node", str(frontend / "scripts" / "prepare-content.mjs")], cwd=frontend, env=env, capture_output=True, text=True)
    assert prepared.returncode == 0, prepared.stderr
    catalog = json.loads((frontend / "public/generated/catalog.json").read_text())
    assert {x["id"] for x in catalog["items"]} == {"one", "two"}
    graph = subprocess.run(["node", str(frontend / "scripts" / "build-graph.mjs")], cwd=frontend, capture_output=True, text=True)
    assert graph.returncode == 0, graph.stderr
    graph_data = json.loads((frontend / "public/generated/graph.json").read_text())
    assert {x["id"] for x in graph_data["nodes"]} == {"one", "two"}
    assert graph_data["edges"] == [{"source":"one","target":"two"}]
