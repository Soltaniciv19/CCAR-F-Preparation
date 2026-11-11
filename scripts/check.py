"""Run offline checks against reference implementations, not learner attempts."""

import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def run(args, *, cwd=ROOT, env=None):
    print(f"\n$ {' '.join(map(str, args))} (in {cwd.relative_to(ROOT) or '.'})", flush=True)
    subprocess.run(args, cwd=cwd, env=env, check=True)


def main():
    python = sys.executable
    run([python, "-m", "ruff", "check", "."])
    run([python, "-m", "ruff", "format", "--check", "."])
    run([python, "-m", "pytest", "tests", "-q"])
    env = os.environ.copy()
    env["COURSE_REFERENCE"] = "1"
    lessons = sorted(str(path / "tests") for path in (ROOT / "course").glob("0[1-5]_*"))
    run([python, "-m", "pytest", *lessons, "-q"], env=env)
    for project in sorted((ROOT / "projects").glob("0[1-3]_*")):
        project_env = os.environ.copy()
        project_env["PYTHONPATH"] = str(project / "solution")
        run([python, "-m", "pytest", "tests", "-q"], cwd=project, env=project_env)
    clean_env = os.environ.copy()
    for name in ("P4_WORKSPACE", "P5_WORKSPACE", "P6_WORKSPACE"):
        clean_env.pop(name, None)
    for project in sorted((ROOT / "projects").glob("0[4-6]_*")):
        run([python, "-m", "pytest", str(project / "tests"), "-q"], env=clean_env)


if __name__ == "__main__":
    main()
