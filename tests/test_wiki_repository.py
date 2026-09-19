"""WikiRepository（CRUD 能力层，Repository 模式）的 TDD 契约测试。

覆盖 read/list 复用定位、deprecate/delete=CASCADE（级联把绑定该 wiki 的 question
经 QuestionStore.refresh_status 置 disabled、写一条 CDR、软删 retire）、以及重复
调用幂等。返回一律走 tools.contract 统一信封。
"""

from __future__ import annotations

import json
import time
from pathlib import Path

from tools.front_matter import FrontMatter
from tools.question import QuestionStore
from tools.wiki_repository import WikiRepository


def _write_wiki(root: Path, wiki_id: str) -> Path:
    metadata = {
        "schema_version": "wiki/v1",
        "id": wiki_id,
        "title": wiki_id,
        "domain": "tools",
        "kind": "knowledge",
        "status": "draft",
        "sources": [],
        "evidence": [],
    }
    path = root / "content" / "wiki" / "tools" / f"{wiki_id}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(FrontMatter.render(metadata, "# body\n"), encoding="utf-8")
    return path


def _write_question(root: Path, question_id: str, wiki_id: str) -> None:
    """直接落一份合法的 question/v1（绑定 wiki_id），绕过 wiki 校验重活。"""
    store = QuestionStore(root)
    question = {
        "schema_version": "question/v1",
        "id": question_id,
        "type": "single_choice",
        "confidentiality": "public",
        "wiki_claim": {
            "vault_id": "public",
            "wiki_id": wiki_id,
            "claim_id": "c1",
            "content_sha256": "sha256:" + "0" * 64,
            "evidence_sha256": "sha256:" + "0" * 64,
        },
        "prompt": "示例题干？",
        "options": [{"id": "a", "text": "A"}, {"id": "b", "text": "B"}],
        "correct_option_ids": ["a"],
        "answer": None,
        "explanation": "",
        "rubric": None,
        "company_tags": [],
        "source_refs": [],
        "status": "enabled",
        "created_at": time.time(),
        "review_state": None,
    }
    question["content_sha256"] = QuestionStore._content_hash(question)
    path = store.paths.practice_questions / f"{question_id}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(question, ensure_ascii=False) + "\n", encoding="utf-8")


def test_read_returns_metadata_and_body(tmp_path: Path):
    _write_wiki(tmp_path, "wiki-read")
    result = WikiRepository(tmp_path).read("public", "wiki-read")
    assert result["status"] == "ok"
    assert result["metadata"]["id"] == "wiki-read"
    assert result["object_ref"]["object_type"] == "wiki"


def test_read_missing_is_object_not_found(tmp_path: Path):
    result = WikiRepository(tmp_path).read("public", "ghost")
    assert result["status"] == "blocked"
    assert result["error_code"] == "object_not_found"


def test_list_enumerates_wikis(tmp_path: Path):
    _write_wiki(tmp_path, "wiki-a")
    _write_wiki(tmp_path, "wiki-b")
    result = WikiRepository(tmp_path).list("public")
    assert result["status"] == "ok"
    ids = sorted(item["object_ref"]["object_id"] for item in result["items"])
    assert ids == ["wiki-a", "wiki-b"]


def test_delete_cascades_disables_bound_questions_and_writes_cdr(tmp_path: Path):
    _write_wiki(tmp_path, "wiki-cx")
    _write_question(tmp_path, "q-bound", "wiki-cx")
    _write_question(tmp_path, "q-other", "wiki-else")

    result = WikiRepository(tmp_path).delete("public", "wiki-cx")
    assert result["status"] == "ok"
    assert result["changed"] is True
    assert result["retired"] is True
    assert "q-bound" in result["disabled_questions"]
    assert "q-other" not in result["disabled_questions"]

    store = QuestionStore(tmp_path)
    assert store.load("q-bound")["status"] == "disabled"
    assert store.load("q-other")["status"] == "enabled"

    cdr_dir = tmp_path / "content" / "decisions"
    assert list(cdr_dir.glob("*.md"))
    assert (tmp_path / "audit" / "retire" / "wiki.jsonl").exists()


def test_delete_is_idempotent(tmp_path: Path):
    _write_wiki(tmp_path, "wiki-idem")
    _write_question(tmp_path, "q-i", "wiki-idem")

    first = WikiRepository(tmp_path).delete("public", "wiki-idem")
    assert first["changed"] is True

    second = WikiRepository(tmp_path).delete("public", "wiki-idem")
    assert second["status"] == "ok"
    assert second["changed"] is False
    ledger = tmp_path / "audit" / "retire" / "wiki.jsonl"
    assert ledger.read_text("utf-8").strip().count("\n") == 0


def test_deprecate_alias_matches_delete(tmp_path: Path):
    _write_wiki(tmp_path, "wiki-dep")
    result = WikiRepository(tmp_path).deprecate("public", "wiki-dep")
    assert result["status"] == "ok"
    assert result["retired"] is True


def test_delete_missing_wiki_is_object_not_found(tmp_path: Path):
    result = WikiRepository(tmp_path).delete("public", "ghost")
    assert result["status"] == "blocked"
    assert result["error_code"] == "object_not_found"
