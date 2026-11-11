"""Implement the offline orchestration exercise; this is not the SDK runtime."""

from dataclasses import dataclass


@dataclass
class State:
    task: str
    completed: dict
    failures: dict
    events: list


def execute(task, workers, hook=lambda event: None, state=None):
    raise NotImplementedError


def save(state):
    raise NotImplementedError


def resume(data):
    raise NotImplementedError
