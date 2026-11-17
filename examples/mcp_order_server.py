"""Local read-only MCP server, pinned to the official MCP Python SDK v2.

Run: python -m examples.mcp_order_server (waits for stdio MCP protocol).
Reference: https://py.sdk.modelcontextprotocol.io/get-started/
"""

import json

from mcp import types
from mcp.server import MCPServer

from ccarf.tools import lookup_order

server = MCPServer("CCAR-F read-only order lab")
ORDERS = {"O-100": {"customer_id": "C-7", "status": "paid", "paid_cents": 12000}}


@server.tool()
def get_order(order_id: str) -> types.CallToolResult:
    """Read one exact order for the lab's fixed authenticated customer; never modifies it.

    This local fixture has no real customer authentication or remote multi-tenant deployment.
    """
    outcome = lookup_order({"order_id": order_id}, customer_id="C-7", orders=ORDERS)
    return types.CallToolResult(
        content=[types.TextContent(type="text", text=json.dumps(outcome))],
        structured_content=outcome,
        is_error=not outcome["ok"],
    )


@server.resource("orders://catalog")
def catalog() -> str:
    """Describe available fixture data and schema without exploratory order scans."""
    return json.dumps(
        {
            "fixture_order_ids": ["O-100"],
            "fields": ["customer_id", "status", "paid_cents"],
            "scope": "local fixture only",
        }
    )


if __name__ == "__main__":
    server.run(transport="stdio")
