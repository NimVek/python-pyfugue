import pytest

from pyfugue.contrib.messaging import (
    ContentMessage,
    Publisher,
    SimpleMessage,
    publish,
    subscribe,
)


@pytest.mark.parametrize("subscriber", [lambda message: print(message.content)])
def test_register(subscriber, capsys):
    publisher = Publisher(None)
    publisher.subscribe("test", subscriber)
    publisher.publish(ContentMessage("test", "local"))

    captured = capsys.readouterr()

    assert captured.out == "local\n"


@pytest.mark.parametrize(
    ("topic", "output"), [("subscribed", "subscribed\n"), ("notsubscribed", "")]
)
def test_topic(topic, output, capsys):
    publisher = Publisher(None)
    publisher.subscribe("subscribed", lambda message: print(message.topic))
    publisher.publish(SimpleMessage(topic))

    captured = capsys.readouterr()

    assert captured.out == output


@pytest.mark.parametrize(
    ("subscriber", "output"),
    [
        (
            (
                (lambda message: print("first"), 100),
                (lambda message: print("second"), 0),
            ),
            "first\nsecond\n",
        ),
        (
            (
                (lambda message: print("first"), -100),
                (lambda message: print("second"), 0),
            ),
            "second\nfirst\n",
        ),
    ],
)
def test_order(subscriber, output, capsys):
    publisher = Publisher(None)
    for i in subscriber:
        publisher.subscribe("test", i[0], i[1])
    publisher.publish(SimpleMessage("test"))

    captured = capsys.readouterr()

    assert captured.out == output


def test_discard(capsys):
    def discard(message):
        message.discard()

    publisher = Publisher(None)
    publisher.subscribe("test", lambda x: print("first"), 100)
    publisher.subscribe("test", discard, 50)
    publisher.subscribe("test", lambda x: print("second"))
    publisher.publish(SimpleMessage("test"))

    captured = capsys.readouterr()

    assert captured.out == "first\n"


@pytest.mark.parametrize("subscriber", [lambda message: print(message.content)])
def test_register_global(subscriber, capsys):
    subscribe("test", subscriber)
    publish(ContentMessage("test", "global"))

    captured = capsys.readouterr()

    assert captured.out == "global\n"


@pytest.mark.parametrize(
    ("topic", "propagate", "output"),
    [("propagate", True, "global\nlocal\n"), ("nopropagate", False, "local\n")],
)
def test_propagate(topic, propagate, output, capsys):
    subscribe(topic, lambda x: print("global"), 50)
    publisher = Publisher()
    publisher.subscribe(topic, lambda x: print("local"), 25)
    publisher.publish(SimpleMessage(topic), propagate)

    captured = capsys.readouterr()

    assert captured.out == output


def test_complex(capsys):
    subscribe("complex", lambda x: print("complex_global"), 50)
    p1 = Publisher()
    p1.subscribe("complex", lambda x: print("complex_p1"), 25)
    p2 = Publisher()
    p2.subscribe("complex", lambda x: print("complex_p2"), 20)

    p1.publish(SimpleMessage("complex"))
    print(":next:")
    p2.publish(SimpleMessage("complex"))
    print(":next:")
    p1.publish(SimpleMessage("complex"), False)

    captured = capsys.readouterr()

    assert captured.out == "".join(
        (
            "complex_global\n",
            "complex_p1\n",
            ":next:\n",
            "complex_global\n",
            "complex_p2\n",
            ":next:\n",
            "complex_p1\n",
        )
    )
