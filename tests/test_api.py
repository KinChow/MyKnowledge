from fastapi.testclient import TestClient
from backend.app import create_app
from pathlib import Path
import json
import tempfile
import socket
import subprocess
import sys
import time
from urllib.request import urlopen
from backend.server import _loopback_host

ITEMS = [{"vault_id": "public", "object_id": "one", "title": "公开条目", "body": "离线查询", "public_publishable": True, "public_release": True, "status": "published", "effective_confidentiality": "public", "content_sha256": "sha256:one"}, {"vault_id": "private", "object_id": "secret", "title": "私有条目", "body": "内部", "confidentiality": "internal"}]

def test_cli_query_matches_api_query_result(tmp_path: Path):
    manifest = tmp_path / "queries" / "public" / "manifest.json"; body = tmp_path / "wiki" / "one.md"
    manifest.parent.mkdir(parents=True); body.parent.mkdir(parents=True); body.write_text("离线查询", encoding="utf-8")
    manifest.write_text(json.dumps({"schema_version": "public-projection/v1", "projection": "public", "items": [{**ITEMS[0], "id": "one", "body_path": "wiki/one.md"}]}), encoding="utf-8")
    client = TestClient(create_app(root=tmp_path))
    api_result = client.get("/api/query", params={"q": "离线", "scope": "public"}).json()
    cli = subprocess.run([sys.executable, "-m", "tools.cli", "query", "离线", "--root", str(tmp_path)], capture_output=True, text=True, check=False)
    assert cli.returncode == 0
    assert json.loads(cli.stdout) == api_result

