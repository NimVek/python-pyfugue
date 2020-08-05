"""Interfaces for UI."""
import abc


__all__ = ["IUIController", "IUISession"]


class IUISession(abc.ABC):  # noqa: R0903
    """User Interface Session."""


class IUIController(abc.ABC):
    """User Interface Controller."""

    @abc.abstractmethod
    def start(self):
        """Startup the User Interface."""

    @abc.abstractmethod
    def stop(self):
        """Stop the User Interface."""

    @property  # type: ignore[misc]
    @abc.abstractmethod
    def active(self) -> IUISession:
        """The active UIsession."""

    @active.setter  # type: ignore[misc]
    @abc.abstractmethod
    def active(self, session: IUISession):
        pass

    @abc.abstractmethod
    def create(self) -> IUISession:
        """Create a UISession."""
