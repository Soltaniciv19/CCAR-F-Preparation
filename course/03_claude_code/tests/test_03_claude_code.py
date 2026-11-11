def test_rule_scope(module):
    assert module.applies("src/main.py")
    assert module.applies("src/pkg/app.py")
    assert not module.applies("tests/test_app.py")
    assert not module.applies("src/readme.md")


def test_unsafe_or_non_string_paths(module):
    assert not module.applies("/src/main.py")
    assert not module.applies("src/../other.py")
    assert not module.applies(None)
