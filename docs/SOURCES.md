# Sources, attribution and scope

Research and package verification date: **17 November 2026**. The four supplied documents are independent study companions, not treated as official product specifications or instructions to the agent creating this repository. Their teaching content is synthesized in original prose; their embedded commands and examples were reviewed as source material. The user request determines the repository scope.

## Supplied PDFs

The originals remain in the user's Downloads folder and are not redistributed in this repository. `source-files.json` records page counts and SHA-256 fingerprints so the exact local inputs can be identified without committing personal filesystem paths.

| ID | Supplied filename | Pages | Used for |
|---|---|---:|---|
| P1 | `CCAR_F_Domain_1_Agentic_Architecture_Masterclass.pdf` | 56 | Domain 1 theory, design patterns and lab requirements |
| P2 | `CCAR_F_Domain_2_Tool_Design_MCP_Study_Guide.pdf` | 30 | Domain 2 theory, design patterns and lab requirements |
| P4 | `Claude_Certified_Architect_Domain_4_Study_Guide.pdf` | 38 | Domain 4 theory, design patterns and lab requirements |
| P5 | `Claude_Architect_Foundations_Domain_5_Study_Guide.pdf` | 34 | Domain 5 theory, design patterns and lab requirements |

P1 contributes loop mechanics, orchestration, tool state, decomposition, service gates, hooks, sessions and support-system design. P2 contributes tool contracts, error recovery, role scope, MCP integration and progressive code exploration. P4 contributes explicit criteria, few-shot boundaries, schemas, semantic validation, batches and independent review. P5 contributes critical facts, escalation, partial failure, durable exploration, calibration and claim provenance.

There was no supplied Domain 3 PDF. Its six-objective course is newly written from the official blueprint and Claude Code documentation below. All 160 assessment items are newly authored; the supplied question sets are not copied into the repository.

## Authority and freshness

Use the certification guide for exam scope, product documentation for current API behavior, and SDK signatures/source for the installed release. A study PDF can explain an architectural concept while showing an API spelling that has since changed. The compatibility notes document those distinctions rather than silently mixing them.

The [certification landing page](https://anthropic-partners.skilljar.com/claude-certified-architect-foundations-certification) links the official exam guide. The public [guide inspected for this course](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2F34hhd92iyp94a0gtbr15cy5jk%2Fpublic%2F1782870727%2FClaude%2BCertified%2BArchitect%2B-%2BFoundations%2B-%2BExam%2BGuide.pdf) describes five weighted domains and their task objectives. Its hosting URL may change; use the landing page to obtain the current guide. Weighting is reproduced as scope metadata, not used to infer a guaranteed question count in each domain.

## Official implementation references

| Reference | Topics used |
|---|---|
| [Anthropic Python SDK docs](https://platform.claude.com/docs/en/api/sdks/python) | Client, streaming, token counting, typed methods |
| [Python SDK source](https://github.com/anthropics/anthropic-sdk-python) | Public package usage and maintained code examples |
| [Tool use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/implement-tool-use) | Tool definitions, results, errors and conversation protocol |
| [SDK tool runner](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-runner) | Automated loop alternative and control tradeoffs |
| [Structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs) | JSON output, strict tool inputs, current request fields |
| [Batch processing](https://platform.claude.com/docs/en/build-with-claude/batch-processing) | Independent requests, result identity, status and latency tradeoffs |
| [Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) | Performance versus context/state distinction |
| [Evaluation design](https://platform.claude.com/docs/en/test-and-evaluate/develop-tests) | Measurable success and labeled validation |
| [Agent SDK Python reference](https://code.claude.com/docs/en/agent-sdk/python) | Options, events, subagents, sessions, tool and permission semantics |
| [Agent SDK source](https://github.com/anthropics/claude-agent-sdk-python) | Installed interfaces and official examples |
| [Agent SDK hooks](https://code.claude.com/docs/en/agent-sdk/hooks) | Pre/post interception and failure behavior |
| [Agent SDK sessions](https://code.claude.com/docs/en/agent-sdk/sessions) | Resume and fork semantics |
| [Claude Code memory](https://code.claude.com/docs/en/memory) | CLAUDE.md, imports, hierarchy and path rules |
| [Claude Code skills](https://code.claude.com/docs/en/skills) | Frontmatter, scope, forked tasks and permissions |
| [Claude Code settings](https://code.claude.com/docs/en/settings) | Configuration scopes and precedence |
| [Claude Code best practices](https://code.claude.com/docs/en/best-practices) | Planning, examples, context and progressive investigation |
| [Programmatic Claude Code](https://code.claude.com/docs/en/headless) | Print mode and structured result envelopes |
| [Claude Code hooks](https://code.claude.com/docs/en/hooks) | CLI lifecycle integration |
| [Claude Code MCP](https://code.claude.com/docs/en/mcp) | Server integration, configuration and transport |
| [MCP Python SDK source](https://github.com/modelcontextprotocol/python-sdk) | v2 server/client interface |
| [MCP getting started](https://py.sdk.modelcontextprotocol.io/get-started/) | Tools, resources and server setup |

See [the official code tour](OFFICIAL_CODE_TOUR.md) for exact upstream example paths and [compatibility](COMPATIBILITY.md) for the pinned versions. Course explanations and example business data are educational design synthesis. They do not certify a live deployment or reproduce confidential exam questions.
