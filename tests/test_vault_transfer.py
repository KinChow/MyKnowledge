from pathlib import Path
import subprocess

from tools.vault_transfer import VaultTransfer


def _workspace(tmp_path: Path) -> tuple[Path, Path, Path, Path]:
    public, private = tmp_path / "public", tmp_path / "private"
    public.mkdir(); private.mkdir()
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
    (private / "wiki").mkdir(); (private / "wiki" / "secret.md").write_text("secret\n", encoding="utf-8")
    service = VaultTransfer(public, manifest)
    result = service.preview("private", "wiki/secret.md", "public", "wiki/secret.md")
    assert result["error_code"] == "confidentiality_downgrade"
    assert not (public / "wiki" / "secret.md").exists()


def test_cross_vault_copy_and_move_use_explicit_owner_and_locks(tmp_path: Path):
    root, public, private, manifest = _workspace(tmp_path)
    (public / "wiki").mkdir(); (public / "wiki" / "note.md").write_text("note\n", encoding="utf-8")
    service = VaultTransfer(public, manifest)
    preview = service.preview("public", "wiki/note.md", "private", "wiki/note.md")
    assert preview["state"] == "previewed"
    assert service.apply(preview["operation_id"])["state"] == "awaiting_confirmation"
    applied = service.apply(preview["operation_id"], confirmed=True)
    assert applied["state"] == "applied"
    assert (private / "wiki" / "note.md").read_text(encoding="utf-8") == "note\n"
    assert (public / "wiki" / "note.md").exists()

    move = service.preview("public", "wiki/note.md", "private", "wiki/moved.md", move=True)
    assert service.apply(move["operation_id"], confirmed=True)["state"] == "applied"
    assert not (public / "wiki" / "note.md").exists()
    assert (private / "wiki" / "moved.md").read_text(encoding="utf-8") == "note\n"
