"""Bootstrap runtime-path regression checks."""

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_bootstrap_script_is_valid_and_uses_migrated_simple_path():
    script = (ROOT / "scripts" / "bootstrap.sh").read_text(encoding="utf-8")
    result = subprocess.run(["bash", "-n", str(ROOT / "scripts" / "bootstrap.sh")])
    assert result.returncode == 0
    assert 'SIMPLE_LIB_DIR="${ROOT}/var/state/lib"' in script
    assert "state/lib" not in script.replace("var/state/lib", "")
    assert 'mkdir -p "$SIMPLE_LIB_DIR"' in script


def test_start_scripts_are_valid_and_bind_loopback():
    backend = ROOT / "scripts" / "start-backend.sh"
    frontend = ROOT / "scripts" / "start-frontend.sh"
    for path in (backend, frontend):
        result = subprocess.run(["bash", "-n", str(path)], check=False)
        assert result.returncode == 0, path
        text = path.read_text(encoding="utf-8")
        assert "127.0.0.1" in text
        assert "0.0.0.0" not in text
    backend_text = backend.read_text(encoding="utf-8")
    assert ".venv/bin/python" in backend_text
    assert "backend.server" in backend_text
    frontend_text = frontend.read_text(encoding="utf-8")
    assert "MYKNOWLEDGE_CONTENT_MODE=" in frontend_text
    assert "prepare-content.mjs" in frontend_text
    assert "node_modules/.bin/astro" in frontend_text
    assert "先跑" not in frontend_text
    assert "自动重连" in frontend_text
