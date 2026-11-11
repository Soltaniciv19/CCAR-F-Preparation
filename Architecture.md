# Claude Certified Architect Foundations — course architecture

Status: original implementation plan, 11 November 2026. The repository now contains the course; use the root README and individual lesson/project READMEs for implemented commands and current limitations. The plan below preserves the intended scope and is not itself a claim that every optional live integration has been verified.

## 1. Goal and scope

Build a self-paced Python course for preparing for Claude Certified Architect — Foundations. The learner will study using **Claude Code CLI with a Haiku model as an interactive tutor**. The course has two sequential parts:

1. **Learn the five domains:** short explanations, runnable focused examples, diagrams where useful, small experiments, and original scenario questions with explanations.
2. **Build and apply:** progressively implement agents with the Claude Messages API and Claude Agent SDK, use MCP, and complete Claude Code and integration assignments. Finish with a cross-domain capstone and exam-style review.

The learner should be able to explain architectural trade-offs, implement and test core patterns, identify failure modes, and justify a solution in a scenario. Exercises are practice, not claims to reproduce actual exam questions or guarantee certification.

The [provided Ravn study guide](https://ravnhq.github.io/claude-certified-architect/guides/en.html) is a community resource based on an official guide. Its five domain weights are used for planning, not as a guarantee of current exam content. It contains inconsistent scenario counts; verify current exam rules and objectives against Anthropic's current official certification materials when available. Product documentation is the authority for current API and CLI behavior. Keep exam-oriented explanations distinct from current implementation details when they differ.

### Assumptions

- Learner has basic Python, command-line and Git familiarity; a short setup and Python refresher will fill gaps.
- Course language is English. Content must explain terminology without requiring previous agent-building experience.
- Claude Code and an available Haiku model are installed and authenticated by the learner. Live API/SDK exercises additionally need compatible API access and may incur separate charges; do not assume a Claude Code subscription includes API credits.
- Use synthetic data and local, simulated services by default. No real refunds, external messages, production credentials, or repository changes outside the course workspace.
- Initial target: Python 3.11 or newer, a local virtual environment, and `pytest`. Select and pin supported dependency versions during implementation after checking current documentation.

## 2. Learning experience

### Workflow for each lesson

1. State objectives, prerequisites, estimated time, domain references, and whether it runs offline or calls a paid service.
2. Explain one concept with a concrete scenario, a small diagram or trace if helpful, and exam-relevant trade-offs.
3. Run and inspect a deliberately small example; predict behavior before running, then modify one variable.
4. Complete a learner-owned exercise with requirements, starter files, allowed tools, constraints, observable acceptance criteria and commands.
5. Run deterministic checks, discuss what they establish and what still requires judgment, then answer short original scenario questions.
6. Record a concise reflection and progress; revisit failed concepts before advancing.

Each lesson contains `README.md`, `example.py` or an explicitly named configuration example, `exercise/`, `tests/`, `questions.md`, `hints.md`, and `solution/` where applicable. A lesson may link to shared fixtures rather than duplicate them. Solutions and answer keys are separate: Claude should not reveal them unless the learner asks or chooses review mode. Examples should be readable without network access; live examples should have a deterministic offline equivalent when the concept can be simulated.

### Claude Code tutor contract

A future root `CLAUDE.md` will tell Claude Code to act as a patient tutor: start by asking the learner what they already know, explain in small steps, ask for predictions, let the learner write code, give incremental hints on request, and review against published criteria. Do not silently complete or overwrite learner work. If asked for a full solution, give it and explain the reasoning. Identify simulated behavior and paid calls clearly, never ask for a secret in chat, and get the learner's explicit consent before running paid calls or applying changes outside the exercise workspace. Tutor guidance does not replace the tool permission system or deterministic checks.

A future `/study` skill can load a specified lesson and guide one step at a time; `/review` can discuss a learner's attempt without exposing the solution by default. These are planned project skills, not commands that exist today. Keep root instructions short; load lesson details on demand. Use path-scoped rules only where they demonstrate the curriculum or improve the relevant exercises. Verify current Claude Code support for skills and configuration when implementing.

### Progress and feedback

Use a local, learner-editable `progress.md` with lesson status, date, questions to revisit and evidence (test result or reflection). Never infer mastery only from a passing test or an LLM's judgment. No account, telemetry, leaderboard or automatic progress submission. Design questions and fixtures so the learner can repeat an exercise without deleting previous work; reset instructions must say what they overwrite.

## 3. Curriculum and exam coverage

Weights below come from the provided guide. Study allocation is a guide, not a claim about the number of exam questions. Each ID maps to a lesson or exercise to be built; the rightmost column provides a traceable check of coverage.

| Domain and weight | Learning examples and concepts | Practical evidence |
|---|---|---|
| **D1 Agent architecture and orchestration (27%)** | **D1.1** Messages loop, stop reasons and multiple tool calls; **D1.2–1.3** coordinator/subagent roles, task delegation and explicit context; **D1.4** deterministic workflow gates and handoffs; **D1.5** SDK hooks; **D1.6** fixed versus adaptive decomposition; **D1.7** state, resume and fork. | P1 manual tool loop; P2 SDK subagents/hooks and session exercise; P6 capstone. |
| **D2 Tool design and MCP integration (18%)** | **D2.1** clear descriptions and input schemas; **D2.2** typed error and retryability; **D2.3** least-privilege tool allocation and tool choice; **D2.4** MCP server, resources and configuration; **D2.5** selecting Claude Code's built-in file/search/shell tools. | P1 local tools; P3 MCP service; P4 safe codebase exploration. |
| **D3 Claude Code configuration and workflows (20%)** | **D3.1** `CLAUDE.md` scope, imports and hierarchy; **D3.2** skills and slash commands; **D3.3** path-specific rules; **D3.4** plan mode versus direct edits; **D3.5** iterative refinement; **D3.6** noninteractive CI and structured review output. | P4 project configuration and refactor; P5 local CI review simulation. |
| **D4 Prompt engineering and structured output (20%)** | **D4.1** explicit criteria; **D4.2** representative few-shot examples; **D4.3** schema-constrained outputs and tool use; **D4.4** syntax versus semantic validation, bounded retries and feedback; **D4.5** batch versus interactive trade-offs and result correlation; **D4.6** independent, multi-pass review. | P1 structured result; P5 extraction and review pipeline; P6 quality evaluation. |
| **D5 Context management and reliability (15%)** | **D5.1** context budget, facts and summarization; **D5.2** ambiguity and escalation; **D5.3** subagent error propagation and partial results; **D5.4** targeted large-codebase investigation; **D5.5** human review and confidence calibration; **D5.6** citations, provenance, conflicts and uncertainty. | P2 partial-failure handling; P4 targeted investigation; P6 evidence-backed synthesis and escalation. |

### Part 1: proposed domain lessons

Every domain lesson includes the workflow above and at least one executable example, one learner change, and original scenario questions. CLI configuration examples use a disposable fixture project; where an SDK feature cannot be faithfully simulated, the lesson explains the distinction and offers an optional real execution.

- **D1 — Agent architecture:** trace a simulated model/tool conversation, compare fixed and adaptive workflows, pass a bounded task to mock subagents, enforce a policy in code, observe hook events, and compare checkpoint/resume/fork. Explain when orchestration complexity is justified and when direct code is enough.
- **D2 — Tools and MCP:** improve ambiguous tool descriptions, validate inputs, compare retryable and non-retryable errors, map tools to roles, inspect MCP tools/resources and configuration, and choose appropriate file/search/shell operations in a fixture repository.
- **D3 — Claude Code:** inspect instruction scope, create a path-specific rule and skill in a sandbox, practice plan versus direct execution, iteratively refine a small change, and examine a noninteractive review workflow. Explain that scoped instruction files influence behavior but are not security boundaries.
- **D4 — Prompting and output:** compare vague/explicit/few-shot prompts on a small labeled fixture set; validate structured output and business rules; feed actionable validation errors into bounded retries; compare batch and interactive processing; review with independent passes. Differentiate valid JSON, schema validity and factual correctness.
- **D5 — Context and reliability:** trim noisy tool output while preserving exact facts, propagate a failed subtask without inventing results, escalate ambiguous/high-impact cases, investigate a fixture repository using focused search, and synthesize conflicting dated evidence with attribution and uncertainty.

### Scenario coverage

Use original course scenarios inspired by the guide: customer support with simulated refunds (P1/P3/P6); code generation and refactoring (P4); multi-agent research with local sources (P2/P6); developer productivity and repository exploration (D2/D5/P4); CI code review (P5); and structured extraction (D4/P5). Do not describe a scenario count or exam format as authoritative without checking current official materials.

## 4. Part 2: practical projects

Projects are ordered by dependency. Each supplies a README, starter code, fixtures, public tests, acceptance criteria, hints, a separate reference solution, and a reflection. Tests focus on externally observable behavior and critical failure cases; an LLM is never the only grader. Learners implement the core behavior themselves.

| ID | Build and assignment | Minimum acceptance criteria | Dependencies and mode |
|---|---|---|---|
| **P0 Setup and baseline** | Install Python dependencies, configure Claude Code's Haiku model, run a baseline knowledge check, and use the tutor on a tiny exercise. | Offline checks pass; learner can identify current model and locate configuration; no secrets committed. | First; offline except optional model/tutor access. |
| **P1 Messages API agent** | Build a customer-support agent using the Anthropic Python SDK's Messages API and local `lookup_order`, `get_policy`, `request_escalation` tools. Handle a conversation and return a structured decision. | Dispatch every requested tool call and match results to IDs; preserve appropriate message history and tool results; terminate on final response; bound turns; report unknown tools, validation failures and truncation; refuse simulated refund without policy gate. Tests replay scripted responses offline. | D1, D2, D4; mock by default; optional live call. |
| **P2 Claude Agent SDK orchestration** | Implement coordinator and specialized research/analysis subagents with explicit task context, restricted tools and a hook; save and resume a session where supported. | Explain SDK-managed versus manual loops; demonstrate delegation, hook behavior and state handling; propagate a failed subtask as partial coverage rather than fabricate; test orchestration offline where feasible and document live-only behavior. | P1, D1, D5; optional live SDK run. |
| **P3 MCP integration** | Create a local MCP server exposing a small synthetic order or policy store, with distinct tools and a read-only resource. Connect a client/agent and configure a disposable Claude Code project. | Validate inputs, describe tools clearly, expose expected resource, handle a missing record and transient failure distinctly, restrict side effects, and demonstrate configuration and lifecycle with local integration tests. | P1, D2; local server; model call optional. |
| **P4 Claude Code workshop** | In a disposable fixture repository, add scoped guidance and a skill, investigate a bug, plan a multi-file change, implement a small refactor, and review a diff. | Instructions load at intended scope; path rule applies to its fixture; tests pass; learner explains plan/direct choice, tool choices and final diff. Provide a resettable sandbox. | D2, D3, D5; Claude Code access required for interactive portion. |
| **P5 Extraction and review pipeline** | Extract structured records from synthetic documents and build a separate code-review workflow; compare prompt variants, validation, bounded retries, batch design and independent review passes. | Parse and validate schema and domain rules; report missing/uncertain fields; correlate results with input IDs even if reordered; distinguish retryable failures; evaluate a labeled holdout and report precision/recall where applicable; review has evidence and avoids unsupported claims. | D3, D4, P1; offline fixtures; optional live and batch runs. |
| **P6 Capstone: support research assistant** | Combine a coordinator, specialized agents, local MCP data, structured output, citations, policy checks, escalation and a simulated human handoff. Write a short architecture decision record and demonstrate failure recovery. | End-to-end happy path and at least ambiguity, tool failure, conflicting sources and escalation paths; no unauthorized side effects; bounded execution; preserve source/date and partial coverage; tests pass and learner explains cost, reliability and design trade-offs. | P1–P5; offline baseline and optional live demonstration. |

For each project, include at least one extension, such as token-budget comparison, stronger source tracking, or a better evaluation set. Reference solutions explain design choices and limitations rather than presenting a single architecture as the only correct answer.

## 5. Technical design

### Three distinct integration surfaces

1. **Messages API via the `anthropic` Python package:** the application sends model requests and owns conversation history, tool dispatch, validation, termination and retries. A `tool_use` response requires executing authorized local tools and returning matching `tool_result` blocks before continuing. Preserve the model's complete assistant content as required by the protocol; support multiple tool calls and handle non-success stop reasons explicitly.
2. **Claude Agent SDK via `claude-agent-sdk`:** demonstrate its agent runtime, tool permissions, subagents, hooks and sessions using the current Python API. Treat its runtime, permissions and authentication requirements as distinct from a hand-written Messages API loop; do not assume the two share identical model names or execution behavior. Explain that loading project settings in the SDK is opt-in and verify the current `setting_sources` behavior when using project instructions.
3. **Claude Code CLI:** the learner runs the course and practices project instructions, skills, tools, planning and noninteractive workflows. Claude Code's model setting is separate from Python application configuration. The tutor must not turn assignments into demonstrations by silently implementing them.

Implement a small set of explicit interfaces, not a framework: a model client boundary with real and scripted adapters, typed tool registry, typed outcome/error representation, policy gate, fixture loader and event log. Share only stable utilities; keep examples readable and independent enough to inspect. Avoid hidden network calls at import time. A simulated adapter must say it is a simulation and must not imply deterministic fixtures prove real model quality.

### Model, credentials and cost

- Configure the tutor's Haiku model using the current Claude Code documented model selector. For example, the documented CLI alias can be selected with `claude --model haiku`; check the active model with `/status` or `/model`. Let learners choose a supported Haiku alias or model available to their account; do not assume an alias exists everywhere or that fallback never occurs.
- Separately configure API and SDK model IDs through environment/configuration, documented in `.env.example` without real credentials. Resolve actual IDs and API feature support against current official documentation during implementation; avoid hard-coding a potentially retired ID. Demonstrate an explicit override.
- Read secrets from the environment; never print keys, send them to the tutor, store them in fixtures, or commit `.env`. Add `.gitignore` when the project is implemented.
- Live calls are opt-in via a clear flag or marker. Show which operation is paid before execution, and provide a small max-output-token limit, bounded turns, timeouts and retry limits. Report usage when available; do not promise a fixed price. Point to current pricing and the learner's provider dashboard.
- Authentication for Claude Code and the Agent SDK may depend on environment and provider. Document supported options from current docs, and fail with an actionable message rather than automatically switching providers.

### Tool and workflow safety

Use mock data, an allowlist of tools, schema validation, bounded input/output sizes and explicit error types. Model output is untrusted: validate it and enforce policy in application code. Simulated mutations run only on temporary local data and require a deterministic authorization gate; escalation represents an artifact or local queue, never an actual outbound message. Treat tool output and retrieved documents as data, not instructions. Log events without secrets or personal data. Never use unrestricted shell execution from a model response. CLI/SDK examples must document permissions and run in isolated exercise directories.

### Testing and evaluation

- **Fast default:** run formatting/lint checks and `pytest` offline, with fixed fixtures and scripted model responses. Verify tool-loop protocol, tool-call IDs, multiple calls, stop conditions, schema/semantic validation, retry limits, policy gates, error propagation, provenance and session serialization where applicable.
- **Integration:** run the local MCP server and client against ephemeral fixtures; test startup/cleanup and error responses without external services. Keep any SDK behavior that requires actual Claude clearly marked live-only instead of presenting a mock as proof.
- **Opt-in live:** mark tests `live`; require explicit user action and relevant credentials. Validate invariants and output shape, not exact generated text. Avoid costs or network on default test runs. Record model ID and usage when available; no fixed success guarantee for nondeterministic outputs.
- **Learning evaluation:** original scenario questions include explanations for both correct and tempting incorrect choices. Project rubric assesses correctness, error handling, security, tests, architectural reasoning and communication. Use public tests as a feedback mechanism, plus a small separate holdout/evaluation set with transparent criteria; do not claim passing hidden tests proves mastery.
- **Readiness:** complete all domains and core projects, explain choices without relying on a solution, resolve weak areas, and achieve a self-selected target on multiple original practice sets. Practice scores are study feedback, not a predicted exam score.

## 6. Proposed project layout

```text
CCAR-F/
├── Architecture.md                 # this plan
├── README.md                       # setup, learning path and safety
├── CLAUDE.md                       # concise tutor contract
├── pyproject.toml                  # package, dependencies, pytest configuration
├── .env.example                    # placeholders only
├── .gitignore
├── .claude/
│   ├── rules/                      # focused rules for applicable paths
│   └── skills/{study,review}/      # optional tutoring workflows
├── course/
│   ├── 00_setup/
│   ├── 01_agent_architecture/
│   ├── 02_tools_and_mcp/
│   ├── 03_claude_code/
│   ├── 04_prompting_and_output/
│   └── 05_context_and_reliability/
├── projects/
│   ├── 01_messages_agent/
│   ├── 02_agent_sdk/
│   ├── 03_mcp/
│   ├── 04_claude_code_workshop/
│   ├── 05_extraction_and_review/
│   └── 06_capstone/
├── src/ccar_course/                # small reusable adapters and utilities
├── fixtures/                       # synthetic orders, documents and repositories
├── tests/                          # shared protocol and integration tests
├── assessments/                    # original practice sets and separate keys
├── docs/                           # glossary, troubleshooting, sources, ADRs
└── progress.md                     # local learner-maintained record
```

Each project gets its own `README.md`, `starter/`, `tests/`, `hints.md`, and `solution/`. Keep keys and solutions out of default tutor context; this is a learning convention, not access control. Group tests by lesson/project so they can run independently. Use isolated temporary copies of fixture repositories when exercising Claude Code. The root README will provide verified commands for installation, a single offline check, one lesson, each project and opt-in live tests after implementation.

## 7. Suggested implementation sequence

1. **Foundation:** create Python packaging, dependency lock strategy, setup guide, synthetic fixtures, offline test command, tutor contract, model/secret configuration and progress template. Verify fresh setup before expanding content.
2. **Part 1:** deliver the five domain lessons in order, each with its example, exercise, tests, questions, hints and solution. Review every coverage ID in the matrix against the linked guide.
3. **Part 2:** implement P1 through P6 sequentially, including starter code and working reference solutions. Verify every published acceptance criterion with a suitable check or explicit human review.
4. **Assessment and polish:** add original scenario sets, rubric, glossary, troubleshooting and source links. Test the full learner path with no credentials and separately test supported live paths only when credentials and consent are available.
5. **Maintenance:** record dependency versions and documentation review date. Recheck APIs, model availability, Claude Code configuration and certification objectives before releases. Clearly label exam-specific material versus current product behavior.

### Definition of done for the course

A new learner can follow the root README, complete all five domains and six practical projects, run a meaningful offline test suite, and understand which activities need Claude Code or paid API access. Every objective in the coverage matrix has lesson material and assessable practice. Each reference solution passes its tests, every live-only feature is labeled, no secrets or real personal data are present, and all commands have been verified in a clean environment. The learner can explain the capstone's trade-offs and failure handling. Use the root README and project documentation for actual verification and remaining live-only limitations.

## 8. Sources to check during implementation

- [Provided Ravn study guide](https://ravnhq.github.io/claude-certified-architect/guides/en.html) — community domain breakdown and scenarios; verify certification details with current official materials.
- [Messages API](https://platform.claude.com/docs/en/api/messages) and [tool use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview) — current protocol and tool behavior.
- [Claude Agent SDK overview](https://code.claude.com/docs/en/agent-sdk/overview), [subagents](https://code.claude.com/docs/en/agent-sdk/subagents), [hooks](https://code.claude.com/docs/en/agent-sdk/hooks) and [sessions](https://code.claude.com/docs/en/agent-sdk/sessions).
- [Claude Code overview](https://code.claude.com/docs/en/overview), [model configuration](https://code.claude.com/docs/en/model-config), [memory](https://code.claude.com/docs/en/memory), [skills](https://code.claude.com/docs/en/skills), [MCP](https://code.claude.com/docs/en/mcp) and [headless use](https://code.claude.com/docs/en/headless).
- [MCP documentation](https://modelcontextprotocol.io/docs/getting-started/intro), [structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs), [batch processing](https://platform.claude.com/docs/en/build-with-claude/batch-processing), and [pricing](https://platform.claude.com/docs/en/about-claude/pricing).
