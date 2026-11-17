# Domain 2 exercises

Attempt these in `work/domain2/`; solutions and question answers are in a separate file.

## Lab 1: Redesign ambiguous tools (2.1, 2.3)

Replace `manage_customer(text)` and `do_order_action(text)` with clear contracts for accessible order lookup, refund request and human handoff. For each specify when to use it, when not to use it, JSON input schema, returned evidence, errors and side effects. Keep authenticated identity outside model arguments.

Deliver a tool-routing table for five user requests, Python definitions and a role-to-tool matrix for researcher, support coordinator and billing executor. Acceptance: a researcher cannot request a payment through an alternate broadly scoped tool, and overlapping descriptions no longer select the wrong operation in your designed test cases.

## Lab 2: Recover without erasing errors (2.2)

Implement a read wrapper with at most three attempts and exponential delay. Inject two timeouts then success, a permission failure, malformed ID and a successful empty result. Use an injected sleeper to make offline checks immediate.

Deliver an error envelope and a next-action table. Acceptance: timeout is retryable, permission failure is not blindly retried, empty success remains successful, and exhausted recovery retains error type and attempt count. Explain how a refund timeout differs from a read timeout and design reconciliation before retry.

## Lab 3: Read-only MCP server and catalog (2.4)

Build a local stdio server with one exact-ID order tool and a catalog resource. Use only synthetic data. Run it through a client, list tools/resources, invoke the tool, then read the catalog. Use stderr for diagnostics.

Deliver Python server, launch configuration and a host-client-server diagram. Acceptance: the catalog can be discovered, unknown orders produce an explicit no-match result, and no real account data or credentials are embedded. Design how remote Streamable HTTP authentication and tenant isolation would differ from this local fixture.

## Lab 4: Trace a Python call through aliases (2.5)

Create a tiny package with `api.py -> exported alias in __init__.py -> backend.py`. Ask a code assistant to identify all callers, then make one targeted change to the backend validation. Record which tool is used for filename discovery, content search, exact reading, editing and test execution.

Deliver a cited call path and before/after behavior. Acceptance: searching the original function name alone is shown to miss the alias caller; the final trace includes it. Simulate a nonunique Edit anchor and describe how re-reading current contents leads to a safe targeted edit or reviewed full-file fallback.

For each lab include one normal case, two failures, a design diagram and one limitation. Use the 10-point rubric from Domain 1.
