# Full practice exam: 60 original questions

Use 120 minutes and select one best answer per question. Do not open ANSWERS.md until finished. Four shared scenarios organize the questions. Domain allocation is 16/11/12/12/9, a rounded study approximation of the published weights, not a prediction of an actual exam form.

## Scenario: Support resolution

A retail assistant handles order status, missing parcels and refunds. Authentication is supplied by the host, payment tools can change real state, and agents use separate contexts.

### M01

The first response says "refund ready" and requests a lookup. What should the harness inspect to decide its next step?

A. stop_reason and the structured tool call
B. Only the reassuring text
C. Only the customer sentiment
D. Only whether a receipt was mentioned

### M02

An order is paid but the authenticated principal owns a different order. Where should the refund be blocked?

A. Only by asking the model to double-check
B. Inside the refund service using trusted ownership state
C. Only in the final response wording
D. Only by the schema requiring an order ID

### M03

A proposed tool both searches by name and sometimes refunds the first match. What redesign is best?

A. Keep the tool and lower temperature
B. Separate exact accessible lookup from an explicitly gated write
C. Add a longer generic description
D. Increase output tokens

### M04

The customer says "Please connect me with an agent now." What is the appropriate route?

A. Require three failed automated steps first
B. Classify emotion before deciding
C. Continue because the case seems easy
D. Handoff with verified facts and attempted actions

### M05

The request contains both a charge issue and a delivery issue. How should tasks be organized?

A. Separate concerns, run independent reads, then synthesize
B. Investigate only the first concern
C. Assign every worker both concerns with no scope
D. Respond after whichever worker returns first

### M06

The delivery backend returns a successful no-match response. What should be recorded?

A. The search succeeded with no match in its scope
B. The service was unavailable
C. The parcel definitely never existed
D. A retryable network failure

### M07

A payment request has no response after submission. What state belongs in the case record?

A. Confirmed successful payment
B. No payment attempt occurred
C. Unknown outcome pending reconciliation
D. Confirmed failed payment

### M08

A policy-research specialist is accidentally offered refund tools. What correction is strongest?

A. Add please do not refund to its description only
B. Rely on the final answer review
C. Remove write capabilities and enforce appropriate backend credentials
D. Rename it careful_researcher

### M09

The case is compacted after 40 turns. Which material should remain outside the narrative summary?

A. Exact verified IDs, amounts and committed receipt state
B. Only greetings and sentiment
C. Only the latest assistant wording
D. Every raw search page without structure

### M10

An unauthorized action is detected only after the payment result returns. What architectural change is required?

A. Increase reviewer confidence
B. Add a pre-execution gate and retain service authorization
C. Use the post-tool message to erase the transaction
D. Remove receipt logging

### M11

A tool receives an invalid identifier format. Which next action is appropriate?

A. Infer the identifier from the nearest customer name
B. Return structured validation feedback so input can be corrected
C. Retry unchanged until the service recovers
D. Return a generic successful empty result

### M12

A billing worker must use findings from delivery research. How should those findings be supplied?

A. Assume isolated sessions share memory
B. Only send the worker role name
C. Ask it to reconstruct the prior transcript from its intuition
D. Explicit structured facts with source references in its task input

### M13

Shipping research succeeds but billing remains unavailable. What should a useful handoff preserve?

A. Confirmed shipping evidence, billing error, attempts and next action
B. Only a generic unavailable message
C. A fabricated billing conclusion
D. A success flag for both topics

### M14

A saved session is resumed after the order has been refunded elsewhere. What must happen?

A. Use a new operation key without checking state
B. Read the current ledger before any new refund
C. Trust the earlier unpaid-refund state
D. Fork to remove the competing refund

### M15

The agent proposes a refund amount that differs from the confirmed user request. What should validate it?

A. Only natural-language confidence
B. Only whether the response parses as JSON
C. Only whether the tool name is correct
D. A deterministic comparison against trusted requested amount and policy

## Scenario: Repository migration and CI

A Python monorepo is migrating a shared storage client. Tests span several packages. Claude Code is used locally and in a noninteractive review job. Generated changes are reviewed separately.

### M16

Shared storage invariants are currently in a maintainer's home instruction file. Where should team guidance live?

A. The model's last answer
B. Committed project instructions with focused imported standards
C. Only the maintainer's personal memory
D. An untracked editor note

### M17

A test convention must apply across packages. Which scope best matches?

A. One unscoped rule for every unrelated file type
B. A remote MCP server description
C. Path-scoped rules matching the distributed test files
D. Only the storage directory instruction file

### M18

The migration has competing transaction and retry designs. What should precede broad implementation?

A. Edit every caller immediately
B. Increase model randomness
C. Wait for production failures to expose requirements
D. Investigate current behavior and resolve alternatives in plan mode

### M19

Mapping entrypoints and collecting fixture conventions are independent reads. How may they be scheduled?

