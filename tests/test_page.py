"""The panel finds this page through its entry point and serves it."""
from ovos_webui import pages


def test_the_panel_finds_the_page_and_loads_it_cleanly():
    reg = pages.load()
    page = reg.by_id()["mark1"]
    assert page.package == "ovos-control-panel-mark1" and not page.builtin
    assert not [p for p in reg.problems if p.get("page") == "mark1"]


def test_the_page_is_served(token_client):
    token_client.headers["Authorization"] = "Bearer s3cret-token"
    assert 'id="mark1-canvas"' in token_client.get("/mark1").text
