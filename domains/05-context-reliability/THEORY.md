# Domain 5: Context Management & Reliability

## 5.1 Preserve facts rather than hoping the model remembers

Context is finite working material, not a durable application database. A long support conversation may contain the verified customer ID, several order IDs, a corrected amount and a failed lookup. A summary that merges them into "customer has an order problem" destroys the exact distinctions needed for a safe action.

Maintain separate layers: trusted case facts, source evidence, task state, a compact conversational summary and recent messages. Include exact IDs, money, dates, verification status and authoritative receipt IDs in a persistent facts block. Update that block from trusted tool/service results. Do not let a generated summary overwrite it.

```json
{
  "case_facts": {
    "customer_id": "C-7",
    "order_id": "O-100",
    "identity_source": "authenticated_session",
    "requested_refund_cents": 1200,
    "refund_status": "not_requested"
  },
  "summary": "Customer also reports a delivery problem.",
  "pending": ["check_delivery", "confirm_refund_request"]
}
```

Put critical constraints and facts where they will be consistently included, rather than relying on a buried paragraph in a large history. Retrieve a small relevant evidence set instead of indiscriminately attaching every document. Use summarization for lower-priority narrative, preserving references back to the original sources.

Input context capacity and output-token limits are different. Increasing maximum output tokens does not recover forgotten evidence or ensure attention to a long middle section. Prompt caching can reduce cost/latency for eligible repeated prefixes; it does not expand context capacity, correct stale facts or serve as a persistent business-state store.

## 5.2 Clarification, resolution and escalation

Escalate promptly when the user explicitly requests a human, policy requires an exception, or allowed recovery has made no meaningful progress. An upset tone alone does not prove a case needs escalation. A polite request can still require an authorized policy decision.

If two customer records match, ask for one approved disambiguating identifier. Do not select the most recent record or the closest name and then perform an account mutation. Clarification should request the minimum appropriate information and follow the application's identity process.

Keep ambiguity and authorization distinct. Knowing which order the user means does not prove they own it. A model can help interpret the concern, but service-level identity and permission checks must precede sensitive operations.

Create a handoff packet that makes the next person effective: case ID, verified identity reference, concerns, policy gap, evidence, attempted actions, committed outcomes, unresolved uncertainty and recommended next decision. Retain partial useful findings even when one backend is unavailable. Do not ask the human to rediscover everything because the model's final prose omitted the state.

## 5.3 Propagate failures without fabricating absence

A worker that receives a timeout should report unavailable evidence and what it tried. Returning `[]` as if the search succeeded can cause the coordinator to claim no incidents occurred. This is a reliability defect caused by lost error semantics.

Perform bounded local recovery for safe transient failures. Then return a structured status, failure category, attempted method/query, attempt count, partial findings and possible alternative. The coordinator can switch sources, narrow the task or synthesize a partial report with clearly marked coverage gaps.

Not every worker failure should abort the whole run. If two of three independent research areas succeed, an honest partial report may still be useful. Whether to proceed depends on the decision: a missing optional background statistic differs from missing ownership verification for a refund. Define which missing evidence blocks downstream action.

Unknown outcomes after writes deserve a distinct state. "The response timed out" does not mean "the refund failed." Reconcile before repeating. The final answer should only claim confirmed state, preserve unresolved outcomes and identify the next action.

## 5.4 Explore large repositories with durable evidence

Map the relevant structure, trace an entry point through imports/wrappers, inspect tests and record findings. Symptoms of context degradation include repeated broad searches, generic guesses replacing named evidence, forgotten dependencies and citations to a stale file revision.

Use an isolated exploration worker for a bounded question, with explicit known findings and an output contract. Ask for path, symbol, revision, observed control flow and unresolved assumptions. A concise evidence summary protects the coordinator's context better than copying every file read.

Persist a scratchpad and recovery manifest outside the transcript. The manifest should include schema version, run ID, base commit, completed tasks, artifact references, pending work, constraints and verification time. Save atomically where possible. On resume, reload it and compare the current revision; a changed commit means observations need revalidation.

The reference manifest uses atomic file replacement and records whether revalidation is needed. It does not implement a distributed work queue, encrypted storage, lease management or full power-loss guarantees. Add these only when the deployment requires them. A checkpoint should never silently mark pending work as completed merely because a process restarted.

`/compact` can reduce conversational clutter. It is useful alongside durable evidence, not a replacement for it. Likewise, a session fork preserves a reasoning baseline while files and services may continue changing.

## 5.5 Human review and calibrated confidence

Overall accuracy can hide severe segment failures. If 900 typed invoices are 99% correct and 100 handwritten invoices are 79% correct, the combined accuracy is 97%. The handwritten segment still has a 21% error rate. Inspect document type, field, source quality, language and impact.

A model reporting confidence 0.95 is not automatically correct 95% of the time. Calibration compares score bands to independently labeled outcomes. If the 0.9-1.0 band is only 80% correct, a nominal 0.95 threshold cannot justify automatic approval. Evaluate on a representative holdout set and recheck after distribution shifts.

Route review using consequence, validation status and empirically measured uncertainty. High-impact fields or contradictory evidence may require review regardless of reported confidence. Lower-risk validated fields may be automated with an audit sample. Thresholds belong to a measured application policy, not a universal exam number.

Do not sample only low-confidence cases. A system can be confidently wrong. Stratify random audits by document type, field and confidence band, including the supposedly easy cases. Oversampling rare strata is useful for diagnosis; estimate overall performance using population-aware weighting rather than treating an unweighted audit sample as the production distribution.

The reference sampler returns a reproducible sample within each stratum. It demonstrates selection, not calibration training, confidence intervals or risk acceptance. A production evaluation loop needs independent labels, segment sizes, reviewed disagreements and change tracking.

## 5.6 Preserve provenance and uncertainty through synthesis

A claim should carry metric, value, unit, period, population, method, source identifier, publication date and locator. Separate the observation period from publication date. A report published in 2026 may describe data collected in 2025.

Two values are not directly comparable if one counts registered sites in 2025 and the other estimates all sites in 2026. If comparable claims disagree, preserve both sources, identify the conflict and seek targeted verification. Do not select a value because the source is newer without examining what changed; do not average incompatible measurements.

The reference comparator checks a set of comparison dimensions and distinguishes consistent, conflicting and noncomparable claims. It intentionally uses exact normalized strings. A production system should normalize units and numeric representation explicitly and document tolerances for estimates. It should not declare semantic agreement from identical text alone.

Synthesis should distinguish supported findings, contested findings, noncomparable measurements and missing coverage. Keep attribution attached to each claim as it moves between workers. A readable summary that drops source IDs and dates may be short but no longer verifiable.

## A reliability design walkthrough

A research coordinator receives two dated statistics and one timeout. It stores the two claims with their measurement dimensions, records the third source as unavailable after bounded attempts, compares only like-for-like claims, and produces a report with evidence and coverage limitations. On restart it loads the manifest and rechecks changed sources. For high-impact extracted fields it routes review using validation and calibrated segment risk, while auditing some high-confidence outputs.

This design preserves uncertainty as data. It prevents a generation step from quietly converting "not observed," "not available," "not comparable" and "false" into the same status.

Sources: supplied PDF P5, [context and compaction](https://code.claude.com/docs/en/best-practices), [prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching), [evaluation design](https://platform.claude.com/docs/en/test-and-evaluate/develop-tests), [source register](../../docs/SOURCES.md).
