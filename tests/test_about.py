import pytest

import pyfugue


@pytest.mark.parametrize(
    ("key", "value"),
    [
        ("title", "pyFugue"),
        ("summary", "A Mud client based on python."),
        ("uri", "https://github.com/NimVek/python-pyfugue/"),
        ("author", "NimVek"),
        ("email", "NimVek@users.noreply.github.com"),
        ("license", "GPL-3.0-or-later"),
    ],
)
def test_about(key, value):
    assert getattr(pyfugue, f"__{key}__") == value
