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
