"""Every local operation is protected even when the caller claims public scope."""

import asyncio

import pytest
from fastapi.testclient import TestClient

from backend.app import create_app
from tools.access_policy import CAPABILITY_SCOPES, capability_for
from tools.mcp_server import create_server
from tools.skill_runtime import ALLOWED_ACTIONS

PRACTICE = [
    ("GET", "/api/practice/questions"),
    ("GET", "/api/practice/errors"),
    ("GET", "/api/practice/queue"),
    ("GET", "/api/practice/sessions/missing"),
    ("POST", "/api/practice/sessions"),
    ("POST", "/api/practice/sessions/missing/progress?current_index=0"),
    ("POST", "/api/practice/missing/answer"),
    ("POST", "/api/practice/missing/review?rating=3"),
    ("POST", "/api/practice/missing/quality"),
    ("POST", "/api/practice/missing/enable"),
    ("POST", "/api/practice/missing/disable"),
    ("DELETE", "/api/practice/missing"),
    ("GET", "/api/list/public/question"),
    ("GET", "/api/list/public/source"),
]


@pytest.mark.parametrize("method,url", PRACTICE)
@pytest.mark.parametrize("scope", ["public", "local"])
def test_local_routes_cannot_be_made_anonymous(tmp_path, method, url, scope):
    client = TestClient(create_app(root=tmp_path, items=[], capability_token="secret"))
    url += ("&" if "?" in url else "?") + "scope=" + scope
    response = client.request(
        method,
        url,
        json="a" if url.startswith("/api/practice/missing/answer") else None,
    )
    assert response.status_code == 401, response.text
    response = client.request(
        method,
        url,
        json="a" if "/answer?" in url else None,
        headers={
            "X-MyKnowledge-Capability": "secret",
            "X-MyKnowledge-Audience": "wrong",
        },
    )
    assert response.status_code == 403


@pytest.mark.parametrize("method,url", PRACTICE)
def test_route_requires_its_capability_scope(tmp_path, method, url):
    app = create_app(root=tmp_path, items=[], capability_token="secret")
    app.state.capability_scopes = set()
    response = TestClient(app).request(
        method,
        url,
        json="a" if url.endswith("/answer") else None,
        headers={"X-MyKnowledge-Capability": "secret"},
    )
    assert response.status_code == 403, response.text
    assert response.json()["detail"]["code"] == "capability_scope_invalid"


@pytest.mark.parametrize(
    "origin",
    [
        "http://localhost.evil.example",
        "http://127.0.0.1.evil.example",
        "null",
        "https://kinchow.github.io",
        "http://localhost:9999",
        "http://user@localhost:4321",
    ],
)
def test_origin_exact_allowlist(tmp_path, origin):
    client = TestClient(create_app(root=tmp_path, items=[], capability_token="secret"))
    r = client.post(
        "/api/practice/sessions?scope=public",
        headers={"Origin": origin, "X-MyKnowledge-Capability": "secret"},
    )
    assert r.status_code == 403
    assert r.json()["detail"]["code"] == "origin_not_allowed"


@pytest.mark.parametrize("configured", [False, True])
def test_mcp_all_protected_actions_share_policy(tmp_path, monkeypatch, configured):
    monkeypatch.delenv("MYKNOWLEDGE_MCP_CAPABILITY_TOKEN", raising=False)

    async def run():
        server = create_server(
            tmp_path, capability_token="secret" if configured else None
        )
        for action in sorted(ALLOWED_ACTIONS):
            payload = {"object_type": "question"} if action == "list" else {}
            if capability_for(action, payload) is None:
                continue
            result = await server.call_tool(
                "myknowledge_dispatch", {"action": action, "payload": payload}
            )
            assert (
                result.structured_content["error_code"] == "capability_token_required"
            ), action

    asyncio.run(run())
    assert capability_for("future_mutation") == "write"
    assert capability_for("question_delete") == capability_for("delete") == "write"
    assert set(CAPABILITY_SCOPES) == {
        "write",
        "local-read",
        "private-read",
        "vault-check",
    }


@pytest.mark.parametrize("method,url", PRACTICE)
def test_correct_token_reaches_domain_not_auth_failure(tmp_path, method, url):
    client = TestClient(create_app(root=tmp_path, items=[], capability_token="secret"))
    response = client.request(
        method,
        url,
        json="a" if "/answer" in url else None,
        headers={"X-MyKnowledge-Capability": "secret"},
    )
    assert response.status_code not in {401, 403, 500}, response.text


@pytest.mark.parametrize(
    "method,url,body",
    [
        ("DELETE", "/api/object/public/wiki/one", None),
        ("POST", "/api/object/public/wiki/one/purge", None),
        ("POST", "/api/source/update", {}),
        ("POST", "/api/practice/import", {}),
        ("GET", "/api/read/public/source/one", None),
    ],
)
def test_management_routes_never_anonymous(tmp_path, method, url, body):
    client = TestClient(create_app(root=tmp_path, items=[], capability_token="secret"))
    assert client.request(method, url, json=body).status_code == 401
