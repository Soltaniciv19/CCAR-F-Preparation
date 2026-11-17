"""Check course navigation, assessment integrity, coverage and Python syntax offline."""

from __future__ import annotations

import ast
import json
import re
from collections import Counter
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
CONTENT_DIRS = (
    "domains",
    "docs",
    "ccarf",
    "examples",
    "capstone",
    "verification",
    "scripts",
    "practice-exam",
)


def main():
    failures = []
    paths = list(ROOT.glob("*.md"))
    for folder in CONTENT_DIRS:
        paths.extend((ROOT / folder).rglob("*.md"))
    for path in paths:
        content = path.read_text()
        # Examples may intentionally show files to create; inspect actual prose links.
        prose = re.sub(r"```.*?```", "", content, flags=re.S)
        for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", prose):
            if "://" in target or target.startswith(("#", "mailto:")):
                continue
            local = target.split("#", 1)[0]
            if local and not (path.parent / unquote(local)).exists():
                failures.append(f"Broken link: {path.relative_to(ROOT)} -> {target}")
        if "<!-- QUESTION_KEY -->" in content:
            failures.append(f"Unfinished answer key: {path}")
    domain_index = json.loads((ROOT / "practice-exam/question-index.json").read_text())
    mock_index = json.loads((ROOT / "practice-exam/mock-index.json").read_text())
    if len(domain_index) != 100 or len(mock_index) != 60:
        failures.append("Expected 100 domain and 60 mixed assessment items")
    if Counter(q["domain"] for q in domain_index) != {d: 20 for d in range(1, 6)}:
        failures.append("Expected 20 questions per domain")
    if Counter(q["domain"] for q in mock_index) != {1: 16, 2: 11, 3: 12, 4: 12, 5: 9}:
        failures.append("Mixed-exam weight approximation changed")
    expected_objectives = {
        f"{d}.{n}"
        for d, count in [(1, 7), (2, 5), (3, 6), (4, 6), (5, 6)]
        for n in range(1, count + 1)
    }
    if {q["objective"] for q in domain_index} != expected_objectives:
        failures.append("Domain questions must cover all 30 objectives")
    question_paths = sorted((ROOT / "domains").glob("*/QUESTIONS.md"))
    question_paths.append(ROOT / "practice-exam/EXAM.md")
    rendered_items = {}
    for path in question_paths:
        text = path.read_text()
        for match in re.finditer(
            r"^#{2,3} ((?:D[1-5]-Q|M)\d{2})[^\n]*\n(.*?)(?=^#{2,3} |\Z)", text, flags=re.M | re.S
        ):
            qid, body = match.groups()
            options = re.findall(r"^([A-D])\. (.+)$", body, flags=re.M)
            if [letter for letter, _ in options] != list("ABCD"):
                failures.append(f"Four labeled options required: {qid}")
            if len({option for _, option in options}) != 4:
                failures.append(f"Duplicate option text: {qid}")
            if qid in rendered_items:
                failures.append(f"Duplicate question ID: {qid}")
            rendered_items[qid] = body
    all_index = domain_index + mock_index
    if set(rendered_items) != {q["id"] for q in all_index}:
        failures.append("Rendered questions and indexes disagree")
    domain_answers = "\n".join(
        p.read_text() for p in (ROOT / "domains").glob("*/ANSWERS_AND_SOLUTIONS.md")
    )
    mock_answers = (ROOT / "practice-exam/ANSWERS.md").read_text()
    for q in all_index:
        source = mock_answers if q["id"].startswith("M") else domain_answers
        if not re.search(rf"^#+ {q['id']}: {q['answer']}(?:\s|$)", source, flags=re.M):
            failures.append(f"Missing or mismatched answer: {q['id']}")
    for folder in sorted((ROOT / "domains").iterdir()):
        required = {
            "README.md",
            "THEORY.md",
            "EXERCISES.md",
            "QUESTIONS.md",
            "ANSWERS_AND_SOLUTIONS.md",
            "solution.py",
        }
        if not required <= {p.name for p in folder.iterdir()}:
            failures.append(f"Incomplete domain folder: {folder.name}")
        if len(re.findall(r"^## Lab \d:", (folder / "EXERCISES.md").read_text(), re.M)) != 4:
            failures.append(f"Expected four labs: {folder.name}")
    py_count = 0
    for folder in CONTENT_DIRS:
        for path in (ROOT / folder).rglob("*.py"):
            ast.parse(path.read_text(), filename=str(path))
            py_count += 1
    if failures:
        raise SystemExit("\n".join(failures))
    print(
        f"PASS: {len(paths)} Markdown files, {len(rendered_items)} questions, "
        f"30 objectives, 20 labs, {py_count} Python files; local links and keys consistent"
    )


if __name__ == "__main__":
    main()
