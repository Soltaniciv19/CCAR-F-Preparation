"""Illustrate holdout scoring with fixed predictions, not generated output."""

import json
from pathlib import Path
from pipeline import evaluate

fixtures = json.loads(
    (Path(__file__).resolve().parents[1] / "fixtures" / "receipts.json").read_text()
)
expected = {item["id"]: item["merchant"] for item in fixtures}
variants = {
    "vague simulation": {"r1": "Maple Books", "r2": None, "r3": None},
    "explicit simulation": {"r1": "Maple Books", "r2": "North Cafe", "r3": None},
    "few-shot simulation": {"r1": "Maple Books", "r2": "North Cafe", "r3": None},
}
for name, predictions in variants.items():
    print(name, evaluate(expected, predictions))
