import json
import subprocess
import shutil
import hashlib
import os
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "frontend" / "scripts" / "validate-projection.mjs"
FRONTEND = Path(__file__).parents[1] / "frontend"


def test_starlight_content_collection_uses_projection_output():
    config = (FRONTEND / "src/content.config.ts").read_text(encoding="utf-8")
    assert "docsLoader" in config
    assert "docsSchema" in config
    assert "defineCollection" in config

def test_graph_page_is_static_and_reads_generated_graph_only():
    page = (FRONTEND / "src/pages/graph.astro").read_text(encoding="utf-8")
    assert "public/generated/graph.json" in page
    assert "sources" not in page and "practice" not in page and "queries/local" not in page


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

def test_prepare_content_rejects_confirmation_precondition_drift(tmp_path: Path):
    root = tmp_path / "repo"; frontend = tmp_path / "frontend"; frontend.mkdir()
    script = frontend / "prepare-content.mjs"; script.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(Path(__file__).parents[1] / "frontend/scripts/prepare-content.mjs", script)
    body = root / "wiki" / "item.md"; body.parent.mkdir(parents=True); body.write_text("# Item\n", encoding="utf-8")
    from tools.release_confirmation import write_event
    (root / "release" / "public-confirmations").mkdir(parents=True)
    event = {"schema_version":"public-release-confirmation/v1", "event_id":"event-one", "operation_id":"op-one", "target_ref":{"vault_id":"public","object_type":"wiki","object_id":"item"}, "target_vault":"public", "actor_type":"human", "actor_id":"alice", "decision":"approve", "release_input_sha256":"sha256:old", "reviewed_content_sha256":"sha256:old", "reviewed_evidence_sha256":"sha256:evidence", "leak_gate_report_sha256":"sha256:leak", "leak_gate_report_scope":"input-tree", "reason":"Reviewed public release", "confirmation_nonce":"nonce-one"}
    written = write_event(root, event)
    manifest = {"schema_version":"public-projection/v1","projection":"public","items":[{"id":"item","vault_id":"public","public_publishable":True,"public_release":True,"status":"published","effective_confidentiality":"public","body_path":"wiki/item.md","public_confirmation_path":"release/public-confirmations/event-one.json","public_confirmation_sha256":written["event_sha256"],"release_input_sha256":"sha256:new","content_sha256":"sha256:old","evidence_sha256":"sha256:evidence"}]}
    (root / "queries" / "public").mkdir(parents=True); (root / "queries" / "public" / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    result = subprocess.run(["node", str(script)], cwd=frontend, env={**os.environ, "MYKNOWLEDGE_ROOT":str(root), "MYKNOWLEDGE_CONTENT_MODE":"projection"}, capture_output=True, text=True)
    assert result.returncode != 0 and "confirmation_precondition_mismatch" in result.stderr


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
        body = (wiki / f"{ident}.md").read_bytes()
        content_hash = "sha256:" + hashlib.sha256(body).hexdigest()
        event = {"schema_version":"public-release-confirmation/v1", "event_id":f"event-{ident}", "operation_id":f"op-{ident}", "target_ref":{"vault_id":"public","object_type":"wiki","object_id":ident}, "target_vault":"public", "actor_type":"human", "actor_id":"alice", "decision":"approve", "release_input_sha256":"sha256:input", "reviewed_content_sha256":content_hash, "reviewed_evidence_sha256":"sha256:evidence", "leak_gate_report_sha256":"sha256:leak", "leak_gate_report_scope":"input-tree", "reason":"Reviewed public release", "confirmation_nonce":f"nonce-{ident}"}
        written = write_event(root, event)
        items.append({"id":ident,"vault_id":"public","public_publishable":True,"public_release":True,"status":"published","effective_confidentiality":"public","body_path":f"wiki/{ident}.md","public_confirmation_path":f"release/public-confirmations/event-{ident}.json","public_confirmation_sha256":written["event_sha256"],"release_input_sha256":"sha256:input","content_sha256":content_hash,"evidence_sha256":"sha256:evidence","title":title,"route":ident,"links":links})
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


def test_leak_gate_reports_input_scope_and_rejects_practice(tmp_path: Path):
    script = Path(__file__).parents[1] / "frontend/scripts/leak-gate.mjs"
    target = tmp_path / "practice" / "questions"; target.mkdir(parents=True)
    (target / "q.json").write_text('{"answer":"secret"}', encoding="utf-8")
    result = subprocess.run(["node", str(script), "--scope", "input-tree", str(tmp_path)], capture_output=True, text=True, check=False)
    assert result.returncode != 0
    assert json.loads(result.stderr)["schema_version"] == "public-input-leak-gate/v1"

def test_leak_gate_rejects_question_payload_even_under_public_path(tmp_path: Path):
    target = tmp_path / "wiki"; target.mkdir(parents=True)
    (target / "leaked.md").write_text('{"schema_version":"question/v1","answer":"secret interview answer"}', encoding="utf-8")
    result = subprocess.run(["node", str(Path(__file__).parents[1] / "frontend/scripts/leak-gate.mjs"), "--scope", "input-tree", str(tmp_path)], capture_output=True, text=True, check=False)
    assert result.returncode == 2
    assert "leaked.md" in json.loads(result.stderr)["findings"][0]

def test_leak_gate_rejects_active_html_and_mermaid_callbacks(tmp_path: Path):
    target = tmp_path / "wiki"; target.mkdir()
    (target / "unsafe.md").write_text("<iframe src=\"https://evil.example\"></iframe>\n", encoding="utf-8")
    result = subprocess.run(["node", str(Path(__file__).parents[1] / "frontend/scripts/leak-gate.mjs"), "--scope", "input-tree", str(target)], capture_output=True, text=True, check=False)
    assert result.returncode == 2
    (target / "unsafe.md").write_text("```mermaid\ngraph TD\nclick A href https://evil.example\n```\n", encoding="utf-8")
    result = subprocess.run(["node", str(Path(__file__).parents[1] / "frontend/scripts/leak-gate.mjs"), "--scope", "input-tree", str(target)], capture_output=True, text=True, check=False)
    assert result.returncode == 2


def test_validate_build_rejects_pagefind_count_mismatch(tmp_path: Path):
    target = tmp_path / "dist"; (target / "pagefind").mkdir(parents=True)
    (target / "index.html").write_text("<html></html>", encoding="utf-8")
    (target / "pagefind" / "pagefind-entry.json").write_text(json.dumps({"languages": {"zh-cn": {"page_count": 2}}}), encoding="utf-8")
    (tmp_path / "public" / "generated").mkdir(parents=True)
    (tmp_path / "public" / "generated" / "catalog.json").write_text(json.dumps({"items": []}), encoding="utf-8")
    (tmp_path / "public" / "generated" / "graph.json").write_text(json.dumps({"nodes": [], "edges": []}), encoding="utf-8")
    script = Path(__file__).parents[1] / "frontend/scripts/validate-build.mjs"
    result = subprocess.run(["node", str(script), str(target)], cwd=tmp_path, capture_output=True, text=True, check=False)
    assert result.returncode != 0 and "pagefind_html_count_mismatch" in result.stderr


def test_validate_build_requires_exact_sitemap_catalog_closure(tmp_path: Path):
    target = tmp_path / "dist"; target.mkdir()
    (target / "index.html").write_text("<html></html>", encoding="utf-8")
    (target / "sitemap.xml").write_text("<urlset><url><loc>/</loc></url><url><loc>/graph/</loc></url><url><loc>/one/</loc></url><url><loc>/private/</loc></url></urlset>", encoding="utf-8")
    generated = tmp_path / "public" / "generated"; generated.mkdir(parents=True)
    (generated / "catalog.json").write_text(json.dumps({"items": [{"id": "one", "route": "one"}]}), encoding="utf-8")
    (generated / "graph.json").write_text(json.dumps({"nodes": [{"id": "one"}], "edges": []}), encoding="utf-8")
    script = Path(__file__).parents[1] / "frontend/scripts/validate-build.mjs"
    result = subprocess.run(["node", str(script), str(target)], cwd=tmp_path, capture_output=True, text=True, check=False)
    assert result.returncode != 0 and "sitemap_catalog_not_closed" in result.stderr
    (target / "sitemap.xml").write_text("<urlset><url><loc>/</loc></url><url><loc>/graph/</loc></url><url><loc>/one/</loc></url></urlset>", encoding="utf-8")
    result = subprocess.run(["node", str(script), str(target)], cwd=tmp_path, capture_output=True, text=True, check=False)
    assert result.returncode == 0
