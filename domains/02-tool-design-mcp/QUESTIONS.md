# Domain 2: 20 original exam-style questions

Choose one best answer (A-D). Record your reason and the decisive scenario constraint. The answer guide is separate. These are original study items, not official exam content.

## D2-Q01 | Objective 2.1

Two tools have identical descriptions and are often confused. What should be changed first?

A. Increase output tokens for every call
B. Rewrite selection boundaries and evaluate discriminating cases
C. Raise temperature to explore more tools
D. Add choose carefully to the prompt without changing contracts

## D2-Q02 | Objective 2.1

Which interface best separates evidence gathering from money movement?

A. Exact-ID order lookup plus a separately gated refund operation
B. One manage_order tool accepting arbitrary prose
C. A lookup that may issue refunds as a convenience
D. A refund function that infers identity from a name

## D2-Q03 | Objective 2.1

A tool uses a closed JSON schema. What must still be checked at execution?

A. Only whether the output is a string
B. Nothing because the schema proves safe intent
C. Only model confidence in the request
D. Business ownership and authorization of the requested record

## D2-Q04 | Objective 2.2

A search backend times out. Which returned meaning is correct?

A. No incidents exist in the domain
B. A completed research topic without results
C. Evidence unavailable with a transient error and attempts
D. Successful search with zero matches

## D2-Q05 | Objective 2.2

A valid query returns no matching records. What should the wrapper do?

A. Replace it with a likely record
B. Return a successful empty result
C. Convert it to a retryable timeout
D. Retry indefinitely until at least one match appears

## D2-Q06 | Objective 2.2

An exact-ID lookup fails because credentials lack access. What recovery is appropriate?

A. Stop blind retries and repair authorization or escalate
B. Exponential retries with unchanged credentials until the cap
C. Convert the result to not found across the whole system
D. Ask the model to infer the private data

## D2-Q07 | Objective 2.2

A read fails twice transiently and then succeeds. What recovery design fits?

A. A new model session after each failure
B. Unbounded retries with no delay
C. Return an empty list after the first failure
D. Bounded backoff with preserved attempt metadata

## D2-Q08 | Objective 2.3

A support researcher only needs policy documents. Which access design is strongest?

A. Rely solely on a role name containing researcher
B. Permit billing writes because they may be useful later
C. Expose narrow research tools and enforce read-only backend permissions
D. Offer every tool and ask it to be careful

## D2-Q09 | Objective 2.3

On a compatible model, what does named tool_choice primarily control?

A. Whether a remote write commits successfully
B. The requested next tool selection
C. All later business workflow prerequisites
D. The identity of the authenticated user

## D2-Q10 | Objective 2.3

A strict tool schema is supplied with auto selection. What should the application assume?

A. The model may still choose not to call a tool
B. The tool is guaranteed to be called exactly once
C. Every offered tool must execute
D. The service can skip argument and policy validation

## D2-Q11 | Objective 2.4

What is the relationship between an MCP host and servers?

A. Every server is a separate model
B. The model directly executes every server process without a host
C. One host can connect to only one server
D. A host manages client connections to one or more capability servers

## D2-Q12 | Objective 2.4

Which MCP feature best exposes a documentation catalog for discovery?

A. A hidden local environment variable
B. An unconditional system prompt containing every document
C. A resource with a stable URI
D. A payment mutation tool

## D2-Q13 | Objective 2.4

A local stdio server prints debug logs to stdout and protocol parsing fails. What is the fix?

A. Switch every tool to a prompt template
B. Send diagnostics to stderr and reserve stdout for protocol traffic
C. Increase the model token budget
D. Return fewer JSON properties

## D2-Q14 | Objective 2.4

A new remote multi-client MCP integration is being designed. Which transport is generally appropriate?

A. Streamable HTTP with an explicit authentication design
B. Stdio over a shared terminal log
C. Legacy SSE solely because an old blog used it
D. A folder of CLAUDE.md files instead of a transport

## D2-Q15 | Objective 2.4

A reviewed team MCP configuration should travel with Git without personal secrets. Which scope fits?

A. Only one developer's user configuration
B. A real token committed in a shared README
C. A local untracked configuration assumed to reach everyone
D. Project .mcp.json with environment-based credential references

## D2-Q16 | Objective 2.4

A standard issue-tracker integration is needed. What should be evaluated before writing a custom server?

A. Whether all issue contents can be copied into the root prompt
B. Whether JSON schemas eliminate third-party trust concerns
C. An appropriate maintained server and its auth/capability fit
D. Whether a larger model can simulate the issue tracker

## D2-Q17 | Objective 2.5

You know a function name but not its callers. Which built-in operation should start the search?

A. Bash to execute the function against production data
B. Grep for content references and discovered aliases
C. Glob matching the function name as a filename only
D. Write a replacement module

## D2-Q18 | Objective 2.5

You need all Python test filenames in an unfamiliar repository. Which tool fits?

A. Glob with a suitable filename pattern
B. Grep for every line in every file
C. Edit the root README
D. A refund lookup tool

## D2-Q19 | Objective 2.5

A targeted Edit fails because its anchor appears four times. What should happen next?

A. Keep shortening the anchor
B. Assume the first occurrence is correct
C. Overwrite the file from stale memory
D. Read current content and select a unique context or reviewed full-file fallback

## D2-Q20 | Objective 2.5

Searching a backend function name finds no API callers, but a wrapper reexports it under another name. What is next?

A. Read only its docstring
B. Increase the search output truncation limit without changing the query
C. Search every discovered exported alias and follow imports
D. Conclude the function is unused
