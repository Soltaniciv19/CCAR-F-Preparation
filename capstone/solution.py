"""Offline capstone: application-owned identity, gated refund, safe replay, handoff.

This is a deterministic support harness, not a live model or payment integration.
The model-facing executor cannot choose the authenticated customer identity.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field

from ccarf.architecture import Order, RefundService
from ccarf.reliability import route_case
from ccarf.tools import failure


@dataclass
class Case:
    case_id: str
    authenticated_customer: str | None
    concerns: list[str]
    operations: list[dict] = field(default_factory=list)


class SupportApplication:
    def __init__(self):
        self.billing = RefundService({"O-100": Order("C-7", 12000)})

    def execute_refund(
        self,
        case: Case,
        args: dict,
        *,
        confirmed_order_id: str,
        confirmed_amount: int,
        operation_key: str,
    ) -> dict:
        # Confirmation and operation identity originate in trusted application state
        # for this user-confirmed action, not in model-generated tool arguments.
        if not isinstance(args, dict) or set(args) != {"order_id", "amount_cents"}:
            return failure("validation", "BAD_ARGUMENTS", False, "Unexpected fields")
        if args["order_id"] != confirmed_order_id:
            return failure(
                "validation", "UNCONFIRMED_ORDER", False, "Order differs from confirmation"
            )
        if type(args["amount_cents"]) is not int or args["amount_cents"] != confirmed_amount:
            return failure(
                "validation", "UNCONFIRMED_AMOUNT", False, "Amount differs from confirmation"
            )
        try:
            receipt = self.billing.refund(
                authenticated_customer=case.authenticated_customer,
                order_id=args["order_id"],
                amount_cents=args["amount_cents"],
                idempotency_key=operation_key,
            )
        except PermissionError as exc:
            return failure("authorization_or_policy", "BLOCKED", False, str(exc))
        except ValueError as exc:
            return failure("validation", "INVALID_REFUND", False, str(exc))
        if not any(r["receipt_id"] == receipt["receipt_id"] for r in case.operations):
            case.operations.append(receipt)
        return {"ok": True, "data": receipt}

    def handoff(
        self, case: Case, reason: str, partial_findings: list[dict], pending: list[str]
    ) -> dict:
        return {
            "case_id": case.case_id,
            "customer_id": case.authenticated_customer,
            "concerns": case.concerns,
            "reason": reason,
            "confirmed_operations": case.operations.copy(),
            "partial_findings": partial_findings,
            "pending": pending,
            "next_action": "Human review of remaining concern; do not repeat committed operations",
        }


def main():
    app = SupportApplication()
    case = Case("CASE-8", "C-7", ["duplicate_charge", "missing_delivery"])
    args = {"order_id": "O-100", "amount_cents": 1200}
    first = app.execute_refund(
        case,
        args,
        confirmed_order_id="O-100",
        confirmed_amount=1200,
        operation_key="CASE-8-billing",
    )
    replay = app.execute_refund(
        case,
        args,
        confirmed_order_id="O-100",
        confirmed_amount=1200,
        operation_key="CASE-8-billing",
    )
    assert replay == first
    assert app.billing.refunded["O-100"] == 1200
    print("Refund:", json.dumps(first))
    print("Replay returned same receipt:", replay == first)
    reason = route_case(recovery_exhausted=True)
    packet = app.handoff(
        case,
        reason,
        [{"topic": "billing", "source": first["data"]["receipt_id"], "status": "confirmed"}],
        ["delivery_status_unavailable_after_bounded_read_recovery"],
    )
    print("Handoff:", json.dumps(packet, indent=2))


if __name__ == "__main__":
    main()
