# Compatibility and verification snapshot

Checked on **17 November 2026** against official documentation and installed public package signatures. Model access is account-specific and no paid live API requests were made during repository verification.

| Component | Pinned version | Important API choices |
|---|---|---|
| Anthropic Python SDK | 2.10.0 | `Anthropic`, Messages, streaming, `output_config`, batches |
| Claude Agent SDK | 0.2.183 | `query`, `ClaudeAgentOptions`, `AgentDefinition`, hooks, resume/fork |
| MCP Python SDK | 2.3.0 | `mcp.server.MCPServer`; stdio and Streamable HTTP |
| Pydantic | 2.14.3 | Optional typed parsing pattern |
| Python | 3.11+ supported by course | Verification performed with Python 3.12.16 and stdlib checks on host Python |

## Exam concepts versus current interfaces

| Topic | Study concept | Current implementation note |
|---|---|---|
| Subagent spawning | Blueprint calls it Task | Current examples use Agent; interpret legacy events explicitly |
| Forced tool use | auto, any, named tool | Support varies by model/settings; strict input shape does not force invocation |
| Structured final JSON | Schema-constrained response | Raw create requests use `output_config.format`; parsing helpers can accept a Pydantic `output_format` class |
| Available tools | Give a role a narrow set | Agent SDK `allowed_tools` is preapproval; use explicit `tools`/restrictions too |
| Skill frontmatter | Blueprint describes allowed-tools as controlling access | Current docs describe preapproval; it is not sufficient as an exclusive sandbox |
| SDK settings loading | Project/user/local configuration affects behavior | Set `setting_sources` explicitly for controlled runs; old defaults differ |
| Permission interception | Check sensitive actions | `can_use_tool` is not called for every preapproved action; PreToolUse and service gates matter |
| Hook failure | Critical guard should block | Pinned `HookMatcher` supports `on_failure="block"` |
| MCP Python examples | Older guides commonly use FastMCP | Pinned official v2 examples use MCPServer; do not mix imports across versions |
| MCP field spelling | Wire results use isError | Pinned v2 Python objects expose `is_error`; serialization retains wire aliases |
| Remote transport | MCP can connect remote services | Prefer supported Streamable HTTP for new deployments; legacy SSE may remain for compatibility |
| Sessions | Preserve conversational baseline | Files, credentials, approvals and ledgers remain live and need revalidation |

`requirements-sdk.lock` records the resolved optional environment. It is not generated from private credentials or the user's existing venv. When upgrading, check request signatures, tool inventories, permission flow, structured-output support, hook errors, CLI result shape and MCP protocol behavior, then rerun verification before changing the snapshot.

The official exam guide currently states 60 single-answer questions in 120 minutes. Domain weights are 27/18/20/20/15. Avoid mapping a raw practice percentage to an official scaled score. Recheck the certification landing page before scheduling the exam.

References: [official certification](https://anthropic-partners.skilljar.com/claude-certified-architect-foundations-certification), [Python SDK](https://platform.claude.com/docs/en/api/sdks/python), [Agent SDK reference](https://code.claude.com/docs/en/agent-sdk/python), [MCP v2](https://py.sdk.modelcontextprotocol.io/whats-new/), [skill frontmatter](https://code.claude.com/docs/en/skills).
