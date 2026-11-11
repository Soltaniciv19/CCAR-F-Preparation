"""Connect the capstone to P3's real local MCP server without a model call."""

import asyncio
import json
from pathlib import Path
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from assistant import assist

SERVER = Path(__file__).resolve().parents[2] / "03_mcp" / "solution" / "order_server.py"


async def run(order_id, max_calls=2):
    """Collect two MCP results and pass conservative interpretations to the gate."""
    request = {"order_id": order_id, "requested_action": "refund"}
    calls = 0

    def escalate(reason):
        return {
            "decision": "escalate",
            "coverage": "partial",
            "reason": reason,
            "mcp_calls": calls,
            "handoff": {"order_id": order_id, "reason": reason, "coverage": "partial"},
        }

    if not isinstance(order_id, str) or not order_id.strip() or max_calls < 2:
        return escalate("invalid request or insufficient MCP call budget")
    server = StdioServerParameters(command=sys.executable, args=[str(SERVER)])
    try:
        async with stdio_client(server) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                calls += 1
                result = await session.call_tool("lookup_order", {"order_id": order_id})
                if result.is_error:
                    return escalate("MCP order tool failed")
                data = result.structured_content or json.loads(result.content[0].text)
                if "order" not in data:
                    return escalate(str(data.get("error", "missing order")))
                calls += 1
                resource = await session.read_resource("policy://refund")
                text = resource.contents[0].text
    except Exception:
        return escalate("MCP server or transport unavailable")

    class CollectedServices:
        def get_order(self, _order_id):
            # P3's delivered status does not establish refund eligibility.
            return {"eligible": None}

        def get_policies(self):
            # The P3 resource does not provide a dated, machine-readable decision.
            return [{"id": "policy://refund", "date": None, "refund_allowed": None, "text": text}]

    decision = assist(request, CollectedServices(), max_calls=max_calls)
    decision["mcp_calls"] = calls
    decision["source"] = {"id": "policy://refund", "date": None, "text": text}
    return decision


if __name__ == "__main__":
    print(json.dumps(asyncio.run(run(sys.argv[1] if len(sys.argv) > 1 else "order-1")), indent=2))
