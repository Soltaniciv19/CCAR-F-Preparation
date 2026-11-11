# D3 · Claude Code configuration and workflows

**Objectives:** Reason about instruction scope, path-specific rules, skills, planning, iteration, and noninteractive review.  
**References:** D3.1–D3.6 in [Architecture.md](../../Architecture.md).  
**Prerequisites:** Basic Python and the preceding lesson (setup first).  
**Time:** 70–100 minutes. **Mode:** Offline, no paid calls.

## Concept

Project `CLAUDE.md` provides shared instructions; nested instructions and path-scoped rules can focus guidance on specific work. Imports and configuration hierarchy affect what is loaded: check the current Claude Code documentation and active project context. Instructions guide behavior; they are not security boundaries. A skill packages a reusable workflow that is loaded when relevant or invoked. Work in a disposable directory when experimenting.

Plan first when a change is uncertain, cross-cutting or has substantial consequences; direct edits suit a clear, small task. Review a diff and refine against explicit criteria. Noninteractive CI can produce structured review findings, but parse and validate the output and retain human review. The Python exercise models only a narrow scope decision, not Claude Code's actual matching implementation.

## Predict and inspect

Before running the example, predict its output. Run `python course/03_claude_code/example.py` from the repository root. Change one value, predict the new result, and run it again. Restore the file afterwards.

## Exercise

Implement `applies(path)` to model a rule for Python files strictly inside `src/`. Accept a relative POSIX path string, reject absolute paths and any `..` component, and return true only when the first component is `src`, at least one component follows, and the final component ends in `.py`. Use no filesystem access.

Edit only `exercise/attempt.py`; use the Python standard library and the published criteria above. Run `python -m pytest course/03_claude_code/tests -q`. The starter deliberately raises `NotImplementedError` until you implement it. Tests establish the displayed cases, not mastery or real model behavior. Add cases you consider important. For incremental help, read [hints](hints.md); the [reference solution](solution/solution.py) is separate and should be opened only for review. To check the reference, run `COURSE_REFERENCE=1 python -m pytest course/03_claude_code/tests -q` (on Windows PowerShell, set `$env:COURSE_REFERENCE='1'` first and remove it afterward).

## Apply the concept

Complete the additional [domain lab](lab.md) to practice the remaining concepts.

## Review and reflect

Answer [the scenario questions](questions.md) before looking at their answer key. When is a plan useful, and why do scoped instructions not replace permissions? Record your result, open questions and a brief reflection in [progress.md](../../progress.md).
