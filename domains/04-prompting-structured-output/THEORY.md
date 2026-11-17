# Domain 4: Prompt Engineering & Structured Output

## 4.1 Explicit criteria improve precision

A prompt is an operational specification. It should define the goal, relevant inputs, decision criteria, exclusions, output format and failure behavior. "Review carefully and report only high-confidence issues" does not define what an issue is. Different runs may flag style, speculative security problems or a valid local convention.

A precise review criterion might be: "Report a comment mismatch only when the comment claims observable behavior that the reachable implementation contradicts. Cite the comment and contradicting branch. Skip wording preferences and missing comments." This provides a categorical rule that can be evaluated against labeled examples.

Precision is `true positives / all reported positives`; recall is `true positives / all actual positives`. High recall with many false positives may make a reviewer unusable. Measure categories separately: security, data loss, behavioral bugs, comment mismatch and style can have very different error rates. Temporarily disable a noisy nonessential category while improving its criteria and examples, then evaluate on a holdout set before restoring it.

Define severity by concrete impact. A reachable authorization bypass differs from a small display issue. Require trigger, evidence, impact and suggested repair. A severity label without a demonstrated path is not strong evidence. Keep numerical confidence separate from the finding's consequences and verification status.

## 4.2 Few-shot examples teach judgment

Few-shot examples demonstrate how to apply a rule, especially when natural language leaves ambiguity. Include a positive case, a superficially similar negative case, and a difficult boundary case. Match the desired output format exactly so the model learns both selection and presentation.

For invoice extraction, examples should cover varied layout, absent purchase-order numbers, explicit contradictions and ambiguous dates. A training example that invents a missing field teaches the wrong behavior even if the JSON shape is perfect. Use `null` for unavailable values and a separate reason/status where that distinction matters.

```text
Input: "PO: AB-91. Total EUR 12.00."
Output: po_number="AB-91", stated_total="12.00", status="observed"

Input: "No purchase order was provided. Total EUR 12.00."
Output: po_number=null, stated_total="12.00", status="missing_po"

Input: "Two items at EUR 4.00. Stated total EUR 10.00."
Output: computed_total="8.00", stated_total="10.00", status="conflict"
```

These are conceptual field examples; the full live schema includes source evidence. Do not reuse evaluation cases as all of your prompt examples. A prompt can memorize familiar cases without generalizing to a new supplier or layout. Evaluate rare and ambiguous formats separately.

## 4.3 Structured output: shape is one layer

Distinguish three mechanisms. Prompting for JSON asks for a format but does not itself enforce it. Schema-constrained final output controls the response shape. Tool input schemas describe callable arguments, with strict enforcement where supported. For extraction that has no external side effect, schema-constrained output can be simpler than pretending that a reporting function is a business action.

The checked Python SDK uses `output_config={"format": {"type": "json_schema", "schema": ...}}` with `messages.create`. A Pydantic model can also be used with the SDK parsing helper. Do not interchange a raw schema dictionary with a Pydantic class or copy a historical beta field into a current SDK method. See [sdk_structured.py](../../examples/sdk_structured.py) for a complete request.

Model/configuration compatibility matters. The blueprint's `any` and named `tool` selection concepts describe forcing a tool action where supported. `auto` does not guarantee a call, even with a strict input schema. A schema can constrain `currency` to an enum and require an amount field; it cannot prove the source really states that amount or that the amount may be paid.

Use nullable required fields to represent missing data explicitly. An omitted property, a known empty value and an unavailable value have different semantics. Closed schemas prevent unexpected fields but still require business validation. Refusal, output truncation and incomplete responses must be handled before parsing or persisting the result.

## 4.4 Validate meaning, evidence and policy

An extraction pipeline has at least four checks:

1. Completion and shape: the request ended appropriately and the response matches the schema.
2. Semantics: dates are valid, quantities are positive, currency is consistent and totals make sense.
3. Provenance: every material value has source support in the actual supplied document/version.
4. Policy: any downstream action meets business approval and authorization rules.

