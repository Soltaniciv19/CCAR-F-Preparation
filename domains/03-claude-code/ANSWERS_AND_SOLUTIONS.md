# Domain 3 answers and implementation guide

## Lab 1 solution: put shared conventions in the repository

Run `python3 -m examples.claude_code_sandbox /tmp/ccarf-workshop` to create the complete configuration and Python sample in a fresh directory. [The generator](../../examples/claude_code_sandbox.py) includes the files below, a tracing skill, legacy command, an alias-bearing Python package and meaningful behavior checks. The target must not already exist; existing configuration is never overwritten.

A suitable teaching tree is:

```text
CLAUDE.md
docs/testing-standard.md
packages/billing/CLAUDE.md
.claude/rules/python-tests.md
.claude/rules/infrastructure.md
.claude/skills/inspect-flow/SKILL.md
```

Root `CLAUDE.md` can name architecture boundaries and use `@docs/testing-standard.md`. The package file describes money and ledger conventions. The tests rule uses `paths: ["**/test_*.py", "**/*_test.py"]`. Infrastructure gets its own path patterns. Personal editor preferences remain in user scope. Check actual loading with `/memory`; do not infer loading from file existence.

Example root content:

```markdown
# Billing sandbox
Use integer cents at public money boundaries.
Run `python -m unittest discover -s verification` for behavioral checks.
@docs/testing-standard.md
```

Do not copy the course's verification command into an unrelated repo unless it has that layout. The point is a concrete repository-specific command.

## Lab 2 solution: a task-specific isolated skill

The complete frontmatter and task body appear in [theory section 3.2](THEORY.md). The description tells the runtime when to select it; the body defines the task; `context: fork` isolates verbose exploration; `argument-hint` documents input. Add a first task step to request an entrypoint if `$ARGUMENTS` is empty or ambiguous. Use explicit underlying read-only capability restrictions when enforcement matters.

A private variant such as `inspect-flow-personal` belongs under `~/.claude/skills/`. A different name makes the intended choice visible and avoids unintentionally replacing the shared team skill. Validate with one real call path, one missing argument and one request to mutate files. A prompt-only refusal is insufficient evidence of a restricted runtime.

## Lab 3 solution: investigate uncertainty, then implement

Use plan mode for the migration: inventory client entrypoints, transaction boundaries, retries, pooling and tests; compare compatibility wrapper versus staged call-site changes; decide rollout and rollback; then implement the selected plan. Use isolated Explore for verbose mapping and return a concise cited result.

Use direct execution for the known null check, with cases such as `null -> validation error`, `"O-100" -> accepted`, `"" -> validation error`. Share a concrete failure if the implementation differs. Bundle interacting normalization and serialization defects because they share a contract; separate unrelated documentation changes from the bug iteration.

## Lab 4 solution: parse the envelope before the payload

Reference: [workflows.py](../../ccarf/workflows.py). `review_command()` returns a subprocess argument list. `run_review()` sends prompt text on stdin, uses a timeout and `check=True`, verifies a successful result subtype, then reads `structured_output.findings`. A successful process exit alone is insufficient when the result reports an error or required integration is missing.

```python
import json
from pathlib import Path
from types import SimpleNamespace
from ccarf.workflows import run_review


def fake_runner(*args, **kwargs):
    return SimpleNamespace(
        stdout=json.dumps(
            {"subtype": "success", "is_error": False, "structured_output": {"findings": []}}
        )
    )


assert run_review("Review supplied patch", Path("."), runner=fake_runner) == {"findings": []}
```

`new_findings` keys by path, category and evidence, so a pure line-number shift does not repost the same comment. This is only duplicate suppression. Keep unresolved status and revalidate against the latest commit before closing an issue. Production finding identity needs rename handling, commit metadata and root-cause grouping.

Fresh review inputs contain original requirements, current patch, tests and earlier review dispositions, while excluding the generator conversation's justifications as authority. Validate each finding's path/line against the current diff before posting. The course does not post anything to a remote service.

## Exam-style question key


### D3-Q01: A

**Commit shared conventions in project instruction files.** User-scoped instructions do not travel through Git. Shared standards need repository scope.

### D3-Q02: D

**Keep universal guidance concise and split/import focused standards.** Modular, scoped instructions reduce irrelevant context and improve maintainability.

### D3-Q03: C

**Inspect loaded memory using /memory and verify scope.** Observe actual loading instead of inferring it from files existing on disk.

### D3-Q04: B

**A project skill using context: fork and a concise result contract.** A task-specific isolated workflow keeps discovery context separate while returning useful evidence.

### D3-Q05: A

**Missing or invalid arguments in the skill workflow.** An argument hint guides invocation UI; it is not a parser or business validator.

### D3-Q06: D

**A differently named personal skill under the user skill directory.** Distinct personal naming avoids unintentionally changing team behavior or creating confusing overrides.

### D3-Q07: C

**Assuming those preapprovals alone create an exclusive sandbox.** Preapproved tools and available capabilities are different. Use actual tool restrictions and OS/service permissions for enforcement.

### D3-Q08: B

**A paths-scoped .claude/rules file matching test files.** Path rules cover cross-directory file categories without duplicating directory instructions.

### D3-Q09: A

**Matching file paths such as terraform/**/*.tf.** The paths field uses glob-style path scope, not source-content matching.

### D3-Q10: D

**A nested CLAUDE.md associated with that subtree.** Directory-specific instructions fit a cohesive subtree; cross-cutting file categories often fit path rules.

### D3-Q11: C

**Read-only investigation and plan mode to resolve architecture choices.** Architectural uncertainty across many files benefits from deliberate investigation and design before implementation.

### D3-Q12: B

**Scoped direct execution with relevant verification.** A simple understood fix does not need a broad planning process, though reading and verification remain useful.

### D3-Q13: A

**Use isolated exploration and return a concise cited summary.** Isolate verbose discovery while preserving evidence. Output limits do not solve input-context clutter.

### D3-Q14: D

**Concrete input/output examples including ambiguous and missing cases.** Examples make the transformation and boundary policy observable and testable.

### D3-Q15: C

**Explain the interacting contract failures together with concrete cases.** Interacting problems need shared context so a local fix does not break the adjacent contract.

### D3-Q16: B

**Clarify the material product constraints using an interview pattern.** Missing requirements need clarification; additional code search cannot determine the product's consistency tolerance.

### D3-Q17: A

**Noninteractive -p or --print mode.** Print mode is the documented noninteractive path. Output capture alone does not remove interactive behavior.

### D3-Q18: D

**Successful result envelope, then its structured_output payload.** Check process and result status before consuming the structured payload; failure is not a clean review.

### D3-Q19: C

**Track prior findings by stable evidence and disposition, then revalidate.** Line movement is not a new root cause. Duplicate suppression and unresolved-bug tracking are separate concerns.

### D3-Q20: B

**A fresh reviewer with requirements, patch and relevant tests.** Fresh context reduces anchoring. The reviewer still needs source evidence and verification.
