# Domain 1: 20 original exam-style questions

Choose one best answer (A-D). Record your reason and the decisive scenario constraint. The answer guide is separate. These are original study items, not official exam content.

## D1-Q01 | Objective 1.1

A response contains explanatory text and two client tool calls. What should the harness do next?

A. Execute only the first call and discard the second
B. Replace the assistant response with a summary before continuing
C. Execute both permitted calls and return results matched by tool-use ID
D. Display the text as the final answer

## D1-Q02 | Objective 1.1

A tool response says "all done" but stop_reason is tool_use. Which signal controls the loop?

A. Whether at least one tool previously succeeded
B. The protocol stop reason and requested tool blocks
C. The phrase all done
D. Whether the text is nonempty

## D1-Q03 | Objective 1.1

The model reaches max_tokens while producing an extraction. What is the strongest handling?

A. Mark the response incomplete and apply a bounded recovery policy
B. Persist the valid-looking prefix
C. Treat the response as end_turn because generation stopped
D. Raise the global turn cap and mark this attempt successful

## D1-Q04 | Objective 1.1

A support loop hits its resource limit with an ownership check unfinished. What should it return?

A. A resolved status because the configured loop ended
B. A refund based on the last likely owner
C. A final answer claiming no matching order
D. An incomplete status with saved progress and the unresolved check

## D1-Q05 | Objective 1.2

All research workers finish, but privacy was never assigned. What should the coordinator change?

A. Treat worker completion as complete research coverage
B. Run synthesis repeatedly over the same results
C. Track coverage against the original question and delegate the missing topic
D. Increase every worker output limit

## D1-Q06 | Objective 1.2

A simple request always launches six specialists and becomes slow. What is the best redesign?

A. Remove the coordinator and let workers negotiate privately
B. Select workers based on task needs and avoid unnecessary delegation
C. Give every specialist the full task and use the first answer
D. Double all worker budgets

## D1-Q07 | Objective 1.3

A synthesis worker receives only "combine previous findings" in an isolated session. What is missing?

A. Explicit findings, sources, constraints and output requirements
B. A larger model temperature
C. A longer description of the synthesis role only
D. A promise that parent memory is shared

## D1-Q08 | Objective 1.3

Two workers must independently read disjoint source collections. There is spare capacity. What is appropriate?

A. Serialize them because all multi-agent tasks require ordering
B. Let both edit the shared final report concurrently
C. Skip aggregation and concatenate whichever finishes first
D. Run them concurrently and aggregate attributed results

## D1-Q09 | Objective 1.3

A current Agent SDK reviewer is preapproved for Read and Grep. What additional measure creates a narrow capability set?

A. Rely only on the reviewer description
B. Give it Bash to make a read-only role convenient
C. Set explicit available tools and enforce underlying read-only permissions
D. Assume allowed_tools hides every unlisted capability

## D1-Q10 | Objective 1.4

A model supplies verified=true with a refund call. What must the service use?

A. The model confidence in ownership
B. Authentication and approval state from trusted application context
C. The model flag if its schema is valid
D. The most recent conversation summary

## D1-Q11 | Objective 1.4

A refund call times out after being sent to the provider. What is the safest next action?

A. Reconcile the original operation using its stable idempotency identity
B. Send a fresh refund with a new key
C. Assume timeout means no money moved
D. Mark it committed because the request was sent

## D1-Q12 | Objective 1.4

An operation key already identifies a 2000-cent refund. A retry uses 3000 cents under that key. What should happen?

A. Return a new 3000-cent receipt
B. Silently update the old receipt amount
C. Treat every repeated key as harmless regardless of arguments
D. Reject the request fingerprint conflict

## D1-Q13 | Objective 1.5

A team wants to block an unauthorized tool call before it executes. Which interception point fits?

A. A summary generated after the final response
B. An audit export at session end
C. PreToolUse with a trusted gate
D. PostToolUse with a warning

## D1-Q14 | Objective 1.5

A critical guard callback may crash. What should the design include?

A. Move the entire check to PostToolUse
B. Supported fail-closed hook configuration plus service-side authorization
C. Assume every exception blocks automatically
D. Convert guard exceptions to unconditional approval

## D1-Q15 | Objective 1.5

Two tools return epoch and ISO timestamps. Where should actual normalization happen?

A. In a deterministic result adapter or appropriate post-tool processing
B. Only in a prompt asking the final model to prefer UTC
C. By dropping all timestamps
D. In a prerequisite ownership gate before the calls return

## D1-Q16 | Objective 1.6

A user reports a missing package and a duplicate charge. What is the best decomposition?

A. Treat the latest concern as replacing the earlier one
B. Give the same full request to every specialist
C. Resolve shipping first and assume billing is the same cause
D. Investigate each concern with relevant evidence, then synthesize one response

## D1-Q17 | Objective 1.6

A candidate report is repeatedly sent back with "improve it." What is the best control improvement?

A. Increase the number of identical reviewers indefinitely
B. Remove all validation to reduce iterations
C. Define measurable criteria, targeted feedback and bounded refinement
D. Continue until the model reports very high confidence

## D1-Q18 | Objective 1.7

A resumed session remembers yesterday's order eligibility. What should happen before a refund?

A. Increase context length to preserve yesterday's observation
B. Revalidate current authoritative order and approval state
C. Trust the saved transcript as a transaction snapshot
D. Fork the session to make the old fact current

## D1-Q19 | Objective 1.7

Two forked coding sessions start from one transcript and use the same directory. What remains shared?

A. The live filesystem unless separate checkouts are supplied
B. Only immutable baseline files
C. No resources because forks snapshot everything
D. Only model usage counters

## D1-Q20 | Objective 1.4

A human escalation recipient cannot see the agent transcript. What handoff is best?

A. The final sentence from the model
B. The entire raw tool log without a case summary
C. A confidence score and no evidence
D. Verified facts, attempted actions, committed outcomes, gaps and next decision
