# Orchestration lab

Work offline on paper or in a new file in `exercise/`. No SDK or model call is needed.

1. Trace this turn: the assistant requests `lookup` with ID `a` and `policy` with ID `b`. `lookup` succeeds and `policy` fails. Draw the next user message with both IDs and identify which result is an error. Preserve the original assistant content before adding the results.
2. Design a support coordinator that delegates order research and policy research. Specify the context, allowed tools and output for each subagent. Mark the policy result as failed. How does the coordinator answer without inventing a policy?
3. Draw a fixed flow with a gate that rejects a refund unless an explicit policy says it is allowed. Compare it with an adaptive research flow and name a turn limit for each. What could a logging hook observe, and why must the gate remain in application code?
4. Write a checkpoint containing message history, pending calls and gate state. Describe resuming it, then make a copy as a fork and change only the new branch. Do not treat this simulation as evidence of Agent SDK session support.

**Check:** The trace has one result per call ID, failure is visible, the gate cannot be bypassed by model text, and the fork does not mutate the original checkpoint. Project P2 explores SDK behavior separately.
