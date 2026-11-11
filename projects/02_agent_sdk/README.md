# P2: Agent SDK orchestration concepts

**Time:** 75 minutes. **Prerequisites:** P1, D1, D5. **Mode:** offline simulation; no SDK execution or charges.

Implement a coordinator that passes each worker an explicit task and role, records hook events, preserves successful partial results when another worker fails, and can serialize and resume a checkpoint. Resume retries failed work without rerunning successful work. Never invent a result for a failed worker. Work in `starter/orchestration.py`:

```sh
cd projects/02_agent_sdk
PYTHONPATH=starter pytest tests -q
```

When ready, compare with `PYTHONPATH=solution pytest tests -q`. This exercise simulates orchestration concepts; its hook, worker restrictions and checkpoint are **not** evidence of actual SDK behavior. The [Claude Agent SDK](https://platform.claude.com/docs/en/agent-sdk/overview) manages its own runtime and differs from the manual Messages loop. Study the current official documentation for subagent tool permissions, hooks, sessions and opt-in `setting_sources` before trying a live SDK run. Authentication and model selection are separate from Claude Code; live use may incur charges. An optional live example is described below.

**Extension:** record which source each worker used. **Reflection:** what can a consumer safely conclude from partial coverage?

`solution/live_sdk.py` is an optional, paid SDK example. It requires the Agent SDK and its supported authentication, plus `CLAUDE_AGENT_MODEL` set to an available model. From this directory run `python solution/live_sdk.py --live` only after consenting to the paid call. It uses a disposable directory, no project settings, a budget and turn limit, and an Agent-only tool set with a tool-free subagent. Delegation is model-dependent; this live path has not been tested with credentials. The SDK's permissions still apply, and its runtime is distinct from the simulation.
