# Domain 5 answers and implementation guide

## Lab 1 solution: separate stores by authority

[build_context](../../ccarf/reliability.py) places `case_facts`, structured evidence and narrative summary in separate keys. Facts come from authenticated state and tool receipts. A production prompt should explicitly identify the summary as a nonauthoritative aid; model output cannot mutate the facts store.

```python
from pathlib import Path
from tempfile import TemporaryDirectory
from ccarf.reliability import save_manifest, load_manifest

with TemporaryDirectory() as directory:
    path = Path(directory) / "state.json"
    save_manifest(path, commit="abc", completed=["map"], pending=["trace"])
    assert not load_manifest(path, "abc")["needs_revalidation"]
    assert load_manifest(path, "def")["needs_revalidation"]
```

The save writes a same-filesystem temporary file, flushes it and atomically replaces the target. It prevents readers observing a partially written JSON document under ordinary local operation. It is not a distributed lease/transaction system, and full power-loss durability may require directory fsync and platform-specific guarantees. Store source hashes and artifact locators for finer revalidation than a single repository commit.

## Lab 2 solution: route from the actual blocking condition

`route_case` prioritizes explicit human request, then unresolved identity, policy exception and recovery exhaustion. It does not infer complexity from anger. A real handoff includes case ID, verified identity reference, concerns, requested resolution, attempted actions, partial evidence, failure details and next decision.

A timed-out search returns `ok=false`, category and attempts. A successful empty query returns `ok=true` and no matches. The coordinator may produce a partial report when a missing optional topic is disclosed; missing identity verification still blocks a payment.

## Lab 3 solution: comparison dimensions are evidence

`Claim` carries metric, value, unit, period, population, method, source, publication date and locator. `compare_claims` checks comparison dimensions before values. A/B differ in period, population and method: mark noncomparability. A/third have matching dimensions but different values: retain both and request verification.

Publication date is not the same as observation period. A newer publication may describe an older period, a revised method or a wider population. Source attribution must remain with each claim during synthesis. Production comparators should normalize compatible units and numeric forms, rather than applying arbitrary equality or averaging.

## Lab 4 solution: segment evaluation plus audit sampling

Overall accuracy is `(891+79)/(900+100)=970/1000=97%`. Typed accuracy is 99%; handwritten accuracy is 79%. The weak segment matters even though its population is smaller. Route contradictions and high-impact fields to review; use thresholds calibrated against labels for other fields. No universal confidence cutoff follows from these figures.

`stratified_sample` groups by document type, field and confidence band, then samples reproducibly from each group. Include high-confidence outputs to detect confident errors. If every stratum contributes the same number despite unequal populations, use stratum population weights to estimate overall accuracy; unweighted pooled sample accuracy would overrepresent small strata.

Maintain a labeled holdout, review disagreement process and segment metrics over time. Recalibrate after new suppliers, languages, OCR behavior or layouts change the input distribution.

## Exam-style question key


### D5-Q01: C

**A separate trusted facts store populated from service results.** Generated summaries should not overwrite authoritative transactional facts.

### D5-Q02: B

**Persist and reinclude critical facts with evidence references.** Context engineering preserves exact facts; output length does not recover lost input evidence.

### D5-Q03: A

**The cache becomes a durable current business-state database.** Caching is a performance mechanism, not business-state persistence or freshness validation.

### D5-Q04: D

**Honor the request and hand over a useful case packet.** Explicit human preference is itself a handoff trigger.

### D5-Q05: C

**Request an approved disambiguating identifier before action.** Identity ambiguity must be resolved through an appropriate process, not probability or convenience.

### D5-Q06: B

**Acknowledge the concern and resolve within policy.** Sentiment is not a reliable proxy for task complexity or policy authority.

### D5-Q07: A

**Escalate to an authorized decision maker with the policy gap.** Policy gaps require authority, regardless of tone.

### D5-Q08: D

**Failure category, attempted method, partial findings and missing scope.** Structured failure information enables alternate strategies and honest partial synthesis.

### D5-Q09: C

**Use supported findings and disclose the coverage gap.** Partial useful output can be acceptable when the gap is explicit and does not block the decision.

### D5-Q10: B

**Unknown outcome versus confirmed failure.** A timed-out write may already have committed. Reconciliation precedes another operation.

### D5-Q11: A

**Saved findings need revalidation against current files.** Revision changes can invalidate observations. Preserve evidence while marking what must be rechecked.

### D5-Q12: D

**Concise findings with paths, symbols, revision and limitations.** Compression should preserve evidence and unresolved assumptions, not merely shorten prose.

### D5-Q13: C

**Completed tasks, pending work, source revision and artifact references.** Recovery requires durable task and evidence state, not just conversation continuity or usage metrics.

### D5-Q14: B

**Segment-specific error and impact, not the aggregate alone.** A large easy segment can hide substantial errors in a smaller consequential segment.

### D5-Q15: A

**Calibration against independently labeled representative outcomes.** Self-reported scores require empirical calibration and risk-specific policy.

### D5-Q16: D

**Confidently wrong outputs in high-confidence strata.** Audit high-confidence outputs too, preferably stratified by type and field, to detect hidden systematic errors.

### D5-Q17: C

**Weight strata by their production population shares.** Unequal sampling changes sample composition. Population-aware weighting is needed for an overall estimate.

### D5-Q18: B

**Preserve both and label them not directly comparable.** Comparison requires matching dimensions such as period, population, method and units.

### D5-Q19: A

**Keep attribution, flag conflict and seek targeted verification.** A genuine conflict remains visible until evidence or a documented methodology resolves it.

### D5-Q20: D

**Both publication date and observation period.** Publication time and measurement period answer different questions and prevent false contradictions.