def test_cli_read_and_backlinks_use_public_projection(tmp_path: Path):
    wiki = tmp_path / "wiki"; wiki.mkdir()
    (wiki / "one.md").write_text("one", encoding="utf-8")
    (wiki / "two.md").write_text("See [one](/wiki/one).", encoding="utf-8")
    manifest = {"schema_version": "public-projection/v1", "projection": "public", "items": [
        {"id": "one", "vault_id": "public", "public_publishable": True, "public_release": True, "status": "published", "effective_confidentiality": "public", "body_path": "wiki/one.md", "title": "One"},
        {"id": "two", "vault_id": "public", "public_publishable": True, "public_release": True, "status": "published", "effective_confidentiality": "public", "body_path": "wiki/two.md", "title": "Two"},
    ]}
    out = tmp_path / "queries" / "public"; out.mkdir(parents=True); (out / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    read = subprocess.run([sys.executable, "-m", "tools.cli", "read", "one", "--root", str(tmp_path)], capture_output=True, text=True, check=False)
    assert read.returncode == 0 and json.loads(read.stdout)["body"] == "one"
    links = subprocess.run([sys.executable, "-m", "tools.cli", "backlinks", "one", "--root", str(tmp_path)], capture_output=True, text=True, check=False)
    assert links.returncode == 0 and json.loads(links.stdout)["items"] == [{"vault_id": "public", "object_type": "wiki", "object_id": "two"}]

def test_server_runner_rejects_remote_bind():
    import argparse
    assert _loopback_host("127.0.0.1") == "127.0.0.1"
    try:
        _loopback_host("0.0.0.0")
    except argparse.ArgumentTypeError as error:
        assert "remote bind" in str(error)
    else:
        raise AssertionError("remote bind must be rejected")

def test_uvicorn_loopback_runner_serves_health_and_rotates_token():
    with tempfile.TemporaryDirectory() as directory, socket.socket() as probe:
        probe.bind(("127.0.0.1", 0)); port = probe.getsockname()[1]
        probe.close()
        process = subprocess.Popen([sys.executable, "-m", "backend.server", "--root", directory, "--port", str(port)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            deadline = time.time() + 8
            while time.time() < deadline:
                try:
                    with urlopen(f"http://127.0.0.1:{port}/api/health", timeout=0.3) as response:
                        assert response.status == 200
                        assert json.loads(response.read())["status"] == "ok"
                        break
                except OSError:
                    time.sleep(0.05)
            else:
                raise AssertionError("uvicorn did not become ready")
            token_path = Path(directory) / "state" / "capability-token"
            assert token_path.stat().st_mode & 0o777 == 0o600
            with urlopen(f"http://127.0.0.1:{port}/api/query?q=offline&scope=public", timeout=1) as response:
                assert response.status == 200
        finally:
            process.terminate(); process.wait(timeout=5)
            assert not (Path(directory) / "state" / "capability-token").exists()

def test_create_app_loads_public_projection_when_items_are_not_injected():
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        manifest = root / "queries" / "public" / "manifest.json"
        body = root / "wiki" / "one.md"
        manifest.parent.mkdir(parents=True); body.parent.mkdir(parents=True); body.write_text("离线查询", encoding="utf-8")
        manifest.write_text(json.dumps({"schema_version": "public-projection/v1", "projection": "public", "items": [{**ITEMS[0], "id": "one", "body_path": "wiki/one.md"}]}), encoding="utf-8")
        client = TestClient(create_app(root=root))
        result = client.get("/api/query", params={"q": "离线", "scope": "public"})
        assert result.status_code == 200
        assert [item["object_ref"]["object_id"] for item in result.json()["items"]] == ["one"]

def test_get_post_query_equivalent():
    client = TestClient(create_app(items=ITEMS, capability_token="token"))
    get = client.get("/api/query", params={"q": "离线", "scope": "public"})
    post = client.post("/api/retrieve", headers={"X-MyKnowledge-Capability": "token"}, json={"query": "离线", "scope": "public"})
    assert get.status_code == post.status_code == 200
    assert get.json() == post.json()

def test_get_query_accepts_retrieve_projection_flags_without_contract_drift():
    client = TestClient(create_app(items=ITEMS, capability_token="token"))
    get = client.get("/api/query", params={"q": "离线", "scope": "public", "include_sources": "true", "include_archive": "false"})
    post = client.post("/api/retrieve", headers={"X-MyKnowledge-Capability": "token"}, json={"query": "离线", "scope": "public", "include_sources": True, "include_archive": False})
    assert get.status_code == post.status_code == 200
    assert get.json() == post.json()

def test_public_post_requires_capability_but_public_get_remains_anonymous():
    client = TestClient(create_app(items=ITEMS, capability_token="token"))
    assert client.get("/api/query", params={"q": "离线", "scope": "public"}).status_code == 200
    retrieve = client.post("/api/retrieve", json={"query": "离线", "scope": "public"})
    ask = client.post("/api/ask", json={"query": "离线", "scope": "public"})
    assert retrieve.status_code == ask.status_code == 401
    assert retrieve.json()["detail"]["code"] == "capability_token_required"

def test_get_query_rejects_unknown_parameters():
    client = TestClient(create_app(items=ITEMS, capability_token="token"))
    response = client.get("/api/query", params={"q": "离线", "scope": "public", "include_private": "true"})
    assert response.status_code == 400
    assert response.json()["detail"]["code"] == "schema_invalid"

def test_private_scope_requires_capability():
    client = TestClient(create_app(items=ITEMS, capability_token="token"))
    assert client.post("/api/retrieve", json={"query": "内部", "scope": "local"}).status_code == 401
    assert client.post("/api/retrieve", headers={"X-MyKnowledge-Capability": "token"}, json={"query": "内部", "scope": "local"}).status_code == 200
    private = client.post("/api/retrieve", headers={"X-MyKnowledge-Capability": "token"}, json={"query": "内部", "scope": "private"})
    assert private.status_code == 400
    assert private.json()["detail"]["code"] == "vault_ids_required"


def test_capability_audience_is_checked_when_supplied():
    client = TestClient(create_app(items=ITEMS, capability_token="token"))
    headers = {"X-MyKnowledge-Capability": "token", "X-MyKnowledge-Audience": "other-service"}
    response = client.post("/api/retrieve", headers=headers, json={"query": "内部", "scope": "local"})
    assert response.status_code == 403
    assert response.json()["detail"]["code"] == "capability_audience_invalid"


def test_capability_token_expires_by_process_ttl():
    client = TestClient(create_app(items=ITEMS, capability_token="token"))
    client.app.state.capability_token_created_at -= client.app.state.capability_token_ttl_seconds + 1
    response = client.post("/api/retrieve", headers={"X-MyKnowledge-Capability": "token"}, json={"query": "内部", "scope": "local"})
    assert response.status_code == 403
    assert response.json()["detail"]["code"] == "capability_token_expired"

def test_capability_scope_registry_is_enforced():
    client = TestClient(create_app(items=ITEMS, capability_token="token"))
    client.app.state.capability_scopes = {"local-read"}
    response = client.get("/api/vault/check", headers={"X-MyKnowledge-Capability": "token"})
    assert response.status_code == 403
    assert response.json()["detail"]["code"] == "capability_scope_invalid"

def test_ask_is_explicitly_unavailable_offline():
    client = TestClient(create_app(items=ITEMS, capability_token="token"))
    body = client.post("/api/ask", headers={"X-MyKnowledge-Capability": "token"}, json={"query": "离线", "scope": "public"}).json()
    assert body["availability"] == "unavailable"
    assert body["answer"] is None

def test_citation_replay_api_is_read_only_and_capability_scoped():
    from tools.evidence_anchor import EvidenceAnchor
    snapshot = "可回放的证据文本。"
    citation = EvidenceAnchor.anchor(snapshot, snapshot, min_chars=1)
    client = TestClient(create_app(items=ITEMS, capability_token="token"))
    assert client.post("/api/citation/replay", json={"citation": citation, "snapshot": snapshot}).status_code == 401
    response = client.post("/api/citation/replay", params={"scope": "local"}, headers={"X-MyKnowledge-Capability": "token"}, json={"citation": citation, "snapshot": snapshot})
    assert response.status_code == 200
    assert response.json()["state"] == "valid"
    assert client.post("/api/citation/replay", params={"scope": "local"}, headers={"X-MyKnowledge-Capability": "token"}, json={"citation": citation, "snapshot": snapshot, "url": "https://evil.example"}).status_code == 422

def _write_public_manifest(root: Path, items: list[dict]) -> None:
    """Fixture：真实形态 public projection manifest（与 PublicProjectionGenerator 输出同构）。"""
    import json as _json
    out = root / "queries" / "public"
    out.mkdir(parents=True, exist_ok=True)
    (out / "manifest.json").write_text(_json.dumps({"schema_version": "public-projection/v1", "projection": "public", "items": items}), encoding="utf-8")

def _released_item(object_id: str, body: str) -> dict:
    return {"id": object_id, "title": object_id, "route": f"/wiki/{object_id}", "body_path": f"wiki/{object_id}.md", "vault_id": "public", "status": "published", "public_publishable": True, "public_release": True, "effective_confidentiality": "public", "content_sha256": f"sha256:{object_id}", "links": []}

def test_public_read_and_backlinks(tmp_path: Path):
    wiki = tmp_path / "wiki"
    wiki.mkdir(parents=True)
    (wiki / "target.md").write_text("# Target\n正文", encoding="utf-8")
    (wiki / "consumer.md").write_text("See [/wiki/target](/wiki/target)", encoding="utf-8")
    (wiki / "draft.md").write_text("# 未发布草稿\n内部内容", encoding="utf-8")  # 不进 manifest
    _write_public_manifest(tmp_path, [_released_item("target", "# Target"), {**_released_item("consumer", "See target"), "links": ["/wiki/target"]}])
    client = TestClient(create_app(root=tmp_path, capability_token="token"))
    read = client.get("/api/read/public/wiki/target")
    assert read.status_code == 200
    assert read.json()["object_ref"] == {"vault_id": "public", "object_type": "wiki", "object_id": "target"}
    assert "# Target" in read.json()["body"]
    links = client.get("/api/backlinks/public/wiki/target")
    assert links.status_code == 200
    assert links.json()["items"] == [{"vault_id": "public", "object_type": "wiki", "object_id": "consumer"}]
    # 未通过发布门禁的 canonical wiki 不得经 public API 暴露
    assert client.get("/api/read/public/wiki/draft").status_code == 404

def test_read_missing_object_is_structured_404(tmp_path: Path):
    client = TestClient(create_app(root=tmp_path, capability_token="token"))
    response = client.get("/api/read/public/wiki/missing")
    assert response.status_code == 404
    assert response.json()["detail"]["code"] == "object_not_found"

def test_non_public_read_requires_capability_even_when_vault_unavailable(tmp_path: Path):
    client = TestClient(create_app(root=tmp_path, capability_token="token"))
    missing = client.get("/api/read/team/wiki/target", params={"scope": "local"})
    assert missing.status_code == 401
    omitted_scope = client.get("/api/read/team/wiki/target")
    assert omitted_scope.status_code == 401
    authorized = client.get("/api/read/team/wiki/target", params={"scope": "local"}, headers={"X-MyKnowledge-Capability": "token"})
    assert authorized.status_code == 404
    assert authorized.json()["detail"]["code"] == "vault_unavailable"

def test_object_route_rejects_path_traversal_and_unknown_type(tmp_path: Path):
    client = TestClient(create_app(root=tmp_path, capability_token="token"))
    assert client.get("/api/read/public/wiki/%2E%2E").status_code == 422
    assert client.get("/api/read/public/unknown/id").status_code == 404

def test_practice_api_is_private_and_does_not_bypass_validator(tmp_path: Path):
    client = TestClient(create_app(root=tmp_path, capability_token="token"))
    assert client.post("/api/practice/q-one/answer", json="a").status_code == 401
    response = client.post("/api/practice/q-one/answer", params={"scope": "local"}, headers={"X-MyKnowledge-Capability": "token"}, json="a")
    assert response.status_code == 404
    assert response.json()["detail"]["code"] == "question_not_found"

def test_capability_token_rotates_with_secure_permissions(tmp_path: Path):
    first = create_app(root=tmp_path)
    token_path = tmp_path / "state" / "capability-token"
    token_one = token_path.read_text(encoding="utf-8").strip()
    assert first.state.capability_token == token_one
    assert (tmp_path / "state").stat().st_mode & 0o777 == 0o700
    assert token_path.stat().st_mode & 0o777 == 0o600
    second = create_app(root=tmp_path)
    token_two = token_path.read_text(encoding="utf-8").strip()
    assert token_two != token_one
    client = TestClient(second)
    assert client.post("/api/retrieve", headers={"X-MyKnowledge-Capability": token_one}, json={"query": "x", "scope": "local"}).status_code == 403

def test_cross_origin_post_is_rejected_before_capability_check():
    client = TestClient(create_app(items=ITEMS, capability_token="token"))
    response = client.post("/api/retrieve", headers={"Origin": "https://evil.example", "X-MyKnowledge-Capability": "token"}, json={"query": "离线", "scope": "public"})
    assert response.status_code == 403
    assert response.json()["detail"]["code"] == "origin_not_allowed"

def test_non_loopback_host_is_rejected():
    client = TestClient(create_app(items=ITEMS, capability_token="token"))
    response = client.post("/api/retrieve", headers={"Host": "remote.example", "X-MyKnowledge-Capability": "token"}, json={"query": "离线", "scope": "public"})
    assert response.status_code == 403
    assert response.json()["detail"]["code"] == "host_not_allowed"

def test_retrieve_enforces_policy_vault_limit():
    client = TestClient(create_app(items=ITEMS, capability_token="token"))
    response = client.post("/api/retrieve", headers={"X-MyKnowledge-Capability": "token"}, json={"query": "x", "scope": "public", "vault_ids": [f"v-{i}" for i in range(17)]})
    assert response.status_code == 400
    assert response.json()["detail"]["code"] == "query_limit_exceeded"

def test_api_passes_vault_allowlist_into_retriever_before_search():
    class RecordingRetriever:
        def __init__(self): self.calls = []
        def search(self, query, scope="local", top_k=8, vault_ids=None):
            self.calls.append((query, scope, top_k, vault_ids))
            return {"schema_version":"query-result/v1","items":[],"scope":scope,"method":"deterministic-fallback","index_version":"none","generated_from":"","availability":"available","availability_reason":"none","degraded":True,"confidentiality_max":"public","limits":[],"warnings":[]}
    client = TestClient(create_app(items=ITEMS, capability_token="token"))
    retriever = RecordingRetriever(); client.app.state.retriever = retriever
    response = client.post("/api/retrieve", headers={"X-MyKnowledge-Capability":"token"}, json={"query":"x","scope":"private","vault_ids":["private"]})
    assert response.status_code == 200
    assert retriever.calls == [("x", "private", 8, ["private"])]


def test_request_body_limit_is_fail_closed():
    client = TestClient(create_app(items=ITEMS, capability_token="token"))
    response = client.post("/api/retrieve", headers={"Content-Length": str(1_048_577), "X-MyKnowledge-Capability": "token"}, content=b"{}")
    assert response.status_code == 413
    assert response.json()["detail"]["code"] == "request_too_large"


def test_source_and_wiki_preview_apply_require_capability_and_confirmation(tmp_path: Path):
    client = TestClient(create_app(root=tmp_path, capability_token="token"))
    body = {"files": {"wiki/api.md": "# API\n"}, "vault_id": "public"}
    assert client.post("/api/wiki/preview", json=body).status_code == 401
    preview = client.post("/api/wiki/preview", headers={"X-MyKnowledge-Capability": "token"}, json=body)
    assert preview.status_code == 200
    operation_id = preview.json()["operation_id"]
    blocked = client.post(f"/api/operation/{operation_id}/apply", headers={"X-MyKnowledge-Capability": "token"}, json={})
    assert blocked.json()["state"] == "awaiting_confirmation"
    applied = client.post(f"/api/operation/{operation_id}/apply", headers={"X-MyKnowledge-Capability": "token"}, json={"confirmed": True})
    assert applied.json()["state"] == "applied"
    assert (tmp_path / "wiki" / "api.md").read_text() == "# API\n"


def test_vault_check_requires_capability(tmp_path: Path):
    client = TestClient(create_app(root=tmp_path, capability_token="token"))
    assert client.get("/api/vault/check").status_code == 401
    result = client.get("/api/vault/check", headers={"X-MyKnowledge-Capability": "token"})
    assert result.status_code == 200
    assert result.json()["schema_version"] == "vault-check/v1"


def test_validate_endpoint_requires_capability_and_reuses_wiki_validator(tmp_path: Path):
    wiki = tmp_path / "wiki" / "target.md"; wiki.parent.mkdir(parents=True); wiki.write_text("---\nschema_version: wiki/v1\nid: target\ntitle: Target\ndomain: tools\nkind: reference\nstatus: planned\n---\n# Target\n", encoding="utf-8")
    client = TestClient(create_app(root=tmp_path, capability_token="token"))
    assert client.post("/api/validate/public/wiki/target").status_code == 401
    response = client.post("/api/validate/public/wiki/target", headers={"X-MyKnowledge-Capability": "token"})
    assert response.status_code == 200
    assert response.json()["schema_version"] == "validation-result/v1"
    assert response.json()["object_ref"]["vault_id"] == "public"

def test_validate_endpoint_rejects_wrong_capability_audience(tmp_path: Path):
    wiki = tmp_path / "wiki" / "target.md"; wiki.parent.mkdir(parents=True); wiki.write_text("---\nschema_version: wiki/v1\nid: target\ntitle: Target\nkind: reference\nstatus: planned\n---\n# Target\n", encoding="utf-8")
    client = TestClient(create_app(root=tmp_path, capability_token="token"))
    response = client.post("/api/validate/public/wiki/target", headers={"X-MyKnowledge-Capability": "token", "X-MyKnowledge-Audience": "wrong"})
    assert response.status_code == 403
    assert response.json()["detail"]["code"] == "capability_audience_invalid"


def test_private_vault_read_and_backlinks_are_owner_scoped(tmp_path: Path):
    public = tmp_path / "public"; private = tmp_path / "private"
    public.mkdir(); private.mkdir()
    import subprocess
    for vault in (public, private): subprocess.run(["git", "init", "-q", str(vault)], check=True)
    (public / "wiki").mkdir(); (public / "wiki" / "same.md").write_text("public", encoding="utf-8")
    (private / "wiki").mkdir(); (private / "wiki" / "same.md").write_text("private", encoding="utf-8")
    (private / "wiki" / "consumer.md").write_text("See same.md", encoding="utf-8")
    config = public / "config"; config.mkdir()
    (config / "vaults.local.yaml").write_text(f"schema_version: 1\nlayout: superproject\nworkspace_root: {tmp_path}\npublic_vault_id: public\nvaults:\n  - {{id: public, path: public}}\n  - {{id: private, path: private, confidentiality: internal}}\n", encoding="utf-8")
    _write_public_manifest(public, [_released_item("same", "public")])
    client = TestClient(create_app(root=public, capability_token="token"))
    response = client.get("/api/read/private/wiki/same", params={"scope": "private"}, headers={"X-MyKnowledge-Capability": "token"})
    assert response.status_code == 200
    assert response.json()["body"] == "private"
    assert response.json()["path"] == "wiki/same.md"
    links = client.get("/api/backlinks/private/wiki/same", params={"scope": "private"}, headers={"X-MyKnowledge-Capability": "token"})
    assert links.status_code == 200
    assert links.json()["items"] == [{"vault_id": "private", "object_type": "wiki", "object_id": "consumer"}]
    public_read = client.get("/api/read/public/wiki/same")
    assert public_read.json()["body"] == "public"


def test_practice_api_exposes_deterministic_mode_and_llm_unavailable(tmp_path: Path):
    from tools.question import QuestionStore
    report = {"valid": True, "object_ref": {"object_type": "wiki", "object_id": "wiki-one"}, "metadata": {"evidence": [{"claim_id": "claim-one"}]}, "derived": {"evidence_state": "supported"}, "hashes": {"content_sha256": "sha256:c", "evidence_sha256": "sha256:e"}}
    spec = {"id": "q-one", "type": "short_answer", "wiki_id": "wiki-one", "claim_id": "claim-one", "prompt": "Explain", "rubric": ["核心"]}
    QuestionStore(tmp_path).create(spec, wiki_report=report)
    client = TestClient(create_app(root=tmp_path, capability_token="token"))
    headers = {"X-MyKnowledge-Capability": "token"}
    deterministic = client.post("/api/practice/q-one/answer", params={"scope": "local", "scoring_mode": "deterministic"}, headers=headers, json="包含核心")
    assert deterministic.status_code == 200 and deterministic.json()["scoring_provider"] == "deterministic_rubric"
    unavailable = client.post("/api/practice/q-one/answer", params={"scope": "local", "scoring_mode": "llm"}, headers=headers, json="x")
    assert unavailable.status_code == 200 and unavailable.json()["reason"] == "provider_unavailable"


def test_practice_review_api_persists_fsrs_card_state(tmp_path: Path):
    from tools.question import QuestionStore
    report = {"valid": True, "object_ref": {"object_type": "wiki", "object_id": "wiki-one"}, "metadata": {"evidence": [{"claim_id": "claim-one"}]}, "derived": {"evidence_state": "supported"}, "hashes": {"content_sha256": "sha256:c", "evidence_sha256": "sha256:e"}}
    spec = {"id": "q-review", "type": "short_answer", "wiki_id": "wiki-one", "claim_id": "claim-one", "prompt": "Explain", "rubric": ["核心"]}
    QuestionStore(tmp_path).create(spec, wiki_report=report)
    client = TestClient(create_app(root=tmp_path, capability_token="token"))
    response = client.post("/api/practice/q-review/review", params={"scope": "local", "rating": 3}, headers={"X-MyKnowledge-Capability": "token"})
    assert response.status_code == 200
    body = response.json()
    assert body["schema_version"] == "practice-review/v1"
    if body.get("state") == "scheduled":
        assert body["review_state_schema"] == "fsrs-card/v1"
        assert QuestionStore(tmp_path).load("q-review")["review_state"]["card_id"] == body["card"]["card_id"]
