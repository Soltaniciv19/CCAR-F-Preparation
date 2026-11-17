# Domain 1 answers and implementation guide

Try [the exercises](EXERCISES.md) and [questions](QUESTIONS.md) first. The question key follows the lab solutions below.

## Lab 1 solution: preserve protocol evidence

Reference: [run_loop](../../ccarf/architecture.py), exercised by [offline_demo](../../examples/offline_demo.py). The harness sends the user prompt, appends the complete assistant content, collects every client-tool call, executes through a checked dispatcher, then appends one user message containing all results. IDs bind results to calls; array position does not.

```python
from ccarf.architecture import run_loop
from ccarf.tools import dispatcher

orders = {"O-100": {"customer_id": "C-7", "status": "paid"}}
# request(history) is your fake or SDK-backed model callable.
# outcome = run_loop(request, dispatcher(orders, "C-7"), "Check O-100")
```

The executable fake request is in the demo; the real request adapter is in [sdk_tool_loop.py](../../examples/sdk_tool_loop.py). A text block such as "I will check" is retained but does not terminate execution. `max_tokens` returns an incomplete status. A budget-exhausted run cannot be labeled resolved. Unexpected executor exceptions propagate rather than becoming a fabricated successful result.

For parallel execution first classify side effects and dependencies. Run only independent reads together, then return every result with its own ID. Preserve errors individually; one failed read must not erase other evidence.

## Lab 2 solution: trusted state and an atomic ledger transition

Reference: `RefundService` in [architecture.py](../../ccarf/architecture.py). The authenticated principal is supplied by the trusted adapter, not extracted from a `verified` flag in tool arguments. Under one lock, verify accessible ownership, check replay fingerprint, check eligibility and remaining amount, then record the receipt and cumulative refund.

```python
from ccarf.architecture import Order, RefundService

service = RefundService({"O-100": Order("C-7", 12000)})
request = dict(
    authenticated_customer="C-7",
    order_id="O-100",
    amount_cents=2000,
    idempotency_key="case-8-refund-1",
)
first = service.refund(**request)
assert service.refund(**request) == first
assert service.refunded["O-100"] == 2000
```

An 8000-cent race allows one transition and rejects the other because the remaining amount is 4000. A boolean is rejected even though Python's `bool` subclasses `int`. A changed request under the same key is a conflict, not a new transaction.

Production extension: persist an operation row with a unique key and canonical request hash, perform database checks transactionally, call a provider with its idempotency mechanism, and reconcile unknown responses by original operation ID. The in-memory lock is process-local and loses state on restart; it is not a distributed payment implementation.

## Lab 3 solution: compare requirements with verified coverage

Represent `required={price,migration,reliability,privacy}` separately from worker completion. [uncovered](../../ccarf/architecture.py) subtracts coverage only from completed results. Here it returns migration and privacy. Issue two targeted tasks with nonoverlapping scope, and rerun synthesis when usable evidence arrives. For partial evidence, preserve useful findings but do not mark the missing topic covered without a deliberate policy.

Each task receives the original question, known findings, source locators and output schema. A synthesis worker receives structured records; it does not inherit another session's memory. The coordinator tracks attempted strategies and decides whether to retry, switch sources or report gaps. Present the final comparison with supported topics, unresolved topics and source dates.

## Lab 4 solution: fail closed and re-read mutable state

[sdk_hooks.py](../../examples/sdk_hooks.py) constructs `HookMatcher(on_failure="block")` and a denial response. It intentionally has no approval backend and therefore cannot authorize a refund. A real callback reads a trusted approval record bound to operation, amount and identity. PostToolUse can normalize a result or enrich an audit log; it is too late to prevent an already committed write.

[sdk_sessions.py](../../examples/sdk_sessions.py) captures a successful `ResultMessage.session_id` and forks a follow-up. The transcript persists, but the filesystem is live. Re-read files after external edits and use separate worktrees for alternative implementations. A service must revalidate current ownership and policy even if the transcript contains yesterday's successful lookup.

## Exam-style question key

The generated key below includes the best answer and the constraint that rules out alternatives.


### D1-Q01: C

**Execute both permitted calls and return results matched by tool-use ID.** Text and tool calls can coexist. Preserve complete assistant content and return every call result; text alone is not completion.

### D1-Q02: B

**The protocol stop reason and requested tool blocks.** Natural language is not a reliable control signal. The runtime must follow the structured protocol.

### D1-Q03: A

**Mark the response incomplete and apply a bounded recovery policy.** Truncation is not successful completion. Parsing or persisting a plausible prefix can lose fields and evidence.

### D1-Q04: D

**An incomplete status with saved progress and the unresolved check.** A cap controls resources. It neither proves task completion nor authorizes a blocked operation.

### D1-Q05: C

**Track coverage against the original question and delegate the missing topic.** Completed tasks can still cover an incomplete decomposition. The missing topic requires evidence gathering.

### D1-Q06: B

**Select workers based on task needs and avoid unnecessary delegation.** Delegation has cost and aggregation overhead. Dynamic selection preserves scope while avoiding unnecessary work.

### D1-Q07: A

**Explicit findings, sources, constraints and output requirements.** Task-specific context is not automatically shared. The handoff must carry the evidence needed for synthesis.

### D1-Q08: D

**Run them concurrently and aggregate attributed results.** Independent reads can benefit from parallelism. Shared writes and final aggregation still need controlled coordination.

### D1-Q09: C

**Set explicit available tools and enforce underlying read-only permissions.** Preapproval is not an exclusive tool inventory. Explicit capabilities and service or OS permissions provide stronger boundaries.

### D1-Q10: B

**Authentication and approval state from trusted application context.** A schema-valid self-assertion is not authentication. Authority must originate outside model-controlled arguments.

### D1-Q11: A

**Reconcile the original operation using its stable idempotency identity.** The outcome is unknown; a new operation can duplicate a committed side effect.

### D1-Q12: D

**Reject the request fingerprint conflict.** Idempotency binds identity to a logical request. A changed payload under the same key must not silently execute.

### D1-Q13: C

**PreToolUse with a trusted gate.** Pre-execution interception can prevent the call. Post-execution observation cannot undo an already committed action.

### D1-Q14: B

**Supported fail-closed hook configuration plus service-side authorization.** Failure semantics must be explicit. The business service remains protected if a runtime hook fails or is bypassed.

### D1-Q15: A

**In a deterministic result adapter or appropriate post-tool processing.** Normalization needs parsing and conversion of actual values. A formatting hint alone does not transform data.

### D1-Q16: D

**Investigate each concern with relevant evidence, then synthesize one response.** Distinct concerns need coverage. Independent investigations may run concurrently while final communication stays unified.

### D1-Q17: C

**Define measurable criteria, targeted feedback and bounded refinement.** Evaluator-optimizer loops need criteria and limits. Vague iteration can consume resources without resolving a specific gap.

### D1-Q18: B

**Revalidate current authoritative order and approval state.** Sessions preserve conversation continuity, not current business authority or external state.

### D1-Q19: A

**The live filesystem unless separate checkouts are supplied.** Conversation branching does not automatically isolate files. Parallel implementations need workspace isolation.

### D1-Q20: D

**Verified facts, attempted actions, committed outcomes, gaps and next decision.** A structured handoff makes the human effective and distinguishes completed actions from unresolved questions.
