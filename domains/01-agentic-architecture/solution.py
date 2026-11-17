"""Runnable offline worked solution. Run this file from any working directory."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from ccarf.architecture import Order, RefundService, uncovered
from examples.offline_demo import main

main()
service = RefundService({"O-100": Order("C-7", 12000)})
request = dict(
    authenticated_customer="C-7", order_id="O-100", amount_cents=1200, idempotency_key="one"
)
receipt = service.refund(**request)
assert service.refund(**request) == receipt
print("Idempotent receipt:", receipt)
print(
    "Missing scope:",
    uncovered({"price", "privacy"}, [{"status": "complete", "covered_topics": ["price"]}]),
)
