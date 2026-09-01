import subprocess
from pathlib import Path
from unittest import mock

from tools.vault_transfer import VaultTransfer


def _workspace(tmp_path: Path) -> tuple[Path, Path, Path, Path]:
    public, private = tmp_path / "public", tmp_path / "private"
    public.mkdir(parents=True, exist_ok=True)
    private.mkdir(parents=True, exist_ok=True)
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
    (private / "content" / "wiki").mkdir(parents=True, exist_ok=True)
    (private / "content" / "wiki" / "secret.md").write_text(
        "secret\n", encoding="utf-8"
    )
    service = VaultTransfer(public, manifest)
    result = service.preview(
        "private", "content/wiki/secret.md", "public", "content/wiki/secret.md"
    )
    assert result["error_code"] == "confidentiality_downgrade"
    assert not (public / "content" / "wiki" / "secret.md").exists()


def test_cross_vault_copy_and_move_use_explicit_owner_and_locks(tmp_path: Path):
    root, public, private, manifest = _workspace(tmp_path)
    (public / "content" / "wiki").mkdir(parents=True, exist_ok=True)
    (public / "content" / "wiki" / "note.md").write_text("note\n", encoding="utf-8")
    service = VaultTransfer(public, manifest)
    preview = service.preview(
        "public", "content/wiki/note.md", "private", "content/wiki/note.md"
    )
    assert preview["state"] == "previewed"
    assert service.apply(preview["operation_id"])["state"] == "awaiting_confirmation"
    applied = service.apply(preview["operation_id"], confirmed=True)
    assert applied["state"] == "applied"
    assert (private / "content" / "wiki" / "note.md").read_text(
        encoding="utf-8"
    ) == "note\n"
    assert (public / "content" / "wiki" / "note.md").exists()

    move = service.preview(
        "public", "content/wiki/note.md", "private", "content/wiki/moved.md", move=True
    )
    assert service.apply(move["operation_id"], confirmed=True)["state"] == "applied"
    assert not (public / "content" / "wiki" / "note.md").exists()
    assert (private / "content" / "wiki" / "moved.md").read_text(
        encoding="utf-8"
    ) == "note\n"


def test_cross_vault_move_rolls_back_target_when_source_delete_fails(tmp_path: Path):
    root, public, private, manifest = _workspace(tmp_path)
    source = public / "content" / "wiki" / "note.md"
    source.parent.mkdir(parents=True, exist_ok=True)
    source.write_text("note\n", encoding="utf-8")
    target = private / "content" / "wiki" / "note.md"
    service = VaultTransfer(public, manifest)
    preview = service.preview(
        "public", "content/wiki/note.md", "private", "content/wiki/note.md", move=True
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
    assert not (public / "var" / "state" / "locks" / "public.owner").exists()
    assert not (public / "var" / "state" / "locks" / "private.owner").exists()


def test_transfer_confirmation_event_is_validated(tmp_path):
    """F011 review：跨 vault 迁移与 write 通道同确认语义。"""
    import subprocess as sp

    ws = tmp_path
    pub, a, b = ws / "pub", ws / "va", ws / "vb"
    for v in (pub, a, b):
        v.mkdir(parents=True, exist_ok=True)
        sp.run(["git", "init", "-q", str(v)], check=True)
    (a / "content" / "wiki").mkdir(parents=True)
    (a / "content" / "wiki" / "n.md").write_text("x", encoding="utf-8")
    m = pub / "config" / "vaults.local.yaml"
    m.parent.mkdir(parents=True)
    m.write_text(
        f"schema_version: 1\nlayout: superproject\nworkspace_root: {ws}\nvaults:\n  - {{id: pub, path: pub}}\n  - {{id: va, path: va, confidentiality: internal}}\n  - {{id: vb, path: vb, confidentiality: internal}}\n",
        encoding="utf-8",
    )
    from tools.vault_transfer import VaultTransfer

    t = VaultTransfer(pub, m)
    pv = t.preview("va", "content/wiki/n.md", "vb", "content/wiki/n.md")
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
    assert not (b / "content" / "wiki" / "n.md").exists()
