"""Home page layout contract: req42 reading order, persistent nav, latest
changes and the vault status strip. No pytest.

The home page is what a workshop sees on the projector first. Its tiles must
follow the req42 block order (01 Business Goals → 12 Risks), every page must
carry the same navigation bar, and the reader must be able to tell at a glance
what moved in the vault since they last looked.

Run from the dashboard dir:
    .venv/bin/python tests/test_home_layout.py
"""
import os
import sys
import tempfile
import time
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
(_tmp / "sources").mkdir()
os.environ["WIKI_DIR"] = str(_wiki)
os.environ["ADR_DIR"] = str(_tmp / "adr")
os.environ["RAW_SOURCES_DIR"] = str(_tmp / "sources")
os.environ["WIKI_CONFIG"] = str(_tmp / "wiki.yaml")
os.environ["DASH_STARTUP_GRACE"] = "3600"
os.environ["DASH_HEARTBEAT_GRACE"] = "3600"

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))  # import app.py

import app  # noqa: E402

QR = """---
id: QR-001
type: quality-requirement
title: Fast checkout
status: draft
created: 2026-09-07
updated: 2026-09-07
sources: []
related: []
tags: [quality-requirement]
---

# Fast checkout
"""
ORDER = ["tile-vision", "tile-stakeholders", "tile-scope", "tile-backlog", "tile-models",
         "tile-quality", "tile-constraints", "tile-glossary", "tile-issues", "tile-adrs", "tile-changes"]


def _home():
    app._PARSE_CACHE.clear()
    return app.app.test_client().get("/").get_data(as_text=True)


def test_tiles_follow_req42_reading_order():
    body = _home()
    positions = [body.index(k) for k in ORDER]          # raises if a tile is missing
    assert positions == sorted(positions), positions
    assert "tile-req42" not in body and "tile-search" not in body


def test_every_page_has_the_main_nav():
    c = app.app.test_client()
    for route in ("/", "/glossary", "/issues", "/req42/backlog"):
        body = c.get(route).get_data(as_text=True)
        assert 'class="mainnav"' in body, route
        assert 'id="nav-search"' in body, route


def test_quality_tile_counts_and_changes_tile_lists_the_page():
    f = _wiki / "quality-requirements" / "QR-001-fast-checkout.md"
    f.write_text(QR, encoding="utf-8")
    # backdate it: a file written this second renders as "just now", which
    # would not exercise the relative-time branch the tile is there for
    os.utime(f, (time.time() - 600, time.time() - 600))
    try:
        body = _home()
        q = body[body.index("tile-quality"):body.index("tile-constraints")]
        assert '<span class="num">1</span>' in q, q
        ch = body[body.index("tile-changes"):]
        assert "QR-001" in ch and "Fast checkout" in ch, ch[:600]
        assert "ago" in ch
    finally:
        f.unlink()


def test_recent_changes_shape():
    (_wiki / "glossary" / "GLO-001-x.md").write_text(
        QR.replace("QR-001", "GLO-001").replace("quality-requirement", "glossary-term"),
        encoding="utf-8")
    try:
        app._PARSE_CACHE.clear()
        rows = app.recent_changes(5)
        assert rows and set(rows[0]) >= {"id", "title", "kind", "url", "when"}, rows
        assert rows[0]["url"] == "/page/glossary/GLO-001-x"
    finally:
        (_wiki / "glossary" / "GLO-001-x.md").unlink()


def test_vault_status_strip():
    body = _home()
    assert 'class="vault-status"' in body
    assert "open issue" in body           # "0 open issues" on the empty vault


if __name__ == "__main__":
    test_tiles_follow_req42_reading_order()
    test_every_page_has_the_main_nav()
    test_quality_tile_counts_and_changes_tile_lists_the_page()
    test_recent_changes_shape()
    test_vault_status_strip()
    print("OK: home layout, navigation and latest changes")
