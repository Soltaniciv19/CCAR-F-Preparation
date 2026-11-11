from orchestration import execute, save, resume
import pytest


def test_partial_failure_and_resume():
    seen = []

    def fail(context):
        raise RuntimeError("unavailable")

    state = execute(
        "compare sources", {"research": lambda ctx: ctx["task"], "analysis": fail}, seen.append
    )
    assert state.completed == {"research": "compare sources"}
    assert state.failures == {"analysis": "RuntimeError"}
    assert len(seen) == 2
    restored = resume(save(state))
    state = execute(
        "compare sources",
        {"research": lambda _: pytest.fail("replayed"), "analysis": lambda ctx: ctx["role"]},
        state=restored,
    )
    assert state.completed["analysis"] == "analysis" and not state.failures


def test_checkpoint_does_not_change_task():
    state = execute("first", {})
    with pytest.raises(ValueError):
        execute("second", {}, state=state)
