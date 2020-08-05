"""The Session module."""


class Session:  # noqa: R0903
    """The Session manages all session related information."""

    def __init__(self, app):
        """Construtor.

        Args:
            app: the app the session resides in
        """
        self.app = app
        self.ui = self.app.ui.create()
