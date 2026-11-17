# Domain 4 answers and implementation guide

## Lab 1 solution: define observable categories

An acceptable finding contract is `{path,line,category,severity,trigger,evidence,impact,suggested_fix}`. Report only reachable behavior that contradicts the intended contract or violates a concrete security boundary. Skip style changes and claims without a demonstrated path. For a comment-mismatch category, require the comment's behavior claim and the contradicting implementation branch.

Few-shot pairs should show why superficially similar code is acceptable in one context and unsafe in another. Example: a parameterized SQL query with a variable value is acceptable; interpolating user input into SQL syntax is a real finding; a helper with unknown parameterization requires inspecting that helper before reporting. Evaluate on separate labeled cases. Track precision by category and severity rather than asking the model for higher confidence.

## Lab 2 solution: preserve 135 and compute 125

References: [validate_invoice](../../ccarf/extraction.py), [sdk_structured.py](../../examples/sdk_structured.py), [offline demo](../../examples/offline_demo.py).

```python
from ccarf.extraction import validate_invoice

source = "Total: 135.00"
record = {
    "items": [{"quantity": 2, "unit_price": "40.00"}, {"quantity": 1, "unit_price": "45.00"}],
    "stated_total": "135.00",
    "po_number": None,
    "evidence": {"stated_total": {"start": 7, "end": 13, "quote": "135.00"}},
}
outcome = validate_invoice(record, source)
assert outcome["status"] == "human_review"
assert outcome["computed_total"] == "125.00"
assert outcome["stated_total"] == "135.00"
```

This compact fixture demonstrates total validation; the full source is supplied to the live example. The validator refuses malformed values and marks unsupported evidence. The source is never rewritten to make accounting balance. Decimal strings avoid binary floating-point artifacts. Production extraction should also ground every line item, normalize document offsets consistently and distinguish tax/shipping/discounts before interpreting an apparent mismatch.

## Lab 3 solution: recover by cause and correlate by identity

`retry_feedback` serializes the source, prior extraction and exact errors. Retain trusted instructions separately and treat serialized source text as untrusted data; delimiters alone do not enforce policy. A field assigned to the wrong present source label can be retried once. Missing evidence requires retrieval or review, not fabricated content.

`correlate_batch` validates unknown, duplicate and missing IDs and returns a dictionary keyed by `custom_id`. The [batch SDK example](../../examples/sdk_batches.py) demonstrates submission and per-ID result retrieval. Requeue the 20 expired requests if appropriate; repair/chunk the 10 oversized documents before resubmitting them. Do not reprocess the 970 successes.

Planning bound: worst-case collection wait plus processing window is nearly `12+24=36` hours. A six-hour cadence reaches 30 hours before overhead, leaving no headroom. A strict deadline needs monitoring and fallback, not an assumption that batch always completes early.

## Lab 4 solution: make units part of the interface

Bad boundary: parser returns `quantity=24` pieces, pricing multiplies by `price_per_box=1200` cents, producing 28800 cents. The intended cost is two boxes at 1200 cents: 2400 cents. Fix by explicitly converting pieces to supported pack quantities or by accepting `boxes` at the pricing interface. Specify the policy for quantities not divisible by 12 instead of silently rounding.

File-local review checks validation and arithmetic. The integration pass tracks the unit from parser to pricing and finds the mismatch. The fresh reviewer receives requirements and code, not the generator's defense of the design. A meaningful check asserts the 24-piece outcome and the chosen nonmultiple policy.

## Exam-style question key


### D4-Q01: D

**Define observable comment-behavior contradictions and explicit exclusions.** Concrete categorical criteria improve precision more directly than vague confidence requests.

### D4-Q02: C

**Disable or narrow that category while evaluating improved criteria.** Repair the noisy category using labels and examples; severity relabeling does not remove false findings.

### D4-Q03: B

**Present, absent and ambiguous PO cases with correct null/evidence behavior.** Boundary examples demonstrate missingness policy and avoid teaching fabrication.

### D4-Q04: A

**Positive and near-miss negative decisions with evidence-based rationale.** Few-shot examples should teach the decision boundary, not merely appearance.

### D4-Q05: D

**The requested response structure.** Shape enforcement leaves semantic, provenance and policy validation to other layers.

### D4-Q06: C

**A required nullable PO property.** Required nullable fields represent unavailable values explicitly without inventing content.

### D4-Q07: B

**The installed SDK signature and current output_config.format documentation.** Request syntax is a versioned SDK contract. Prompting cannot repair a client-side parameter error.

### D4-Q08: A

**Preserve both values and flag the contradiction.** Faithful extraction records source contradictions rather than manufacturing consistency.

### D4-Q09: D

**Reject or review the unsupported provenance.** Evidence must refer to the actual supplied source/version and support the field.

### D4-Q10: C

**Original source, failed record and exact field-assignment error.** A targeted correction addresses a recoverable extraction mistake using the relevant evidence.

### D4-Q11: B

**Keep it unavailable and retrieve another legitimate source or route review.** Retries cannot create missing evidence. Null and explicit unavailability preserve truth.

### D4-Q12: A

**To avoid binary floating-point artifacts in currency invariants.** Numeric representation supports exact arithmetic but does not establish provenance or business semantics.

### D4-Q13: D

**Synchronous review with bounded execution.** Blocking short deadlines generally require synchronous processing rather than unpredictable batch completion.

### D4-Q14: C

**Message Batches with per-request IDs and status handling.** Independent nonblocking volume is a good batch use case; identity and failures still need management.

### D4-Q15: B

**By unique custom_id.** Batch correlation is identity-based, not order-based.

### D4-Q16: A

**Retry eligible expirations and repair oversized inputs before selective resubmission.** Cause-specific selective recovery avoids wasted cost and repeated deterministic failures.

### D4-Q17: D

**No, worst-case waiting plus processing approaches 36 hours.** Collection delay must be included. Strict commitments also need headroom, monitoring and fallback.

### D4-Q18: C

**Focused local passes plus a cross-file integration pass and deduplication.** Local and integration checks catch different errors; aggregation must reconcile evidence and root causes.

### D4-Q19: B

**The cross-file data/units contract.** The interfaces are locally plausible but incompatible in meaning. Integration review traces units.

### D4-Q20: A

**Evidence verification and appropriate deterministic checks.** Independent review reduces anchoring, but approval is not a proof of program behavior.
