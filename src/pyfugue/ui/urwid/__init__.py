"""UI based on urwid."""
__all__ = ["create"]

from . import controller


def create() -> controller.UrwidUIController:
    """Create the urwid bases UI Controller.

    Returns:
        created Controller
    """
    return controller.UrwidUIController()
