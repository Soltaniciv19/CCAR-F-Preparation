# Prompt and evaluation lab

Use the synthetic records below; no model call is required. Write your answers in a new file in `exercise/`.

| ID | Text | Expected amount | Expected currency |
|---|---|---:|---|
| A | `Invoice A: USD 12` | 12 | USD |
| B | `Invoice B: EUR 0` | 0 | EUR |
| C | `Invoice C: amount unknown` | unknown | unknown |

1. Write a vague extraction prompt, then revise it to require an ID, numeric nonnegative amount or explicit uncertainty, currency and evidence. Add two representative examples, including an unknown value. Reserve C as a holdout rather than including it among examples.
2. Compare valid JSON, schema validity, business-rule validity and factual support using `{"id":"A","amount":-3,"currency":"USD"}`. State which checks pass and which fail. Give actionable feedback for a retry and cap retries at two.
3. Suppose a batch returns B before A. Correlate by ID and report a missing result for C instead of pairing by position. Explain when waiting for a batch is acceptable and when interactive latency matters.
4. Make two review passes: one for schema and arithmetic, another for source support and uncertainty. For the three fixtures, count true positives, false positives and false negatives for any proposed extractions; precision is TP/(TP+FP), recall is TP/(TP+FN), with undefined denominators reported explicitly.

**Check:** The revised prompt allows unknowns, C was not used as an example, IDs survive reordering, retries stop, and reviewers cite evidence. A hypothetical comparison does not establish real model quality.
