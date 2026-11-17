# Domain 5: 20 original exam-style questions

Choose one best answer (A-D). Record your reason and the decisive scenario constraint. The answer guide is separate. These are original study items, not official exam content.

## D5-Q01 | Objective 5.1

A summary changes a verified refund amount from 1200 to 2100 cents. What design prevents authority drift?

A. A higher output-token cap
B. Ask the model to remember the original amount better
C. A separate trusted facts store populated from service results
D. A longer narrative summary only

## D5-Q02 | Objective 5.1

A long session loses an exact order ID. What is the best remedy?

A. Trust the most recent guessed identifier
B. Persist and reinclude critical facts with evidence references
C. Increase only maximum output tokens
D. Remove all source locators from summaries

## D5-Q03 | Objective 5.1

A team enables prompt caching. Which assumption is incorrect?

A. The cache becomes a durable current business-state database
B. Eligible repeated prefixes may reduce processing cost
C. Cache behavior depends on request structure
D. Critical facts still need authoritative storage

## D5-Q04 | Objective 5.2

A user explicitly asks for a human during an otherwise simple case. What should happen?

A. Force the user through every automated step first
B. Escalate only if sentiment is negative
C. Ask the model to convince the user to remain automated
D. Honor the request and hand over a useful case packet

## D5-Q05 | Objective 5.2

Two plausible customer records match a name before a refund. What is next?

A. Choose the closest spelling
B. Refund both and ask later
C. Request an approved disambiguating identifier before action
D. Choose the most recent account

## D5-Q06 | Objective 5.2

An angry customer needs a routine authorized replacement and has not requested a human. What fits?

A. Infer a policy exception from the tone
B. Acknowledge the concern and resolve within policy
C. Escalate solely because of sentiment
D. Deny the request to reduce risk

## D5-Q07 | Objective 5.2

A polite customer requests an exception absent from policy. What should happen?

A. Escalate to an authorized decision maker with the policy gap
B. Invent a reasonable exception
C. Approve because the customer is polite
D. Retry the policy lookup until wording changes

## D5-Q08 | Objective 5.3

One of three independent research workers times out after bounded recovery. What should the coordinator receive?

A. A successful empty list with no error
B. A claim that the topic has no evidence anywhere
C. Nothing until every worker succeeds
D. Failure category, attempted method, partial findings and missing scope

## D5-Q09 | Objective 5.3

Two research topics succeed and one optional background topic is unavailable. What final handling may be appropriate?

A. Discard every useful result automatically
B. Invent a background statistic from the summary
C. Use supported findings and disclose the coverage gap
D. Claim complete coverage because most workers succeeded

## D5-Q10 | Objective 5.3

Which distinction matters after a payment tool timeout?

A. High model confidence versus low confidence alone
B. Unknown outcome versus confirmed failure
C. Positive sentiment versus negative sentiment
D. Long response versus short response

## D5-Q11 | Objective 5.4

A repository investigation restarts on a new commit. What should a manifest loader indicate?

A. Saved findings need revalidation against current files
B. All completed work is automatically current
C. The old session ID authorizes current code changes
D. The model should ignore the saved evidence entirely

## D5-Q12 | Objective 5.4

An exploration worker read 80 files. What should it return to preserve coordinator context?

A. Every file verbatim
B. Only an unsupported conclusion
C. A summary with all locators removed
D. Concise findings with paths, symbols, revision and limitations

## D5-Q13 | Objective 5.4

What should a crash-recovery manifest preserve?

A. Only a model confidence value
B. Only the total token count
C. Completed tasks, pending work, source revision and artifact references
D. Only the final answer text

## D5-Q14 | Objective 5.5

Typed cases are 99% accurate and handwritten cases 79%, with 97% overall. What should guide review?

A. The model's highest confidence label
B. Segment-specific error and impact, not the aggregate alone
C. The 97% score as proof every segment is safe
D. Only document count

## D5-Q15 | Objective 5.5

The model claims 0.98 confidence for fields. What makes a threshold defensible?

A. Calibration against independently labeled representative outcomes
B. Treat 0.98 as measured accuracy automatically
C. Use the same threshold for all fields and impacts
D. Ask the model to restate the score

## D5-Q16 | Objective 5.5

An audit samples only low-confidence records. What blind spot remains?

A. No blind spot because confidence is exact
B. Only output formatting
C. Only low token usage
D. Confidently wrong outputs in high-confidence strata

## D5-Q17 | Objective 5.5

Rare strata are oversampled equally with common strata. How should overall accuracy be estimated?

A. Ignore rare strata entirely
B. Average model confidence instead of labels
C. Weight strata by their production population shares
D. Use the unweighted pooled sample as production accuracy

## D5-Q18 | Objective 5.6

Two sources report different values for different years and populations. What is the best treatment?

A. Call every difference a contradiction
B. Preserve both and label them not directly comparable
C. Average them into one definitive value
D. Choose the larger number

## D5-Q19 | Objective 5.6

Comparable primary sources disagree on the same metric and period. What should synthesis do?

A. Keep attribution, flag conflict and seek targeted verification
B. Choose whichever was read last
C. Remove both source IDs to simplify the report
D. Invent a midpoint without a method

## D5-Q20 | Objective 5.6

A publication dated 2026 reports data collected in 2025. Which fields should be retained?

A. Only the newer-looking date
B. Only the file download timestamp
C. No dates because they confuse comparisons
D. Both publication date and observation period
