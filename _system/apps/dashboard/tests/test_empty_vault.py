"""Every route must render against a vault with zero pages — no pytest.

This is the starter repo's core guarantee: on day one of a workshop the wiki
is empty and the dashboard is on a projector. A 500 here is the worst possible
first impression.

Run from the dashboard dir:
    .venv/bin/python tests/test_empty_vault.py
"""
import os
import sys
import tempfile
from pathlib import Path

WIKI_FOLDERS = [
    "glossary", "goals", "stakeholders", "context", "external-interfaces",
    "data-models", "activity-models", "use-cases", "functional-requirements",
    "quality-requirements", "constraints", "issues",
]

_tmp = Path(tempfile.mkdtemp())
_wiki = _tmp / "wiki"
for _f in WIKI_FOLDERS:
    (_wiki / _f).mkdir(parents=True)
(_tmp / "adr").mkdir()
os.environ["WIKI_DIR"] = str(_wiki)
os.environ["ADR_DIR"] = str(_tmp / "adr")
os.environ["WIKI_CONFIG"] = str(_tmp / "wiki.yaml")
# without a browser heartbeat the watchdog SIGTERMs this process (ADR-0022)
os.environ["DASH_STARTUP_GRACE"] = "3600"
os.environ["DASH_HEARTBEAT_GRACE"] = "3600"

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))  # import app.py

import app  # noqa: E402

# /leaving is deliberately NOT exercised: it arms the self-shutdown watchdog,
# which would SIGTERM this test process. Its behaviour is covered by ADR-0022.
GET_ROUTES = [
    "/", "/glossary", "/graph/glossary", "/issues", "/stakeholders", "/adrs",
    "/search", "/goals", "/data-model", "/req42", "/req42/backlog",
    "/req42/scope", "/req42/models", "/req42/quality", "/req42/constraints",
    "/join",
]
NOT_FOUND_ROUTES = [
    "/page/glossary/GLO-001-nothing",
    "/functional-requirements/FR-001-nothing",
    "/source/SRC-001-nothing",
]


def test_all_get_routes_render_empty():
    client = app.app.test_client()
    for route in GET_ROUTES:
        resp = client.get(route)
        assert resp.status_code == 200, (route, resp.status_code)
        body = resp.get_data(as_text=True)
        assert "Traceback" not in body, route
        assert "jinja2.exceptions" not in body, route


def test_missing_pages_are_404_not_500():
    client = app.app.test_client()
    for route in NOT_FOUND_ROUTES:
        resp = client.get(route)
        assert resp.status_code == 404, (route, resp.status_code)


def test_ping_returns_nickname_and_facilitator_flag():
    client = app.app.test_client()
    resp = client.post("/ping")
    assert resp.status_code == 200
    body = resp.get_json()
    assert body["nickname"] and isinstance(body["is_facilitator"], bool)


def test_data_model_diagrams_are_none_when_no_entities():
    assert app.build_data_model_full_diagram() is None


# routes whose empty state must tell the reader what to do next
CTA_ROUTES = ["/", "/glossary", "/stakeholders", "/goals", "/req42/backlog",
              "/data-model", "/issues"]


def test_empty_views_offer_a_next_step():
    client = app.app.test_client()
    for route in CTA_ROUTES:
        body = client.get(route).get_data(as_text=True)
        assert "raw/" in body, \
            f"{route} empty state does not tell the reader to add a source"


def test_vision_tile_is_an_empty_state_not_a_demo_placeholder():
    """The Vision tile is the first tile on the projector on day one.

    It used to render as `🎯 Vision [Demo] / — placeholder / "Not yet captured
    — coming soon."` — inherited chrome from the vault this dashboard was
    extracted from, where the Goal type did not exist yet. It read as "this
    dashboard is a mock-up" and was the only empty tile with no next step.
    The whole-page CTA check above cannot see it: the other tiles satisfy it.
    """
    body = app.app.test_client().get("/").get_data(as_text=True)
    assert "badge-demo" not in body, "the Demo chip is back on the empty home page"
    assert "coming soon" not in body, "the 'coming soon' placeholder line is back"
    start = body.index("tile-vision")
    tile = body[start:start + 900]
    assert "empty-state" in tile, "the empty Vision tile has no empty state"
    assert "bootstrap" in tile, "the empty Vision tile offers no next step"
    assert "placeholder" not in tile, "the Vision tile still shows a placeholder counter"


if __name__ == "__main__":
    test_all_get_routes_render_empty()
    test_missing_pages_are_404_not_500()
    test_ping_returns_nickname_and_facilitator_flag()
    test_data_model_diagrams_are_none_when_no_entities()
    test_empty_views_offer_a_next_step()
    test_vision_tile_is_an_empty_state_not_a_demo_placeholder()
    print(f"OK: {len(GET_ROUTES)} routes render on an empty vault")
