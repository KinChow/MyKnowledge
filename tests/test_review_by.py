"""WIKI-003 `review_by`：续期是报告项，不得动摇任何 hash、状态或人工确认。

fixture 全部取仓库真实产物（`content/wiki/reading-notes/how-to-read-a-book.md`
与带 `public-release-confirmation` 的 `content/wiki/work-methods/aar.md`），
不合成 hash——`excluded_from_content_hash` 这条契约在 2026-08-28 之前是纯文档，
唯一能证明它成立的方式是拿真实页面跑两遍 validator 逐字节对比。
"""

from __future__ import annotations

import shutil
from pathlib import Path

from tools.schemas import schemas_value
from tools.validation import WikiValidator

ROOT = Path(__file__).resolve().parents[1]
READING_PAGE = "content/wiki/reading-notes/how-to-read-a-book.md"
CONFIRMED_PAGE = "content/wiki/work-methods/aar.md"
# validator 的全部事实源：canonical 内容 + 快照 + 审计确认 + 发布确认
FACT_ROOTS = ("content", "archive", "audit", "release")


def _real_tree(tmp_path: Path) -> Path:
    root = tmp_path / "repo"
    root.mkdir()
    for name in FACT_ROOTS:
        shutil.copytree(ROOT / name, root / name)
    return root


def _insert_review_by(path: Path, value: str = "2027-03-01") -> None:
    """在 front matter 内插入 review_by（作者手写口径，不经派生写入）。"""
    text = path.read_text(encoding="utf-8")
    marker = "\nupdated_at:"
    assert marker in text, path
    path.write_text(
        text.replace(marker, f"\nreview_by: '{value}'{marker}", 1), encoding="utf-8"
    )


def test_review_by_is_declared_in_allowed_fields_and_excluded_from_content_hash():
    """12.1：两处声明必须同时存在。

    只加 `allowed_fields` 会让续期作废人工审计确认，只加
    `excluded_from_content_hash` 会让 schema 直接拒收该字段。
    """
    allowed = schemas_value(
        ROOT, "field_contracts", "wiki", "allowed_fields", default=None
    )
    excluded = schemas_value(
        ROOT, "hash_inputs", "excluded_from_content_hash", default=None
    )
    assert allowed is not None and excluded is not None, "schemas.yaml 契约缺失"
    assert "review_by" in allowed
    assert "review_by" in excluded


def test_adding_review_by_leaves_both_hashes_byte_identical(tmp_path: Path):
    """12.2：真实页面增删 review_by，content/evidence hash 逐字节不变。"""
    root = _real_tree(tmp_path)
    page = root / READING_PAGE

    baseline = WikiValidator(root).validate(page)
    assert baseline["valid"], baseline["errors"]
    # fixture 真实性自证：拷贝树的 hash 必须等于仓库原地校验结果
    real = WikiValidator(ROOT).validate(ROOT / READING_PAGE)
    assert baseline["hashes"] == real["hashes"]

    _insert_review_by(page)
    renewed = WikiValidator(root).validate(page)
    assert renewed["valid"], renewed["errors"]
    assert renewed["hashes"]["content_sha256"] == baseline["hashes"]["content_sha256"]
    assert renewed["hashes"]["evidence_sha256"] == baseline["hashes"]["evidence_sha256"]


def test_adding_review_by_keeps_the_existing_confirmation_and_every_state(
    tmp_path: Path,
):
    """12.3：已有 operation-confirmation + 发布确认的页面续期后状态全等。"""
    root = _real_tree(tmp_path)
    page = root / CONFIRMED_PAGE

    baseline = WikiValidator(root).validate(page)
    assert baseline["valid"], baseline["errors"]
    # 该页面的 publishable 由真实人工确认驱动，否则本用例证明不了"确认仍有效"
    assert baseline["derived"]["public_publishable"] is True

    _insert_review_by(page)
    renewed = WikiValidator(root).validate(page)
    assert renewed["valid"], renewed["errors"]
    assert renewed["derived"] == baseline["derived"]
    assert renewed["hashes"] == baseline["hashes"]


def test_malformed_review_by_is_rejected_not_silently_ignored(tmp_path: Path):
    """report-only 不等于免校验：格式非法必须报字段级错误（fail-closed）。"""
    root = _real_tree(tmp_path)
    page = root / READING_PAGE
    _insert_review_by(page, value="2027/03/01")

    report = WikiValidator(root).validate(page)
    assert not report["valid"]
    assert any(error["path"].endswith("review_by") for error in report["errors"]), (
        report["errors"]
    )


def test_doctor_lists_due_review_without_changing_any_state(tmp_path: Path):
    """AC-F013-009：到期只进 doctor 清单，`status` 与全部 `*_state` 不变。"""
    import json
    import subprocess
    import sys

    root = _real_tree(tmp_path)
    page = root / CONFIRMED_PAGE
    _insert_review_by(page, value="2020-01-01")
    before = WikiValidator(root).validate(page)
    assert before["valid"], before["errors"]

    out = subprocess.run(
        [sys.executable, "-m", "tools.doctor", "--root", str(root)],
        capture_output=True,
        text=True,
        cwd=ROOT,
        check=False,
    )
    assert out.returncode == 0, out.stdout  # 到期不阻断
    check = {c["name"]: c for c in json.loads(out.stdout)["checks"]}["review_due"]
    assert check["state"] == "warning"
    assert check["reason"] == "review_due"
    entry = check["due"]["work-methods"][0]  # 按 domain 分组
    assert entry["object_id"] == "aar" and entry["overdue_days"] > 0

    after = WikiValidator(root).validate(page)
    assert after["derived"] == before["derived"]
    assert after["hashes"] == before["hashes"]
    assert page.read_text(encoding="utf-8").count("status: published") == 1
