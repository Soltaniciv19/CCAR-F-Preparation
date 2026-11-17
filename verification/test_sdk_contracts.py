"""Optional offline SDK serialization and real local MCP protocol checks. No paid API calls."""

import asyncio
import importlib.util
import json
import sys
import unittest
from pathlib import Path

SDK_AVAILABLE = all(
    importlib.util.find_spec(name) for name in ("anthropic", "claude_agent_sdk", "mcp")
)


@unittest.skipUnless(SDK_AVAILABLE, "Install .[sdk] for optional SDK and MCP checks")
class SDKContractTests(unittest.TestCase):
    def test_structured_request_serializes_current_field(self):
        import httpx2
        from anthropic import Anthropic

        from examples.sdk_structured import SCHEMA

        observed = []

        def respond(request):
            observed.append(json.loads(request.content))
            return httpx2.Response(
                200,
                json={
                    "id": "msg_offline",
                    "type": "message",
                    "role": "assistant",
                    "model": "test-model",
                    "content": [{"type": "text", "text": "{}"}],
                    "stop_reason": "end_turn",
                    "stop_sequence": None,
                    "usage": {"input_tokens": 1, "output_tokens": 1},
                },
            )

        with Anthropic(
            api_key="offline-placeholder",
            http_client=httpx2.Client(transport=httpx2.MockTransport(respond)),
        ) as api:
            message = api.messages.create(
                model="test-model",
                max_tokens=100,
                messages=[{"role": "user", "content": "test"}],
                output_config={"format": {"type": "json_schema", "schema": SCHEMA}},
            )
        self.assertEqual(message.stop_reason, "end_turn")
        self.assertEqual(observed[0]["output_config"]["format"]["schema"], SCHEMA)
        self.assertNotIn("output_format", observed[0])

    def test_agent_options_and_worker_types(self):
        from examples.sdk_agent import options

        config = options(Path("."))
        self.assertEqual(config.tools, ["Read", "Grep", "Glob", "Agent"])
        self.assertEqual(config.setting_sources, [])
        self.assertTrue(config.strict_mcp_config)
        self.assertEqual(config.agents["reviewer"].tools, ["Read", "Grep", "Glob"])
        self.assertEqual(config.agents["researcher"].maxTurns, 4)

    def test_fail_closed_hook_denies_without_trusted_approval(self):
        from examples.sdk_hooks import guard_refund, guarded_options

        result = asyncio.run(guard_refund({"tool_name": "mcp__billing__refund"}, "call", {}))
        self.assertEqual(result["hookSpecificOutput"]["permissionDecision"], "deny")
        self.assertEqual(guarded_options().hooks["PreToolUse"][0].on_failure, "block")

    def test_mcp_real_stdio_roundtrip_from_foreign_working_directory(self):
        from mcp import ClientSession
        from mcp.client.stdio import StdioServerParameters, stdio_client

        launcher = Path(__file__).resolve().parents[1] / "examples" / "launch_mcp.py"

        async def check():
            parameters = StdioServerParameters(
                command=sys.executable, args=[str(launcher)], cwd="/tmp"
            )
            async with stdio_client(parameters) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    tools = await session.list_tools()
                    self.assertIn("get_order", [tool.name for tool in tools.tools])
                    resources = await session.list_resources()
                    self.assertIn("orders://catalog", [str(r.uri) for r in resources.resources])
                    result = await session.call_tool("get_order", {"order_id": "O-100"})
                    self.assertFalse(result.is_error)
                    payload = json.loads(next(c.text for c in result.content if c.type == "text"))
                    self.assertTrue(payload["ok"])
                    self.assertEqual(payload["data"]["paid_cents"], 12000)
                    invalid = await session.call_tool("get_order", {"order_id": "bad"})
                    self.assertTrue(invalid.is_error)
                    absent = await session.call_tool("get_order", {"order_id": "O-missing"})
                    self.assertFalse(absent.is_error)
                    self.assertIsNone(absent.structured_content["data"])
                    catalog = await session.read_resource("orders://catalog")
                    self.assertIn("O-100", catalog.contents[0].text)

        asyncio.run(asyncio.wait_for(check(), timeout=20))


if __name__ == "__main__":
    unittest.main()
