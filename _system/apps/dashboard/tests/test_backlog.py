"""Plain-assert test for build_backlog() — no pytest dependency.

Run from the dashboard dir inside a venv that has the app's requirements:
    python3 -m venv .venv
    .venv/bin/pip install -q -r requirements.txt
    .venv/bin/python tests/test_backlog.py

WIKI_DIR points at tests/fixtures/wiki, a small neutral vault, so the suite is
independent of whatever content this starter is filled with.
"""
import os
import sys
from pathlib import Path

_FIXTURE = Path(__file__).resolve().parent / "fixtures" / "wiki"
os.environ["WIKI_DIR"] = str(_FIXTURE)
os.environ["ADR_DIR"] = str(_FIXTURE.parent / "adr")
os.environ["DASH_STARTUP_GRACE"] = "3600"
os.environ["DASH_HEARTBEAT_GRACE"] = "3600"

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))  # import app.py

import app  # noqa: E402


def test_build_backlog_counts_and_shape():
    bl = app.build_backlog()

    # --- internal-consistency invariants (hold for any valid vault) ---
    assert bl["total_epics"] == len(bl["epics"]), \
        (bl["total_epics"], len(bl["epics"]))
    assert sum(e["n_features"] for e in bl["epics"]) == bl["total_features"], \
        (sum(e["n_features"] for e in bl["epics"]), bl["total_features"])
    assert sum(e["n_stories"] for e in bl["epics"]) == bl["total_stories"], \
        (sum(e["n_stories"] for e in bl["epics"]), bl["total_stories"])
    assert bl["orphans"] == [], bl["orphans"]

    by_id = {e["id"]: e for e in bl["epics"]}

    # --- stable structure (FR IDs are stable and never reused) ---
    # FR-001 is the fixture's fully broken-down epic: 1 feature, 2+1 = 3 stories.
    fr001 = by_id["FR-001"]
    feat_ids = [f["id"] for f in fr001["features"]]
    assert feat_ids == ["FR-002"], feat_ids
    assert fr001["n_features"] == 1, fr001["n_features"]
    assert fr001["n_stories"] == 3, fr001["n_stories"]

    # Story order within a feature is driven by the `order` frontmatter, not by
    # ID, so assert membership (as sets) rather than sequence.
    feat_by_id = {f["id"]: f for f in fr001["features"]}
    fr002_stories = {s["id"] for s in feat_by_id["FR-002"]["stories"]}
    assert fr002_stories == {"FR-003", "FR-004"}, fr002_stories

    # FR-001 also has a story hung straight off the epic; more may be added
    # later, so assert SUPERSET (>=) rather than equality.
    fr001_direct = {s["id"] for s in fr001["direct_stories"]}
    assert fr001_direct >= {"FR-005"}, fr001_direct

    # at least one leaf epic with no children at all (also the fixture's
    # explicit Enabler epic: goal: [])
    fr006 = by_id["FR-006"]
    assert fr006["n_features"] == 0, fr006["n_features"]
    assert fr006["n_stories"] == 0, fr006["n_stories"]
    assert fr006["features"] == [], fr006["features"]

    print("OK build_backlog:", bl["total_epics"], "epics",
          bl["total_features"], "features", bl["total_stories"], "stories")


def test_goal_epic_diagram_string():
    bl = app.build_backlog()
    dia = app._mermaid_goal_epic_tree(app.load_goals(), bl)
    assert dia is not None
    assert dia.startswith("graph TD"), dia[:40]
    # objectives present and clickable to their goal cards on /goals
    assert "GOAL-002" in dia and "/goals#GOAL-002" in dia
    # epics present and clickable to their FR page under the new folder route
    assert "FR-001" in dia and "/functional-requirements/" in dia
    # enabler epics (goal: []) stay reachable under the Plattform node
    assert "ENABLER" in dia and "FR-006" in dia
    # two levels only — no story IDs leak into the overview map
    assert "FR-003" not in dia
    print("OK goal-epic diagram:", dia.count("-->"), "edges")


