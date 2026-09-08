"""Maturity bars: the four-bucket status distribution (accepted / review /
draft / deprecated) rendered as a thin stacked bar on every home tile and at
the top of each list page. No pytest.

Run from the dashboard dir:
    .venv/bin/python tests/test_maturity.py
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
os.environ["DASH_STARTUP_GRACE"] = "3600"
os.environ["DASH_HEARTBEAT_GRACE"] = "3600"

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE))

import app  # noqa: E402

GLO = """---
id: {id}
type: glossary-term
title: {title}
status: {status}
created: 2026-09-07
updated: 2026-09-07
sources: []
related: []
tags: [glossary]
---

# {title}

**Definition.** Something.
"""


def test_maturity_buckets_and_aliases():
    m = app.maturity(["draft", "accepted", "proposed", "superseded", "resolved", "weird", ""])
    by = {s["status"]: s["n"] for s in m["segments"]}
    assert by == {"accepted": 2, "review": 1, "draft": 3, "deprecated": 1}, by
    assert m["total"] == 7
    assert sum(s["pct"] for s in m["segments"]) in (99, 100, 101)
    assert [s["status"] for s in m["segments"]] == ["accepted", "review", "draft", "deprecated"]
    assert app.maturity([]) == {"total": 0, "segments": [], "label": "nothing yet"}


def test_bar_renders_on_home_tile_and_list_page():
    for i, st in ((1, "draft"), (2, "accepted")):
        (_wiki / "glossary" / f"GLO-00{i}-t{i}.md").write_text(GLO.format(id=f"GLO-00{i}", title=f"T{i}", status=st), encoding="utf-8")
    try:
        app._PARSE_CACHE.clear()
        c = app.app.test_client()
        home = c.get("/").get_data(as_text=True)
        tile = home[home.index("tile-glossary"):home.index("tile-issues")]
        assert 'maturity-seg maturity-accepted" style="flex-basis: 50%"' in tile, tile
        assert "maturity-draft" in tile
        page = c.get("/glossary").get_data(as_text=True)
        assert 'class="maturity' in page
    finally:
        for i in (1, 2):
            (_wiki / "glossary" / f"GLO-00{i}-t{i}.md").unlink()


if __name__ == "__main__":
    test_maturity_buckets_and_aliases()
    test_bar_renders_on_home_tile_and_list_page()
    print("OK: maturity bars")
