"""Disposable browser-test API. Never loads or writes the personal practice root."""

import argparse
from pathlib import Path

import uvicorn

from backend.app import create_app
from tools.question import QuestionStore


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--port", type=int, required=True)
    args = parser.parse_args()
    # The Node lifecycle owner creates this private empty directory and sentinel.
    if not (args.root / ".browser-fixture").is_file():
        raise ValueError("browser_fixture_root_required")
    store = QuestionStore(args.root)
    for topic in ("single", "multi", "resume", "error"):
        for index in range(2 if topic == "resume" else 1):
            spec = {
                "id": f"e2e-{topic}-{index}",
                "type": "multi_choice" if topic == "multi" else "single_choice",
                "domain": "tools",
                "topic": topic,
                "concept_id": f"e2e-{topic}",
                "skill": "recall",
                "prompt": f"E2E {topic} {index}: select the correct arithmetic result",
                "options": [
                    {"id": "a", "text": "2 + 2 = 4"},
                    {"id": "b", "text": "2 + 3 = 5"},
                    {"id": "c", "text": "2 + 2 = 9"},
                ],
                "correct_option_ids": ["a", "b"] if topic == "multi" else ["a"],
                "explanation": "Synthetic browser fixture, never personal content.",
                "wiki_refs": [],
            }
            result = store.import_spec(spec)
            if result["status"] != "ok":
                raise ValueError(result)
    uvicorn.run(
        create_app(root=args.root, items=[]),
        host="127.0.0.1",
        port=args.port,
        proxy_headers=False,
        log_level="warning",
    )


if __name__ == "__main__":
    main()
