# P0: Setup and baseline

**Objectives:** create an isolated Python environment, identify the tutor model, run checks and establish a baseline. **Prerequisites:** basic shell and Python. **Time:** 30–45 minutes. **Domains:** all. **Mode:** offline except optional Claude Code access.

Follow the root README setup. Python values, functions and lists are sufficient for the initial exercises. Run `python course/00_setup/example.py` and predict the result before changing the budget. Run `python -m pytest course/00_setup/tests` to check your exercise. Start with `exercise/budget.py` and implement the function without consulting `solution/`. A failed test is expected until you complete it. Reset by copying the starter from your own backup; do not overwrite your attempt without saving it first.

For the interactive tutor, start `claude --model haiku` in the course directory, if available, and inspect `/status` or `/model`. Availability and account configuration vary. Ask the tutor to explain a Python function, then write a second test yourself. This uses Claude Code, not API credits in a Python script; billing and access depend on your account. Do not paste credentials into chat.

Answer `questions.md`, then note one result and one question in `progress.md`. Tests establish only the listed behavior; explain why a turn limit is useful. Reference answers and a solution are separate.
