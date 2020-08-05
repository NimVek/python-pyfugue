"""User Interfaces."""

import importlib
import typing

from .interface import IUIController


tui: typing.List[str] = ["urwid"]
gui: typing.List[str] = []

__all__ = ["create", "tui", "gui", "IUIController"]


def create(candidates: typing.List[str]) -> IUIController:
    """Create a UI Controller based on the given list of candidates.

    Args:
        candidates: list oft possible UIs


    Returns:
        one of the choosen UIController
    """
    result: IUIController

    for item in candidates:
        module = importlib.import_module(f".{item}", package=__name__)
        result = module.create()  # type: ignore[attr-defined]

    return result
