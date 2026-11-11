# D4 · Prompting and structured output

**Objectives:** Write explicit criteria, use representative examples, distinguish syntax, schema and semantic validation, bound retries, correlate batches, and use independent review passes.  
**References:** D4.1–D4.6 in [Architecture.md](../../Architecture.md).  
**Prerequisites:** Basic Python and the preceding lesson (setup first).  
**Time:** 70–95 minutes. **Mode:** Offline, no paid calls.

## Concept

Specific task criteria and representative examples can reduce ambiguity, but examples are not a substitute for evaluation. Valid JSON is only syntactically valid: a schema also checks types and required fields; business rules and source verification determine whether values make sense. Give actionable validation feedback and a bounded retry budget rather than retrying indefinitely.

Batch processing can lower per-item overhead when latency is flexible, but output order must not be assumed: correlate by input ID. Interactive calls suit immediate feedback. Independent passes can check different failure modes, but agreement between model calls is not proof; compare findings with evidence and use a labeled holdout.

## Predict and inspect

Before running the example, predict its output. Run `python course/04_prompting_and_output/example.py` from the repository root. Change one value, predict the new result, and run it again. Restore the file afterwards.

## Exercise

Implement `validate(record)` returning a list of error strings. Require a dictionary with a nonempty string `id`, a numeric non-boolean `amount` at least zero, and `currency` equal to `USD` or `EUR`. Return an empty list only when all rules pass. Use the exact error names `id`, `amount`, and `currency`; for a non-dictionary return `["record"]`.

Edit only `exercise/attempt.py`; use the Python standard library and the published criteria above. Run `python -m pytest course/04_prompting_and_output/tests -q`. The starter deliberately raises `NotImplementedError` until you implement it. Tests establish the displayed cases, not mastery or real model behavior. Add cases you consider important. For incremental help, read [hints](hints.md); the [reference solution](solution/solution.py) is separate and should be opened only for review. To check the reference, run `COURSE_REFERENCE=1 python -m pytest course/04_prompting_and_output/tests -q` (on Windows PowerShell, set `$env:COURSE_REFERENCE='1'` first and remove it afterward).

## Apply the concept

Complete the additional [domain lab](lab.md) to practice the remaining concepts.

## Review and reflect

Answer [the scenario questions](questions.md) before looking at their answer key. What could still be wrong after a record passes schema and business-rule checks? Record your result, open questions and a brief reflection in [progress.md](../../progress.md).
