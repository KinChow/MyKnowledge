from pathlib import Path

from tools.evidence_anchor import EvidenceAnchor
from tools.front_matter import FrontMatter
from tools.ingest.source_ingestor import SourceIngestor
from tools.validation.validator import WikiValidator
from wiki_fixtures import WIKI_BODY


def test_source_to_wiki_evidence_chain_is_replayable(tmp_path: Path):
    source_input = tmp_path / "note.txt"
    source_input.write_text("可回放的证据正文，包含稳定引用。", encoding="utf-8")
    ingestor = SourceIngestor(tmp_path)
    preview = ingestor.preview({"source_type": "local-file", "input_path": str(source_input), "domain": "tools", "source_id": "e2e-source", "media_type": "text/plain"})
    assert preview["state"] == "previewed"
    applied = ingestor.apply(preview["operation_id"], confirmed=True, actor_id="e2e")
    assert applied["state"] == "applied"

    source_path = tmp_path / "sources" / "tools" / "e2e-source.md"
    snapshot_path = tmp_path / "archive" / "text" / f"{applied['snapshot_sha256'].removeprefix('sha256:')}.md"
    anchor = EvidenceAnchor(tmp_path).preview(source_path, snapshot_path, "可回放的证据正文，包含稳定引用。", min_chars=12)
    assert anchor["state"] == "previewed"
    anchored = EvidenceAnchor(tmp_path).apply(anchor["operation_id"], confirmed=True)
    assert anchored["state"] == "applied"
    source_meta, _ = FrontMatter.parse(source_path.read_text(encoding="utf-8"))
    evidence = source_meta["evidence_items"][0]

    wiki = tmp_path / "wiki" / "tools" / "e2e-wiki.md"
    wiki.parent.mkdir(parents=True)
    metadata = {"schema_version": "wiki/v1", "id": "e2e-wiki", "title": "E2E", "domain": "tools", "kind": "knowledge", "status": "review", "publication_scope": "none", "confidentiality": "public", "tags": ["e2e"], "aliases": [], "related": [], "sources": ["e2e-source"], "updated_at": "2026-08-27", "evidence": [{"claim_id": "e2e-claim", "claim": "证据链可回放。", "targets": [{"source_id": "e2e-source", "evidence_id": evidence["evidence_id"]}], "support": "direct", "supporting_quotes": [{"evidence_id": evidence["evidence_id"], "exact": "可回放的证据正文，包含稳定引用。"}]}]}
    wiki.write_text(FrontMatter.render(metadata, WIKI_BODY), encoding="utf-8")
    report = WikiValidator(tmp_path).validate(wiki)
    assert report["valid"], report["errors"]
    assert report["hashes"]["evidence_sha256"]
    assert report["resolution"]["resolved_targets"][0]["resolved_object_ref"]["object_id"] == "e2e-source"
