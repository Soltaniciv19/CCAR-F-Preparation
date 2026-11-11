"""Implement a bounded Messages-style agent; see README for the contract."""

from dataclasses import dataclass, field


@dataclass
class Result:
    status: str
    text: str = ""
    messages: list = field(default_factory=list)
    decision: dict = field(default_factory=dict)


def dispatch(name, arguments):
    raise NotImplementedError


def run(client, prompt, max_turns=4):
    raise NotImplementedError
