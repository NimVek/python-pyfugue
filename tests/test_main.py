"""Tests for `pyfugue` package."""
import pytest

from pyfugue import main  # noqa: E0611


@pytest.mark.parametrize(
    ("argument", "expected"),
    [
        ("--help", "show this help message and exit"),
        ("-h", "show this help message and exit"),
        ("--version", "pyfugue "),
    ],
)
def test_standard_arguments(capsys, argument, expected):
    with pytest.raises(SystemExit):
        main.main(args=[argument])
    captured = capsys.readouterr()
    assert expected in captured.out
