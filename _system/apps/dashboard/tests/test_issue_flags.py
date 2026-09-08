"""Open-issue flags on home tiles: a small badge on each tile that has at
least one OPEN issue pointing at one of its pages, plus the /issues?filter=
preselect the tile's flag links to. No pytest.

Run from the dashboard dir:
    .venv/bin/python tests/test_issue_flags.py
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
id: GLO-001
type: glossary-term
title: Tour
status: accepted
created: 2026-09-07
updated: 2026-09-07
sources: []
related: []
tags: [glossary]
---

# Tour
"""

ISS_OPEN = """---
id: ISS-001
type: issue
title: Open question about the tour
status: open
created: 2026-09-07
updated: 2026-09-07
sources: []
related: ["[[GLO-001-tour]]"]
tags: [issue]
severity: major
kind: question
---

# Open question about the tour
"""

ISS_DONE = """---
id: ISS-002
type: issue
title: Resolved question about the tour
status: resolved
created: 2026-09-07
updated: 2026-09-07
sources: []
related: ["[[GLO-001-tour]]"]
tags: [issue]
severity: major
kind: question
---

# Resolved question about the tour
"""

(_wiki / "glossary" / "GLO-001-tour.md").write_text(GLO, encoding="utf-8")
(_wiki / "issues" / "ISS-001-open.md").write_text(ISS_OPEN, encoding="utf-8")
(_wiki / "issues" / "ISS-002-done.md").write_text(ISS_DONE, encoding="utf-8")


def test_open_issue_counts_by_folder():
    app._PARSE_CACHE.clear()
    assert app.open_issue_counts() == {"glossary": 1}


def test_tile_flag_and_plural():
    body = app.app.test_client().get("/").get_data(as_text=True)
    g = body[body.index("tile-glossary"):body.index("tile-issues")]
    assert 'class="tile-flag"' in g and "1 open issue<" in g, g
    s = body[body.index("tile-stakeholders"):body.index("tile-scope")]
    assert "tile-flag" not in s


def test_issues_page_preselects_open_filter():
    body = app.app.test_client().get("/issues?filter=open").get_data(as_text=True)
    assert "URLSearchParams" in body


if __name__ == "__main__":
    test_open_issue_counts_by_folder()
    test_tile_flag_and_plural()
    test_issues_page_preselects_open_filter()
    print("OK: issue flags")
