"""Implementation of [IUISession](pyfugue.ui.interface.IUISession)."""
import urwid


class UrwidUISession(urwid.Frame):  # noqa: R0903
    """Urwid bases UI Session."""

    def __init__(self):
        """Setup the Session Windows."""
        self.__output = urwid.ListBox(urwid.SimpleListWalker([urwid.Text("Output")]))
        self.__status = urwid.Divider("_")
        self.__input = urwid.Edit()
        super().__init__(
            self.__output,
            footer=urwid.Pile([self.__status, self.__input], focus_item=1),
            focus_part="footer",
        )
