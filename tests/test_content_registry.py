"""``tools.content_registry`` 路由契约：只路由、fail-closed、统一信封。"""

from __future__ import annotations

import json
from pathlib import Path

from tools.content_registry import ContentCapability, ContentRegistry


def _seed_public_wiki(root: Path) -> None:
    """写一份最小可用的 public projection（allowlisted item + 正文）。"""
    (root / "content" / "wiki").mkdir(parents=True, exist_ok=True)
    (root / "content" / "wiki" / "one.md").write_text("# One\n本文", encoding="utf-8")
    manifest_dir = root / "var" / "queries" / "public"
    manifest_dir.mkdir(parents=True, exist_ok=True)
    (manifest_dir / "manifest.json").write_text(
        json.dumps(
            {
                "schema_version": "public-projection/v1",
                "projection": "public",
                "items": [
                    {
                        "id": "one",
                        "vault_id": "public",
                        "public_publishable": True,
                        "public_release": True,
                        "status": "published",
                        "confidentiality": "public",
                        "body_path": "content/wiki/one.md",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )


def test_registry_routes_known_object_type_read_and_list(tmp_path: Path):
    _seed_public_wiki(tmp_path)
    registry = ContentRegistry(tmp_path)
    assert registry.object_types() == frozenset({"wiki"})

    read = registry.read("wiki", object_id="one")
    assert read["status"] == "ok"
    assert read["schema_version"] == "read-result/v1"
    assert read["body"] == "# One\n本文"
    assert read["object_ref"]["object_type"] == "wiki"

    listing = registry.list("wiki")
    assert listing["status"] == "ok"
    assert {item["object_id"] for item in listing["items"]} == {"one"}


def test_registry_read_miss_is_blocked_object_not_found(tmp_path: Path):
    _seed_public_wiki(tmp_path)
    result = ContentRegistry(tmp_path).read("wiki", object_id="missing")
    assert result["status"] == "blocked"
    assert result["error_code"] == "object_not_found"


def test_registry_fail_closes_on_unknown_object_type(tmp_path: Path):
    registry = ContentRegistry(tmp_path)
    read = registry.read("skill", object_id="x")
    assert read["status"] == "blocked"
    assert read["error_code"] == "object_type_not_found"
    assert read["object_type"] == "skill"

    listing = registry.list("skill")
    assert listing["status"] == "blocked"
    assert listing["error_code"] == "object_type_not_found"
    assert registry.capability("skill") is None


def test_registry_only_routes_injected_capabilities(tmp_path: Path):
    """能力可注入：注册表只查表分发，不含领域逻辑。"""
    calls: list[tuple[str, dict]] = []

    def fake_read(root: Path, **kwargs) -> dict:
        calls.append(("read", kwargs))
        return {"schema_version": "read-result/v1", "status": "ok", "routed": True}

    def fake_list(root: Path, **kwargs) -> dict:
        return {"schema_version": "object-list/v1", "status": "ok", "items": []}

    registry = ContentRegistry(
        tmp_path,
        capabilities=[ContentCapability("note", read=fake_read, list=fake_list)],
    )
    assert registry.object_types() == frozenset({"note"})
    assert registry.read("note", object_id="n1")["routed"] is True
    assert calls == [("read", {"object_id": "n1"})]
    miss = registry.read("wiki", object_id="one")
    assert miss["error_code"] == "object_type_not_found"
