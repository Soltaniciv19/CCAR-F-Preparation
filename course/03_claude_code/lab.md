# Disposable configuration lab

This activity creates only local fixture files. It is offline unless you choose to run Claude Code; its availability and authentication are separate from this course's Python environment. Before using a CLI, consult the [current rules](https://code.claude.com/docs/en/memory) and [skills](https://code.claude.com/docs/en/skills) documentation.

1. Create `exercise/sandbox/` and a small `src/example.py` inside it. Add a `CLAUDE.md` with a concise instruction for that sandbox. Add a path-scoped rule under `.claude/rules/` for Python files and a skill under `.claude/skills/` that asks for a short explanation before a change. Include current documented frontmatter and a `SKILL.md`. Do not place a secret in any file.
2. Write down what you expect to apply inside and outside the matching path. Inspect parent project guidance and any imports: hierarchy and imports affect context. An instruction file is not a security boundary.
3. Propose a small two-file refactor and a one-line typo fix. Choose plan or direct edit for each and explain the risk. Make a small change inside the sandbox, review its diff and refine it against your criteria. Without a Git repository, compare the original and edited files manually.
4. Design a noninteractive review output with file, line, severity and evidence. Describe how CI would validate those fields and handle an unsupported finding before displaying it.

**Check:** The rule and skill are in the disposable project, include the documented metadata, and have clear scopes. If Claude Code is available, verify actual loading there; inspecting the files alone does not establish runtime behavior. Remove only the `exercise/sandbox/` directory you created to reset it; this deletes its contents, so save any notes elsewhere first.
