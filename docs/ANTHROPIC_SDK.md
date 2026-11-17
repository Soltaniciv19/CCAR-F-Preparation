# Anthropic SDKs: mental model, API patterns and Python examples

## Choose the abstraction deliberately

| Component | What it supplies | What your code still owns |
|---|---|---|
| `anthropic` Python SDK | Typed Claude API requests, streaming, parsing helpers, batch endpoints, errors | Client-tool execution, trusted state, business authorization and orchestration |
| `claude-agent-sdk` | Claude Code's agent runtime, built-in tools, subagents, hooks, sessions and event stream | Capability design, deployment isolation, service policy and outcome validation |
| Claude Code CLI | Interactive/noninteractive repository workflows and configuration | Repository standards, CI credentials, output handling and review policy |
| `mcp` Python SDK | Standardized server/client capability interfaces and transports | Handler semantics, authentication integration, data scope and service operations |

Do not implement a second Messages loop inside `query()` just because both use a Claude model. Agent SDK already owns an execution loop. Conversely, `client.messages.create()` does not execute your local Python tool by itself.

## 1. Configuration and a minimal Messages call

The official SDK reads `ANTHROPIC_API_KEY` by default. Our [common configuration](../examples/common.py) supplies a bounded timeout and retry count, and requires `ANTHROPIC_MODEL` so you select an account-enabled model. Secrets are neither checked in nor printed.

