"""Live: capture a session and fork a follow-up, without editing files."""

import argparse
import asyncio
from pathlib import Path

from claude_agent_sdk import ClaudeAgentOptions, ResultMessage, query


def options(workspace: Path, **kwargs):
    return ClaudeAgentOptions(
        cwd=workspace.resolve(),
        tools=["Read", "Glob", "Grep"],
        allowed_tools=["Read", "Glob", "Grep"],
        permission_mode="dontAsk",
        setting_sources=[],
        mcp_servers={},
        strict_mcp_config=True,
        max_turns=4,
        max_budget_usd=0.5,
        **kwargs,
    )


async def run_once(prompt: str, config):
    terminal = None
    async for event in query(prompt=prompt, options=config):
        if isinstance(event, ResultMessage):
            terminal = event
    if terminal is None or terminal.is_error or terminal.subtype != "success":
        raise RuntimeError("No successful session result")
    return terminal.session_id, terminal.result


async def main(workspace: Path):
    session, report = await run_once(
        "Read README.md and summarize the Python entrypoint.", options(workspace)
    )
    print("Base session:", session, report)
    fork, alternative = await run_once(
        "Re-read current README.md. Identify a different organization for the entrypoint, without edits.",
        options(workspace, resume=session, fork_session=True),
    )
    print("Fork:", fork, alternative)
    if fork == session:
        raise RuntimeError("Expected a distinct forked session")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace", required=True, type=Path)
    args = parser.parse_args()
    if not args.workspace.is_dir():
        parser.error("workspace must be a disposable directory")
    asyncio.run(main(args.workspace))
