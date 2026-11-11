"""Example tool metadata, not an MCP server."""

tool = {
    "name": "lookup_order",
    "description": "Read a synthetic order by exact ID; does not modify it.",
    "input_schema": {
        "type": "object",
        "properties": {"order_id": {"type": "string"}},
        "required": ["order_id"],
        "additionalProperties": False,
    },
}
print(tool)
