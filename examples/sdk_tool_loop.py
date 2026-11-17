"""Live manual client-tool loop; uses a read-only fake order backend.

Adapted architecture, original implementation. Official tool protocol:
https://platform.claude.com/docs/en/agents-and-tools/tool-use/implement-tool-use
"""

from ccarf.architecture import run_loop
from ccarf.tools import LOOKUP_TOOL, dispatcher
from examples.common import client, model_id


def main():
    orders = {"O-100": {"customer_id": "C-7", "status": "paid", "paid_cents": 12000}}
    model = model_id()
    with client() as api:

        def request(history):
            response = api.messages.create(
                model=model,
                max_tokens=700,
                tools=[LOOKUP_TOOL],
                tool_choice={"type": "auto"},
                messages=history,
                system="Use order evidence. Never claim a refund was issued by this read-only tool.",
            )
            return response.model_dump(mode="json")

        result = run_loop(request, dispatcher(orders, "C-7"), "What is the status of O-100?")
    print(result.status, result.text)
    if result.status != "complete":
        raise RuntimeError("Agent stopped without a complete answer")


if __name__ == "__main__":
    main()
