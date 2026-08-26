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
