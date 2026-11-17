# Domain 3: Claude Code Configuration & Workflows

This domain fills the gap in the supplied PDFs. It is written from the official exam objectives and Claude Code documentation, with version-specific behavior called out. Practice in a disposable repository; the sample files are teaching assets, not changes to your personal Claude configuration.

## 3.1 Instruction hierarchy and modular project memory

Claude Code uses instruction files to provide context that would otherwise need repeating. User instructions at `~/.claude/CLAUDE.md` describe personal preferences across projects. A repository's `CLAUDE.md` or `.claude/CLAUDE.md` carries shared project knowledge. Nested `CLAUDE.md` files provide instructions associated with a particular subtree as those files become relevant. A teammate does not receive your home-directory instructions through Git.

Imagine a team where only one developer gets the expected test style. If the standards live in that developer's user-level file, the inconsistency is a scope problem. Move shared conventions into the repository and commit them. Increasing the model's output budget will not share a missing file.

Keep the root file short and actionable: architecture boundaries, how to run checks, conventions the model cannot infer, and important domain constraints. An entire API manual or a 100-step task recipe belongs elsewhere. A good instruction says "Currency is represented as integer cents in the billing service; reject floats at the public boundary." A vague statement like "write excellent code" adds little operational guidance.

Imports use `@path/to/file` syntax within a `CLAUDE.md`. For example, `@docs/testing-standard.md` can keep maintained testing guidance in one place. Imports load referenced material; they are not a security boundary and should not contain secrets. Topic files in `.claude/rules/` provide another way to split conventions. Use `/memory` to inspect loaded instruction files and diagnose scope, instead of assuming a file was loaded because it exists.

Instructions and settings solve different problems. Markdown provides model context. JSON settings configure runtime behavior such as permissions, hooks and model defaults. A prose "never deploy" rule does not provide the same enforcement as absent deployment credentials and a blocked deployment tool. Settings can exist at user, project, local and managed scopes, and managed policy can constrain other settings. Check the current precedence rules rather than assuming the nearest Markdown file overrides every runtime restriction.

## 3.2 Commands and skills

A reusable workflow is usually a skill. A skill folder contains `SKILL.md` and optional references/scripts. Project skills in `.claude/skills/` are versionable and shared; personal skills in `~/.claude/skills/` belong to the user. Legacy `.claude/commands/*.md` command files remain relevant to the exam and supported workflows, while current documentation presents commands and skills through a unified skill system.

Use a skill for a task such as reviewing an API contract, generating a migration checklist or analyzing a subsystem. Use `CLAUDE.md` for standards that apply broadly whenever working in the project. Putting a long review recipe in always-loaded project memory wastes context when the user only wants a small edit.

```markdown
---
name: inspect-flow
description: Trace a Python call path and return cited evidence.
argument-hint: "[entrypoint or question]"
context: fork
agent: Explore
allowed-tools: Read, Grep, Glob
---
Investigate $ARGUMENTS in the repository. Return file paths, symbols,
observed behavior, and unresolved assumptions. Keep the report concise.
```

`context: fork` runs the task in an isolated subagent context, useful when exploration produces verbose output. The parent receives the useful result rather than every discovery detail. Supply a clear task and output contract; an isolated context does not magically know what an earlier session found.

`argument-hint` improves the invocation UI; it does not validate that an argument is supplied or well formed. Skill logic must handle a missing identifier or ambiguous task. `$ARGUMENTS` substitutes invocation arguments. Treat interpolated user text as data rather than inserting it into shell commands without proper handling.

The exam describes `allowed-tools` as controlling skill tool access. In current Claude Code, the frontmatter preapproves listed tools during the skill; do not assume it creates an exclusive sandbox. For read-only work also restrict the actual tool set or subagent capability and underlying credentials/filesystem. This distinction matters when a skill has a Bash-capable runtime that could write files despite a read-oriented prompt.

A personal variant should have a distinct name rather than unexpectedly overriding the team's workflow. Inspect naming and precedence when two skills appear to collide. Verify a skill by invoking it in the sandbox and observing its behavior, not merely by validating that the YAML parses.

## 3.3 Path-specific rules

Rules can be conditional on file paths. A test convention may apply to files in `services/`, `packages/`, and `integration/` rather than one subtree. Use frontmatter `paths` globs instead of copying a `CLAUDE.md` into every folder.

```markdown
---
paths:
  - "**/test_*.py"
  - "**/*_test.py"
---
Use deterministic fixtures. For money operations include duplicate-request
and unknown-outcome cases. Assert externally visible behavior.
```

An unscoped rules file is broadly loaded; a path-scoped rule loads when matching files become relevant under Claude Code's documented behavior. Test with a matching and a nonmatching file. A common mistake is using a glob for a filename while intending a content search: `paths` matches locations, not function names.