A. Concurrently while both rewrite the same client
B. Skip one because both are discovery
C. Concurrently with scoped outputs and later aggregation
D. Only serially because both use Python

### M20

A trace command produces many pages but only a short result is needed centrally. What configuration fits?

A. A private skill assumed to be shared by Git
B. An isolated skill with context: fork and a clear output contract
C. A root instruction that always prints all traces
D. A larger main-session output limit

### M21

The old client is reexported as Store in a package initializer. Which search completes the caller map?

A. Search only the original class definition
B. Use Glob to find a file named Store only
C. Assume reexports have no callers
D. Search Store imports and uses as well as the original symbol

### M22

The migration must preserve null behavior. What input best reduces interpretation drift?

A. Only the instruction preserve behavior
B. Only an output-token increase
C. A list of unrelated style preferences
D. Concrete old/new input-output cases and failing examples

### M23

A new caller uses seconds while the shared client expects milliseconds. Which review pass targets this?

A. Only a formatting pass
B. Only isolated syntax checks
C. Only the generator's self-summary
D. A cross-file interface and units pass

### M24

The CI process must never wait for conversational input. Which flag is essential?

A. Only --verbose
B. -p or --print
C. --batch as a universal CLI mode
D. --interactive-review

### M25

The CLI exits with a JSON result indicating failure. What should the adapter do?

A. Parse any text field as an approved review
B. Silently publish an all-clear comment
C. Fail the review job with diagnostics
D. Convert it to an empty successful findings list

### M26

Two migration alternatives are implemented from a shared session baseline. What additional isolation is needed?

A. Only different branch descriptions in prompts
B. Separate checkouts for file-changing alternatives
C. Only separate conversation IDs
D. Only higher turn budgets

### M27

A rerun sees the same defect at a new line number. What should the review integration retain?

A. Stable evidence identity and unresolved disposition
B. Only the old numeric line
C. No previous findings
D. A fresh duplicate comment every run

### M28

The discovery notebook references a commit that has changed. What is the next reliability step?

A. Assume the saved summary is current
B. Delete the evidence and guess from naming
C. Increase output capacity
D. Revalidate cited paths and assumptions before acting

### M29

Retry handling and transaction behavior fail together. How should feedback be provided?

A. Ask for cleaner architecture only
B. Hide the failed tests to avoid anchoring
C. Describe both interacting failures with the shared expected contract
D. Send unrelated isolated complaints with no common context

### M30

The generator says its design is sound. What reviewer input is strongest?

A. Only its confidence score
B. Only the final success message
C. Fresh context containing requirements, patch and relevant tests
D. Only the generator's justification

## Scenario: Research and developer productivity

A coordinator compares three deployment options using web evidence, internal docs and repository analysis. Workers have isolated context, one documentation source is unavailable, and the report must remain cited.

### M31

All assigned workers finish, but operational migration risk is absent. What must the coordinator inspect?

A. Only report length
B. Only the number of agents launched
C. Coverage of the original requirements and targeted missing work
D. Only worker process exit codes

### M32

Internal documentation has a maintained topic catalog. How should an MCP integration expose it?

A. As an implicit model memory assumed always present
B. As debug output mixed into stdio
C. As an addressable resource discoverable by the host/client
D. As a refund mutation

### M33

The document analyst needs earlier web findings. What handoff preserves verifiability?

A. Claims plus source URLs, dates, locators and limitations
B. Only an informal conclusion
C. Only a worker name
D. Only raw token counts

### M34

Two reported adoption counts use different populations and collection methods. What should the report say?

A. One source is false solely because values differ
B. They are not directly comparable, with both methods attributed
C. The larger count is automatically correct
D. The average is the definitive count

### M35

The internal-doc tool times out after its read retries. What must be returned?

A. A synthesized replacement document
B. Typed unavailable status, attempts and any partial findings
C. An empty successful catalog
D. A claim that no relevant internal guidance exists

### M36

Only one option requires deep repository analysis. Which delegation strategy fits?

A. Run every specialist on every option by default
B. Remove the coordinator and let workers exchange unlogged messages
C. Skip the option to keep task counts equal
D. Select the necessary specialist for that option

### M37

Two like-for-like primary measurements disagree. How should the coordinator respond?

A. Preserve both attributions and request targeted verification
B. Choose the one that arrived last
C. Remove the discrepancy from the summary
D. Average without documenting any method

### M38

A reusable repository inspection workflow is needed only when invoked. What form fits?

A. All steps in always-loaded root memory
B. A personal-only file assumed visible to the team
C. An undocumented shell alias requiring a human terminal
D. A task-specific skill rather than a long universal instruction

### M39

A research loop keeps receiving tool requests until its deadline. What should the runtime report?

A. A definitive report based on guessed missing claims
B. A reset that discards every observation
C. A bounded incomplete result with completed evidence and pending scope
D. A success because the process stopped

### M40

A remote team evidence server is being added. Which design concern remains after choosing MCP?

