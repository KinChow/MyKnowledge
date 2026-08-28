import json
from pathlib import Path

from tools.public_projection import PublicProjectionGenerator
from tools.release_confirmation import write_event


class FakeValidator:
    def __init__(self, reports):
        self.reports = reports

    def validate(self, path: Path):
        return self.reports[path.stem]


def _event(object_id: str, content: str, evidence: str):
    return {
        "schema_version": "public-release-confirmation/v1",
        "event_id": f"event-{object_id}",
        "operation_id": f"op-{object_id}",
        "target_ref": {
            "vault_id": "public",
            "object_type": "wiki",
            "object_id": object_id,
        },
        "target_vault": "public",
        "actor_type": "human",
        "actor_id": "alice",
        "decision": "approve",
        "release_input_sha256": "sha256:input",
        "reviewed_content_sha256": content,
        "reviewed_evidence_sha256": evidence,
        "leak_gate_report_sha256": "sha256:leak",
        "leak_gate_report_scope": "input-tree",
        "reason": "Reviewed public knowledge release",
        "confirmation_nonce": f"nonce-{object_id}",
    }


def test_public_projection_generator_requires_matching_confirmation(tmp_path: Path):
    wiki = tmp_path / "wiki"
    wiki.mkdir()
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
            "derived": {"public_publishable": True},
            "hashes": {"content_sha256": "sha256:one", "evidence_sha256": "sha256:e1"},
        },
        "two": {
            "valid": True,
            "object_ref": {
                "vault_id": "public",
                "object_type": "wiki",
                "object_id": "two",
            },
            "derived": {"public_publishable": True},
            "hashes": {"content_sha256": "sha256:two", "evidence_sha256": "sha256:e2"},
        },
    }
    (tmp_path / "release" / "public-confirmations").mkdir(parents=True)
    write_event(tmp_path, _event("one", "sha256:one", "sha256:e1"))
    result = PublicProjectionGenerator(tmp_path, FakeValidator(reports)).generate()
    assert result["item_count"] == 1
    assert {
        item["id"]
        for item in json.loads(
            (tmp_path / "queries" / "public" / "manifest.json").read_text()
        )["items"]
    } == {"one"}
    assert {item["object_id"] for item in result["skipped"]} == {"two"}


def test_public_projection_generator_does_not_emit_private_or_unconfirmed_items(
    tmp_path: Path,
):
    wiki = tmp_path / "wiki"
    wiki.mkdir()
    (wiki / "private.md").write_text("secret", encoding="utf-8")
    reports = {
        "private": {
            "valid": True,
            "object_ref": {
                "vault_id": "private",
                "object_type": "wiki",
                "object_id": "private",
            },
            "derived": {"public_publishable": False},
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
    (public / "wiki").mkdir(parents=True)
    (private / "wiki").mkdir(parents=True)
    (public / "wiki" / "same.md").write_text("public fact", encoding="utf-8")
    (private / "wiki" / "same.md").write_text("PRIVATE SECRET", encoding="utf-8")
    reports = {
        "same": {
            "valid": True,
            "object_ref": {
                "vault_id": "public",
                "object_type": "wiki",
                "object_id": "same",
            },
            "derived": {"public_publishable": True},
            "hashes": {
                "content_sha256": "sha256:public",
                "evidence_sha256": "sha256:e",
            },
        }
    }
    (public / "release" / "public-confirmations").mkdir(parents=True)
    write_event(public, _event("same", "sha256:public", "sha256:e"))
    result = PublicProjectionGenerator(public, FakeValidator(reports)).generate()
    manifest = json.loads(
        (public / "queries" / "public" / "manifest.json").read_text(encoding="utf-8")
    )
    assert result["item_count"] == 1
    assert manifest["items"][0]["body_path"] == "wiki/same.md"
    assert "PRIVATE SECRET" not in json.dumps(manifest)
    assert not any("team-internal" in json.dumps(item) for item in manifest["items"])
