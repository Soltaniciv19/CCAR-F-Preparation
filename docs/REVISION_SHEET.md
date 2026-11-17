# Decision rules for final revision

Read these as conditional architectural rules. Explain the constraint behind each before using it to answer a scenario.

| Observed problem | Prefer | Avoid |
|---|---|---|
| Text plus tool calls | Follow stop reason; return every matching result | Stopping at the text |
| Turn/token/deadline cap reached | Incomplete outcome with progress | Labeling the run resolved |
| Missing research topic | Coverage check and targeted delegation | Repeated synthesis over unchanged evidence |
| Worker needs earlier facts | Explicit structured handoff | Imaginary shared conversation memory |
| Sensitive side effect | Trusted service prerequisites and idempotency | Model-provided verification flags |
| Lost write response | Reconcile original operation identity | New-key blind retry |
| Hook must prevent a call | PreToolUse with tested failure semantics | Prevention only in PostToolUse |
| Forked implementations | Separate file-changing checkouts | Assuming conversation forks snapshot files |
| Tool misrouting | Distinct selection contracts and trace evaluation | More vague prompting |
| Timeout versus no match | Separate unavailable error from successful empty | Erasing both into [] |
| Permanent permission failure | Repair scope/credentials or escalate | Identical retries |
| Local MCP server | stdio and stderr diagnostics | Debug prints on stdout |
| Remote MCP service | Supported network transport plus auth | Treating protocol compatibility as trust |
| Discover source hierarchy | Catalog/resource | Repeated blind scans |
| Find paths / find symbols | Glob / Grep | Confusing names with source content |
| Teammate misses instructions | Check project versus user scope | Increasing model output budget |
| Cross-directory conventions | Path-scoped rules | Duplicated nested files everywhere |
| Verbose optional workflow | Isolated on-demand skill | Always-loaded recipe |
| Large uncertain migration | Investigation and plan | Immediate broad edits |
| Small clear fix | Scoped direct execution and verification | Unnecessary architecture ceremony |
| Ambiguous transformation | Concrete examples and failed cases | Try harder |
| CI execution | Print mode, envelope validation, bounded subprocess | Interactive hangs or false clean reviews |
| Noisy review category | Explicit criteria, labels and boundary examples | Confidence language alone |
| Schema-valid extraction | Check semantics, source support and policy | Treating shape as truth |
| Contradictory source total | Preserve stated and computed values | Invented balancing data |
| Missing source page | Retrieve before extraction retry | Guessing absent facts |
| Nightly independent volume | Batch with IDs/status recovery | Position-based result mapping |
| Short blocking SLA | Bounded synchronous processing | Assuming batch latency is guaranteed |
| Large patch | Local plus integration passes | Only isolated file review |
| Long conversation | Persistent facts/evidence plus summary | Summary as ledger |
| Explicit human request | Prompt useful handoff | Mandatory automated exhaustion first |
| Ambiguous identity | Approved clarification then authentication | Closest-match guessing |
| Weak small segment | Segment-specific evaluation and review | Aggregate accuracy only |
| High reported confidence | Calibrate and audit high-confidence strata | Treating scores as measured accuracy |
| Different source statistics | Compare units, period, population and method | Averaging incomparable observations |

Complete [the practice exam](../practice-exam/EXAM.md) without this sheet, then explain every error using the full theory chapters.
