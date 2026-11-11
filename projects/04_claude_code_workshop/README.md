# P4 — Claude Code workshop

**Objectives:** investigate a defect with focused tools, distinguish planning from a direct edit, add scoped guidance and a reusable skill, and review a multi-file change. **Prerequisites:** D2, D3, D5. **Time:** 60–90 minutes. **Mode:** fixture and tests offline; the interactive Claude Code part requires an authenticated CLI.

The disposable store quote fixture calculates subtotal, discount and shipping. A discount currently applies to shipping too. Find the defect, plan a small change across `app.py` and `pricing.py`, then implement and review it. Do not use a production repository. Instructions and rules influence the assistant; they are not a security boundary.

1. Create a new workspace: `python projects/04_claude_code_workshop/make_sandbox.py /tmp/ccar-p4-work` (choose a path that does not exist). The script never overwrites a directory. Make another copy for a reset; keep your previous work.
2. From that directory, start Claude Code with a supported Haiku selection, for example `claude --model haiku`. Use `/status` or `/model` to inspect the active model. Ask for a hint or review, not an implementation; make changes yourself.
3. Locate the calculation with focused search and file reads. Explain why you chose those tools. Predict the result for subtotal 100, rate 0.1 and shipping 10 before running `python app.py 100 0.1 10`.
4. Plan the multi-file change. Make `pricing.py` own the pricing calculation and validate finite non-negative values and a finite rate between 0 and 1. `app.py` should call it and emit JSON with `total` or a nonzero exit on invalid values. Shipping is added after the discount. A direct edit may be enough for a trivial typo; explain why this change merits a plan.
5. Add a path-scoped rule under `.claude/rules/` for Python files and a skill under `.claude/skills/` that asks for a quote test before changing pricing. Inspect the loaded instructions in your installed Claude Code version. Record the paths and what applied; this check requires the CLI.
6. Run `P4_WORKSPACE=/tmp/ccar-p4-work python -m pytest projects/04_claude_code_workshop/tests -q` from the course root, then review your changes in a Git diff if you initialized Git in the sandbox. Explain the tests, the scope of the rule, and remaining risks.

The default tests check the reference solution: `python -m pytest projects/04_claude_code_workshop/tests -q`. Tests check behavior, not whether Claude loaded a rule. The `solution/` directory contains one possible implementation; ask the tutor before opening it. An extension is to use `Decimal` for currency and add edge cases. Reflection: what did focused investigation omit, and when would you broaden it?
