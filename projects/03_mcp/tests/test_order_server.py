import asyncio
import json
import sys

import order_server
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


def test_local_mcp_client_lifecycle():
    async def check():
        server = StdioServerParameters(command=sys.executable, args=[order_server.__file__])
        async with stdio_client(server) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                tools = await session.list_tools()
                assert {tool.name for tool in tools.tools} == {"lookup_order", "get_policy"}
                resources = await session.list_resources()
                assert str(resources.resources[0].uri) == "policy://refund"
                policy = await session.read_resource("policy://refund")
                assert "human" in policy.contents[0].text
                for order_id, expected in [
                    ("order-1", "order"),
                    ("missing", "not_found"),
                    ("temporary-error", "temporarily_unavailable"),
                ]:
                    result = await session.call_tool("lookup_order", {"order_id": order_id})
                    data = result.structured_content or json.loads(result.content[0].text)
                    assert expected in data or data.get("error") == expected
                    if order_id == "temporary-error":
                        assert data["retryable"] is True
                bad = await session.call_tool("lookup_order", {"order_id": 4})
                assert bad.is_error

    asyncio.run(check())
