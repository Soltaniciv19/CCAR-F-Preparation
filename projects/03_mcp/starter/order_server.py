"""Implement a local MCP server with the official Python SDK."""

from mcp.server import MCPServer

mcp = MCPServer("synthetic-orders")

# Add lookup_order, get_policy, and the policy://refund resource here.

if __name__ == "__main__":
    mcp.run(transport="stdio")
