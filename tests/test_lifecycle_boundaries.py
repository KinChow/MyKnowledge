import time

import pytest
from test_question import REPORT, QuestionTests

from tools import retire_ledger
from tools.content_repository import purge_precondition
from tools.paths import RepoPaths
from tools.question import QuestionStore
from tools.wiki_repository import WikiRepository


def test_restore_cancels_purge_and_delete_starts_new_retention(tmp_path):
    store = QuestionStore(tmp_path)
    store.create(QuestionTests().base(), wiki_report=REPORT)
    paths = RepoPaths(tmp_path)
    retire_ledger.append_retire(
        paths,
        "question",
        vault_id="local",
        object_id="q-one",
        reason="fixture",
        at=time.time() - 15 * 86400,
    )
    store.disable("q-one")
    assert store.list(status="all")["total"] == 0
    assert store.read("q-one")["status"] == "blocked"
    store.enable("q-one")
    assert store.read("q-one")["status"] == "ok"
    assert store.list()["total"] == 1
    assert store.purge("q-one")["error_code"] == "not_deleted"
    store.delete("q-one")
    assert store.purge("q-one")["error_code"] == "retention_not_elapsed"
    assert store.purge("q-one", grace_days=0)["purged"]


def test_deleted_wiki_default_read_list_and_restore(tmp_path):
    p = tmp_path / "content/wiki/test-wiki.md"
    p.parent.mkdir(parents=True)
    p.write_text("# Wiki")
    repo = WikiRepository(tmp_path)
    assert repo.delete("public", "test-wiki")["retired"]
    assert repo.read("public", "test-wiki")["error_code"] == "object_not_found"
    assert repo.list()["items"] == []
    retire_ledger.append_restore(
        RepoPaths(tmp_path),
        "wiki",
        vault_id="public",
        object_id="test-wiki",
        reason="restore",
    )
    assert repo.read("public", "test-wiki")["status"] == "ok"


@pytest.mark.parametrize(
    "bad",
    [
        "{broken",
        "{}",
        '{"object_id":"q-one","event":"unknown"}',
        '{"object_id":"q-one","event":[]}',
        '{"object_id":"q-one","event":"delete","at":0,"schema_version":"invalid"}',
    ],
)
def test_corrupt_ledger_never_allows_purge(tmp_path, bad):
    paths = RepoPaths(tmp_path)
    retire_ledger.append_retire(
        paths, "question", vault_id="local", object_id="q-one", reason="fixture", at=0
    )
    with (paths.audit_retire / "question.jsonl").open("a") as f:
        f.write(bad + "\n")
    assert (
        purge_precondition(paths, "question", "q-one", tmp_path)
        == "retention_not_elapsed"
    )


@pytest.mark.parametrize("response", [{}, [{}], [[]], ["a", {}], 1, "a"])
def test_multichoice_invalid_response_is_structured(tmp_path, response):
    store = QuestionStore(tmp_path)
    store.create(QuestionTests().base("multi_choice"), wiki_report=REPORT)
    assert store.answer("q-one", response)["error_code"] == "response_option_unknown"
    assert not store.paths.practice_reviews("q-one").exists()