The essential pattern is the same as the [official Python SDK getting-started example](https://github.com/anthropics/anthropic-sdk-python):

```python
from anthropic import Anthropic

client = Anthropic()
message = client.messages.create(
    model=model_id,
    max_tokens=300,
    messages=[{"role": "user", "content": "Explain a policy gate."}],
)
```

Here `model_id` is your configured string. The course's executable version is [sdk_messages.py](../examples/sdk_messages.py); the small snippet above is an adaptation of the public API pattern, not a standalone script. A system instruction is supplied through the request's `system` argument, not by inventing a `system` entry in the Messages conversation array.

Responses contain structured content blocks. Filter text blocks when rendering prose, but preserve the complete content for a subsequent tool loop. Inspect `stop_reason` before treating the answer as complete. Record model, usage and request metadata appropriate to your privacy requirements. Usage is observed after the call; token counting is a planning estimate before it.

Official reference: [Python SDK](https://platform.claude.com/docs/en/api/sdks/python).

## 2. Streaming and asynchronous applications

`client.messages.stream(...)` is a context manager. Iterate `text_stream` for incremental display, then get the final message to inspect completion and usage. Receiving some text does not imply the final stream succeeded; network failure or truncation can occur after a useful-looking prefix.

Use `AsyncAnthropic` when integrating into an async service. Await requests, use async streaming interfaces and limit concurrency deliberately. Async I/O improves overlap of independent waits; it does not make a dependent workflow parallel or provide transaction isolation. Keep request, tool and deadline budgets visible across the whole operation.

The course's [streaming example](../examples/sdk_messages.py) makes two generation requests to compare ordinary and streaming output. Do not mistake that demonstration for one request billed twice by streaming itself.

## 3. Manual client-tool loop

[sdk_tool_loop.py](../examples/sdk_tool_loop.py) adapts SDK responses into the offline loop. `LOOKUP_TOOL` offers a narrow read-only contract. The request includes tool definitions and history. On `tool_use`, the dispatcher validates arguments and authenticated scope; the loop appends matching `tool_result` blocks in a user message. On `end_turn`, it returns the answer. Special stop reasons remain explicit incomplete outcomes.

The backend is synthetic. A real adapter injects the principal from authenticated application state; it does not accept identity truth from the model. Keep complete assistant blocks for protocol continuity. Return errors with the correct call ID rather than dropping failed calls.

Official reference: [implement tool use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/implement-tool-use). SDK tool runners can automate ordinary loops; use a manual loop when custom orchestration and approval are important, and inspect current runner budgets/error behavior before deployment.

## 4. Structured output and Pydantic

The runnable [structured extraction](../examples/sdk_structured.py) uses a raw JSON schema:

```python
output_config = {"format": {"type": "json_schema", "schema": schema}}
```

Pass that to `messages.create`, check completion, parse text and run local semantic/evidence validation. A required nullable field represents missing data without making up a value. A schema-enforced total is still not proof of arithmetic, provenance or payment eligibility.

The checked SDK also supports Pydantic models through `messages.parse(output_format=ModelClass, ...)`. That helper argument is different from a deprecated raw `output_format` dictionary on a create request. It translates the model schema and exposes a parsed result. Pydantic validation may add local constraints; always understand which constraints the API enforces versus your application validates.

```python
from pydantic import BaseModel, ConfigDict

class Decision(BaseModel):
    model_config = ConfigDict(extra="forbid")
    case_id: str
    reason: str | None

# parsed = client.messages.parse(model=model_id, max_tokens=300,
#     messages=[{"role": "user", "content": "Classify this case..."}],
#     output_format=Decision)
# Check completion and parsed.parsed_output before using the result.
```

This is an API-shape example; the executable raw-schema path is preferred for the invoice lab so the schema is visible. Strict tool input schemas and final JSON output constrain different surfaces. Check model support before using forced tool modes or particular schema features.

Official reference: [structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs).

## 5. Batches and result identity

[sdk_batches.py](../examples/sdk_batches.py) has mutually exclusive submission and check modes:

```bash
python -m examples.sdk_batches --submit
python -m examples.sdk_batches --check BATCH_ID_FROM_SUBMISSION
```

Submission creates paid independent requests. Save the returned ID, inspect `processing_status` and per-request counts, and retrieve results only when ready. Correlate `custom_id`, not result position. Retain succeeded/errored/expired/canceled disposition for every source document and retry selectively.

The example disables automatic retries around batch submission because a lost creation response leaves uncertainty about whether a batch exists. Production submission needs a durable job ledger and reconciliation. Do not promise a hard interactive deadline using the batch processing window.

Official reference: [Message Batches](https://platform.claude.com/docs/en/build-with-claude/batch-processing).

## 6. Agent SDK: tools, subagents and results

[sdk_agent.py](../examples/sdk_agent.py) configures a bounded researcher/reviewer system. `query()` streams typed events. `ClaudeAgentOptions` supplies workspace, available tools, preapprovals, settings sources, MCP configuration and budgets. `AgentDefinition` supplies a worker prompt, description and narrow tool set.

`tools=[...]` is the explicit top-level built-in tool inventory. `allowed_tools=[...]` preapproves listed calls; unlisted available tools may still reach the permission flow. `disallowed_tools` removes capabilities. Per-worker `AgentDefinition.tools` narrows that worker. Underlying read-only filesystems and credentials are still required where enforcement matters.

The example sets `setting_sources=[]`, `strict_mcp_config=True`, empty MCP servers and `permission_mode="dontAsk"` for a controlled demonstration. This intentionally limits ambient filesystem settings and configured integrations; managed policy and other runtime inputs have their own documented behavior. It does not claim those flags create a complete OS sandbox. The ordinary CLI may load user/project/local settings by default; do not generalize an old SDK default to the pinned version.

The coordinator can invoke the current `Agent` tool. The historical blueprint calls the spawning mechanism `Task`; log either name when interpreting mixed-version telemetry. Task-specific findings still need explicit handoff. `AgentDefinition` uses camelCase for some advanced fields such as `maxTurns`, while `ClaudeAgentOptions` uses snake_case `max_turns`.

A terminal result carries session ID, subtype, error indicator, usage/cost metadata and result text where available. A result event is not always success. Require an appropriate successful terminal status and handle exceptions separately. The sample budget limits are intentionally small; a complex task may finish incomplete rather than exceeding them.

Official references: [Python Agent SDK](https://code.claude.com/docs/en/agent-sdk/python), [official source repository](https://github.com/anthropics/claude-agent-sdk-python).

## 7. Hooks and permission callbacks

[sdk_hooks.py](../examples/sdk_hooks.py) constructs a `PreToolUse` hook returning a documented deny shape. It has no trusted approval store and therefore always denies the fictional billing tool. `HookMatcher(on_failure="block")` requests fail-closed behavior when the callback fails. The service still checks identity and policy.

Do not treat `can_use_tool` as an unconditional interceptor. It is part of the permission flow and can be bypassed by preapproved calls. A PreToolUse hook is the appropriate interception point when a check must run for calls that would otherwise be allowed. PostToolUse fits normalization/audit after execution, not prevention of a prior side effect.

The standalone hook example makes no API call. Run it with `python -m examples.sdk_hooks` after installing optional packages. Verification checks denial fields and fail-closed registration without invoking a real payment server.

Official reference: [Agent SDK hooks](https://code.claude.com/docs/en/agent-sdk/hooks).

## 8. Sessions and filesystem state

[sdk_sessions.py](../examples/sdk_sessions.py) captures the session ID, then resumes with `fork_session=True` for an alternative read-only analysis. Use `resume=session_id` without the fork flag to continue the original history. Re-read mutable files in either case. A fork is not a filesystem snapshot or a new isolated checkout.

Record session ID alongside an application manifest that names evidence revision, completed work and pending tasks. Do not store a session ID as proof that a payment remains eligible or a prior API response remains current.

Official reference: [sessions](https://code.claude.com/docs/en/agent-sdk/sessions).

## 9. MCP server implementation

[mcp_order_server.py](../examples/mcp_order_server.py) uses the official MCP Python SDK v2's `MCPServer`. Decorated tools expose callable operations; resources expose content by URI. A fixed synthetic customer keeps the lab small and must be replaced with authenticated scope in any real deployment.

Use [launch_mcp.py](../examples/launch_mcp.py) as an absolute-script entrypoint when your host has a different working directory. Launch via an interpreter with the optional `mcp` package installed. Never print arbitrary logs to the stdio protocol channel.

Official references: [MCP Python SDK source](https://github.com/modelcontextprotocol/python-sdk), [get started](https://py.sdk.modelcontextprotocol.io/get-started/).

## Errors, budgets and observability

Separate transport/authentication errors, rate limits, schema/argument errors, model refusal/truncation, tool execution errors and business-policy rejection. Recover at the layer that has the needed information. Use bounded retries and service guidance for transient safe reads. Reconcile unknown writes. Do not stack application retries on SDK retries without accounting for the multiplied attempt budget.

Log request/operation identity, model/version, prompt/schema version, usage, latency, status, validation failures and recovery attempts where appropriate. Avoid logging credentials and unnecessary sensitive source content. The local tests verify protocol and application behavior; they do not claim live model quality, account access or production SLA validation.

Continue with the [official code tour](OFFICIAL_CODE_TOUR.md) and [compatibility notes](COMPATIBILITY.md).
