from fastapi.testclient import TestClient
from backend.app import create_app
from pathlib import Path

ITEMS = [{"vault_id": "public", "object_id": "one", "title": "公开条目", "body": "离线查询", "public_publishable": True, "content_sha256": "sha256:one"}, {"vault_id": "private", "object_id": "secret", "title": "私有条目", "body": "内部", "confidentiality": "internal"}]

def test_get_post_query_equivalent():
    client = TestClient(create_app(items=ITEMS, capability_token="token"))
    get = client.get("/api/query", params={"q": "离线", "scope": "public"})
    post = client.post("/api/retrieve", json={"query": "离线", "scope": "public"})
    assert get.status_code == post.status_code == 200
    assert get.json() == post.json()

def test_private_scope_requires_capability():
    client = TestClient(create_app(items=ITEMS, capability_token="token"))
    assert client.post("/api/retrieve", json={"query": "内部", "scope": "local"}).status_code == 401
    assert client.post("/api/retrieve", headers={"X-MyKnowledge-Capability": "token"}, json={"query": "内部", "scope": "local"}).status_code == 200


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

def test_ask_is_explicitly_unavailable_offline():
    client = TestClient(create_app(items=ITEMS, capability_token="token"))
    body = client.post("/api/ask", json={"query": "离线", "scope": "public"}).json()
    assert body["availability"] == "unavailable"
    assert body["answer"] is None

def test_public_read_and_backlinks(tmp_path: Path):
    wiki = tmp_path / "wiki" / "guide"
    wiki.mkdir(parents=True)
    (wiki / "target.md").write_text("# Target\n正文", encoding="utf-8")
    (wiki / "consumer.md").write_text("See [target](target.md)", encoding="utf-8")
    client = TestClient(create_app(root=tmp_path, capability_token="token"))
    read = client.get("/api/read/public/wiki/target")
    assert read.status_code == 200
    assert read.json()["object_ref"] == {"vault_id": "public", "object_type": "wiki", "object_id": "target"}
    assert "# Target" in read.json()["body"]
    links = client.get("/api/backlinks/public/wiki/target")
    assert links.status_code == 200
    assert links.json()["items"] == [{"vault_id": "public", "object_type": "wiki", "object_id": "consumer"}]

def test_read_missing_object_is_structured_404(tmp_path: Path):
    client = TestClient(create_app(root=tmp_path, capability_token="token"))
    response = client.get("/api/read/public/wiki/missing")
    assert response.status_code == 404
    assert response.json()["detail"]["code"] == "object_not_found"

def test_non_public_read_requires_capability_even_when_vault_unavailable(tmp_path: Path):
    client = TestClient(create_app(root=tmp_path, capability_token="token"))
    missing = client.get("/api/read/team/wiki/target", params={"scope": "local"})
    assert missing.status_code == 401
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
    response = client.post("/api/retrieve", json={"query": "x", "scope": "public", "vault_ids": [f"v-{i}" for i in range(17)]})
    assert response.status_code == 400
    assert response.json()["detail"]["code"] == "query_limit_exceeded"


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
    report = {"valid": True, "object_ref": {"object_type": "wiki"}, "derived": {"evidence_state": "supported"}, "hashes": {"content_sha256": "sha256:c", "evidence_sha256": "sha256:e"}}
    spec = {"id": "q-one", "type": "short_answer", "wiki_id": "wiki-one", "claim_id": "claim-one", "prompt": "Explain", "rubric": ["核心"]}
    QuestionStore(tmp_path).create(spec, wiki_report=report)
    client = TestClient(create_app(root=tmp_path, capability_token="token"))
    headers = {"X-MyKnowledge-Capability": "token"}
    deterministic = client.post("/api/practice/q-one/answer", params={"scope": "local", "scoring_mode": "deterministic"}, headers=headers, json="包含核心")
    assert deterministic.status_code == 200 and deterministic.json()["scoring_provider"] == "deterministic_rubric"
    unavailable = client.post("/api/practice/q-one/answer", params={"scope": "local", "scoring_mode": "llm"}, headers=headers, json="x")
    assert unavailable.status_code == 200 and unavailable.json()["reason"] == "provider_unavailable"
