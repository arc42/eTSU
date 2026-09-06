"""Regression test for the Task 6 failure mode — no pytest dependency.

Task 6 removed the `en:` key from every REQ42_BLOCKS entry and promoted its
value into `title`, but two templates (req42.html, req42_block.html) still
referenced `.en`. Nothing raised: Jinja's default Undefined renders as an
empty string, so `<span class="req42-title">{{ b.title }}</span>` next to
`<span class="req42-en">{{ b.en }}</span>` rendered the title once and an
*empty* span next to it, and req42_block.html's lead paragraph
(`{{ block.en }} — req42-Baustein {{ block.num }}.`) rendered as a leading
blank plus a dangling em-dash: " — req42-Baustein 03.". The bug was only
caught by rendering the pages against a *populated* vault and looking — the
empty-vault suite can't see it, because on an empty vault every block's
sample list is empty too, so the missing text is invisible either way.

This test renders every GET route against the populated fixture vault
(tests/fixtures/wiki/ — GOAL/STK/FR/GLO content) and asserts that labels
which should carry text actually do.

Run from the dashboard dir:
    .venv/bin/python tests/test_populated_render.py
"""
import os
import re
import sys
from pathlib import Path

_FIXTURE = Path(__file__).resolve().parent / "fixtures" / "wiki"
os.environ["WIKI_DIR"] = str(_FIXTURE)
os.environ["ADR_DIR"] = str(_FIXTURE.parent / "adr")
os.environ["DASH_STARTUP_GRACE"] = "3600"
os.environ["DASH_HEARTBEAT_GRACE"] = "3600"

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))  # import app.py

import app  # noqa: E402

# Same non-parametrized routes as test_empty_vault.py's GET_ROUTES.
# /leaving is deliberately NOT exercised: it arms the self-shutdown watchdog,
# which would SIGTERM this test process. Its behaviour is covered by ADR-0022.
GET_ROUTES = [
    "/", "/glossary", "/graph/glossary", "/issues", "/stakeholders", "/adrs",
    "/search", "/goals", "/data-model", "/req42", "/req42/backlog",
    "/req42/scope", "/req42/models", "/req42/quality", "/req42/constraints",
]

# The 12 req42 block titles app.py now emits (REQ42_BLOCKS[*]["title"]).
# HTML-escaped once, the way Jinja's autoescape would render them.
REQ42_TITLES = [
    "Business Goals", "Stakeholders", "Scope", "Product Backlog",
    "Supporting Models", "Quality Requirements", "Constraints",
    "Domain Terminology", "Assets", "Teams", "Roadmaps",
    "Risks &amp; Assumptions",
]

# An empty label span/element that should never carry a display class but no
# text — the exact shape of the Task 6 bug (req42-en) plus a few sibling
# label classes used the same way elsewhere in the templates.
EMPTY_LABEL_RE = re.compile(
    r'<span class="(req42-title|req42-en|req42-type|term|ml-title)"[^>]*>\s*</span>'
)

# A lead paragraph that starts with a dangling separator — i.e. its first
# real content is missing and only the punctuation that was meant to follow
# it survived (the exact req42_block.html "{{ block.en }} — ..." shape).
DANGLING_LEAD_RE = re.compile(r'<p class="lead">\s*(&mdash;|—|-)\s')


def _bodies():
    client = app.app.test_client()
    out = {}
    for route in GET_ROUTES:
        resp = client.get(route)
        assert resp.status_code == 200, (route, resp.status_code)
        out[route] = resp.get_data(as_text=True)
    return out


def test_all_get_routes_render_populated():
    bodies = _bodies()
    for route, body in bodies.items():
        assert "Traceback" not in body, route
        assert "jinja2.exceptions" not in body, route


def test_no_empty_label_spans():
    bodies = _bodies()
    for route, body in bodies.items():
        m = EMPTY_LABEL_RE.search(body)
        assert m is None, f"{route}: empty label element {m.group(0) if m else ''}"


def test_no_dangling_lead_paragraphs():
    bodies = _bodies()
    for route, body in bodies.items():
        m = DANGLING_LEAD_RE.search(body)
        assert m is None, f"{route}: lead paragraph starts with a dangling separator: {m.group(0) if m else ''}"


def test_req42_lists_all_twelve_block_titles_nonempty():
    body = _bodies()["/req42"]
    for title in REQ42_TITLES:
        needle = f'<span class="req42-title">{title}</span>'
        assert needle in body, f"/req42 missing non-empty block title: {title!r}"
    # and none of the corresponding num/title pairs collapsed into an empty span
    assert '<span class="req42-title"></span>' not in body


def test_req42_block_leads_are_populated():
    # /req42/backlog is served by backlog.html (its own lead), but scope,
    # models, quality and constraints all go through req42_block.html —
    # exactly the template whose lead paragraph broke in Task 6
    # ("{{ block.en }} — req42-Baustein {{ num }}." rendered with a leading
    # blank and a dangling em-dash). Each must show "<Title> — req42 block
    # <NN>." with no gap before the dash.
    for slug, num, title in (
        ("scope", "03", "Scope"),
        ("models", "05", "Supporting Models"),
        ("quality", "06", "Quality Requirements"),
        ("constraints", "07", "Constraints"),
    ):
        body = app.app.test_client().get(f"/req42/{slug}").get_data(as_text=True)
        assert f"{title} — req42 block {num}." in body, (slug, body[:400])


if __name__ == "__main__":
    test_all_get_routes_render_populated()
    test_no_empty_label_spans()
    test_no_dangling_lead_paragraphs()
    test_req42_lists_all_twelve_block_titles_nonempty()
    test_req42_block_leads_are_populated()
    print(f"OK: {len(GET_ROUTES)} routes render on the populated fixture vault; "
          f"no empty labels, no dangling leads, all 12 req42 block titles present")
