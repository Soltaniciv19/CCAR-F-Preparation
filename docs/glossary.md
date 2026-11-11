# Glossary

- **Agent:** an application that selects actions in response to a task and observations. Its capabilities and limits are defined by the surrounding system.
- **Tool call/result:** a model-requested operation and the application's response, linked by a call ID. The application must validate and authorize the call.
- **Stop reason:** why a model response ended; a tool request, final response and truncated response require different handling.
- **MCP:** a protocol for connecting clients to servers that expose capabilities such as tools and resources.
- **Resource:** addressable context provided by an MCP server; a tool is an operation the client can invoke.
- **Hook:** a callback at a lifecycle event that can observe or influence supported actions; exact behavior depends on the runtime.
- **Schema:** a machine-checkable description of an output's structure. Valid structure alone does not establish truth or policy compliance.
- **Provenance:** where a claim came from, including source and date where relevant.
- **Escalation:** transferring a case to a human or other authority when the system lacks evidence or permission to decide.
- **Holdout:** labeled examples reserved for evaluation rather than prompt development; their results are estimates, not proof of general performance.
