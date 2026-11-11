# D5 · Context management and reliability

**Objectives:** Preserve key facts in compact context, propagate failures, escalate ambiguity, investigate efficiently, calibrate confidence and cite conflicting evidence.  
**References:** D5.1–D5.6 in [Architecture.md](../../Architecture.md).  
**Prerequisites:** Basic Python and the preceding lesson (setup first).  
**Time:** 70–95 minutes. **Mode:** Offline, no paid calls.

## Concept

Context is finite. Keep exact identifiers, source dates, relevant facts, open questions and decisions while discarding irrelevant tool output. A summary is lossy, so preserve pointers back to original evidence. Focus repository searches on likely symbols and paths, then expand if the evidence requires it.

A failed subtask means partial coverage, not a license to invent a result. Escalate when high-impact decisions lack required facts or policies conflict. Cite each source and date, distinguish observations from inference, and present conflicts rather than resolving them by confidence alone. Human review and calibrated confidence help but cannot turn missing evidence into a fact.

## Predict and inspect

Before running the example, predict its output. Run `python course/05_context_and_reliability/example.py` from the repository root. Change one value, predict the new result, and run it again. Restore the file afterwards.

## Exercise

Implement `summarize(results)` for a list of dictionaries. Each has `source`, `date`, and either `fact` or `error`. Return `{"evidence": [...], "failed_sources": [...], "partial": bool}`. Evidence entries preserve exactly `source`, `date`, and `fact` in input order; failed sources contain the source name in input order. A result with `error` is failed even if it also has a fact. Set partial true if any source failed. Do not resolve conflicts or invent missing facts.

Edit only `exercise/attempt.py`; use the Python standard library and the published criteria above. Run `python -m pytest course/05_context_and_reliability/tests -q`. The starter deliberately raises `NotImplementedError` until you implement it. Tests establish the displayed cases, not mastery or real model behavior. Add cases you consider important. For incremental help, read [hints](hints.md); the [reference solution](solution/solution.py) is separate and should be opened only for review. To check the reference, run `COURSE_REFERENCE=1 python -m pytest course/05_context_and_reliability/tests -q` (on Windows PowerShell, set `$env:COURSE_REFERENCE='1'` first and remove it afterward).

## Apply the concept

Complete the additional [domain lab](lab.md) to practice the remaining concepts.

## Review and reflect

Answer [the scenario questions](questions.md) before looking at their answer key. How would you handle conflicting dated policies before a high-impact decision? Record your result, open questions and a brief reflection in [progress.md](../../progress.md).
