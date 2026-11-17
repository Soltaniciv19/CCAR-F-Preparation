# Verification results

Verified on 17 November 2026 using the versions recorded in [compatibility](COMPATIBILITY.md).

| Check | Result |
|---|---|
| Python behavioral and optional SDK/MCP checks | 40 tests passed, plus 12 parameterized subtests |
| Disposable Claude Code workshop | Two behavioral tests passed from its generated directory |
| Course integrity | 160 question/key pairs, 30 objectives, 20 labs and local Markdown links consistent |
| Python lint and formatting | Passed for course implementations, examples, solutions and verification scripts |
| Offline demo, capstone and five domain solution scripts | Executed successfully |
| Editable package installation | Succeeded in an isolated verification environment |

The SDK checks serialize a structured-output request through an in-memory HTTP mock, construct Agent SDK options and a fail-closed hook, and launch a real local MCP server/client over stdio from a different working directory. MCP coverage includes discovery, catalog resource reading, successful lookup, execution error and successful no-match behavior.

No paid Claude API requests, live model evaluations, real payments or remote CI executions were performed. Offline checks establish application contracts and local integration behavior; they do not establish live model quality, account access, feature availability on a chosen model, or production operational guarantees.

Reproduce from the course root:

```bash
python3 -m unittest discover -s verification -v
python3 scripts/check_repository.py
python3 -m examples.offline_demo
python3 -m capstone.solution
```

The standard-library run skips four optional checks if SDK dependencies are absent. With the optional environment installed, run `python -m pytest -q` and the lint commands in [setup](SETUP.md). The existing user environment and project configuration were not replaced.
