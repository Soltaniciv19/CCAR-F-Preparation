"""Runnable offline worked solution. Run this file from any working directory."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import json
from types import SimpleNamespace

from ccarf.workflows import new_findings, run_review


def fake_cli(*args, **kwargs):
    print("Noninteractive command:", args[0])
    return SimpleNamespace(
        stdout=json.dumps(
            {"subtype": "success", "is_error": False, "structured_output": {"findings": []}}
        )
    )


print("Review:", run_review("Review the supplied patch and tests", Path("."), runner=fake_cli))
old = {"path": "billing.py", "line": 10, "category": "units", "evidence": "qty * price"}
print("New comments after a line move:", new_findings([{**old, "line": 20}], [old]))
