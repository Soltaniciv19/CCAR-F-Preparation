"""An offline Messages-style loop; scripted responses are not model evaluation."""

import json
from dataclasses import dataclass, field


@dataclass
class Result:
    status: str
    text: str = ""
    messages: list = field(default_factory=list)
    decision: dict = field(default_factory=dict)


def dispatch(name, arguments):
    if not isinstance(arguments, dict) or len(json.dumps(arguments, default=str)) > 2000:
        raise ValueError("tool input must be an object")
    if name == "lookup_order":
        if (
            set(arguments) != {"order_id"}
            or not isinstance(arguments["order_id"], str)
            or len(arguments["order_id"]) > 100
        ):
            raise ValueError("expected a string order_id")
        return {"order_id": arguments["order_id"], "status": "delivered"}
    if name == "get_policy":
        if arguments:
            raise ValueError("get_policy takes no arguments")
        return {"refund": "requires human authorization"}
    if name == "request_escalation":
        if set(arguments) != {"reason"} or not isinstance(arguments["reason"], str):
            raise ValueError("expected a reason")
        return {"queued_locally": True, "reason": arguments["reason"][:200]}
    if name == "refund":
        raise ValueError("refund denied: human policy gate")
    raise ValueError(f"unknown tool: {name}")


def run(client, prompt, max_turns=4):
    """Client.create receives messages and returns stop_reason and content dictionaries."""
    if not isinstance(prompt, str) or len(prompt) > 2000:
        return Result("invalid_input", "prompt must be a string of at most 2000 characters")
    messages = [{"role": "user", "content": prompt}]
    for _ in range(max_turns):
        response = client.create(messages=messages)
        content = response.get("content")
        if not isinstance(content, list) or any(not isinstance(b, dict) for b in content):
            return Result("protocol_error", "invalid content", messages)
        messages.append({"role": "assistant", "content": content})
        reason = response.get("stop_reason")
        if reason == "end_turn":
            text = "\n".join(b.get("text", "") for b in content if b.get("type") == "text")
            try:
                decision = json.loads(text)
                if (
                    not isinstance(decision, dict)
                    or set(decision) != {"action", "reason"}
                    or decision["action"] not in {"inform", "escalate"}
                    or not isinstance(decision["reason"], str)
                    or not decision["reason"]
                ):
                    raise ValueError
            except (ValueError, TypeError):
                return Result("invalid_decision", text, messages)
            return Result("complete", text, messages, decision)
        if reason != "tool_use":
            return Result(
                "truncated" if reason == "max_tokens" else "unexpected_stop", reason or "", messages
            )
        calls = [b for b in content if b.get("type") == "tool_use"]
        if not calls:
            return Result("protocol_error", "tool_use without calls", messages)
        ids = [call.get("id") for call in calls]
        if any(not isinstance(ident, str) or not ident for ident in ids) or len(set(ids)) != len(
            ids
        ):
            return Result("protocol_error", "missing or duplicate tool call ID", messages)
        results = []
        for call in calls:
            try:
                output = dispatch(call.get("name"), call.get("input"))
                results.append(
                    {
                        "type": "tool_result",
                        "tool_use_id": call["id"],
                        "content": json.dumps(output),
                    }
                )
            except ValueError as exc:
                results.append(
                    {
                        "type": "tool_result",
                        "tool_use_id": call["id"],
                        "content": str(exc),
                        "is_error": True,
                    }
                )
        messages.append({"role": "user", "content": results})
    return Result("turn_limit", "", messages)
