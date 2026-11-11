# P3: Local MCP service

**Time:** 90 minutes. **Prerequisites:** P1, D2. **Mode:** local, offline, synthetic data; no model call.

Implement a read-only MCP server in `starter/order_server.py` using the official Python SDK. Expose `lookup_order(order_id)`, `get_policy()` and a `policy://refund` resource. Distinguish missing and invalid IDs from retryable `temporary-error`. Use clear docstrings for tool descriptions and typed inputs. No mutation tool is allowed.

With project dependencies installed, run:

```sh
cd projects/03_mcp
PYTHONPATH=starter pytest tests -q
```

Compare with `PYTHONPATH=solution pytest tests -q` after your attempt. The integration test connects an actual MCP SDK client to a local stdio server and closes both. It uses synthetic data and no model. Consult [MCP documentation](https://modelcontextprotocol.io/docs/getting-started/intro) for the protocol. In a disposable Claude Code project, follow the [MCP configuration guide](https://code.claude.com/docs/en/mcp) using absolute paths to your environment's Python and your chosen `order_server.py`. Inspect the available tools and disconnect after practice. Claude Code model calls may incur charges depending on your account.

**Extension:** add a read-only order resource and test an unknown URI. **Reflection:** why should transient failures and missing records be distinct?
