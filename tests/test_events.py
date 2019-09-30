import pytest

from ctl.events import Events

def test_subscribe_and_trigger():
    events = Events()

    status = [0]
    def handler(events, n, *args, **kwargs):
        status[0] += n
    events.on("test", handler)
    events.trigger("test", n=1)
    assert status[0] == 1

    status = [0]
    def handler(events, *args, **kwargs):
        status[0] = kwargs.get("n",0)+kwargs.get("c",0)
    events.on("test", handler)
    events.trigger("test", n=1, c=1)
    assert status[0] == 2


def test_unsubscribe():
    events = Events()

    status = [0]
    def handler(events, n, *args, **kwargs):
        status[0] += n
    events.on("test", handler)
    events.trigger("test", n=1)
    assert status[0] == 1

    events.trigger("test", n=1)
    assert status[0] == 2

    events.off("test", handler)
    events.trigger("test", n=1)
    assert status[0] == 2


def test_one():
    events = Events()

    status = [0]
    def handler(events, n, *args, **kwargs):
        status[0] += n
    events.one("test", handler)
    events.trigger("test", n=1)
    assert status[0] == 1

    events.trigger("test", n=1)
    assert status[0] == 1

