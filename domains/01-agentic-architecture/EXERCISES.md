# Domain 1 exercises

Write your attempt in a new `work/domain1/` directory. Do not open the [solution guide](ANSWERS_AND_SOLUTIONS.md) until you have a design, a trace and failure examples.

## Lab 1: A protocol-correct support loop (1.1)

Build `run_loop(request, execute, prompt, max_turns)`. The fake model first returns text plus two tool calls, then a final answer. Calls have different IDs, and one lookup returns an application error.

Requirements: preserve the complete assistant response; return both results together with matching IDs; encode the failed result as an error; terminate from `stop_reason`; report truncation and budget exhaustion as incomplete. Do not stop because assistant text exists.

Deliverables: Python implementation, a hand-drawn message trace, and an explanation of what would change for dependency-safe parallel reads. Acceptance cases: two successful calls; one failed call; unknown tool; `max_tokens`; repeated `tool_use` until the cap. Explain why the cap is a safety limit rather than a success criterion.

## Lab 2: A refund gate the model cannot bypass (1.4)

Design a service for order `O-100`, owned by `C-7`, paid amount 12000 cents. Identity comes from a trusted authenticated session. The model supplies only order, amount and an application-assigned operation key.

Implement ownership, eligibility, positive integer amount, cumulative limit and idempotency checks. Replaying the same key and request must return one receipt; changing the amount under that key must fail. Two concurrent 8000-cent requests must not refund 16000 cents.

Deliverables: service diagram, Python service, state before/after each case, and a production design for database transaction plus payment-provider timeout reconciliation. Test unverified identity, another customer's order, boolean amount, over-refund and duplicate submission.

## Lab 3: Coverage-aware coordinator (1.2, 1.3, 1.6)

A user asks for a comparison covering price, migration, reliability and privacy. Three workers all finish but collectively cover only price and reliability. Define task/result schemas and detect the missing coverage.

Design a targeted re-delegation for migration and privacy. Specify source IDs, dates, limitations, failure status and explicit prior findings in every handoff. Draw which tasks may run concurrently and which synthesis steps depend on their results. Explain why running every worker twice is wasteful.

Deliverables: task contracts, coverage check, a partial-failure trace and a final report structure that preserves gaps. Acceptance: a completed worker without coverage metadata cannot silently satisfy every requirement.

## Lab 4: Hooks and session continuity (1.5, 1.7)

Construct a PreToolUse guard for a fictional refund tool. Deny when no trusted approval exists; register supported fail-closed behavior. Demonstrate the callback locally without an API call. Explain how direct service access remains safe.

Design a resume/fork exercise in a disposable checkout: inspect a file, capture a session ID, modify the file externally, then resume with instructions to re-read it. Fork an alternative design without editing. Record what is preserved and what must be revalidated. The optional [SDK scripts](../../docs/ANTHROPIC_SDK.md) show the live integration.

Scoring per lab: 2 points for a clear contract, 2 for the normal path, 3 for required failure behavior, 2 for verification evidence, 1 for production limitations. Aim for at least 8/10 in every lab as a local study target.
