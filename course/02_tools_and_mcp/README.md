# D2 · Tool design and MCP integration

**Objectives:** Describe and validate tools, classify errors, allocate least privilege, and distinguish MCP tools, resources and local code-search tools.  
**References:** D2.1–D2.5 in [Architecture.md](../../Architecture.md).  
**Prerequisites:** Basic Python and the preceding lesson (setup first).  
**Time:** 65–90 minutes. **Mode:** Offline, no paid calls.

## Concept

A tool description tells an agent when to use it and its schema constrains arguments; neither authorizes a side effect. Validate inputs on the server too. A missing record is different from a temporary service outage: the first generally needs different input, while a bounded retry may help the second. Grant each role only tools needed for its task.

MCP provides a client/server protocol. Tools request actions; resources expose context such as a read-only policy. Configuration identifies how a client starts or connects to a server; inspect commands and permissions before trusting them. Local file reads and focused search support investigation; shell commands can run programs and need appropriate caution. This exercise simulates a tool result rather than starting an MCP server.

## Predict and inspect

Before running the example, predict its output. Run `python course/02_tools_and_mcp/example.py` from the repository root. Change one value, predict the new result, and run it again. Restore the file afterwards.

## Exercise

Implement `lookup(order_id, records, available=True)`. Return `{"ok": True, "record": ...}` for an existing record, or `{"ok": False, "error": CODE, "retryable": BOOL}`. Reject blank/non-string IDs as `invalid_input` (not retryable), report unavailable service as `unavailable` (retryable), and missing records as `not_found` (not retryable). Validate before contacting the simulated service.

Edit only `exercise/attempt.py`; use the Python standard library and the published criteria above. Run `python -m pytest course/02_tools_and_mcp/tests -q`. The starter deliberately raises `NotImplementedError` until you implement it. Tests establish the displayed cases, not mastery or real model behavior. Add cases you consider important. For incremental help, read [hints](hints.md); the [reference solution](solution/solution.py) is separate and should be opened only for review. To check the reference, run `COURSE_REFERENCE=1 python -m pytest course/02_tools_and_mcp/tests -q` (on Windows PowerShell, set `$env:COURSE_REFERENCE='1'` first and remove it afterward).

## Apply the concept

Complete the additional [domain lab](lab.md) to practice the remaining concepts.

## Review and reflect

Answer [the scenario questions](questions.md) before looking at their answer key. Which tool descriptions and arguments would help an agent avoid using the wrong tool? Record your result, open questions and a brief reflection in [progress.md](../../progress.md).
