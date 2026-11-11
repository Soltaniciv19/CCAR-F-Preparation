"""Implement the offline extraction and review interfaces."""


def validate_record(record):
    raise NotImplementedError


def process_batch(inputs, extractor, max_attempts=2):
    raise NotImplementedError


def evaluate(expected, predicted):
    raise NotImplementedError


def review(source):
    raise NotImplementedError
