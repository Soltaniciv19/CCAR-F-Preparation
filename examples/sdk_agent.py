"""Live Agent SDK: read-only researcher/reviewer configuration and events.

https://code.claude.com/docs/en/agent-sdk/python
"""

import argparse
import asyncio
from pathlib import Path

from claude_agent_sdk import AgentDefinition, ClaudeAgentOptions, ResultMessage, ToolUseBlock, query


def options(workspace: Path) -> ClaudeAgentOptions:
    return ClaudeAgentOptions(
        cwd=workspace.resolve(),
        tools=["Read", "Grep", "Glob", "Agent"],
        allowed_tools=["Read", "Grep", "Glob", "Agent"],
        permission_mode="dontAsk",
        setting_sources=[],
        mcp_servers={},
        strict_mcp_config=True,
        max_turns=8,
        max_budget_usd=1.0,
        agents={
            "researcher": AgentDefinition(
                description="Trace Python call paths with exact file evidence",
                prompt="Read only. Return paths, symbols, observations and limitations.",
                tools=["Read", "Grep", "Glob"],
                maxTurns=4,
            ),
            "reviewer": AgentDefinition(
                description="Verify supplied findings against repository evidence",
                prompt="Check supplied claims; report unsupported assumptions and missing evidence.",
                tools=["Read", "Grep", "Glob"],
                maxTurns=4,
            ),
        },
    )


async def inspect(workspace: Path):
    success = False
    async for message in query(
        prompt=(
            "Use researcher to inspect README claims about the main Python entrypoint. "
            "Then pass its exact findings and paths to reviewer. Report verified facts and gaps."
        ),
        options=options(workspace),
    ):
        for block in getattr(message, "content", []) or []:
            if isinstance(block, ToolUseBlock) and block.name in {"Agent", "Task"}:
                print("Delegation:", block.name, block.id)
        if isinstance(message, ResultMessage):
            print("Session:", message.session_id, "status:", message.subtype)
            print(message.result)
            success = message.subtype == "success" and not message.is_error
    if not success:
        raise RuntimeError("No successful terminal Agent SDK result")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace", required=True, type=Path)
    args = parser.parse_args()
    if not args.workspace.is_dir():
        parser.error("workspace must be an existing disposable directory")
    asyncio.run(inspect(args.workspace))


if __name__ == "__main__":
    main()
