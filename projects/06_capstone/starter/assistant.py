"""Implement the simulated support coordinator."""


class ServiceError(Exception):
    def __init__(self, message, retryable=False):
        super().__init__(message)
        self.retryable = retryable


def assist(request, services, max_calls=3):
    raise NotImplementedError
