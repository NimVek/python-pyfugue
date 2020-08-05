"""The application class the manages all."""
from . import ui
from .session import Session


__all__ = ["Application"]


class Application:
    """The application class the manages all."""

    def __init__(self):
        """Setup UI."""
        self.__ui = ui.create(["urwid"])

    def start(self):
        """Starts the whole application."""
        self.active = Session(self)
        self.__ui.start()

    def stop(self):
        """Stops the application and exits."""
        self.__ui.stop()

    @property
    def active(self) -> Session:
        """Returns the active [Session]().

        Returns:
            active session
        """
        return self.__active

    @active.setter
    def active(self, session: Session):
        self.__active = session
        self.ui.active = session.ui

    @property
    def ui(self):
        """Returns the used UIController.

        Returns:
            the used UIController
        """
        return self.__ui
