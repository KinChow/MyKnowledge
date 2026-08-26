"""Generate auditable, non-claiming acceptance reports for each Feature."""
from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path


def _git(root: Path, *args: str) -> str:
    result = subprocess.run(["git", *args], cwd=root, capture_output=True, text=True, check=False)
    return result.stdout.strip()


def generate(root: Path, feature: str) -> dict:
    root = Path(root).resolve()
    matches = sorted(root.glob(f"docs/acceptance/{feature}-*.md"))
    if not matches:
        raise ValueError("acceptance_missing")
    doc = matches[0]
    text = doc.read_text(encoding="utf-8")
    scenarios = sorted(set(re.findall(r"AC-" + re.escape(feature) + r"-\d{3}", text)))
    status = "Implemented (partial)"
    report = {
        "schema_version": "acceptance-report/v1",
        "feature": feature,
        "status": status,
        "generated_from": _git(root, "rev-parse", "HEAD"),
        "acceptance_document": str(doc.relative_to(root)),
        "scenario_ids": scenarios,
        "evidence_boundary": "Automated evidence listed in the acceptance document is partial; missing scenarios remain pending and this report does not imply Accepted.",
        "verification": {
            "python_command": ".venv/bin/python -m pytest -q",
            "frontend_command": "npm run validate:config && npm run validate:docs && MYKNOWLEDGE_CONTENT_MODE=projection npm run validate:projection",
            "remote_push": False,
        },
    }
    return report


def main() -> int:
    import argparse
    parser = argparse.ArgumentParser(description="Generate partial acceptance evidence reports")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--feature", action="append")
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args()
    features = args.feature or [f"F{i:03d}" for i in range(1, 13)]
    output = (args.output_dir or args.root / "reports" / "acceptance").resolve()
    output.mkdir(parents=True, exist_ok=True)
    for feature in features:
        report = generate(args.root, feature)
        path = output / f"{feature}-report.json"
        path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(path.relative_to(Path(args.root).resolve()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
