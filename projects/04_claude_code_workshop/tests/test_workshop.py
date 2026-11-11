import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = Path(os.environ.get("P4_WORKSPACE", ROOT / "solution"))


def run(*args):
    return subprocess.run(
        [sys.executable, str(WORKSPACE / "app.py"), *map(str, args)], capture_output=True, text=True
    )


def test_discount_excludes_shipping():
    result = run(100, 0.1, 10)
    assert result.returncode == 0
    assert json.loads(result.stdout)["total"] == 100


def test_zero_and_invalid_values():
    assert json.loads(run(0, 0, 0).stdout)["total"] == 0
    for args in [(-1, 0, 0), (1, 1.1, 0), (1, 0, -1), ("nan", 0, 1), (1, "inf", 0)]:
        assert run(*args).returncode != 0
