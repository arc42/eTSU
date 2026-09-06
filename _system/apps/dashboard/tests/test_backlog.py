"""Plain-assert test for build_backlog() — no pytest dependency.

Run from the dashboard dir inside a venv that has the app's requirements:
    python3 -m venv .venv
    .venv/bin/pip install -q -r requirements.txt
    .venv/bin/python tests/test_backlog.py

WIKI_DIR is left unset so app.py falls back to the repo's wiki/ folder,
making today's real FR hierarchy the test oracle.
"""
import sys
from pathlib import Path

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
    # FR-008 is a curated, fully broken-down epic: 3 features, 3+1+3 = 7 stories.
    fr008 = by_id["FR-008"]
    feat_ids = [f["id"] for f in fr008["features"]]
    assert feat_ids == ["FR-009", "FR-010", "FR-011"], feat_ids
    assert fr008["n_features"] == 3, fr008["n_features"]
    assert fr008["n_stories"] == 7, fr008["n_stories"]

    # Story order within a feature is driven by the `order` frontmatter, not by
    # ID, so assert membership (as sets) rather than sequence.
    feat_by_id = {f["id"]: f for f in fr008["features"]}
    fr009_stories = {s["id"] for s in feat_by_id["FR-009"]["stories"]}
    assert fr009_stories == {"FR-012", "FR-013", "FR-014"}, fr009_stories
    fr010_stories = {s["id"] for s in feat_by_id["FR-010"]["stories"]}
    assert fr010_stories == {"FR-015"}, fr010_stories
    fr011_stories = {s["id"] for s in feat_by_id["FR-011"]["stories"]}
    assert fr011_stories == {"FR-016", "FR-017", "FR-018"}, fr011_stories

    # FR-001 has stories hung straight off the epic; more may be added later,
    # so assert SUPERSET (>=) rather than equality.
    fr001_direct = {s["id"] for s in by_id["FR-001"]["direct_stories"]}
    assert fr001_direct >= {"FR-019", "FR-020", "FR-021"}, fr001_direct

    # at least one leaf epic with no children at all
    fr007 = by_id["FR-007"]
    assert fr007["n_features"] == 0, fr007["n_features"]
    assert fr007["n_stories"] == 0, fr007["n_stories"]
    assert fr007["features"] == [], fr007["features"]

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
    assert "ENABLER" in dia and "FR-008" in dia
    # two levels only — no story IDs leak into the overview map
    assert "FR-012" not in dia
    print("OK goal-epic diagram:", dia.count("-->"), "edges")


def test_fr_subtree_diagram_string():
    bl = app.build_backlog()
    # epic root: features + a nested story, all clicking to their own FR page
    fr008 = next(e for e in bl["epics"] if e["id"] == "FR-008")
    dia = app._mermaid_fr_subtree(fr008)
    assert dia is not None and dia.startswith("graph TD"), (dia or "")[:40]
    assert "FR-008" in dia and "FR-009" in dia and "FR-012" in dia
    assert "/functional-requirements/FR-012-figurenkatalog-importieren" in dia
    assert "/page/functional-requirements/" not in dia  # no links to the old route

    # feature root: just its stories
    fr009 = next(f for f in fr008["features"] if f["id"] == "FR-009")
    fdia = app._mermaid_fr_subtree(fr009)
    assert fdia is not None and "FR-009" in fdia and "FR-013" in fdia, fdia

    # leaf (childless epic, or a story) yields no diagram
    fr007 = next(e for e in bl["epics"] if e["id"] == "FR-007")
    assert app._mermaid_fr_subtree(fr007) is None
    story = fr008["features"][0]["stories"][0]
    assert app._mermaid_fr_subtree(story) is None
    print("OK fr-subtree diagram:", dia.count("-->"), "edges")


def test_fr_ancestors():
    # FR-012 (story) -> FR-009 (feature) -> FR-008 (epic), root first
    chain = [a["id"] for a in app._fr_ancestors("FR-012-figurenkatalog-importieren")]
    assert chain == ["FR-008", "FR-009"], chain
    # an epic has no ancestors
    assert app._fr_ancestors("FR-008-stammdatenpflege") == []
    print("OK fr ancestors:", chain)


def test_fr_route_redirect_and_404():
    app.app.config["TESTING"] = True
    client = app.app.test_client()
    bl = app.build_backlog()
    epic_stem = next(e["stem"] for e in bl["epics"] if e["id"] == "FR-008")
    story_stem = next(
        s["stem"] for e in bl["epics"] for f in e["features"] for s in f["stories"]
    )

    # epic page: full text + breakdown + Product-Backlog breadcrumb (not "Suche")
    resp = client.get(f"/functional-requirements/{epic_stem}")
    assert resp.status_code == 200, resp.status_code
    body = resp.get_data(as_text=True)
    assert "Product Backlog" in body and "Aufschlüsselung" in body
    assert "FR-009" in body                       # a child feature listed

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
    html = app.render_wikilinks("Als [[STK-006-ligapraesident|Ligapräsident]] …", titles, links)
    assert '<a class="wl" href="/page/stakeholders/STK-006-ligapraesident">Ligapräsident</a>' in html, html

    # an FR target resolves to the rich FR route, not /page
    html2 = app.render_wikilinks("siehe [[FR-008-stammdatenpflege]]", titles, links)
    assert 'href="/functional-requirements/FR-008-stammdatenpflege"' in html2, html2

    # provenance and unresolved targets stay non-link spans
    assert '<span class="wl">' in app.render_wikilinks("[[raw/sources/SRC-008-x|Q]]", titles, links)
    assert '<span class="wl">' in app.render_wikilinks("[[Voellig-Unbekannt]]", titles, links)

    # inline-snippet callers pass no link index -> nothing becomes a link
    assert "<a " not in app.render_wikilinks("[[STK-006-ligapraesident|X]]", titles, None)
    print("OK wikilinks -> hyperlinks")


if __name__ == "__main__":
    test_build_backlog_counts_and_shape()
    test_goal_epic_diagram_string()
    test_fr_subtree_diagram_string()
    test_fr_ancestors()
    test_fr_route_redirect_and_404()
    test_body_wikilinks_become_hyperlinks()
    print("ALL PASSED")
