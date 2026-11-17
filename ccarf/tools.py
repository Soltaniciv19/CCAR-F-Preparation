"""Domain 2: narrow tool contracts, typed errors and bounded read recovery."""

from __future__ import annotations

import time
from collections.abc import Callable

LOOKUP_TOOL = {
    "name": "lookup_order",
    "description": (
        "Read one order by exact order_id after customer authentication. "
        "Use for status and paid amount; never issues refunds. Returns an order record "
        "or null if no accessible match exists. Use order ID, not a customer name."
    ),
    "input_schema": {
        "type": "object",
        "properties": {"order_id": {"type": "string"}},
        "required": ["order_id"],
        "additionalProperties": False,
    },
}


def failure(category: str, code: str, retryable: bool, message: str) -> dict:
    return {
        "ok": False,
        "error": {"category": category, "code": code, "retryable": retryable, "message": message},
    }


def lookup_order(args: dict, *, customer_id: str | None, orders: dict) -> dict:
    """Validate at execution time even when the model supplies schema-valid input."""
    if not isinstance(args, dict) or set(args) != {"order_id"}:
        return failure("validation", "BAD_ARGUMENTS", False, "Supply only order_id")
    order_id = args["order_id"]
    if not isinstance(order_id, str) or not order_id.startswith("O-"):
        return failure("validation", "BAD_ORDER_ID", False, "Expected an O- identifier")
    if not customer_id:
        return failure("authorization", "UNAUTHENTICATED", False, "Authenticate first")
    order = orders.get(order_id)
    # Avoid leaking whether another customer's order exists.
    visible = order if order and order["customer_id"] == customer_id else None
    return {"ok": True, "data": dict(visible) if visible else None}


def retry_read(
    operation: Callable[[], dict], *, attempts: int = 3, sleep: Callable[[float], None] = time.sleep
) -> dict:
    """Read-only recovery. Writes require idempotency and unknown-outcome handling."""
    if attempts < 1:
        raise ValueError("attempts must be positive")
    result = None
    for attempt in range(attempts):
        try:
            result = operation()
        except TimeoutError:
            result = failure("transient", "TIMEOUT", True, "Read timed out")
        if result["ok"] or not result["error"]["retryable"]:
            break
        if attempt + 1 < attempts:
            sleep(0.1 * 2**attempt)
    return {**result, "attempts": attempt + 1}


def dispatcher(orders: dict, authenticated_customer: str | None) -> Callable:
    def execute(name: str, args: dict) -> dict:
        if name != "lookup_order":
            return failure("validation", "UNKNOWN_TOOL", False, "Tool not available to role")
        return lookup_order(args, customer_id=authenticated_customer, orders=orders)

    return execute
