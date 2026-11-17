"""Absolute-script entrypoint for MCP hosts with a different working directory."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from examples.mcp_order_server import server  # noqa: E402

if __name__ == "__main__":
    server.run(transport="stdio")
