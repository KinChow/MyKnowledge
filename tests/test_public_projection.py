import json
from pathlib import Path

from tools.public_projection import PublicProjectionGenerator
from tools.release_confirmation import write_event
from tools.release_input import compute as compute_release_input


class FakeValidator:
    def __init__(self, reports):
        self.reports = reports

    def validate(self, path: Path):
        return self.reports[path.stem]


def _lineage_record(root: Path, operation_id: str) -> None:
    """§6.8：确认事件必须指向存在的 owner durable operation record 才能放行。"""
    directory = root / "audit" / "operations"
    directory.mkdir(parents=True, exist_ok=True)
    (directory / f"{operation_id}.json").write_text(
        json.dumps({"operation_id": operation_id, "state": "applied"}),
        encoding="utf-8",
    )


def _event(root: Path, object_id: str, content: str, evidence: str, validator):
    """按生产口径构造确认事件：release_input_sha256 用同一个计算入口算出来。

    手写一个假 hash 会让用例绕过 required_match_fields 的比对——这正是实测里
    "人工确认只绑定正文与证据"能长期存活的原因。
    """
    operation_id = f"op-{object_id}"
    _lineage_record(root, operation_id)
    candidate, error = PublicProjectionGenerator(root, validator).release_candidate(
        object_id
    )
    assert candidate is not None, error
    digest, _material = compute_release_input(
        root,
        item=candidate["item"],
        content_sha256=content,
        operation_id=operation_id,
    )
    return {
        "schema_version": "public-release-confirmation/v1",
        "event_id": f"event-{object_id}",
        "operation_id": operation_id,
        "target_ref": {
            "vault_id": "public",
            "object_type": "wiki",
            "object_id": object_id,
        },
        "target_vault": "public",
        "actor_type": "human",
        "actor_id": "alice",
        "decision": "approve",
        "release_input_sha256": digest,
        "reviewed_content_sha256": content,
        "reviewed_evidence_sha256": evidence,
        "leak_gate_report_sha256": "sha256:leak",
        "leak_gate_report_scope": "input-tree",
        "reason": "Reviewed public knowledge release",
        "confirmation_nonce": f"nonce-{object_id}",
    }


def test_public_projection_generator_requires_matching_confirmation(tmp_path: Path):
    wiki = tmp_path / "content" / "wiki"
    wiki.mkdir(parents=True, exist_ok=True)
    (wiki / "one.md").write_text("# One\n", encoding="utf-8")
    (wiki / "two.md").write_text("# Two\n", encoding="utf-8")
    reports = {
        "one": {
            "valid": True,
            "object_ref": {
                "vault_id": "public",
                "object_type": "wiki",
                "object_id": "one",
            },
            "derived": {"public_publishable": True, "public_release_ready": True},
            "hashes": {"content_sha256": "sha256:one", "evidence_sha256": "sha256:e1"},
        },
        "two": {
            "valid": True,
            "object_ref": {
                "vault_id": "public",
                "object_type": "wiki",
                "object_id": "two",
            },
            "derived": {"public_publishable": True, "public_release_ready": True},
            "hashes": {"content_sha256": "sha256:two", "evidence_sha256": "sha256:e2"},
        },
    }
    (tmp_path / "release" / "public-confirmations").mkdir(parents=True)
    validator = FakeValidator(reports)
    write_event(tmp_path, _event(tmp_path, "one", "sha256:one", "sha256:e1", validator))
    result = PublicProjectionGenerator(tmp_path, validator).generate()
    assert result["item_count"] == 1
    assert {
        item["id"]
        for item in json.loads(
            (tmp_path / "var" / "queries" / "public" / "manifest.json").read_text()
        )["items"]
    } == {"one"}
    assert {item["object_id"] for item in result["skipped"]} == {"two"}


def test_public_projection_generator_does_not_emit_private_or_unconfirmed_items(
    tmp_path: Path,
):
    wiki = tmp_path / "content" / "wiki"
    wiki.mkdir(parents=True, exist_ok=True)
    (wiki / "private.md").write_text("secret", encoding="utf-8")
    reports = {
        "private": {
            "valid": True,
            "object_ref": {
                "vault_id": "private",
                "object_type": "wiki",
                "object_id": "private",
            },
            "derived": {"public_publishable": False, "public_release_ready": False},
            "hashes": {},
        }
    }
    result = PublicProjectionGenerator(tmp_path, FakeValidator(reports)).generate()
    assert result["item_count"] == 0
    assert result["skipped"] == [
        {"object_id": "private", "reason": "not_public_publishable"}
    ]


