# Domain 2 answers and implementation guide

## Lab 1 solution: narrow contracts and roles

[LOOKUP_TOOL](../../ccarf/tools.py) states exact-ID selection, accessible scope, read-only behavior and null-on-no-match semantics. `lookup_order` validates the runtime input and checks the trusted customer's scope. It returns the same no-match behavior for inaccessible and absent orders to avoid exposing another customer's records.

A billing write contract additionally needs amount units, policy prerequisites, stable operation key, committed receipt fields and unknown-outcome semantics. A handoff contract needs the unresolved decision and attempted actions, not an arbitrary conversation dump. Researchers get only source tools; the coordinator gets lookup and handoff; an authorized adapter invokes gated billing. Backend credentials must enforce the same separation.

## Lab 2 solution: bounded read recovery

Reference: [retry_read](../../ccarf/tools.py).

```python
from ccarf.tools import retry_read

attempts = iter([TimeoutError(), TimeoutError(), {"ok": True, "data": []}])
delays = []


def read():
    outcome = next(attempts)
    if isinstance(outcome, Exception):
        raise outcome
    return outcome


result = retry_read(read, sleep=delays.append)
assert result["ok"] and result["attempts"] == 3
assert delays == [0.1, 0.2]
```

A nonretryable authorization failure exits on the first attempt. Empty success is not retried merely because it is empty. A programming error is not silently converted to no matches. Production backoff needs jitter, service-provided retry guidance and an overall deadline.

A lost refund response is an unknown write outcome. Check the original operation/provider receipt and use the same provider-supported idempotency key. Do not generalize this read helper into a payment retry decorator.

## Lab 3 solution: actual MCP protocol surface

The pinned implementation is [mcp_order_server.py](../../examples/mcp_order_server.py). It registers `get_order` and `orders://catalog` on `MCPServer`. The fixed customer is explicitly a fixture, not a production authentication mechanism. Use a launch command such as the following in a disposable repo's project `.mcp.json`, replacing both absolute paths:

```json
{
  "mcpServers": {
    "order-lab": {
      "type": "stdio",
      "command": "/absolute/path/to/.venv-study/bin/python",
      "args": ["/absolute/path/to/CCAR-F/examples/launch_mcp.py"]
    }
  }
}
```

The absolute launcher makes the course root importable regardless of the host's working directory. Inspect both paths before using them; the interpreter must have the optional MCP dependency installed. The MCP protocol itself does not define a universal host configuration schema.

For a real remote server, bind credentials to the requesting tenant, authenticate the transport, enforce authorization in handlers, limit returned fields and paginate catalogs. A resource does not automatically become model context; the host/client must expose or read it according to its integration.

The SDK-contract checks and MCP round-trip verification are in [verification](../../verification/test_sdk_contracts.py). The server maps application failures to a `CallToolResult` with Python `is_error=True` (wire field `isError`). A successful no-match result remains `is_error=False`, with `data=null`. Structured error metadata is retained in the content and structured payload.

## Lab 4 solution: follow every exported name

Use Glob to locate modules, Grep for definitions and exports, Read to inspect the wrapper and backend, then Grep each discovered alias. Keep `api endpoint -> imported alias -> backend symbol` with exact files and revision. Use Edit on a unique current block. If the anchor is ambiguous, re-read instead of repeatedly guessing. Run the relevant behavior check with Bash.

The important deliverable is evidence of the complete call path. Reading the whole repository indiscriminately is slower and can dilute context without resolving the alias relationship.

## Exam-style question key


### D2-Q01: B

**Rewrite selection boundaries and evaluate discriminating cases.** Misrouting caused by overlapping contracts needs a contract repair, not generic prompting or more randomness.

### D2-Q02: A

**Exact-ID order lookup plus a separately gated refund operation.** Different side effects and authorization requirements justify separate narrow contracts.

### D2-Q03: D

**Business ownership and authorization of the requested record.** Schemas constrain structure, not authority or policy eligibility.

### D2-Q04: C

**Evidence unavailable with a transient error and attempts.** Timeout is not negative evidence. Preserve failure semantics for the coordinator.

### D2-Q05: B

**Return a successful empty result.** A successful empty result is a legitimate observation within the query scope.

### D2-Q06: A

**Stop blind retries and repair authorization or escalate.** Authorization failures need changed permissions or a legitimate alternative, not inference or repeated identical requests.

### D2-Q07: D

**Bounded backoff with preserved attempt metadata.** Safe transient read recovery can be local and bounded. Metadata keeps the history observable.

### D2-Q08: C

**Expose narrow research tools and enforce read-only backend permissions.** Tool scope reduces ambiguity; backend permission enforcement limits actual authority.

### D2-Q09: B

**The requested next tool selection.** Selection control is not service authorization, full workflow enforcement or a transaction receipt.

### D2-Q10: A

**The model may still choose not to call a tool.** Strict argument shape and the decision to call are separate properties.

### D2-Q11: D

**A host manages client connections to one or more capability servers.** MCP separates the AI host, client connections and servers that expose capabilities.

### D2-Q12: C

**A resource with a stable URI.** Resources expose addressable content and catalogs without inventing business mutations.

### D2-Q13: B

**Send diagnostics to stderr and reserve stdout for protocol traffic.** Stdio is a protocol channel. Unframed logs corrupt transport independently of model behavior.

### D2-Q14: A

**Streamable HTTP with an explicit authentication design.** Remote deployment needs a supported network transport and authentication; stdio fits local processes.

### D2-Q15: D

**Project .mcp.json with environment-based credential references.** Project scope shares reviewed configuration. Dependencies, credentials and server approval still need environment setup.

### D2-Q16: C

**An appropriate maintained server and its auth/capability fit.** Use existing integrations when fit is good, but inspect permissions and behavior. MCP standardization is not a trust guarantee.

### D2-Q17: B

**Grep for content references and discovered aliases.** Callers are content references; path matching alone misses symbols and aliases.

### D2-Q18: A

**Glob with a suitable filename pattern.** Filename discovery is path matching. Inspect content after narrowing relevant files.

### D2-Q19: D

**Read current content and select a unique context or reviewed full-file fallback.** Ambiguity is evidence to re-read. Safe editing requires current unique context and preservation of other content.

### D2-Q20: C

**Search every discovered exported alias and follow imports.** Wrapper aliases change the names callers use; progressive tracing must include those names.
