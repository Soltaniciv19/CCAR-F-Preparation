# Tool design lab

Work offline. No external service is needed.

1. Improve the description “handles orders” into separate read-only `lookup_order` and simulated `request_escalation` descriptions. State required inputs, output and side effects. Give the research role only the lookup tool and a read-only policy resource.
2. Draw `client → MCP server → synthetic records`. Label which item is a tool, which is a resource, and how a client finds the server. Define a missing-order error and a temporary-unavailability error and decide which could be retried with a limit.
3. Create a temporary fixture directory under `exercise/` with two short text files, one mentioning `refund_policy`. Use a focused search such as `rg -n refund_policy exercise/` and inspect the matching file. Compare a file read, a search and a shell command: which operation is needed at each step? Delete only the fixture files you created when done.

**Check:** The tool schema requires an order ID, descriptions expose side effects, roles have the minimum tools, and missing records are not labeled transient. Project P3 implements a local MCP server; this diagram does not simulate the protocol.
