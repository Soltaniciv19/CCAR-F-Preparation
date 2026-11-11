"""A synthetic, read-only MCP server using the official Python SDK."""

from mcp.server import MCPServer

mcp = MCPServer("synthetic-orders")
ORDERS = {"order-1": {"id": "order-1", "status": "delivered"}}
POLICY = "Refund requests require human review."


@mcp.tool()
def lookup_order(order_id: str) -> dict:
    """Look up one synthetic order by its ID; no real order system is accessed."""
    if not order_id or len(order_id) > 100:
        return {"error": "invalid_input", "retryable": False}
    if order_id == "temporary-error":
        return {"error": "temporarily_unavailable", "retryable": True}
    if order_id not in ORDERS:
        return {"error": "not_found", "retryable": False}
    return {"order": ORDERS[order_id]}


@mcp.tool()
def get_policy() -> str:
    """Read the simulated refund policy."""
    return POLICY


@mcp.resource("policy://refund")
def refund_policy() -> str:
    """The read-only synthetic refund policy."""
    return POLICY


if __name__ == "__main__":
    mcp.run(transport="stdio")
