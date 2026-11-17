# CCAR-F: Python architecture study repository

A self-contained learning path for **Claude Certified Architect - Foundations (CCAR-F)**. It combines the four supplied study PDFs with a newly written Domain 3 and official Anthropic/MCP documentation checked on **17 November 2026**. This is independent study material. All practice questions are original, with one best answer; they are not recalled exam items.

## Start here

1. Read [setup](docs/SETUP.md) and [the learning plan](STUDY_PLAN.md).
2. Follow Domains 1 through 5. In each folder read `THEORY.md`, complete `EXERCISES.md`, then answer `QUESTIONS.md` before opening `ANSWERS_AND_SOLUTIONS.md`.
3. Run the Python implementations, change a design assumption, and inject the failures specified in each lab.
4. Complete the [integrated capstone](capstone/README.md), then the [60-question practice exam](practice-exam/EXAM.md).
5. Use the [coverage map](CURRICULUM_MAP.md) and [progress tracker](PROGRESS.md) to revisit weak objectives.

## Domains

| Domain | Weight | Learning material | Main implementation |
|---|---:|---|---|
| 1. Agentic Architecture & Orchestration | 27% | [Domain 1](domains/01-agentic-architecture/README.md) | [Protocol loop and refund gate](ccarf/architecture.py) |
| 2. Tool Design & MCP Integration | 18% | [Domain 2](domains/02-tool-design-mcp/README.md) | [Contracts, dispatch and recovery](ccarf/tools.py) |
| 3. Claude Code Configuration & Workflows | 20% | [Domain 3](domains/03-claude-code/README.md) | [CLI review adapter](ccarf/workflows.py) |
| 4. Prompt Engineering & Structured Output | 20% | [Domain 4](domains/04-prompting-structured-output/README.md) | [Evidence and arithmetic validators](ccarf/extraction.py) |
| 5. Context Management & Reliability | 15% | [Domain 5](domains/05-context-reliability/README.md) | [Provenance, routing and persistence](ccarf/reliability.py) |

Each domain contains theory, four build/design exercises, 20 scenario questions, an explained answer key, and implementation guidance. The separate full practice exam contains another 60 questions. See [Anthropic SDK guide](docs/ANTHROPIC_SDK.md) for live Messages, streaming, structured output, tool loops, batch, Agent SDK, hooks and sessions examples.

## Run without API access

Python 3.11+ is sufficient for the offline code. Run from this repository's root:

```bash
python3 -m examples.offline_demo
python3 -m capstone.solution
python3 -m unittest discover -s verification -v
python3 scripts/check_repository.py
```

For SDK examples and development tools, create a separate environment:

```bash
uv venv .venv-study --python 3.12
uv pip install --python .venv-study/bin/python -e '.[sdk,dev]'
source .venv-study/bin/activate
```

Live examples make paid API calls only when explicitly run. They read `ANTHROPIC_API_KEY` and require an explicit `ANTHROPIC_MODEL`; no credentials are included. No API calls are necessary to complete the theory, offline labs or assessments.

## How to use the sources

The [source register](docs/SOURCES.md) identifies all supplied PDFs and the official references. The PDFs remain in Downloads; the repository contains original explanations and code rather than redistributed PDFs. Domain 3 is sourced from the official blueprint, Claude Code documentation, and verified SDK behavior.

Distinguish the **exam's architectural concepts** from a particular SDK release. Tool names, forced tool selection, hook fields, model support and settings defaults can change. [Compatibility notes](docs/COMPATIBILITY.md) record the checked versions and important differences. A schema-valid result still requires source and policy validation.

## Repository layout

```text
domains/           Five independent study folders; solutions are separated
ccarf/             Reusable, offline Python reference implementations
examples/          Runnable offline demo and optional live SDK integrations
capstone/          Integrated support-system design and implementation
practice-exam/     Unseen mixed-domain practice questions and separate key
docs/              Setup, SDK reference, sources, glossary and revision sheet
verification/      Behavioral and SDK-contract checks
scripts/           Repository integrity checks
```

See [validation results](docs/VALIDATION.md) for the checks run on the course and the limits of offline verification.
