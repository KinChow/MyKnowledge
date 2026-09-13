import json
from pathlib import Path

from tools.question import QuestionStore
from tools.question_quality import QuestionQualityService, deterministic_quality


def _import_question(root: Path) -> str:
    source = root / "question.json"
    source.write_text(json.dumps({
        "id": "q-quality",
        "type": "single_choice",
        "domain": "llm-inference",
        "topic": "attention",
        "concept_id": "mha",
        "skill": "mechanism",
        "prompt": "为什么需要 KV Cache？",
        "options": [{"id": "a", "text": "复用历史 K/V"}, {"id": "b", "text": "减少参数"}],
        "correct_option_ids": ["a"],
        "explanation": "Decode 时复用历史 K/V。",
    }, ensure_ascii=False), encoding="utf-8")
    return QuestionStore(root).import_file(source)["question_id"]


def test_quality_writes_deterministic_report(tmp_path: Path):
    question_id = _import_question(tmp_path)
    result = QuestionQualityService(tmp_path).validate(question_id)
    assert result["report"]["deterministic"]["state"] == "pass"
    assert (tmp_path / "content/practice/quality/q-quality.json").exists()


def test_quality_llm_reviewer_gets_no_review_state(tmp_path: Path):
    question_id = _import_question(tmp_path)
    seen = {}

    def reviewer(payload):
        seen.update(payload)
        return {"state": "pass", "score": 0.9, "findings": [], "suggestions": []}

    result = QuestionQualityService(tmp_path).validate(
        question_id, mode="llm", llm_reviewer=reviewer
    )
    assert result["report"]["llm"]["score"] == 0.9
    assert "review_state" not in json.dumps(seen)


def test_quality_detects_duplicate_options():
    result = deterministic_quality({
        "type": "single_choice",
        "prompt": "这是一个足够长的题干？",
        "options": [{"id": "a", "text": "相同"}, {"id": "b", "text": "相同"}],
        "correct_option_ids": ["a"],
        "explanation": "说明",
    })
    assert result["state"] == "fail"
    assert any(item["code"] == "option_text_duplicate" for item in result["findings"])
