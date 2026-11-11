# D1 · Agent architecture and orchestration

**Objectives:** Trace a Messages tool round, choose fixed or adaptive decomposition, delegate bounded work, and distinguish policy gates, hooks, checkpoints, resume and forks.  
**References:** D1.1–D1.7 in [Architecture.md](../../Architecture.md).  
**Prerequisites:** Basic Python and the preceding lesson (setup first).  
**Time:** 75–100 minutes. **Mode:** Offline, no paid calls.

## Concept

A model response can request several tools in one assistant turn. Preserve the complete assistant response, execute each authorized request, and return one result with the matching ID for each request before the next model call. Stop on a final response; treat truncation and turn limits as failures rather than final answers. The example is a scripted simulation, not a real Messages API client.

A coordinator should give a subagent a narrow task, needed context, permitted tools and an expected result. Fixed decomposition works when steps are predictable; adaptive decomposition can investigate unknowns but adds cost and makes progress harder to bound. A deterministic gate enforces policy regardless of what a model recommends. Hooks observe or control lifecycle events; they do not replace the gate. A checkpoint stores state for resuming; a fork starts a separate branch from a checkpoint. Whether a real SDK supports a particular hook or session operation depends on its current API.

## Predict and inspect

Before running the example, predict its output. Run `python course/01_agent_architecture/example.py` from the repository root. Change one value, predict the new result, and run it again. Restore the file afterwards.

## Exercise

Implement `dispatch(calls, allowed)` in `exercise/attempt.py`. Return one result per input in order, carrying its `id`. The only known operation is `lookup`, which takes a nonempty string `order_id` and returns `{"order_id": ..., "status": "shipped"}`. For disallowed or unknown names return `error: "not_allowed"`; for invalid input return `error: "invalid_input"`. Do not execute arbitrary code. Never omit a call, even if another call fails.

Edit only `exercise/attempt.py`; use the Python standard library and the published criteria above. Run `python -m pytest course/01_agent_architecture/tests -q`. The starter deliberately raises `NotImplementedError` until you implement it. Tests establish the displayed cases, not mastery or real model behavior. Add cases you consider important. For incremental help, read [hints](hints.md); the [reference solution](solution/solution.py) is separate and should be opened only for review. To check the reference, run `COURSE_REFERENCE=1 python -m pytest course/01_agent_architecture/tests -q` (on Windows PowerShell, set `$env:COURSE_REFERENCE='1'` first and remove it afterward).

## Apply the concept

Complete the additional [domain lab](lab.md) to practice the remaining concepts.

## Review and reflect

Answer [the scenario questions](questions.md) before looking at their answer key. When would a fixed workflow be sufficient, and what state would a resumed conversation need to preserve? Record your result, open questions and a brief reflection in [progress.md](../../progress.md).
