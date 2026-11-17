# Setup and execution

## Offline first

Use Python 3.11 or newer. All `ccarf` implementations and the offline demo use only the standard library. From the repository root:

```bash
python3 -m examples.offline_demo
python3 -m capstone.solution
python3 -m unittest discover -s verification -v
python3 scripts/check_repository.py
```

`unittest` runs offline behavior checks. The SDK-contract test is skipped when optional packages are absent. It imports libraries and inspects signatures without contacting Anthropic. The offline demo uses a fake model response; it does not measure model quality.

## Install optional SDKs

```bash
uv venv .venv-study --python 3.12
uv pip install --python .venv-study/bin/python -e '.[sdk,dev]'
source .venv-study/bin/activate
python -m pytest -q
ruff check ccarf examples capstone verification scripts
```

Alternatively use `python3 -m venv .venv-study`, activate it, and run `python -m pip install -e '.[sdk,dev]'`. If your OS Python cannot create a venv, use `uv` or install your distribution's Python venv package. The existing `.venv` need not be changed.

Direct dependencies are pinned in `pyproject.toml`; `requirements-sdk.lock` records the resolved optional environment used for verification. It is a reproducibility snapshot for Python 3.12, not a promise of compatibility on every platform.

## Authentication and model selection

Set `ANTHROPIC_API_KEY` in your shell or secret manager. Do not place a real key in a tracked file. Set `ANTHROPIC_MODEL` to a model available in your account and compatible with the feature being exercised. The examples deliberately require a value instead of silently selecting a model.

```bash
export ANTHROPIC_MODEL='your-supported-model-id'
python -m examples.sdk_messages
python -m examples.sdk_structured
python -m examples.sdk_tool_loop
```

Set the key separately using your normal secret-management workflow. These scripts do not automatically read `.env`. Inspect each file before running it. Batch submission has a separate `--submit` option; polling is one check per invocation to keep it observable and avoid hidden long waits.

The Agent SDK uses its own Claude Code runtime and documented authentication configuration. An API key may be used where supported; Claude subscription and third-party deployment authentication have different conditions. Follow the [Agent SDK authentication guidance](https://code.claude.com/docs/en/agent-sdk/overview). Run Agent SDK and CLI examples only in a disposable checkout; repository instructions and MCP integrations can affect their behavior.

## Commands and expected observations

| Command | Expected observation |
|---|---|
| `python3 -m examples.offline_demo` | A complete fake tool loop, validated order lookup, and invoice conflict |
| `python3 -m capstone.solution` | A committed refund, safe replay, and an escalation packet |
| `python3 -m examples.claude_code_sandbox /tmp/ccarf-workshop` | A new disposable configuration/Python workshop; target must not exist |
| `python -m examples.mcp_order_server` | A stdio server waits for an MCP client; no business data printed to stdout |
| `python -m examples.sdk_messages` | A Messages answer and streaming output from two API requests |
| `python -m examples.sdk_structured` | Schema-constrained extraction followed by local validation |
| `python -m examples.sdk_agent --workspace /absolute/disposable/repo` | A bounded read-only Agent SDK inspection |
| `python -m examples.sdk_sessions --workspace /absolute/disposable/repo` | A session ID and a forked read-only follow-up |

## Troubleshooting by layer

`ModuleNotFoundError`: activate the correct environment and install the optional extras. `401` or `403`: verify deployment/authentication and permissions; changing prompts will not repair credentials. Unknown model or unsupported tool choice: check model access and the feature compatibility table. `429`: respect server guidance and bound recovery. CLI timeout: inspect runtime/authentication and return a failed CI check, never a fabricated clean review. A tool timeout after a write requires reconciliation of the original operation before retrying.

If a structured response is truncated, refused, or otherwise incomplete, do not parse it as a complete result. If a schema-valid extraction fails arithmetic or evidence validation, diagnose the source and semantics rather than changing JSON formatting instructions.
