from pathlib import Path

SKILL = Path(__file__).parents[1] / "skills" / "myknowledge" / "SKILL.md"


def test_canonical_skill_exists_and_routes_through_tools():
    text = SKILL.read_text(encoding="utf-8")
    assert "name: myknowledge" in text
    assert "tools.cli" in text
    assert "explicit human confirmation" in text
    assert "commit/push/reset" in text


def test_skill_does_not_define_direct_file_write_or_public_practice_route():
    text = SKILL.read_text(encoding="utf-8").lower()
    assert "edit markdown" in text
    assert "never public" in text
