"""One deterministic trace across loop, tools and extraction. No API calls."""

from ccarf.architecture import run_loop
from ccarf.extraction import validate_invoice
from ccarf.tools import dispatcher


def main():
    responses = iter(
        [
            {
                "stop_reason": "tool_use",
                "content": [
                    {"type": "text", "text": "I will check the order."},
                    {
                        "type": "tool_use",
                        "id": "call-1",
                        "name": "lookup_order",
                        "input": {"order_id": "O-100"},
                    },
                ],
            },
            {
                "stop_reason": "end_turn",
                "content": [
                    {"type": "text", "text": "The order is paid. No refund has been requested."}
                ],
            },
        ]
    )
    orders = {"O-100": {"customer_id": "C-7", "status": "paid", "paid_cents": 12000}}
    result = run_loop(lambda history: next(responses), dispatcher(orders, "C-7"), "Check O-100")
    print("Loop:", result.status, "turns:", result.turns, "answer:", result.text)
    print("Tool evidence:", result.history[2]["content"][0]["content"])
    source = "Total: 135.00"
    record = {
        "items": [{"quantity": 2, "unit_price": "40.00"}, {"quantity": 1, "unit_price": "45.00"}],
        "stated_total": "135.00",
        "po_number": None,
        "evidence": {"stated_total": {"start": 7, "end": 13, "quote": "135.00"}},
    }
    print("Invoice:", validate_invoice(record, source))


if __name__ == "__main__":
    main()
