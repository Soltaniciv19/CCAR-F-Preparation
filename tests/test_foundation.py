"""Smoke checks for the course's offline foundation."""

import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


def test_setup_reference():
    path = ROOT / "course/00_setup/solution/budget.py"
    spec = importlib.util.spec_from_file_location("setup_solution", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert module.remaining(3, 1) == 2
    assert module.remaining(1, 3) == 0
    with pytest.raises(ValueError):
        module.remaining(0, -1)


def test_tutor_and_progress_exist():
    assert (ROOT / "CLAUDE.md").is_file()
    assert (ROOT / "progress.md").is_file()
