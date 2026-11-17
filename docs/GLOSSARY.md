# Glossary

| Term | Meaning and practical consequence |
|---|---|
| Agent harness | Runtime around model calls; owns execution, state, limits and observation |
| Agentic loop | Repeated model/tool interaction driven by new evidence |
| Workflow | Code-defined transitions suitable when the process is known |
| Coordinator | Owner of decomposition, coverage, delegation, recovery and synthesis |
| Subagent | A bounded worker with isolated conversation and explicit task context |
| Coverage | Whether all original concerns have supported treatment, distinct from worker completion |
| Tool contract | Purpose, selection boundary, inputs, outputs, errors and side effects |
| tool_use | Assistant content requesting a tool action; local code still executes client tools |
| tool_result | A matching result bound to a tool-use ID, including failure indication when needed |
| end_turn | Normal completion of a model turn, not proof of every business outcome |
| Idempotency | Repeating a logical operation yields one effect, with payload-bound identity |
| Unknown outcome | An operation may have committed although the response was lost |
| Prerequisite gate | Deterministic check that blocks an action until trusted conditions hold |
| PreToolUse | Interception before execution, useful for prevention |
| PostToolUse | Processing after execution, useful for normalization and audit |
| Fail closed | Failure of a critical check denies rather than grants authority |
| MCP host | AI application managing user interaction and client connections |
| MCP client | Connection-side component speaking MCP to a server |
| MCP server | Capability provider exposing tools, resources and prompts |
| Resource | Addressable content such as a catalog or document |
| stdio | Local-process transport; stdout must remain protocol traffic |
| Streamable HTTP | Network transport suitable for remote MCP deployments |
| CLAUDE.md | Project/personal instructions provided as model context |
| Path rule | A convention conditionally loaded for matching file paths |
| Skill | Reusable on-demand workflow with instructions and optional supporting files |
| Plan mode | Investigation/design phase for uncertain architectural work |
| Print mode | Noninteractive CLI execution through -p or --print |
| Structured output | Schema-constrained response shape; does not prove truth or authority |
| Semantic validation | Checks values and relationships, such as totals and units |
| Provenance | Source, locator, date and method supporting a specific claim |
| Few-shot prompting | Teaching behavior with concrete input/output and judgment examples |
| Precision | Fraction of reported findings that are genuinely correct |
| Recall | Fraction of actual target findings that were detected |
| Calibration | Comparing predicted score bands with observed labeled correctness |
| Stratification | Separating evaluation groups to reveal hidden segment behavior |
| Manifest | Durable record of progress, evidence revision and pending work |
| Compaction | Reducing conversational history; critical facts still need durable preservation |
| Prompt cache | Performance mechanism for eligible repeated prefixes; not a state database |
| Session fork | Divergent conversation history from a baseline; files may still be shared |
| custom_id | Stable per-request identity used for batch result correlation |

Return to [the SDK guide](ANTHROPIC_SDK.md) or [main course](../README.md).