def test_fr_subtree_diagram_string():
    bl = app.build_backlog()
    # epic root: features + a nested story, all clicking to their own FR page
    fr001 = next(e for e in bl["epics"] if e["id"] == "FR-001")
    dia = app._mermaid_fr_subtree(fr001)
    assert dia is not None and dia.startswith("graph TD"), (dia or "")[:40]
    assert "FR-001" in dia and "FR-002" in dia and "FR-003" in dia
    assert "/functional-requirements/FR-003-scan-a-book" in dia
    assert "/page/functional-requirements/" not in dia  # no links to the old route

    # feature root: just its stories
    fr002 = next(f for f in fr001["features"] if f["id"] == "FR-002")
    fdia = app._mermaid_fr_subtree(fr002)
    assert fdia is not None and "FR-002" in fdia and "FR-003" in fdia, fdia

    # leaf (childless epic, or a story) yields no diagram
    fr006 = next(e for e in bl["epics"] if e["id"] == "FR-006")
    assert app._mermaid_fr_subtree(fr006) is None
    story = fr001["features"][0]["stories"][0]
    assert app._mermaid_fr_subtree(story) is None
    print("OK fr-subtree diagram:", dia.count("-->"), "edges")


def test_fr_ancestors():
    # FR-003 (story) -> FR-002 (feature) -> FR-001 (epic), root first
    chain = [a["id"] for a in app._fr_ancestors("FR-003-scan-a-book")]
    assert chain == ["FR-001", "FR-002"], chain
    # an epic has no ancestors
    assert app._fr_ancestors("FR-001-lending") == []
    print("OK fr ancestors:", chain)


def test_fr_route_redirect_and_404():
    app.app.config["TESTING"] = True
    client = app.app.test_client()
    bl = app.build_backlog()
    epic_stem = next(e["stem"] for e in bl["epics"] if e["id"] == "FR-001")
    story_stem = next(
        s["stem"] for e in bl["epics"] for f in e["features"] for s in f["stories"]
    )

    # epic page: full text + breakdown + Product-Backlog breadcrumb (not "Suche")
    resp = client.get(f"/functional-requirements/{epic_stem}")
    assert resp.status_code == 200, resp.status_code
    body = resp.get_data(as_text=True)
    assert "Product Backlog" in body and "Aufschlüsselung" in body
    assert "FR-002" in body                       # a child feature listed

    # story page: a leaf still resolves (full text, no breakdown diagram)
    assert client.get(f"/functional-requirements/{story_stem}").status_code == 200

    # the old /page route 302-redirects FRs to the new path
    r = client.get(f"/page/functional-requirements/{epic_stem}")
    assert r.status_code == 302, r.status_code
    assert r.headers["Location"].endswith(f"/functional-requirements/{epic_stem}")

    # unknown stem -> 404
    assert client.get("/functional-requirements/FR-999-does-not-exist").status_code == 404
    print("OK fr route + redirect + 404")


def test_body_wikilinks_become_hyperlinks():
    titles, links = app.title_index(), app.link_index()

    # a stakeholder wikilink with an alias -> real anchor to its /page route
    html = app.render_wikilinks("As [[STK-001-librarian|the librarian]] …", titles, links)
    assert '<a class="wl" href="/page/stakeholders/STK-001-librarian">the librarian</a>' in html, html

    # an FR target resolves to the rich FR route, not /page
    html2 = app.render_wikilinks("see [[FR-001-lending]]", titles, links)
    assert 'href="/functional-requirements/FR-001-lending"' in html2, html2

    # provenance and unresolved targets stay non-link spans
    assert '<span class="wl">' in app.render_wikilinks("[[raw/sources/SRC-001-x|Q]]", titles, links)
    assert '<span class="wl">' in app.render_wikilinks("[[Totally-Unknown]]", titles, links)

    # inline-snippet callers pass no link index -> nothing becomes a link
    assert "<a " not in app.render_wikilinks("[[STK-001-librarian|X]]", titles, None)
    print("OK wikilinks -> hyperlinks")


if __name__ == "__main__":
    test_build_backlog_counts_and_shape()
    test_goal_epic_diagram_string()
    test_fr_subtree_diagram_string()
    test_fr_ancestors()
    test_fr_route_redirect_and_404()
    test_body_wikilinks_become_hyperlinks()
    print("ALL PASSED")
