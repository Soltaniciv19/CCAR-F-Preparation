"""Offline orchestration model; this is not the Claude Agent SDK runtime."""

import json
from dataclasses import dataclass, asdict


@dataclass
class State:
    task: str
    completed: dict
    failures: dict
    events: list


def execute(task, workers, hook=lambda event: None, state=None):
    state = state or State(task, {}, {}, [])
    if state.task != task:
        raise ValueError("checkpoint task does not match")
    for name, worker in workers.items():
        if name in state.completed:
            continue
        event = {"worker": name, "task": task, "phase": "start"}
        state.events.append(event)
        hook(event)
        try:
            state.completed[name] = worker({"task": task, "role": name})
            state.failures.pop(name, None)
        except Exception as exc:
            state.failures[name] = type(exc).__name__
    return state


def save(state):
    return json.dumps(asdict(state), sort_keys=True)


def resume(data):
    return State(**json.loads(data))
