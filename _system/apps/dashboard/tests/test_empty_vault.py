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
]
NOT_FOUND_ROUTES = [
    "/page/glossary/GLO-001-nothing",
    "/functional-requirements/FR-001-nothing",
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


def test_ping_is_204():
    client = app.app.test_client()
    assert client.post("/ping").status_code == 204


def test_data_model_diagrams_are_none_when_no_entities():
    assert app.build_data_model_full_diagram() is None
    assert app.build_data_model_kind_diagram() is None


# routes whose empty state must tell the reader what to do next
CTA_ROUTES = ["/", "/glossary", "/stakeholders", "/goals", "/req42/backlog",
              "/data-model", "/issues"]


def test_empty_views_offer_a_next_step():
    client = app.app.test_client()
    for route in CTA_ROUTES:
        body = client.get(route).get_data(as_text=True)
        assert "raw/" in body, \
            f"{route} empty state does not tell the reader to add a source"


if __name__ == "__main__":
    test_all_get_routes_render_empty()
    test_missing_pages_are_404_not_500()
    test_ping_is_204()
    test_data_model_diagrams_are_none_when_no_entities()
    test_empty_views_offer_a_next_step()
    print(f"OK: {len(GET_ROUTES)} routes render on an empty vault")
