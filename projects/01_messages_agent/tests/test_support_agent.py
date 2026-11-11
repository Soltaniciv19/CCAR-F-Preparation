import json
from support_agent import dispatch, run
import pytest


class Script:
    def __init__(self, replies):
        self.replies = iter(replies)
        self.snapshots = []

    def create(self, *, messages):
        self.snapshots.append(json.loads(json.dumps(messages)))
        return next(self.replies)


def call(id, name, data):
    return {"type": "tool_use", "id": id, "name": name, "input": data}


def test_multiple_calls_preserve_history_and_ids():
    blocks = [
        {"type": "text", "text": "Checking"},
        call("a", "lookup_order", {"order_id": "42"}),
        call("b", "get_policy", {}),
    ]
    client = Script(
        [
            {"stop_reason": "tool_use", "content": blocks},
            {
                "stop_reason": "end_turn",
                "content": [
                    {"type": "text", "text": '{"action":"escalate","reason":"Human review"}'}
                ],
            },
        ]
    )
    result = run(client, "Help")
    assert result.status == "complete" and result.decision["action"] == "escalate"
    assert client.snapshots[1][1]["content"] == blocks
    assert [item["tool_use_id"] for item in client.snapshots[1][2]["content"]] == ["a", "b"]


def test_errors_are_tool_results_and_refund_denied():
    client = Script(
        [
            {
                "stop_reason": "tool_use",
                "content": [
                    call("a", "missing", {}),
                    call("b", "lookup_order", {}),
                    call("c", "refund", {}),
                ],
            },
            {"stop_reason": "end_turn", "content": []},
        ]
    )
    result = run(client, "Help")
    assert all(x["is_error"] for x in result.messages[2]["content"])
    with pytest.raises(ValueError, match="denied"):
        dispatch("refund", {})


def test_bounded_and_truncated():
    assert run(Script([{"stop_reason": "max_tokens", "content": []}]), "x").status == "truncated"
    assert (
        run(
            Script([{"stop_reason": "tool_use", "content": [call("1", "get_policy", {})]}]), "x", 1
        ).status
        == "turn_limit"
    )
    assert run(Script([{"stop_reason": "tool_use", "content": []}]), "x").status == "protocol_error"


def test_invalid_decision_and_tool_ids():
    assert (
        run(
            Script(
                [{"stop_reason": "end_turn", "content": [{"type": "text", "text": "not JSON"}]}]
            ),
            "x",
        ).status
        == "invalid_decision"
    )
    for calls in (
        [{"type": "tool_use", "name": "get_policy", "input": {}}],
        [call("a", "get_policy", {}), call("a", "get_policy", {})],
    ):
        assert (
            run(Script([{"stop_reason": "tool_use", "content": calls}]), "x").status
            == "protocol_error"
        )
    assert run(Script([]), "x" * 2001).status == "invalid_input"
