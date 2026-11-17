# Domain 4 exercises

## Lab 1: A precise Python reviewer (4.1, 4.2)

Design a review prompt that reports reachable bugs and security defects while skipping style preferences and unsupported speculation. Define severity by impact, not confidence. Create three few-shot examples: a genuine bug, a valid similar pattern and an ambiguous case requiring more evidence.

Deliver prompt, findings schema and a labeled evaluation table. Acceptance: each accepted finding has location, trigger, evidence and impact; false positives are measurable by category. Explain when to disable a noisy category and how to evaluate its restoration.

## Lab 2: Extract without repairing the source (4.3, 4.4)

Source: `Items: 2 at EUR 40.00; 1 at EUR 45.00. Total EUR 135.00. No PO supplied.` Define a closed schema with items, stated total, nullable PO and exact evidence locators. Implement completion checking, parsing and semantic validation.

Deliver Python validator and one optional live extraction. Acceptance: computed total is 125.00, stated total remains 135.00, PO remains null, and the contradiction goes to review. Add malformed quantity, NaN amount, fabricated PO and wrong source offsets. Explain why exact quote matching is necessary but not sufficient for full semantic provenance.

## Lab 3: Targeted retry and batch operations (4.4, 4.5)

Design one bounded retry for an incorrectly assigned present field. Include source, failed record and specific validator errors. For a missing page retrieve it before retry; for a genuine source contradiction stop trying to "fix" it.

Then design a 1000-document nightly batch with stable custom IDs and result statuses. Deliver out-of-order correlation logic and a resubmission plan for 20 expired and 10 oversized requests. Acceptance: only appropriate failures are retried; the oversized inputs are repaired first. Calculate why a 12-hour collection cadence plus a 24-hour processing window cannot satisfy a 30-hour planning target.

## Lab 4: Independent local and integration review (4.6)

Create a two-file Python example in which a parser returns pieces and a pricing function expects boxes of 12. Each file should look locally plausible. Design fresh reviewer inputs, file-local passes, integration pass and deduplication.

Deliver original code, defect report, corrected design and a cross-file behavior check. Acceptance: the review traces units across the boundary and provides a concrete trigger. Explain why a fresh model context improves independence while still requiring deterministic checks.

Use the shared 10-point rubric and keep your attempts separate from reference code.
