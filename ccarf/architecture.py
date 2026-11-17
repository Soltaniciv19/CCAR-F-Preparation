"""Domain 1: protocol-driven loops and application-owned workflow gates."""

from __future__ import annotations

import json
from collections.abc import Callable
from copy import deepcopy
from dataclasses import dataclass
from threading import Lock


@dataclass(frozen=True)
class RunResult:
    status: str
    text: str
    turns: int
    history: list[dict]


def run_loop(
    request: Callable[[list[dict]], dict],
    execute: Callable[[str, dict], dict],
    prompt: str,
    max_turns: int = 8,
) -> RunResult:
    """Transport-neutral Messages loop; request returns a complete message dict.

    The cap is a resource limit, never a successful-completion signal.
    Tool calls are sequential; parallel execution needs a dependency/side-effect policy.
    """
    if max_turns < 1:
        raise ValueError("max_turns must be positive")
    history = [{"role": "user", "content": prompt}]
    for turn in range(1, max_turns + 1):
        message = request(deepcopy(history))
        content = message["content"]
        history.append({"role": "assistant", "content": content})
        reason = message["stop_reason"]
        text = "".join(b["text"] for b in content if b["type"] == "text")
        calls = [b for b in content if b["type"] == "tool_use"]
        if reason == "end_turn":
            if calls:
                raise ValueError("Unexpected client tool calls on end_turn")
            return RunResult("complete", text, turn, history)
        if reason != "tool_use":
            # max_tokens, refusal, pause_turn, etc. require distinct caller handling.
            return RunResult(f"incomplete:{reason}", text, turn, history)
        if not calls or len({c["id"] for c in calls}) != len(calls):
            raise ValueError("Tool-use response needs distinct call IDs")
        results = []
        for call in calls:
            outcome = execute(call["name"], call["input"])
            results.append(
                {
                    "type": "tool_result",
                    "tool_use_id": call["id"],
                    "content": json.dumps(outcome),
                    "is_error": not outcome["ok"],
                }
            )
        history.append({"role": "user", "content": results})
    return RunResult("budget_exhausted", "", max_turns, history)


@dataclass(frozen=True)
class Order:
    customer_id: str
    paid_cents: int
    refundable: bool = True


class RefundService:
    """In-memory lab ledger. Trusted identity comes from authentication, not model input.

    A real service needs durable transactions and provider idempotency/reconciliation.
    """

    def __init__(self, orders: dict[str, Order]):
        self.orders = dict(orders)
        self.refunded: dict[str, int] = {}
        self.receipts: dict[str, tuple[tuple, dict]] = {}
        self._lock = Lock()

    def refund(
        self,
        *,
        authenticated_customer: str | None,
        order_id: str,
        amount_cents: int,
        idempotency_key: str,
    ) -> dict:
        if not authenticated_customer:
            raise PermissionError("Verified identity required")
        if type(amount_cents) is not int or amount_cents <= 0:
            raise ValueError("Positive integer cents required")
        if not isinstance(idempotency_key, str) or not idempotency_key.strip():
            raise ValueError("Idempotency key required")
        fingerprint = (authenticated_customer, order_id, amount_cents)
        with self._lock:
            order = self.orders.get(order_id)
            if order is None or order.customer_id != authenticated_customer:
                raise PermissionError("Order not available to authenticated customer")
            if idempotency_key in self.receipts:
                previous, receipt = self.receipts[idempotency_key]
                if previous != fingerprint:
                    raise ValueError("Idempotency key reused for a different request")
                return dict(receipt)
            if not order.refundable:
                raise PermissionError("Policy exception requires human review")
            if self.refunded.get(order_id, 0) + amount_cents > order.paid_cents:
                raise ValueError("Refund exceeds remaining paid amount")
            receipt = {
                "status": "committed",
                "order_id": order_id,
                "amount_cents": amount_cents,
                "receipt_id": f"R-{len(self.receipts) + 1}",
            }
            self.refunded[order_id] = self.refunded.get(order_id, 0) + amount_cents
            self.receipts[idempotency_key] = (fingerprint, receipt)
            return dict(receipt)


def uncovered(required: set[str], worker_results: list[dict]) -> set[str]:
    """Completed tasks do not imply complete subject coverage."""
    covered = set()
    for result in worker_results:
        if result["status"] == "complete":
            covered.update(result.get("covered_topics", []))
    return required - covered
