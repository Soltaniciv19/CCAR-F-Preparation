# P5 — Extraction and independent review

**Objectives:** validate structured extraction, correlate reordered results, bound retries, measure a labeled holdout, and ground review findings in evidence. **Prerequisites:** D3, D4 and P1. **Time:** 90–120 minutes. **Mode:** offline simulation; no model is invoked.

A syntactically valid JSON object may violate a schema; a schema-valid record can still be factually wrong. Compare these prompt designs on the synthetic receipts in `fixtures/receipts.json`: (a) “extract the receipt,” (b) explicit fields and USD-only constraints, and (c) the same instructions with representative labeled examples. Run `python projects/05_extraction_and_review/solution/example.py` after your attempt to inspect illustrative fixed predictions and holdout metrics. Those predictions are hand-scripted and do not measure any prompt or model. A live model comparison is optional and needs a separately configured, paid API client; this project does not make live or batch calls. Never infer model quality from the scripted fixture.

Copy `starter/` to your own workspace and implement `pipeline.py`. Public tests default to `solution/`; select your workspace with `P5_WORKSPACE=/absolute/path/to/workspace python -m pytest projects/05_extraction_and_review/tests -q`. Run the reference tests with `python -m pytest projects/05_extraction_and_review/tests -q`.

## Requirements

- A receipt record has a nonempty `merchant`, positive integer `amount_cents` (not a boolean), and `currency` equal to `USD`. `validate_record` returns actionable errors, including missing fields. A missing or uncertain result must be reported, not invented.
- `process_batch` takes input dictionaries with unique `id` and `text` plus an extractor callable. It receives requests containing `id`, `text`, and validation `feedback`, and returns a list of results in any order. A result contains `id` and either `record` or an `error` with `message` and boolean `retryable`. Match by ID, reject duplicate/unknown IDs, retry retryable or invalid results up to `max_attempts`, and return a status and attempts per input. A missing response is retryable. Never retry a non-retryable error.
- `evaluate` compares predicted merchant labels to the labeled holdout by input ID. Report exact-match precision and recall, with zero when a denominator is zero. Read the criteria in the fixtures and report results, not a claimed exam score.
- `review` runs independent detection and evidence-verification passes on source text. Report a finding for an actual `eval(` call only when its cited line is present; do not turn unverified model claims into findings. The toy detector is intentionally limited, not a security scanner.

Exercises: implement the pipeline, simulate a validation failure followed by a corrected response, reorder results, run tests and report holdout metrics. Describe which defects public tests can miss and how your prompt comparisons and independent review differ from deterministic validation. Extension: add a larger holdout and calculate field-level metrics separately. Reflection: when is batching worthwhile, and how does preserving input IDs prevent misattribution?
