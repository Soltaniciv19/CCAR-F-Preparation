# Evidence and investigation lab

Work offline using synthetic data. Write notes under `exercise/`.

1. Compress this trace into at most four lines: order `O-17`; lookup succeeded; policy source `policy-a`, dated `2025-01-01`, says 14 days; source `policy-b`, dated `2025-02-01`, says 30 days; a third source timed out; ten unrelated debug lines were printed. Preserve the exact order ID, both source dates and facts, and the timeout.
2. The customer asks for a refund on day 20. List what remains unknown (including policy applicability), and produce an escalation message without executing a refund. Mark coverage partial because the third source failed.
3. Imagine a repository with `src/refunds.py`, `src/search.py` and many unrelated files. First search for the policy decision and inspect matching call sites. Explain why dumping the whole repository can obscure the evidence.
4. Make a table of source, date, claim and applicability. Explain why the later date alone does not prove supersession. Assign a qualitative confidence level and say what evidence would change it.

**Check:** The summary keeps provenance and the exact identifier; the failure is explicit; no refund is authorized by an unsupported assumption. A human decision is needed if the applicable policy remains unresolved.
