"""The Mark-1 faceplate editors: a page for ovos-control-panel.

A panel extension: the panel finds this page through the
``opm.control_panel.page`` entry point (see pyproject.toml and the panel's
docs/pages.md, "Panel extensions"). It takes the place of the plain Mark-1
page the panel brings for ovos-PHAL-plugin-mk1, and adds what a
controlpanel.json cannot say: drawing the mouth and the eye rings, a live
preview, animations and firmware updates. Nothing here runs outside the
panel.
"""


def routes(r):
    # imported here, so reading PAGE needs no web framework
    from ovos_control_panel_mark1.api import routes as add
    add(r)


PAGE = {
    "api_version": 1,
    "id": "mark1",
    "path": "/mark1",
    "title": {"key": "nav.mark1", "label": "Mark-1 faceplate"},
    "group": "screen",
    "order": 30,
    "needs": ["ovos-PHAL-plugin-mk1"],
    "html": "page.html",
    "icon": "icon.svg",
    "heading": {"key": "hdr.mark1", "label": "Mark-1 faceplate"},
    "i18n": "i18n",
    "routes": routes,
}
