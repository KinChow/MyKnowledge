import subprocess
from pathlib import Path
from unittest import mock

from tools.vault_transfer import VaultTransfer


def _workspace(tmp_path: Path) -> tuple[Path, Path, Path, Path]:
    public, private = tmp_path / "public", tmp_path / "private"
    public.mkdir()
    private.mkdir()
    for path in (public, private):
        subprocess.run(["git", "init", "-q", str(path)], check=True)
    manifest = tmp_path / "vaults.yaml"
    manifest.write_text(
        f"schema_version: 1\nlayout: superproject\nworkspace_root: {tmp_path}\n"
        "public_vault_id: public\nvaults:\n"
        "  - {id: public, path: public, confidentiality: public}\n"
        "  - {id: private, path: private, confidentiality: internal}\n",
        encoding="utf-8",
    )
    return tmp_path, public, private, manifest


def test_private_to_public_transfer_is_blocked_before_write(tmp_path: Path):
    root, public, private, manifest = _workspace(tmp_path)
    (private / "wiki").mkdir()
    (private / "wiki" / "secret.md").write_text("secret\n", encoding="utf-8")
    service = VaultTransfer(public, manifest)
    result = service.preview("private", "wiki/secret.md", "public", "wiki/secret.md")
    assert result["error_code"] == "confidentiality_downgrade"
    assert not (public / "wiki" / "secret.md").exists()


def test_cross_vault_copy_and_move_use_explicit_owner_and_locks(tmp_path: Path):
    root, public, private, manifest = _workspace(tmp_path)
    (public / "wiki").mkdir()
    (public / "wiki" / "note.md").write_text("note\n", encoding="utf-8")
    service = VaultTransfer(public, manifest)
    preview = service.preview("public", "wiki/note.md", "private", "wiki/note.md")
    assert preview["state"] == "previewed"
    assert service.apply(preview["operation_id"])["state"] == "awaiting_confirmation"
    applied = service.apply(preview["operation_id"], confirmed=True)
    assert applied["state"] == "applied"
    assert (private / "wiki" / "note.md").read_text(encoding="utf-8") == "note\n"
    assert (public / "wiki" / "note.md").exists()

    move = service.preview(
        "public", "wiki/note.md", "private", "wiki/moved.md", move=True
    )
    assert service.apply(move["operation_id"], confirmed=True)["state"] == "applied"
    assert not (public / "wiki" / "note.md").exists()
    assert (private / "wiki" / "moved.md").read_text(encoding="utf-8") == "note\n"


def test_cross_vault_move_rolls_back_target_when_source_delete_fails(tmp_path: Path):
    root, public, private, manifest = _workspace(tmp_path)
    source = public / "wiki" / "note.md"
    source.parent.mkdir()
    source.write_text("note\n", encoding="utf-8")
    target = private / "wiki" / "note.md"
    service = VaultTransfer(public, manifest)
    preview = service.preview(
        "public", "wiki/note.md", "private", "wiki/note.md", move=True
    )
    original_unlink = Path.unlink

    def fail_source_delete(path: Path, *args, **kwargs):
        if path == source:
            raise OSError("injected source delete failure")
        return original_unlink(path, *args, **kwargs)

    with mock.patch.object(
        Path, "unlink", autospec=True, side_effect=fail_source_delete
    ):
        result = service.apply(preview["operation_id"], confirmed=True)
    assert result["error_code"] == "apply_failed"
    assert source.read_text(encoding="utf-8") == "note\n"
    assert not target.exists()
    assert not (public / "state" / "locks" / "public.owner").exists()
    assert not (public / "state" / "locks" / "private.owner").exists()


def test_transfer_confirmation_event_is_validated(tmp_path):
    """F011 review：跨 vault 迁移与 write 通道同确认语义。"""
    import subprocess as sp

    ws = tmp_path
    pub, a, b = ws / "pub", ws / "va", ws / "vb"
    for v in (pub, a, b):
        v.mkdir()
        sp.run(["git", "init", "-q", str(v)], check=True)
    (a / "wiki").mkdir(parents=True)
    (a / "wiki" / "n.md").write_text("x", encoding="utf-8")
    m = pub / "config" / "vaults.local.yaml"
    m.parent.mkdir(parents=True)
    m.write_text(
        f"schema_version: 1\nlayout: superproject\nworkspace_root: {ws}\nvaults:\n  - {{id: pub, path: pub}}\n  - {{id: va, path: va, confidentiality: internal}}\n  - {{id: vb, path: vb, confidentiality: internal}}\n",
        encoding="utf-8",
    )
    from tools.vault_transfer import VaultTransfer

    t = VaultTransfer(pub, m)
    pv = t.preview("va", "wiki/n.md", "vb", "wiki/n.md")
    forged = {
        "schema_version": "operation-confirmation/v1",
        "operation_id": pv["operation_id"],
        "scope": "apply",
        "actor_type": "human",
        "actor_id": "a",
        "input_hash": "sha256:forged",
        "diff_hash": pv.get("diff_hash"),
        "event_sha256": "sha256:x",
    }
    assert (
        t.apply(pv["operation_id"], confirmed=True, confirmation=forged)["error_code"]
        == "confirmation_hash_mismatch"
    )
    assert not (b / "wiki" / "n.md").exists()