def test_public_projection_ignores_adjacent_private_checkout(tmp_path: Path):
    public = tmp_path / "public"
    private = tmp_path / "vaults" / "team-internal"
    (public / "content" / "wiki").mkdir(parents=True)
    (private / "content" / "wiki").mkdir(parents=True)
    (public / "content" / "wiki" / "same.md").write_text(
        "public fact", encoding="utf-8"
    )
    (private / "content" / "wiki" / "same.md").write_text(
        "PRIVATE SECRET", encoding="utf-8"
    )
    reports = {
        "same": {
            "valid": True,
            "object_ref": {
                "vault_id": "public",
                "object_type": "wiki",
                "object_id": "same",
            },
            "derived": {"public_publishable": True, "public_release_ready": True},
            "hashes": {
                "content_sha256": "sha256:public",
                "evidence_sha256": "sha256:e",
            },
        }
    }
    (public / "release" / "public-confirmations").mkdir(parents=True)
    validator = FakeValidator(reports)
    write_event(public, _event(public, "same", "sha256:public", "sha256:e", validator))
    result = PublicProjectionGenerator(public, validator).generate()
    manifest = json.loads(
        (public / "var" / "queries" / "public" / "manifest.json").read_text(
            encoding="utf-8"
        )
    )
    assert result["item_count"] == 1
    assert manifest["items"][0]["body_path"] == "content/wiki/same.md"
    assert "PRIVATE SECRET" not in json.dumps(manifest)
    assert not any("team-internal" in json.dumps(item) for item in manifest["items"])


def test_manifest_items_cover_every_declared_required_field(tmp_path: Path):
    """契约测试：manifest item 必须覆盖 schemas.yaml 声明的 required_item_fields。

    实测（2026-09-01）：此前 item 只写 15 个键，声明的 28 个里缺 11 个（含 §6.7
    要求对读者可见的 strength）。声明与实现之间此前没有任何机制保证一致——
    `config/schemas.yaml` 全库零消费方。
    """
    from tools.schemas import schemas_value

    repo = Path(__file__).resolve().parents[1]
    wiki = tmp_path / "content" / "wiki"
    wiki.mkdir(parents=True, exist_ok=True)
    (wiki / "one.md").write_text(
        "---\ntitle: One\ndomain: tools\nkind: knowledge\npublication_scope: public\n---\n# One\n",
        encoding="utf-8",
    )
    (tmp_path / "config").mkdir(parents=True, exist_ok=True)
    for name in ("policy.yaml", "schemas.yaml"):
        (tmp_path / "config" / name).write_text(
            (repo / "config" / name).read_text(encoding="utf-8"), encoding="utf-8"
        )
    reports = {
        "one": {
            "valid": True,
            "object_ref": {
                "vault_id": "public",
                "object_type": "wiki",
                "object_id": "one",
            },
            "derived": {
                "public_publishable": True,
                "public_release_ready": True,
                "strength": "verified",
                "validation_state": "pass",
                "evidence_state": "supported",
                "effective_confidentiality": "public",
            },
            "hashes": {"content_sha256": "sha256:one", "evidence_sha256": "sha256:e1"},
        }
    }
    (tmp_path / "release" / "public-confirmations").mkdir(parents=True)
    validator = FakeValidator(reports)
    write_event(tmp_path, _event(tmp_path, "one", "sha256:one", "sha256:e1", validator))
    result = PublicProjectionGenerator(tmp_path, validator).generate()
    assert result["item_count"] == 1, result
    item = json.loads(
        (tmp_path / "var" / "queries" / "public" / "manifest.json").read_text(
            encoding="utf-8"
        )
    )["items"][0]
    declared = schemas_value(
        tmp_path, "public_projection", "required_item_fields", default=[]
    )
    assert declared, "schemas.yaml 必须声明 required_item_fields"
    assert not set(declared) - set(item), sorted(set(declared) - set(item))
    assert item["strength"] == "verified"


def test_release_input_binds_route_and_body_path_not_only_body(tmp_path: Path):
    """人工确认必须绑定发布输入：只改 route 也要让 public_release 回落。

    实测动机：`release_input_sha256` 此前从未计算（现存事件里它与
    reviewed_content_sha256 逐字相同），因此 route/body_path/attachments/links
    在批准之后改动，页面仍以"已批准"发布。
    """
    from tools.release_input import compute as _compute

    wiki = tmp_path / "content" / "wiki"
    wiki.mkdir(parents=True, exist_ok=True)
    (wiki / "one.md").write_text("# One\n", encoding="utf-8")
    reports = {
        "one": {
            "valid": True,
            "object_ref": {
                "vault_id": "public",
                "object_type": "wiki",
                "object_id": "one",
            },
            "derived": {"public_publishable": True, "public_release_ready": True},
            "hashes": {"content_sha256": "sha256:one", "evidence_sha256": "sha256:e1"},
        }
    }
    validator = FakeValidator(reports)
    candidate, _ = PublicProjectionGenerator(tmp_path, validator).release_candidate(
        "one"
    )
    baseline, _ = _compute(
        tmp_path,
        item=candidate["item"],
        content_sha256="sha256:one",
        operation_id="op-one",
    )
    for field, value in (
        ("route", "/wiki/one-renamed"),
        ("body_path", "content/wiki/moved/one.md"),
        ("links", ["two"]),
        ("attachments", [{"path": "a.png", "sha256": "sha256:a"}]),
    ):
        changed, _ = _compute(
            tmp_path,
            item={**candidate["item"], field: value},
            content_sha256="sha256:one",
            operation_id="op-one",
        )
        assert changed != baseline, field
