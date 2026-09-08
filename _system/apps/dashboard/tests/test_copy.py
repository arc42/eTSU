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
    bad = re.compile(r"participant", re.IGNORECASE)
    for p in list((HERE / "templates").glob("*.html")) + [HERE / "app.py", HERE / "README.md"]:
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
    start = home.index("tile-adrs")
    end = home.index("tile-issues", start)
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


if __name__ == "__main__":
    test_no_participant_wording_anywhere()
    test_presence_list_uses_clients_key()
    test_footer_has_a_pluralisable_unit()
    test_adr_empty_state_does_not_suggest_ingest()
    test_vision_without_objectives_has_a_hint()
    test_search_counts_are_live()
    print("OK: copy contract")
