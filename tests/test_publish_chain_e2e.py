"""Real ingestion -> deterministic validation -> Git-approved projection.

The optional LLM remains advisory; neither provider access nor per-page release
signatures are required. Canonical evidence integrity still blocks publication.
"""

from __future__ import annotations

import json
from pathlib import Path

from wiki_fixtures import WIKI_BODY, _install_spec_doc

from tools.evidence_anchor import EvidenceAnchor
from tools.front_matter import FrontMatter
from tools.ingest.source_ingestor import SourceIngestor

QUOTE = "端到端发布链的可验证引文片段。"
SOURCE_ID = "e2e-release-source"
WIKI_ID = "e2e-release-wiki"


def _ingest_and_anchor(root: Path) -> str:
    body = f"来源正文开头。{QUOTE}来源正文结尾。"
    source_input = root / "incoming.md"
    source_input.write_text(body, encoding="utf-8")
    ingestor = SourceIngestor(root)
    applied = ingestor.ingest(
        {
            "source_type": "local-file",
            "input_path": str(source_input),
            "domain": "tools",
            "source_id": SOURCE_ID,
            "media_type": "text/markdown",
        }
    )
    assert applied["status"] == "ok", applied

    source_path = (
        root / "content" / "sources" / "tools" / f"{SOURCE_ID}" / f"{SOURCE_ID}.md"
    )
    snapshot = (
        root
        / "archive"
        / "text"
        / f"{applied['snapshot_sha256'].removeprefix('sha256:')}.md"
    )
    EvidenceAnchor.anchor_evidence(source_path, snapshot, QUOTE, min_chars=12)
    metadata, _ = FrontMatter.parse(source_path.read_text(encoding="utf-8"))
    return str(metadata["evidence_items"][0]["evidence_id"])


def _write_published_wiki(root: Path, evidence_id: str) -> Path:
    path = root / "content" / "wiki" / "tools" / f"{WIKI_ID}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    metadata = {
        "schema_version": "wiki/v1",
        "id": WIKI_ID,
        "title": "端到端发布链",
        "domain": "tools",
        "kind": "knowledge",
        "status": "published",
        "publication_scope": "public",
        "confidentiality": "public",
        "tags": ["e2e"],
        "aliases": [],
        "related": [],
        "sources": [SOURCE_ID],
        "updated_at": "2026-09-01",
        "evidence": [
            {
                "claim_id": "e2e-claim",
                "claim": "发布链可以从干净页面走到 public_release。",
                "targets": [{"source_id": SOURCE_ID, "evidence_id": evidence_id}],
                "support": "direct",
                "supporting_quotes": [{"evidence_id": evidence_id, "exact": QUOTE}],
            }
        ],
    }
    path.write_text(FrontMatter.render(metadata, WIKI_BODY), encoding="utf-8")
    return path


def test_publish_chain_runs_from_git_commit_without_signatures(tmp_path: Path):
    """Real ingestion/anchor/validation/Git build; no confirmation or model required."""
    import subprocess

    from tools.release_build import prepare_release

    _install_spec_doc(tmp_path)
    evidence_id = _ingest_and_anchor(tmp_path)
    wiki = _write_published_wiki(tmp_path, evidence_id)
    for args in (
        ("init",),
        ("config", "user.name", "Fixture"),
        ("config", "user.email", "fixture@example.invalid"),
        ("add", "."),
        ("commit", "-m", "approved fixture"),
    ):
        subprocess.run(
            ["git", "-C", str(tmp_path), *args], check=True, capture_output=True
        )
    out = tmp_path / "var/state/release/manifest.json"
    manifest = prepare_release(tmp_path, out)
    assert [x["id"] for x in manifest["items"]] == [WIKI_ID]
    assert manifest["approval"] == "git"
    assert manifest["items"][0]["public_release"] is True
    assert not (tmp_path / "release/public-confirmations").exists()
    assert wiki.exists()


def test_llm_failure_is_advisory_but_missing_snapshot_blocks(tmp_path: Path):
    from tools.public_projection import PublicProjectionGenerator
    from tools.validation.validator import WikiValidator

    _install_spec_doc(tmp_path)
    evidence_id = _ingest_and_anchor(tmp_path)
    wiki = _write_published_wiki(tmp_path, evidence_id)
    report = WikiValidator(tmp_path).validate(wiki)
    assert report["valid"]
    hashes = report["hashes"]
    audit = tmp_path / "audit/validation/wiki" / WIKI_ID / "failed.json"
    audit.parent.mkdir(parents=True)
    audit.write_text(
        json.dumps(
            {
                "schema_version": "validation-report/v1",
                "wiki_content_sha256": hashes["content_sha256"],
                "wiki_evidence_sha256": hashes["evidence_sha256"],
                "verdict": "fail",
                "claims": [{"claim_id": "e2e-claim", "verdict": "unsupported"}],
            }
        )
    )
    result = PublicProjectionGenerator(tmp_path).generate(strict=True)
    assert result["status"] == "ok"
    manifest = json.loads((tmp_path / "var/queries/public/manifest.json").read_text())
    assert manifest["items"][0]["validation_state"] == "fail"
    assert manifest["items"][0]["public_release"] is True
    for snapshot in (tmp_path / "archive/text").glob("*.md"):
        snapshot.unlink()
    assert (
        PublicProjectionGenerator(tmp_path).generate(strict=True)["status"] == "blocked"
    )
