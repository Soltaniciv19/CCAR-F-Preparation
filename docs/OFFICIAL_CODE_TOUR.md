# Read Anthropic's own Python examples

The repository includes original runnable teaching code using official APIs, with attribution at the relevant files. For Anthropic-maintained implementations, study the upstream examples below alongside the local versions. Links were checked through the official repository directory listings on 17 November 2026. Upstream `main` can change; compare it with the versions in our compatibility snapshot.

| Official code | Read for | Local exercise |
|---|---|---|
| [Messages](https://github.com/anthropics/anthropic-sdk-python/blob/main/examples/messages.py) | Client creation, message response shape | [Messages/streaming](../examples/sdk_messages.py) |
| [Streaming](https://github.com/anthropics/anthropic-sdk-python/blob/main/examples/messages_stream.py) | Stream lifecycle and response accumulation | Domain 1 completion checks |
| [Tools](https://github.com/anthropics/anthropic-sdk-python/blob/main/examples/tools.py) | Tool definitions and returned blocks | [Manual loop](../examples/sdk_tool_loop.py) |
| [Tool runner](https://github.com/anthropics/anthropic-sdk-python/blob/main/examples/tools_runner.py) | SDK-managed client-tool iteration | Compare against your manual gate design |
| [Structured outputs](https://github.com/anthropics/anthropic-sdk-python/blob/main/examples/structured_outputs.py) | Typed schema/output integration | [Invoice extraction](../examples/sdk_structured.py) |
| [Batch results](https://github.com/anthropics/anthropic-sdk-python/blob/main/examples/batch_results.py) | Batch result iteration and identity | [Selective batch handling](../examples/sdk_batches.py) |
| [Agent SDK quick start](https://github.com/anthropics/claude-agent-sdk-python/blob/main/examples/quick_start.py) | Runtime query and options | Domain 1 runtime selection |
| [Agent SDK agents](https://github.com/anthropics/claude-agent-sdk-python/blob/main/examples/agents.py) | Specialist definitions and delegation | [Researcher/reviewer](../examples/sdk_agent.py) |
| [Agent SDK hooks](https://github.com/anthropics/claude-agent-sdk-python/blob/main/examples/hooks.py) | Interception lifecycle and callback shape | [Fail-closed guard](../examples/sdk_hooks.py) |
| [Agent SDK tool options](https://github.com/anthropics/claude-agent-sdk-python/blob/main/examples/tools_option.py) | Available-tool inventory | Domain 2 capability scope |
| [Agent SDK settings sources](https://github.com/anthropics/claude-agent-sdk-python/blob/main/examples/setting_sources.py) | Filesystem configuration loading | Domain 3 repeatable environments |
| [Agent SDK MCP calculator](https://github.com/anthropics/claude-agent-sdk-python/blob/main/examples/mcp_calculator.py) | SDK-hosted custom tools | Domain 2 integration alternatives |

## An active reading method

For each upstream file, identify the package/version assumptions, initialization, request inputs, output/event types, success criterion, error path and resource limit. Then compare the local example: what was added for authentication boundaries, provenance, budget handling or deterministic validation? Do not execute a file until you know whether it makes requests, writes files or starts an external process.

Start with the official Messages example and trace one request. Next read Tools and map each block to the Domain 1 protocol diagram. Compare the tool runner with a manual loop: which responsibilities are automated, and where does your approval policy run? Finally inspect Agent SDK hooks and settings sources to see why runtime configuration and service enforcement remain distinct.

## Attribution and licensing

Anthropic's source repositories retain their own licenses; follow those licenses if copying substantial upstream code. This course links upstream examples rather than vendoring them. Local implementations are original educational adaptations of documented public API contracts. The short API pattern in [ANTHROPIC_SDK.md](ANTHROPIC_SDK.md) is explicitly attributed to the official getting-started example. MCP is a separate project with its own [source and license](https://github.com/modelcontextprotocol/python-sdk).
