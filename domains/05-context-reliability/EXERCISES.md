# Domain 5 exercises

## Lab 1: Survive context reduction and restart (5.1, 5.4)

A support investigation has 50 messages, corrected order IDs and a verified 1200-cent request. Design a context packet separating trusted facts, evidence, task state and summary. Persist a manifest containing revision, completed and pending work.

Deliver context builder and atomic manifest save/load. Acceptance: a summary claiming a different amount cannot overwrite trusted facts; a changed commit sets a revalidation flag; restarting preserves pending tasks. Explain what atomic replacement does and does not guarantee.

## Lab 2: Choose clarification or escalation (5.2, 5.3)

Implement routing for explicit human request, two plausible customer records, policy exception and exhausted backend recovery. An angry customer with a simple authorized replacement should still be eligible for resolution.

Deliver route function, escalation packet and a trace with one successful research area and one timeout. Acceptance: explicit human request wins; ambiguous identity is clarified before account action; timeout remains unavailable evidence; partial useful findings reach the coordinator.

## Lab 3: Preserve conflicting research evidence (5.6)

Source A reports 4200 registered commercial sites for 2025. Source B reports 4850 estimated all-category sites for 2026. A third source reports 4300 for the same dimensions as A. Define normalized claim records and classify comparisons.

Deliver comparator and a report with supported, contested, noncomparable and unavailable sections. Acceptance: A/B are not directly comparable, A/third are a genuine conflict, and all sources retain publication dates and locators. Do not average the numbers.

## Lab 4: Audit high-confidence mistakes (5.5)

Typed invoices: 891 correct of 900. Handwritten invoices: 79 correct of 100. Compute aggregate and segment accuracy. Design review routing using field consequence, validation errors and calibrated risk. Build a deterministic stratified audit sample including high-confidence records.

Deliver Python sampler, labeled evaluation plan and a review decision table. Acceptance: 97% aggregate does not conceal 79% handwritten accuracy; high-confidence strata are sampled; self-reported confidence is not treated as measured correctness. Explain how unequal sampling affects population estimates.

Use the shared 10-point rubric. Keep production risk thresholds explicit assumptions rather than universal numbers.
