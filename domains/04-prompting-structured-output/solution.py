"""Runnable offline worked solution. Run this file from any working directory."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from ccarf.extraction import correlate_batch, validate_invoice

source = "Total: 135.00"
record = {
    "items": [{"quantity": 2, "unit_price": "40.00"}, {"quantity": 1, "unit_price": "45.00"}],
    "stated_total": "135.00",
    "po_number": None,
    "evidence": {"stated_total": {"start": 7, "end": 13, "quote": "135.00"}},
}
print("Preserved conflict:", validate_invoice(record, source))
print(
    "Out-of-order results:",
    correlate_batch(
        {"a", "b"},
        [
            {"custom_id": "b", "result": {"type": "expired"}},
            {"custom_id": "a", "result": {"type": "succeeded"}},
        ],
    ),
)
