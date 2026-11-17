# Domain 3 exercises

Use a fresh disposable repository. The examples below are tasks to implement, not instructions to change your global Claude configuration.

## Lab 1: A team receives consistent instructions (3.1, 3.3)

A monorepo has Python API code, infrastructure and tests spread across packages. Only one engineer gets the intended testing conventions because the instructions are in their home directory.

Design a project `CLAUDE.md`, imported testing standard, package-specific instruction and path rules for Python tests and infrastructure. Keep universal instructions short. Verify loaded files with `/memory` and compare a matching/nonmatching file. Deliver the directory tree, contents and a scope table. Acceptance: a new teammate receives committed team guidance while personal preferences stay personal.

## Lab 2: Isolated tracing skill (3.2)

Create an `inspect-flow` project skill with a description, `argument-hint`, `context: fork` and read-oriented tool configuration. Give it a Python entrypoint and require paths, symbols, evidence and unresolved questions. Describe a personal variant under a different name.

Deliver the `SKILL.md`, invocation transcript and a negative test for missing arguments. Acceptance: the output is concise and attributable. Explain why `argument-hint` is not input validation and why `allowed-tools` should not be assumed to be an exclusive sandbox in current releases.

## Lab 3: Choose and refine the workflow (3.4, 3.5)

Compare a 40-file database-client migration with a one-line null check whose location and expected behavior are known. For the migration, write an investigation plan with competing approaches, risks and acceptance criteria. For the null check, give concrete input/output cases and make the scoped change.

Deliver mode selection with rationale, two transformation examples, a failing-case report and revised implementation plan. Acceptance: the migration plan cites discovered interfaces; the small fix does not require an unnecessary architecture process. Show which interacting requirements belong in one feedback message.

## Lab 4: Structured independent CI review (3.6)

Write a Python adapter that invokes `claude -p` with a JSON findings schema, no shell interpolation and a timeout. Parse the result envelope, reject failed runs and return the structured payload. Feed a fresh reviewer requirements, patch, tests and prior finding dispositions.

Deliver adapter and mocked subprocess checks. Acceptance: timeout, nonzero exit, invalid JSON and missing `structured_output` all fail visibly. Repeated unchanged findings do not create duplicate comments; unresolved findings remain tracked. Explain how a fresh reviewer differs from asking the generator session to check itself.

Use the shared 10-point lab rubric. Live CLI invocation is optional; mocked result envelopes suffice for the adapter exercise.
