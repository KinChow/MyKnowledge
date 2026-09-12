"""题库 CLI：按子命令组织 F008 的参数与领域调用。"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .question import QuestionStore


def _print_json(result: dict) -> None:
    print(json.dumps(result, ensure_ascii=False, indent=2))


def _add_root(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--root", type=Path, default=Path.cwd())


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m tools.cli question",
        description="F008 personal question bank",
    )
    subparsers = parser.add_subparsers(dest="action", required=True)

    create = subparsers.add_parser("create", help="create a Wiki-bound question")
    _add_root(create)
    create.add_argument("--spec", type=Path, required=True)
    create.add_argument("--wiki", type=Path)

    import_parser = subparsers.add_parser("import", help="import standalone JSON questions")
    _add_root(import_parser)
    import_parser.add_argument("--source", type=Path, required=True)

    list_parser = subparsers.add_parser("list", help="list and filter local questions")
    _add_root(list_parser)
    list_parser.add_argument("--domain")
    list_parser.add_argument("--topic")
    list_parser.add_argument("--skill")
    list_parser.add_argument(
        "--status", choices=["enabled", "disabled", "all"], default="enabled"
    )

    session = subparsers.add_parser("session", help="create a short practice session")
    _add_root(session)
    session_subparsers = session.add_subparsers(dest="session_action", required=True)
    session_create = session_subparsers.add_parser("create", help="create a session")
    session_create.add_argument("--size", type=int, choices=[3, 6, 10], default=6)
    session_create.add_argument("--domain")
    session_create.add_argument("--topic")
    session_create.add_argument("--concept-id")
    session_create.add_argument("--skill")

    errors = subparsers.add_parser("errors", help="list questions needing retry")
    _add_root(errors)
    errors.add_argument("--limit", type=int, default=10)
    errors.add_argument("--domain")
    errors.add_argument("--topic")
    errors.add_argument("--concept-id")
    errors.add_argument("--skill")

    queue = subparsers.add_parser("queue", help="list due and new review questions")
    _add_root(queue)
    queue.add_argument("--size", type=int, choices=[3, 6, 10], default=6)
    queue.add_argument("--domain")
    queue.add_argument("--topic")
    queue.add_argument("--concept-id")
    queue.add_argument("--skill")
    queue.add_argument("--only-due", action="store_true")

    disable = subparsers.add_parser("disable", help="disable one question")
    _add_root(disable)
    disable.add_argument("--question-id", required=True)
    disable.add_argument("--reason", default="manual")

    enable = subparsers.add_parser("enable", help="enable one question")
    _add_root(enable)
    enable.add_argument("--question-id", required=True)

    delete = subparsers.add_parser("delete", help="delete one question")
    _add_root(delete)
    delete.add_argument("--question-id", required=True)

    answer = subparsers.add_parser("answer", help="answer and score one question")
    _add_root(answer)
    answer.add_argument("--question-id", required=True)
    answer.add_argument("--response", required=True)
    answer.add_argument(
        "--scoring-mode", choices=["manual", "deterministic", "llm"], default="manual"
    )

    review = subparsers.add_parser("review", help="schedule one question review")
    _add_root(review)
    review.add_argument("--question-id", required=True)
    review.add_argument("--rating", type=int, required=True)
    return parser


def question_main(argv: list[str]) -> int:
    args = _build_parser().parse_args(argv)
    store = QuestionStore(args.root)
    if args.action == "create":
        result = store.create(
            json.loads(args.spec.read_text(encoding="utf-8")), wiki_path=args.wiki
        )
    elif args.action == "import":
        result = store.import_path(args.source)
    elif args.action == "list":
        result = store.list(
            domain=args.domain,
            topic=args.topic,
            skill=args.skill,
            status=args.status,
        )
    elif args.action == "session":
        result = store.create_session(
            size=args.size,
            domain=args.domain,
            topic=args.topic,
            concept_id=args.concept_id,
            skill=args.skill,
        )
    elif args.action == "errors":
        result = store.error_queue(
            limit=args.limit,
            domain=args.domain,
            topic=args.topic,
            concept_id=args.concept_id,
            skill=args.skill,
        )
    elif args.action == "queue":
        result = store.review_queue(
            size=args.size,
            domain=args.domain,
            topic=args.topic,
            concept_id=args.concept_id,
            skill=args.skill,
            include_new=not args.only_due,
        )
    elif args.action == "disable":
        result = store.disable(args.question_id, reason=args.reason)
    elif args.action == "enable":
        result = store.enable(args.question_id)
    elif args.action == "delete":
        result = store.delete(args.question_id)
    elif args.action == "answer":
        result = store.answer(
            args.question_id,
            json.loads(args.response),
            scoring_mode=args.scoring_mode,
        )
    else:
        result = store.review(args.question_id, args.rating)
    _print_json(result)
    return 0
