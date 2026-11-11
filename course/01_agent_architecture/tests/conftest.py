import importlib.util
import os
from pathlib import Path

import pytest


@pytest.fixture
def module():
    root = Path(__file__).resolve().parents[1]
    relative = (
        "solution/solution.py" if os.getenv("COURSE_REFERENCE") == "1" else "exercise/attempt.py"
    )
    spec = importlib.util.spec_from_file_location("lesson_attempt", root / relative)
    loaded = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(loaded)
    return loaded
