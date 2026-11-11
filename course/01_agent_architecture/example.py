"""A simulated tool round: no model or network access."""

requests = [
    {"id": "a", "name": "lookup", "input": {"order_id": "O-1"}},
    {"id": "b", "name": "policy", "input": {}},
]
print("assistant requests:", requests)
print(
    "user tool results:", [{"tool_use_id": item["id"], "result": "simulated"} for item in requests]
)
print("next step: send every result, then wait for a final response")
