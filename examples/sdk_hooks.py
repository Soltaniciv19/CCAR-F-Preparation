"""Construct a fail-closed PreToolUse gate. No network calls on import or execution.

https://code.claude.com/docs/en/agent-sdk/hooks
The demo does not register an actual billing tool; authorization remains in its service.
"""

import asyncio

from claude_agent_sdk import ClaudeAgentOptions, HookMatcher


async def guard_refund(input_data, tool_use_id, context):
    if input_data.get("tool_name") == "mcp__billing__refund":
        # No trusted approval store is wired in this standalone demonstration: deny.
        return {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": "Trusted approval record required; none configured",
            }
        }
    return {}


def guarded_options():
    return ClaudeAgentOptions(
        hooks={
            "PreToolUse": [
                HookMatcher(
                    matcher="^mcp__billing__refund$", hooks=[guard_refund], on_failure="block"
                )
            ]
        },
        setting_sources=[],
        strict_mcp_config=True,
    )


if __name__ == "__main__":
    print(asyncio.run(guard_refund({"tool_name": "mcp__billing__refund"}, "demo", {})))
