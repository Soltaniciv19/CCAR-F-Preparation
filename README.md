# Claude architecture study course

An offline-first, self-paced Python course for practicing architecture patterns relevant to Claude Certified Architect — Foundations. Start with the five domains, then build through the projects. The exercises and questions are original practice; they are not exam questions, an official exam guide, or a certification guarantee. See [sources and maintenance](docs/sources.md) for the community domain weights and current product documentation.

## Setup

You need Python 3.11 or newer, Git familiarity, and a terminal. The examples use synthetic data. In a shell from this directory:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
python scripts/check.py
```

On Windows activate with `.venv\Scripts\activate`. `uv.lock` records a reproducible dependency resolution; with [uv](https://docs.astral.sh/uv/), use `uv sync --locked --extra dev` instead of the first three commands, then `uv run --locked --extra dev python scripts/check.py`. Direct dependencies are pinned in `pyproject.toml`; the lock also records transitive versions. Installing packages requires network access, but the default checks do not call a model or external service. See [troubleshooting](docs/troubleshooting.md).

For interactive tutoring, install and authenticate [Claude Code](https://code.claude.com/docs/en/overview), then start `claude --model haiku` here if that alias is available to your account. Inspect `/status` or `/model` for the active selection. The tutor follows [CLAUDE.md](CLAUDE.md); `/study` and `/review` are project skills. Instructions influence behavior but do not replace permissions. They ask the tutor not to reveal solutions without a request.

Python API/Agent SDK calls use separate credentials and model configuration. They may incur charges and are not included by assumption in a Claude Code subscription. `.env.example` lists environment variable names only and is not automatically loaded. Never paste secrets into chat or commit `.env`. Optional SDK dependencies can be installed with `python -m pip install -e '.[live]'`. Choose a currently supported model ID and consult [pricing](https://platform.claude.com/docs/en/about-claude/pricing) and your provider dashboard before opting into a live call. The default checks never require credentials. Model availability, provider authentication and CLI behavior can change.

## Learning path

1. [P0: setup and baseline](course/00_setup/README.md).
2. [D1: agent architecture](course/01_agent_architecture/README.md), [D2: tools and MCP](course/02_tools_and_mcp/README.md), [D3: Claude Code](course/03_claude_code/README.md), [D4: prompting and output](course/04_prompting_and_output/README.md), and [D5: context and reliability](course/05_context_and_reliability/README.md).
3. [P1: Messages agent](projects/01_messages_agent/README.md), [P2: Agent SDK orchestration](projects/02_agent_sdk/README.md), [P3: MCP](projects/03_mcp/README.md), [P4: Claude Code workshop](projects/04_claude_code_workshop/README.md), [P5: extraction and review](projects/05_extraction_and_review/README.md), and [P6: capstone](projects/06_capstone/README.md).
4. Take the [practice sets](assessments/README.md), revisit weak areas and record evidence and reflections in [progress.md](progress.md).

Each lesson states its own commands, requirements and constraints. Starters are deliberately incomplete; their checks can fail until you implement them. Reference solutions and answer keys are separate. The root check runs reference and integration tests, not learner attempts. For example, from the root, run `python -m pytest course/01_agent_architecture/tests -q` for your D1 attempt and `COURSE_REFERENCE=1 python -m pytest course/01_agent_architecture/tests -q` for its reference. Project READMEs specify workspace or `PYTHONPATH` selection and reset instructions. Save your work before resetting; the P4 sandbox creator refuses to overwrite an existing directory.

## Working safely and evaluating progress

No default example sends external messages, processes real refunds, or uses production data. Treat model output and retrieved text as untrusted data; validate inputs and enforce authorization in code. Simulated adapters demonstrate control flow, not real model quality. Local tests establish only the cases they cover. For readiness, complete the core exercises, explain the trade-offs and failure paths independently, review weak areas and use a self-selected target on multiple practice sets. See the [glossary](docs/glossary.md) and [project rubric](assessments/README.md).
