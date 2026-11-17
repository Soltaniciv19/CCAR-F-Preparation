# Integrated capstone: support resolution with evidence

Build a support assistant for a customer who reports a duplicate charge and a missing parcel. The objective is one coherent resolution, with sensitive actions enforced by code and partial failures preserved.

## Requirements

1. Accept authenticated identity only from the host's trusted context.
2. Decompose billing and shipping concerns and preserve coverage of both.
3. Offer exact-ID read tools with clear descriptions and structured errors.
4. Gate refunds on ownership, exact order/amount confirmation, eligibility, remaining balance and stable operation identity.
5. Preserve facts and receipts outside a generated summary.
6. Retry safe shipping reads with a cap; return a typed unavailable result if recovery fails.
7. Handoff explicit human requests, policy exceptions and exhausted recovery with useful partial findings.
8. Resume using a durable manifest and revalidate mutable state.

Draw the model/tool boundary, authentication boundary, service state transition, coordinator-worker handoffs and recovery path. Use Python for implementation. Add the Messages API or Agent SDK only after your offline service contracts work.

## Offline reference

Run `python3 -m capstone.solution`. [solution.py](solution.py) demonstrates trusted identity injection, confirmed amount comparison, a refund receipt, safe replay and a partial-failure handoff. It uses the domain reference modules. Its fixed fixtures are synthetic and no payment or API service is contacted.

| Injected condition | Required result |
|---|---|
| Missing identity | Block account mutation |
| Another customer's order | Block without revealing private order details |
| Same operation submitted twice | One committed effect, same receipt |
| Same key with a changed amount | Conflict rather than a second operation |
| Model changes confirmed amount | Validation rejection |
| Model changes confirmed order to another owned order | Validation rejection |
| Concurrent over-refund requests | Ledger invariant maintained |
| Shipping read timeout | Bounded attempts, explicit gap, billing evidence retained |
| Explicit human request | Prompt handoff with current state |
| Changed repository/service facts after resume | Revalidate before action |
| Generated summary claims unconfirmed success | Do not adopt it into the trusted ledger |

The deterministic reference deliberately does not pretend to measure agent decision quality. Implement your own fake model trace using `run_loop`, then optionally wire the live SDK. A complete production design also needs durable transactions, provider idempotency, unknown-outcome reconciliation, access control, telemetry, privacy handling and operational review policy.

## Review rubric

Score each of the following from 0-4: decomposition and coverage; tool contracts; state/authorization enforcement; recovery and escalation; provenance/context; evaluation evidence. A local readiness target is at least 3 in every area, with no unauthorized or duplicate financial effect. This is a learning rubric, not an official exam scoring model.

Produce an architecture decision record comparing a deterministic workflow, a Messages-controlled agent and an Agent SDK implementation. Explain which parts change and which business invariants remain service-owned. Finally, describe what evidence you would collect to evaluate whether adding an agent actually improves resolution quality.
