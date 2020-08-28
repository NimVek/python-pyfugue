"""Messaging System."""

import abc

from functools import total_ordering
from typing import Any, Callable, Dict, Hashable, Optional, Set

from sortedcontainers import SortedList


__all__ = [
    "IMessage",
    "SimpleMessage",
    "ContentMessage",
    "Publisher",
    "publish",
    "subscribe",
]


class IMessage(abc.ABC):
    """Interface Message Class."""

    def __init__(self) -> None:
        """Create Interface of Message."""
        self.__discarded: bool = False

    @property
    @abc.abstractmethod
    def topic(self) -> Hashable:
        """Return topic of the message."""

    def discard(self):
        """Mark the message for discarding."""
        self.__discarded = True

    @property
    def discarded(self):
        """Return if the message is discarded.

        Returns:
            True if message should be discarded
        """
        return self.__discarded


class SimpleMessage(IMessage):
    """Simple Message."""

    def __init__(self, topic: Hashable) -> None:
        """Construct a simple contentless message.

        Args:
            topic: topic of the message
        """
        super().__init__()
        self.__topic = topic

    @property
    def topic(self):
        """Return topic of the message.

        Returns:
            Topic of the Message
        """
        return self.__topic


class ContentMessage(SimpleMessage):
    """Base Message Class."""

    def __init__(self, topic: Hashable, content: Any) -> None:
        """Create message with content.

        Args:
            topic: topic of the message
            content: content of the message
        """
        super().__init__(topic)
        self.content = content


Subscriber = Callable[[IMessage], None]


class Publisher:
    """Publisher of Messages the Subscriber subscribe to."""

    @total_ordering
    class Entry:
        """Class to hold a callable subscriber and a priority."""

        def __init__(self, subscriber: Subscriber, priority: float = 1):
            """Tests if other Entry is equal to this.

            Args:
                subscriber: Callable that is called with a message
                priority: determined the order of the subscriber
            """
            self.subscriber = subscriber
            self.priority = priority

        def __eq__(self, other):
            """Tests if other Entry is equal to this.

            Args:
                other: different Entry

            Returns:
                True if both entrys are equal
            """
            result = False
            if isinstance(other, Publisher.Entry):
                result = self.subscriber == other.subscriber
            return result

        def __le__(self, other):
            """Tests if other Entry has lesser priority than this.

            Args:
                other: different Entry

            Returns:
                True if other entry should be run before
            """
            result = False
            if not isinstance(other, Publisher.Entry):
                result = NotImplemented
            elif self.priority > other.priority:
                result = True
            elif self.priority == other.priority:
                try:
                    result = self.subscriber < other.subscriber  # type: ignore[operator]
                except TypeError:
                    result = False
            return result

    def __init__(self, parent: Optional["Publisher"] = None) -> None:
        """Create a Publisher.

        Args:
            parent: optional parent Publisher
        """
        self.__subscribers: Dict[Hashable, SortedList[Publisher.Entry]] = {}
        self.__parent = parent

    def subscribe(
        self, topic: Hashable, subscriber: Subscriber, priority: float = 1,  # noqa: C0330
    ) -> None:
        """Subscribe a fuction to a topic.

        Args:
            topic: Topic to subscribe to
            subscriber: callable that is called if a message for topic is published
            priority: lower priority is called first
        """
        subscribers = self.__subscribers.setdefault(topic, SortedList())
        subscribers.add(Publisher.Entry(subscriber, priority))

    def __entrys(self, topic: Hashable, parent: bool) -> Set["Publisher.Entry"]:
        result: Set[Publisher.Entry] = SortedList()
        if self.__parent and parent:
            result.update(self.__parent.__entrys(topic, parent))  # noqa: W0212
        result.update(self.__subscribers.get(topic, set()))
        return result

    def publish(self, message: IMessage, parent: bool = True) -> None:
        """Publish a message for a topic.

        Args:
            message: Message to publish
            parent: should the message be published to parent Publisher too
        """
        for i in self.__entrys(message.topic, parent):
            i.subscriber(message)
            if message.discarded:
                break


_publisher = Publisher(None)
Publisher.__init__.__defaults__ = (_publisher,)  # type: ignore[attr-defined]
subscribe = _publisher.subscribe
publish = _publisher.publish
