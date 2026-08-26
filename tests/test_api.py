from fastapi.testclient import TestClient
from backend.app import create_app

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
