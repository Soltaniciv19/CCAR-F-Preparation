# Troubleshooting

- **Python or pip missing:** install Python 3.11 or newer with `venv` and pip, then recreate `.venv`; on some Linux distributions these are separate packages.
- **Imports fail:** activate the virtual environment and run `python -m pip install -e '.[dev]'` from the repository root. For project exercises follow the project's `PYTHONPATH` command.
- **Exercise tests fail:** starters are intentionally incomplete. Read the acceptance criteria and hints; do not treat an uncompleted exercise as a course regression.
- **Claude Code or Haiku unavailable:** complete offline activities and check account access, installation and the current [model configuration](https://code.claude.com/docs/en/model-config). The tutor and Python API use separate configuration.
- **Authentication or billing failure:** consult your provider's current documentation. Do not paste keys into chat or fixtures. A Claude Code subscription does not imply API credit. No default course test requires credentials.
- **A documented CLI feature differs:** check the linked official docs and your installed version. The course's examples may lag the product; instructions and scoped rules are not a security boundary.
