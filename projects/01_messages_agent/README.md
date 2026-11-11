# P1: Messages-style support agent

**Time:** 90 minutes. **Prerequisites:** D1, D2, D4. **Mode:** offline simulation; no network or charges.

Build a bounded support loop. The supplied client has `create(messages=...)` and returns a dictionary with `stop_reason` and `content`. Keep every assistant content block; dispatch every `tool_use`, then append one user message containing matching `tool_result` blocks. Require a JSON final decision with exactly `action` (`inform` or `escalate`) and a nonempty `reason`; return it in `Result.decision`. Reject malformed decisions, oversized prompts and missing or duplicate call IDs. Return a `Result` on final response, truncation, unexpected stop, protocol error, or turn limit. Errors from tools must be returned to the model as error results. No refund can bypass a deterministic human policy gate. Escalation only creates a simulated local result.

Implement `starter/support_agent.py` and run:

```sh
cd projects/01_messages_agent
PYTHONPATH=starter pytest tests -q
```

Compare the reference only after your attempt: `PYTHONPATH=solution pytest tests -q`. Inspect the trace and explain why preserving IDs and complete assistant content matters. Tests exercise the contract, not actual model quality or the full Anthropic API. For a real Messages API application, consult the [current tool-use protocol](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview), configure an available model and credentials separately, and obtain consent before paid calls; the default exercise is offline.

**Extension:** record a structured audit event for each tool result. **Reflection:** when should an unknown tool result end the workflow instead of returning feedback?

The optional `solution/live.py --live` adapter sends a synthetic prompt to the Messages API and may incur charges. Set `ANTHROPIC_MODEL` to a currently available API model and `ANTHROPIC_API_KEY` in your environment (never in chat); install the project's live dependencies first. From this directory run `PYTHONPATH=solution python solution/live.py --live` only after consenting to the paid calls. It reports token usage and uses bounded turns, timeout and retries. Live behavior has not been tested with credentials.
