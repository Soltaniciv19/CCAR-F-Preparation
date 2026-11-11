import importlib.util
from pathlib import Path

import pytest

path = Path(__file__).parents[1] / "exercise" / "budget.py"
spec = importlib.util.spec_from_file_location("budget", path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_remaining():
    assert module.remaining(5, 2) == 3
    assert module.remaining(2, 5) == 0


def test_negative_rejected():
    with pytest.raises(ValueError):
        module.remaining(-1, 0)
