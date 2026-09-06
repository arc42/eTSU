"""The repo's own ADRs must parse into the /adrs table — no pytest.

Unlike the other suites this one deliberately reads the real `_system/adr/`:
the ADRs ship with the starter, they are rendered on `/adrs` and on the home
tile of a fresh clone, and both defects this guards against were in that
shipped content, not in the parser.

  * five ADRs (0017, 0019-0022) used `Date:` + `## Status` + value-on-the-next-
    line instead of the house `- **Status:** … / - **Date:** …`, so they
    rendered `status=unknown, date=—` and added a spurious category to the
    status filter;
  * ADR headings are read as raw text, so `**Goal**` and `` `raw/sources/` ``
    reached the screen with their asterisks and backticks visible.

Run from the dashboard dir:
    .venv/bin/python tests/test_adr_metadata.py
"""
import os
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]

_tmp = Path(tempfile.mkdtemp())
(_tmp / "wiki").mkdir()
os.environ["WIKI_DIR"] = str(_tmp / "wiki")
os.environ["ADR_DIR"] = str(REPO / "_system" / "adr")   # the real ADRs
os.environ["WIKI_CONFIG"] = str(_tmp / "wiki.yaml")
os.environ["DASH_STARTUP_GRACE"] = "3600"
os.environ["DASH_HEARTBEAT_GRACE"] = "3600"

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))  # import app.py

import app  # noqa: E402

KNOWN_STATUSES = {"proposed", "accepted", "superseded", "deprecated", "rejected"}


def _adrs():
    with app.app.app_context():
        adrs = app.load_adrs()
    assert adrs, f"no ADRs parsed from {os.environ['ADR_DIR']}"
    return adrs


def test_every_adr_has_a_known_status():
    bad = [(a["id"], a["status"]) for a in _adrs() if a["status"] not in KNOWN_STATUSES]
    assert not bad, f"ADRs whose status line does not parse: {bad}"


def test_every_adr_has_a_real_date():
    bad = [a["id"] for a in _adrs() if a["date"] == "—"]
    assert not bad, f"ADRs whose date line does not parse: {bad}"


def test_no_adr_title_shows_raw_markdown():
    bad = [(a["id"], a["title"]) for a in _adrs()
           if "*" in a["title"] or "`" in a["title"] or "_" in a["title"]]
    assert not bad, f"ADR titles rendering markdown literally: {bad}"


def test_strip_inline_markdown_leaves_plain_text_alone():
    assert app._strip_inline_markdown("Content type **Goal** for block 01") == \
        "Content type Goal for block 01"
    assert app._strip_inline_markdown("Slim records in `raw/sources/`") == \
        "Slim records in raw/sources/"
    assert app._strip_inline_markdown("Nothing to strip here") == \
        "Nothing to strip here"


if __name__ == "__main__":
    test_every_adr_has_a_known_status()
    test_every_adr_has_a_real_date()
    test_no_adr_title_shows_raw_markdown()
    test_strip_inline_markdown_leaves_plain_text_alone()
    print(f"OK: {len(_adrs())} ADRs parse with a status, a date and a plain title")