Use a nested instruction file when a coherent directory has its own architecture. Use path rules for conventions that cut across directory boundaries, such as Python tests, Terraform files or migrations. Check overlapping rules for contradictions. Repeated instructions consume context and may make a conflict harder to diagnose.

## 3.4 Plan mode and direct execution

Choose plan mode when uncertainty and architectural consequences justify investigation before edits: a shared library migration, a storage change, a 40-file service split or several valid integration designs. The plan should identify current behavior, constraints, alternatives, likely affected components, rollout risk and verification strategy. A useful plan resolves decisions; it is not a prose list of file edits invented before reading code.

Direct execution suits a small well-understood change with clear acceptance criteria, such as rejecting a null field at a known validation point. It can still include reading the function and running an existing test. Planning every one-line change adds overhead without resolving material uncertainty.

Plan mode supports an investigation phase. It does not itself make all external integrations read-only. Keep the available capabilities and service credentials appropriate to the investigation. Use Explore or another isolated read-only worker for verbose discovery. Return a short evidence-bearing summary to the main session, then switch to implementation with the agreed design.

For an unfamiliar caching requirement, use an interview pattern early: ask about staleness tolerance, invalidation, key space, consistency and failure behavior. A missing product constraint cannot be discovered by reading more Python files. Conversely, do not ask a user to choose routine implementation details the repository already establishes.

## 3.5 Iterative refinement with concrete evidence

When transformation instructions produce inconsistent output, add specific input/output examples. "Normalize dates" is underspecified. Examples such as `2026/11/17 -> 2026-11-17`, `missing -> null`, and `03/04/26 -> request locale clarification` show both behavior and ambiguity policy.

Use tests as a feedback channel. Supply the failing input, expected result, observed result and relevant error. A model can act on "a duplicate refund with the same operation key creates a second ledger entry" more effectively than "the service is unreliable." Choose tests for meaningful behavior and risk rather than mirroring every implementation line.

Bundle interacting problems so the implementation can address the shared cause. If field normalization, validation and serialization disagree about nullable values, explain all three together. For independent changes, work in small iterations so regressions are attributable. Repeatedly replacing a long prompt with "try harder" does not provide new evidence.

Keep a distinction between implementation completion and verification completion. A code edit may compile while violating a cross-file contract. Review the changed data path and existing fixtures, then run appropriate checks. Store concise findings with paths and revisions rather than filling the conversation with repeated full-file dumps.

## 3.6 CI/CD integration

Use `claude -p` or `--print` for noninteractive execution. An interactive process can hang an unattended job. `--output-format json` produces a machine-readable CLI result envelope. `--json-schema` requests a structured payload; in the checked CLI, that payload is in `structured_output`, not interchangeable with the whole envelope.

The Python adapter [workflows.py](../../ccarf/workflows.py) passes arguments as a list, supplies the prompt through stdin, sets a timeout, checks the process exit status, rejects error result subtypes, and extracts the structured findings. It never turns a failed invocation into an empty successful review. Its `--tools` selection limits the available built-ins; `--allowedTools` preapproves those reads. Production CI must also use appropriate checkout isolation and credentials.

Run reviewers in a fresh context with the original requirements, patch and relevant tests. The session that generated the code can be anchored to its own assumptions. Fresh review reduces that bias but does not guarantee correctness; require reachable-code evidence and meaningful verification.

On a new commit, include prior finding disposition and ask for new or unresolved issues. Avoid posting duplicate comments on unchanged evidence. Line numbers move, so deduplicate using path, category and stable evidence rather than line number alone. Our local `new_findings` is a simple teaching implementation; a production system should retain commit identity, finding lifecycle and revalidation state. Suppressing a repeated comment is different from closing an unresolved bug.

Existing tests and fixture conventions belong in reviewer/test-generation context. Otherwise the model may suggest tests that already exist or invent unsuitable fixtures. Define accepted finding categories and severity with concrete examples. A noisy CI reviewer can reduce developer trust even when it occasionally finds important bugs.

## A complete team design

Put common commands and architecture conventions in project memory. Put distributed test conventions in path rules. Put optional verbose tracing in an isolated skill. Keep personal preferences in user scope. For a migration, investigate and plan, implement against concrete examples, then run an independent structured CI review. Every configuration choice should answer: who receives it, when it loads, what it changes, and how its behavior is verified.

Official references: [memory](https://code.claude.com/docs/en/memory), [skills](https://code.claude.com/docs/en/skills), [settings](https://code.claude.com/docs/en/settings), [best practices](https://code.claude.com/docs/en/best-practices), [programmatic CLI use](https://code.claude.com/docs/en/headless). Blueprint mapping and verification date are in [sources](../../docs/SOURCES.md) and [compatibility](../../docs/COMPATIBILITY.md).
