# Domain 4: 20 original exam-style questions

Choose one best answer (A-D). Record your reason and the decisive scenario constraint. The answer guide is separate. These are original study items, not official exam content.

## D4-Q01 | Objective 4.1

A reviewer flags harmless comment wording. What prompt improvement most directly addresses the category?

A. Ask for higher confidence only
B. Increase output length
C. Add more unrelated style rules
D. Define observable comment-behavior contradictions and explicit exclusions

## D4-Q02 | Objective 4.1

A review category has a very high false-positive rate and erodes trust. What is appropriate?

A. Lower every severity label without changing selection
B. Ask the model to hide uncertainty
C. Disable or narrow that category while evaluating improved criteria
D. Discard every other accurate category

## D4-Q03 | Objective 4.2

Detailed extraction instructions still mishandle absent PO numbers. What example set is most useful?

A. No examples to avoid influencing the model
B. Present, absent and ambiguous PO cases with correct null/evidence behavior
C. Only five easy documents with PO numbers
D. Examples that fill absent numbers from nearby invoices

## D4-Q04 | Objective 4.2

A review format is consistent but judgment is inconsistent on similar patterns. What should examples emphasize?

A. Positive and near-miss negative decisions with evidence-based rationale
B. Only indentation of the final JSON
C. Only the maximum output length
D. Random unrelated code snippets

## D4-Q05 | Objective 4.3

What does schema-constrained final output primarily guarantee on a supported successful response?

A. That every value is true in the source
B. That business approval has been granted
C. That the document has no contradictions
D. The requested response structure

## D4-Q06 | Objective 4.3

A PO number can be missing but downstream code expects an explicit property. Which schema design fits?

A. An optional field whose absence always means not applicable
B. A free-form notes field instead of a defined contract
C. A required nullable PO property
D. A required string filled with a plausible guess

## D4-Q07 | Objective 4.3

A developer copies a deprecated raw output_format dictionary into a current create call. What should they consult?

A. The refund policy
B. The installed SDK signature and current output_config.format documentation
C. Only an older blog with the same model name
D. The model prompt to reinterpret unsupported parameters

## D4-Q08 | Objective 4.4

An invoice's items sum to 125 but its stated total is 135. What should extraction do?

A. Preserve both values and flag the contradiction
B. Invent a 10-unit adjustment item
C. Replace the stated source total with 125 silently
D. Ignore the item values because JSON is valid

## D4-Q09 | Objective 4.4

An extracted value has a quote from the wrong document version. What is the correct validation outcome?

A. Accept because the quote exists somewhere
B. Treat a valid schema as sufficient
C. Increase confidence to compensate
D. Reject or review the unsupported provenance

## D4-Q10 | Objective 4.4

A date is present but assigned to the wrong field. What feedback makes a retry useful?

A. Only the previous answer with its error hidden
B. A larger context filled with unrelated documents
C. Original source, failed record and exact field-assignment error
D. Try again with no additional information

## D4-Q11 | Objective 4.4

A supplier identifier is genuinely absent from all supplied pages. What should happen?

A. Fill a default plausible string to satisfy the schema
B. Keep it unavailable and retrieve another legitimate source or route review
C. Repeat the same extraction until it invents an identifier
D. Borrow the identifier from a similar invoice

## D4-Q12 | Objective 4.4

Why should invoice arithmetic use integer minor units or Decimal from strings?

A. To avoid binary floating-point artifacts in currency invariants
B. To prove that every source value is correct
C. To authorize payment automatically
D. To eliminate the need to inspect units or taxes

## D4-Q13 | Objective 4.5

A merge check must finish in minutes. Which processing approach fits best?

A. A batch job assumed to finish immediately
B. A daily collection queue without fallback
C. A client-tool loop embedded in one asynchronous batch item
D. Synchronous review with bounded execution

## D4-Q14 | Objective 4.5

A nightly extraction workload tolerates delayed independent results. Which API pattern fits?

A. A refund write for each document
B. A process that assumes outputs arrive in source order
C. Message Batches with per-request IDs and status handling
D. One endless interactive support session

## D4-Q15 | Objective 4.5

Batch results arrive in a different order from inputs. How should they be matched?

A. By whichever source title looks closest
B. By unique custom_id
C. By array position
D. By response length

## D4-Q16 | Objective 4.5

A 1000-request batch has 970 successes, 20 expirations and 10 oversized inputs. What should happen?

A. Retry eligible expirations and repair oversized inputs before selective resubmission
B. Resubmit all 1000 requests unchanged
C. Treat every failure as success to avoid duplicate cost
D. Retry the oversized inputs indefinitely without modification

## D4-Q17 | Objective 4.5

Collection occurs every 12 hours and processing may take 24 hours. Can this alone support a 30-hour planning target?

A. Yes, because batch always starts immediately after arrival
B. Yes, because average latency is enough for a hard bound
C. Yes, because cost discounts imply a latency guarantee
D. No, worst-case waiting plus processing approaches 36 hours

## D4-Q18 | Objective 4.6

A 25-file patch has inconsistent findings across files. Which review organization is best?

A. Only file-local passes without interface review
B. Accept every duplicate as independent evidence
C. Focused local passes plus a cross-file integration pass and deduplication
D. One longer unstructured prompt over every file

## D4-Q19 | Objective 4.6

A parser returns pieces while pricing expects boxes. Where is the key defect visible?

A. The model's self-reported confidence
B. The cross-file data/units contract
C. Only code formatting
D. Only the JSON syntax of the review

## D4-Q20 | Objective 4.6

A fresh reviewer approves generated code. What remains necessary for important behavior?

A. Evidence verification and appropriate deterministic checks
B. Nothing because context independence guarantees correctness
C. Only another confidence score
D. Discard the original requirements
