# A practical learning plan

Budget roughly 55-75 hours, adjusting for your Python and agent experience. Hours are study estimates, not an exam requirement. Read actively: after each concept explain the failure it prevents, the component that enforces it, and the evidence that proves it worked.

| Stage | Time | Work | Exit evidence |
|---|---:|---|---|
| Setup | 2 h | Environment, SDK distinction, offline demo | All local checks run; explain where credentials are used |
| Domain 1 | 12-16 h | Loops, orchestration, state, hooks, sessions | Draw a tool trace and defend a refund gate |
| Domain 2 | 8-10 h | Tool contracts, MCP, permissions, errors | Build a server and classify five failure types |
| Domain 3 | 10-12 h | Instructions, skills, rules, planning, CI | Configure a disposable repo and parse CI output |
| Domain 4 | 10-12 h | Criteria, examples, schemas, validation, batches, review | Extract a contradictory invoice without fabricating |
| Domain 5 | 7-10 h | Context, uncertainty, provenance, calibration | Resume an investigation and preserve evidence gaps |
| Integration | 6-8 h | Capstone and timed practice | Explain mistakes and demonstrate failure handling |

## A four-week route

Week 1: setup and Domain 1. Practice the message loop by hand before running it. Spend one session on the difference between conversation memory and verified state. Finish with the domain questions closed book.

Week 2: Domain 2 and the first half of Domain 3. Design contracts before writing an MCP handler. Put each Claude Code configuration file in the correct scope and explain who receives it. Do not change your real global settings for the exercises.

Week 3: finish Domain 3 and study Domain 4. Review a small Python patch with a fresh reviewer context. Implement extraction validation and compare synchronous and batch scheduling under a deadline.

Week 4: Domain 5, capstone, mixed practice. Inject outages, ambiguous customers, stale state, duplicate requests, unsupported claims and inconsistent totals. Run the full practice exam once under the timing below, then spend at least as long explaining the wrong answers.

## A study session, repeated

1. Recall yesterday's concepts without notes for ten minutes.
2. Read a theory section and draw its control flow.
3. Implement one requirement from the exercises without opening the solution.
4. Run a normal case and a failure case. Record what the failure teaches.
5. Answer a few scenario questions and explain every distractor.
6. Write a decision rule in your own words, with its limitations.

Use the 60-question practice exam for a 120-minute session. The official guide currently describes 60 single-answer multiple-choice questions in 120 minutes. Our question distribution approximates the published weights; it does not reproduce an actual form or scoring model. Any local readiness target is a study heuristic, not a conversion to the certification's scaled score.

Keep a mistake log with columns: objective, my answer, missed constraint, why the correct design works, changed constraint that would make my answer valid. Revisit each mistake after one day, three days, and one week.

Primary references: [official certification landing page](https://anthropic-partners.skilljar.com/claude-certified-architect-foundations-certification), [source register](docs/SOURCES.md).