Consider source text stating two items at EUR 40 and one at EUR 45, with total EUR 135. The computed total is EUR 125. An extractor should preserve the stated 135 and separately report the computed 125 and conflict. It must not invent a EUR 10 item to make the numbers agree. When the source itself is inconsistent, a new model call cannot make it consistent.

Use integer minor units or `Decimal` values created from strings for money. Binary floating point can introduce representation errors. The reference validator rejects boolean quantities, NaN/infinity and unsupported evidence. It uses exact source-string offsets and quotes for the demonstrated fields. Exact quote matching proves that text exists at that location; it does not prove semantic entailment. A production validator should tie every line item and field to the correct document region and handle OCR normalization explicitly.

A targeted retry includes the original source, prior result and exact validator failures. Retry a misassigned field or incorrect date normalization when the source contains the needed information. Retrieve missing pages before retrying extraction. Stop retrying when a field is genuinely absent or a contradiction requires judgment. Bound both attempts and total cost, and preserve the failed result for diagnosis.

Do not automatically overwrite a source value with a computed one. Persist both, attach validation status, and route to the appropriate review queue. A policy threshold is a deterministic gate, not another prompt suggestion.

## 4.5 Batches: throughput under latency constraints

Message Batches group independent requests for asynchronous processing. They fit nightly ingestion or nonblocking audits. A live support interaction or a pre-merge check with a short deadline generally needs synchronous processing. Batch is not a scheduler for an interactive client-tool loop that pauses to execute your local Python tool.

Use unique `custom_id` values and map results by ID. Never zip returned results to input order. Inspect each status: succeeded, errored, expired or canceled. Retry only eligible failed IDs; diagnose oversized inputs or bad schemas before resubmission. Persist source version, prompt version, model and prior attempt IDs to make results traceable.

The checked documentation describes discounted eligible batch token pricing and a processing window up to 24 hours. Recheck current terms before costing production use. Those terms are not a hard end-to-end latency guarantee.

For planning arithmetic, if processing can consume 24 hours and the target is 30 hours from arrival, a 12-hour collection cadence can yield nearly 36 hours and misses the target. A six-hour cadence consumes the whole planning allowance before retries or collection overhead. A strict commitment requires monitoring, headroom and fallback, not only subtraction.

The example [sdk_batches.py](../../examples/sdk_batches.py) separates submission from a single status/result check. It does not silently resubmit a batch if the network loses the creation response. Unknown submission outcomes require reconciliation to avoid duplicate cost and duplicate downstream records.

## 4.6 Independent and multi-pass review

The same conversation that generated an implementation may defend its assumptions when asked to review it. An independent instance gets the requirements, artifact, relevant tests and domain contracts without the generator's explanatory history. Independence reduces anchoring, but still needs evidence and deterministic verification.

A large patch benefits from local passes plus an integration pass. File-local review checks a function's internal behavior. Integration review checks units, interfaces, state transitions and error propagation across files. A parser returning quantity in pieces and a pricing function expecting boxes can each look plausible in isolation while being wrong together.

Aggregate findings by root cause and verify their locations against the current patch. Deduplicate, retain unresolved issues and attach accepted/false-positive/deferred dispositions. Feed measured human feedback into criteria and examples. A second model saying "looks good" is not equivalent to an executable contract check.

## A complete extraction design

Fetch the whole source with a stable document ID; select examples and schema; request bounded structured output; check completion; validate values and evidence; retry only a recoverable extraction mistake; preserve source contradictions; route high-impact ambiguity to review; persist validated output with provenance. Optimize batch throughput only after a labeled pilot demonstrates acceptable behavior.

Sources: supplied PDF P4, [structured output](https://platform.claude.com/docs/en/build-with-claude/structured-outputs), [batch processing](https://platform.claude.com/docs/en/build-with-claude/batch-processing), [evaluation guidance](https://platform.claude.com/docs/en/test-and-evaluate/develop-tests). The full register is [here](../../docs/SOURCES.md).
