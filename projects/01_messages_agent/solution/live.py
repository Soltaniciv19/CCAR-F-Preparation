"""Explicitly opt in to a paid Anthropic Messages API example."""

import argparse
import os

from support_agent import run

TOOLS = [
    {
        "name": "lookup_order",
        "description": "Look up a synthetic order by ID.",
        "input_schema": {
            "type": "object",
            "properties": {"order_id": {"type": "string"}},
            "required": ["order_id"],
            "additionalProperties": False,
        },
    },
    {
        "name": "get_policy",
        "description": "Read the simulated refund policy.",
        "input_schema": {"type": "object", "properties": {}, "additionalProperties": False},
    },
    {
        "name": "request_escalation",
        "description": "Record a local simulated escalation; no message is sent.",
        "input_schema": {
            "type": "object",
            "properties": {"reason": {"type": "string"}},
            "required": ["reason"],
            "additionalProperties": False,
        },
    },
]


class MessagesClient:
    def __init__(self, client, model):
        self.client = client
        self.model = model

    def create(self, *, messages):
        response = self.client.messages.create(
            model=self.model, max_tokens=256, messages=messages, tools=TOOLS
        )
        print(
            f"Usage: {response.usage.input_tokens} input, {response.usage.output_tokens} output tokens"
        )
        return {
            "stop_reason": response.stop_reason,
            "content": [block.model_dump(exclude_none=True) for block in response.content],
        }


def main():
    parser = argparse.ArgumentParser(description="Paid live Messages API example")
    parser.add_argument("--live", action="store_true", help="consent to a paid API call")
    args = parser.parse_args()
    if not args.live:
        parser.error("pass --live to consent to paid API calls")
    model = os.environ.get("ANTHROPIC_MODEL")
    if not model or not os.environ.get("ANTHROPIC_API_KEY"):
        parser.error("set ANTHROPIC_MODEL and ANTHROPIC_API_KEY in your environment")
    import anthropic

    client = anthropic.Anthropic(timeout=30, max_retries=1)
    result = run(
        MessagesClient(client, model),
        "My synthetic order order-1 arrived. What is the refund policy? Return only JSON with action (inform or escalate) and reason.",
        max_turns=4,
    )
    print(f"Status: {result.status}\n{result.text}")


if __name__ == "__main__":
    main()
