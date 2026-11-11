"""Optional paid Agent SDK demonstration with a restricted tool set."""

import argparse
import asyncio
import os
import tempfile


def main():
    parser = argparse.ArgumentParser(description="Paid Claude Agent SDK example")
    parser.add_argument("--live", action="store_true", help="consent to a paid SDK call")
    args = parser.parse_args()
    if not args.live:
        parser.error("pass --live to consent to a paid call")
    model = os.environ.get("CLAUDE_AGENT_MODEL")
    if not model:
        parser.error("set CLAUDE_AGENT_MODEL to a model available to your SDK provider")
    from claude_agent_sdk import AgentDefinition, ClaudeAgentOptions, query

    async def run():
        with tempfile.TemporaryDirectory() as workspace:
            options = ClaudeAgentOptions(
                model=model,
                cwd=workspace,
                setting_sources=[],
                max_turns=3,
                max_budget_usd=0.25,
                tools=["Agent"],
                allowed_tools=["Agent"],
                agents={
                    "analyst": AgentDefinition(
                        description="Analyze a small synthetic research question.",
                        prompt="Analyze only the facts provided; state uncertainty.",
                        tools=[],
                    )
                },
            )
            async for message in query(
                prompt="Ask the analyst to compare these facts: policy A is dated 2024; policy B is dated 2025. State any uncertainty.",
                options=options,
            ):
                if hasattr(message, "result") and message.result:
                    print(message.result)

    asyncio.run(run())


if __name__ == "__main__":
    main()
