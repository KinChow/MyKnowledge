"""Browser gate wiring must not silently disappear from pre-push / deployment."""

import json
import subprocess
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def test_pages_upload_is_after_real_build_and_public_browser_gate():
    config = yaml.safe_load((ROOT / ".github/workflows/deploy-pages.yml").read_text())
    steps = config["jobs"]["build"]["steps"]
    build = next(i for i, s in enumerate(steps) if s.get("run") == "npm run build")
    browser = next(
        i for i, s in enumerate(steps) if s.get("run") == "npm run test:browser:public"
    )
    upload = next(
        i
        for i, s in enumerate(steps)
        if s.get("uses", "").startswith("actions/upload-pages-artifact@")
    )
    assert build < browser < upload
    assert not steps[browser].get("continue-on-error")
    assert "if" not in steps[browser]


def test_release_workflows_materialize_lfs_before_release_checks():
    pages = yaml.safe_load((ROOT / ".github/workflows/deploy-pages.yml").read_text())
    pages_steps = pages["jobs"]["build"]["steps"]
    pages_lfs = next(
        i for i, s in enumerate(pages_steps) if s.get("run") == "git lfs checkout"
    )
    pages_checkout = next(
        i for i, s in enumerate(pages_steps) if s.get("uses") == "actions/checkout@v4"
    )
    pages_build = next(
        i for i, s in enumerate(pages_steps) if s.get("run") == "npm run build"
    )
    assert pages_checkout < pages_lfs < pages_build

    ci = yaml.safe_load((ROOT / ".github/workflows/knowledge-check.yml").read_text())
    frontend_steps = ci["jobs"]["frontend-gates"]["steps"]
    frontend_lfs = next(
        i for i, s in enumerate(frontend_steps) if s.get("run") == "git lfs checkout"
    )
    frontend_checkout = next(
        i
        for i, s in enumerate(frontend_steps)
        if s.get("uses") == "actions/checkout@v4"
    )
    frontend_build = next(
        i
        for i, s in enumerate(frontend_steps)
        if s.get("run") == "npm run check:browser"
    )
    assert frontend_checkout < frontend_lfs < frontend_build


def test_check_command_and_pre_push_cover_both_browser_surfaces():
    scripts = json.loads((ROOT / "frontend/package.json").read_text())["scripts"]
    assert scripts["check:browser"] == "npm run build && npm run test:browser"
    assert scripts["test:browser"] == (
        "npm run test:browser:public && npm run test:browser:local"
    )
    runner = (ROOT / "scripts/run-pre-push-tests.sh").read_text()
    assert "set -euo pipefail" in runner
    assert runner.index("-m pytest -q") < runner.index("run check:browser")
    ci = yaml.safe_load((ROOT / ".github/workflows/knowledge-check.yml").read_text())
    steps = ci["jobs"]["frontend-gates"]["steps"]
    gate = next(s for s in steps if s.get("run") == "npm run check:browser")
    assert gate["env"]["PUBLIC_BASE_PATH"] == "/MyKnowledge/"
    assert "if" not in gate and not gate.get("continue-on-error")


def test_shared_proxy_rejects_non_loopback_and_keeps_rewrite():
    helper = (ROOT / "frontend/src/lib/local-api-proxy.mjs").as_uri()
    program = f"""
import {{localApiProxy}} from {json.dumps(helper)};
for(const target of ['https://127.0.0.1', 'http://localhost.evil.example', 'http://example.org']) {{
  let denied = false;
  try {{ localApiProxy(target, 'unused'); }} catch {{ denied = true; }}
  if(!denied) throw new Error('remote_proxy_allowed');
}}
const proxy = localApiProxy('http://127.0.0.1:8765','unused');
if(proxy.rewrite('/local-api/practice/questions') !== '/api/practice/questions') throw new Error('rewrite_drift');
"""
    subprocess.run(["node", "--input-type=module", "-e", program], check=True)
