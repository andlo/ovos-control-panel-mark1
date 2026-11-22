"""What the editors send must be what ovos-PHAL-plugin-mk1 reads: each test
pins the shape its handler expects."""
import pytest
from ovos_utils.fakebus import FakeBus

from ovos_control_panel_mark1 import device as mark1

WATCHED = ("enclosure.mouth.display", "enclosure.mouth.viseme_list")


@pytest.fixture
def sent():
    bus = FakeBus()
    seen = []
    for topic in WATCHED:
        bus.on(topic, lambda m: seen.append(m))
    return bus, seen


def _find(seen, msg_type):
    for message in seen:
        if message.msg_type == msg_type:
            return message
    raise AssertionError(f"{msg_type} was never sent; got {[m.msg_type for m in seen]}")


def test_the_faceplate_drawing_sends_a_string_the_plugin_can_lower(sent):
    """ovos-PHAL-plugin-mk1 does `clear_previous.lower() == "true"`, so a bool
    raises there and nothing is drawn, whichever way the box is ticked."""
    bus, seen = sent
    grid = [[0] * 32 for _ in range(8)]
    mark1.display_grid(bus, grid, x=0, y=0, clear=True)

    value = _find(seen, "enclosure.mouth.display").data["clearPrev"]
    assert isinstance(value, str), f"clearPrev must be a string, got {type(value).__name__}"
    assert value.lower() == "true"

    seen.clear()
    mark1.display_grid(bus, grid, x=0, y=0, clear=False)
    assert _find(seen, "enclosure.mouth.display").data["clearPrev"].lower() == "false"


def test_a_viseme_is_dated_now_so_the_plugin_does_not_skip_it(sent):
    """The plugin writes a viseme only while `time.time() < start + end`, so a
    start of 0 puts every viseme in the past and none is ever shown."""
    import time

    bus, seen = sent
    mark1.mouth_viseme(bus, 3)

    data = _find(seen, "enclosure.mouth.viseme_list").data
    assert data["start"] > time.time() - 60, (
        "start is a timestamp, not an offset; the plugin skips anything already past"
    )
    (code, end), = data["visemes"]
    # the plugin concatenates the code onto "mouth.viseme="
    assert isinstance(code, str), f"the viseme code must be a string, got {type(code).__name__}"
    assert code == "3"
    assert data["start"] + end > time.time(), "the viseme is over before it is drawn"
