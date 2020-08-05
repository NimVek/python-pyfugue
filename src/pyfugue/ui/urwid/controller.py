"""Implementation of [IUIController](pyfugue.ui.interface.IUIController)."""
import urwid

from pyfugue.ui.interface import IUIController

from .session import UrwidUISession


__all__ = ["UrwidUIController"]


class UrwidUIController(IUIController):
    """Urwid based UI Controller."""

    def __init__(self):
        """Setup the UI with urwid."""
        self.__main = urwid.WidgetWrap(None)
        self.__loop = urwid.MainLoop(self.__main, event_loop=urwid.TwistedEventLoop())

    def start(self):
        """Starts the UI."""
        self.__loop.run()

    def stop(self):
        """Stops the UI.

        Raises:
            ExitMainLoop: to stop the ui and the application
        """
        raise urwid.ExitMainLoop()

    @property
    def active(self):
        """Returns the active UISession.

        Returns:
            the currently active UISession
        """
        return self.__main._w  # noqa: W0212

    @active.setter
    def active(self, session):
        self.__main._w = session  # noqa: W0212

    def create(self):
        """Create new UISession.

        Returns:
            new UISession
        """
        return UrwidUISession()
