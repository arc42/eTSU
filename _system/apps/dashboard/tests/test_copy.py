"""UI copy contract: "client(s)" with correct plurals, empty states that name
the right next step, and no "participant" anywhere. No pytest.

Run from the dashboard dir:
    .venv/bin/python tests/test_copy.py
"""
import json
import os
import re
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
os.environ["DASH_STARTUP_GRACE"] = "3600"
os.environ["DASH_HEARTBEAT_GRACE"] = "3600"

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE))

import app  # noqa: E402

VISION = """---
id: GOAL-001
type: goal
title: A vision without objectives
status: draft
created: 2026-09-07
updated: 2026-09-07
sources: []
related: []
tags: [goal]
stereotype: vision
tile_claim: "Every piece accounted for."
---

# A vision without objectives
"""


def _client():
    app._PARSE_CACHE.clear()
    return app.app.test_client()


def test_no_participant_wording_anywhere():
    """The word is banned in the UI *and* in the code that describes it — a
    comment that still says "participant" is how the wording creeps back.
    This file is the one exception: the ban itself has to name the word."""
    bad = re.compile(r"participant", re.IGNORECASE)
    scanned = (list((HERE / "templates").glob("*.html"))
               + [p for p in (HERE / "tests").glob("test_*.py") if p.name != "test_copy.py"]
               + [HERE / "app.py", HERE / "README.md", HERE / "static" / "style.css"])
    for p in scanned:
        assert not bad.search(p.read_text(encoding="utf-8")), f"'participant' still in {p.name}"


def test_presence_list_uses_clients_key():
    c = _client()
    c.post("/ping", data=json.dumps({"client_id": "yoda"}), content_type="application/json")
    c.post("/ping", data=json.dumps({"client_id": "someone"}), content_type="application/json")
    d = c.get("/presence/list").get_json()
    assert "clients" in d and "participants" not in d, d


def test_footer_has_a_pluralisable_unit():
    body = _client().get("/glossary").get_data(as_text=True)
    assert 'id="presence-unit"' in body
    assert 'id="presence-count"' in body


def test_adr_empty_state_does_not_suggest_ingest():
    body = _client().get("/adrs").get_data(as_text=True)
    assert "architecture decision" in body.lower()
    assert "raw/" not in body, "ADRs are never produced by ingesting raw/"
    home = _client().get("/").get_data(as_text=True)
    # the ADR tile is second-to-last on the home page, ahead of "Latest changes"
    start = home.index("tile-adrs")
    end = home.index("tile-changes", start)
    assert "raw/" not in home[start:end]


def test_vision_without_objectives_has_a_hint():
    (_wiki / "goals" / "GOAL-001-vision.md").write_text(VISION, encoding="utf-8")
    try:
        body = _client().get("/").get_data(as_text=True)
        assert "Every piece accounted for." in body
        assert "No objectives yet" in body
    finally:
        (_wiki / "goals" / "GOAL-001-vision.md").unlink()


def test_search_counts_are_live():
    body = _client().get("/search").get_data(as_text=True)
    assert 'id="search-total"' in body
    assert 'data-total=' in body
    assert "function updateCounts" in body


def test_no_bare_glyph_abbreviations():
    tpl = HERE / "templates"
    for p in tpl.glob("*.html"):
        txt = p.read_text(encoding="utf-8")
        assert "⤳" not in txt, p.name
        assert not re.search(r"\}\}S\b|\}\}F\b|n_stories \}\}S", txt), f"S/F abbreviation in {p.name}"
        assert not re.search(r"\}\} (Features|Stories|Epics)\b", txt), p.name


def test_refresh_time_survives_an_unusable_tz():
    """TZ is whatever the host exports. An unknown zone must fall back to the
    host's own local time, not blow up every render with a 500."""
    saved = app.DISPLAY_TZ
    try:
        for tz in ("Not/AZone", "", "Europe/Berlin"):
            app.DISPLAY_TZ = tz
            stamp = app.inject_refresh_time()["refreshed_at"]
            assert re.match(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}", stamp), (tz, stamp)
    finally:
        app.DISPLAY_TZ = saved


def test_adr_0025_is_indexed():
    # HERE is the dashboard dir itself (tests/test_copy.py's parent.parent),
    # so parents[1] is _system/ (parents[0] is apps/).
    adr = HERE.parents[1] / "adr" / "0025-dashboard-req42-home-and-visual-identity.md"
    assert adr.is_file()
    assert "0025-dashboard-req42-home-and-visual-identity" in (HERE.parents[1] / "index.md").read_text(encoding="utf-8")


if __name__ == "__main__":
    test_no_participant_wording_anywhere()
    test_presence_list_uses_clients_key()
    test_footer_has_a_pluralisable_unit()
    test_adr_empty_state_does_not_suggest_ingest()
    test_vision_without_objectives_has_a_hint()
    test_search_counts_are_live()
    test_no_bare_glyph_abbreviations()
    test_refresh_time_survives_an_unusable_tz()
    test_adr_0025_is_indexed()
    print("OK: copy contract")