A. Only output formatting
B. Only the model context size
C. Transport authentication and per-user source authorization
D. No concerns because MCP makes all content trusted

### M41

An exploration specialist reads a large code subtree. What should the coordinator retain?

A. Concise path/symbol evidence, revision and unresolved assumptions
B. Every raw file automatically
C. Only the number of files read
D. Only a generic architecture guess

### M42

The final report includes speculative defects with no reachable path. What criterion should be tightened?

A. Increase maximum findings
B. Encourage all possible issues equally
C. Require a concrete trigger and cited supporting implementation
D. Ask only for higher confidence

### M43

A synthesis evaluator detects one missing comparison column. What feedback is best?

A. Launch unrelated workers
B. Accept the report because most columns are present
C. Request targeted evidence and a revision for that missing column
D. Repeat improve everything with no specific requirement

### M44

Reviewers confuse an acceptable local pattern with a real bug. What examples help?

A. A genuine defect and a near-miss valid pattern with decision rationale
B. Only formatting samples
C. Only examples copied from the evaluation holdout
D. Only easy positives

### M45

Two evidence tools overlap: one reads a known document, the other searches a catalog. What should their contracts clarify?

A. Only the preferred tone of the answer
B. Only the model output limit
C. Only the names of the maintainers
D. Exact retrieval versus discovery inputs, outputs and selection boundaries

## Scenario: Document extraction operations

A Python pipeline processes invoices from typed and scanned sources. Nightly work tolerates delay, but a separate payment approval gate is interactive. Extracted facts need source evidence, semantic checks and review routing.

### M46

A field may be missing but must be explicit for downstream processing. Which contract fits?

A. An absent property always interpreted as zero
B. A free-form response with no schema
C. A required nullable field with a documented missingness policy
D. A required string containing a plausible placeholder

### M47

A source total conflicts with computed items. What should be persisted?

A. Only the computed value replacing the source
B. A fabricated balancing item
C. Only a success label because the schema passed
D. Both values, source evidence and conflict status

### M48

Which path should serve the interactive approval gate?

A. A bounded synchronous request rather than an assumed immediate batch
B. The nightly batch with no fallback
C. A weekly aggregation job
D. A batch client-tool loop that waits for local payment execution

### M49

A metadata extraction tool uses strict inputs with auto selection. What is still possible?

A. Every tool is called exactly once
B. The payment is authorized automatically
C. The source is guaranteed accurate
D. No tool is called in that response

### M50

A nightly batch returns mixed statuses out of order. How should results be handled?

A. Resubmit all inputs after one failure
B. Treat expired results as empty successful extractions
C. Map custom IDs, inspect each status and selectively recover failures
D. Zip outputs to source order

### M51

Overall accuracy is high but bank-account fields are weak. What should govern automation?

A. The highest self-reported confidence
B. Document count alone
C. Field-specific risk, validation and calibrated segment metrics
D. Overall accuracy alone

### M52

A validated extraction requests payment. Where must approval still be enforced?

A. Only in the extraction prompt
B. Only by requiring a numeric total
C. Only in the final report
D. In the payment service using trusted approval and policy state

### M53

A field is missing because page two was never retrieved. What is next?

A. Fill zero and mark validated
B. Retrieve the missing page before another extraction attempt
C. Repeat the same prompt over page one
D. Guess from other suppliers

### M54

The team wants consistent fixture guidance in local and CI test generation. Where should it be documented?

A. Only a personal user instruction
B. Only a generator's old conversation
C. Only a local untracked note
D. Committed project guidance referencing relevant existing tests

### M55

A current create request needs raw schema-constrained output. Which field family should be checked?

A. A historical output_format dictionary copied without checking
B. The refund idempotency key
C. Only system text saying JSON
D. output_config.format in the installed SDK documentation

### M56

What audit catches confidently wrong outputs across document types?

A. Only low-confidence records
B. Only the easiest typed documents
C. Only the newest supplier regardless of risk
D. Random samples within type, field and confidence strata

### M57

A pre-payment guard is unavailable. What failure mode should critical policy adopt?

A. Fail closed with service-level enforcement intact
B. Assume approval to preserve throughput
C. Move validation to an after-payment report
D. Use model confidence as the missing approval

### M58

The extractor mishandles informal measurements despite detailed prose. What should refinement add?

A. Only a larger response budget
B. Only repeated instructions to be accurate
C. Only a generic style guide
D. Concrete varied examples and exact validation failures

### M59

Resubmitting a whole batch after losing its creation response may do what?

A. Guarantee exactly-once execution automatically
B. Fix all oversized inputs
C. Remove the need for stable document identity
D. Duplicate cost and downstream processing unless submission is reconciled

### M60

An extraction tool returns a total without units, document identity or evidence. What contract improvement is most useful?

A. Only return a confidence score
B. Only increase the model temperature
C. Return currency, stable source identity, locators and validation status
D. Only lengthen the tool name
