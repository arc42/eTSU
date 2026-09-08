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

CTX = """---
id: CTX-001
type: context
title: System context
status: draft
created: 2026-09-07
updated: 2026-09-07
sources: []
related: []
tags: [context]
---

# System context
"""

EIF = """---
id: EIF-001
type: external-interface
title: Payment gateway
status: draft
created: 2026-09-07
updated: 2026-09-07
sources: []
related: []
tags: [external-interface]
partner: Payment gateway
flows: []
---

# Payment gateway
"""

ISS_SCOPE = """---
id: ISS-003
type: issue
title: Scope issue touching two pages
status: open
created: 2026-09-07
updated: 2026-09-07
sources: []
related: ["[[CTX-001-system]]", "[[EIF-001-a]]"]
tags: [issue]
severity: minor
kind: question
---

# Scope issue touching two pages
"""

(_wiki / "glossary" / "GLO-001-tour.md").write_text(GLO, encoding="utf-8")
(_wiki / "issues" / "ISS-001-open.md").write_text(ISS_OPEN, encoding="utf-8")
(_wiki / "issues" / "ISS-002-done.md").write_text(ISS_DONE, encoding="utf-8")


def test_open_issue_counts_by_folder():
    app._PARSE_CACHE.clear()
    counts = app.open_issue_counts()
    assert {k: len(v) for k, v in counts.items()} == {"glossary": 1}
    assert counts == {"glossary": {"ISS-001"}}


def test_tile_flag_and_plural():
    body = app.app.test_client().get("/").get_data(as_text=True)
    g = body[body.index("tile-glossary"):body.index("tile-issues")]
    assert 'class="tile-flag"' in g and "1 open issue<" in g, g
    s = body[body.index("tile-stakeholders"):body.index("tile-scope")]
    assert "tile-flag" not in s


def test_issues_page_preselects_open_filter():
    body = app.app.test_client().get("/issues?filter=open").get_data(as_text=True)
    assert "URLSearchParams" in body


def test_issues_tile_says_no_open_when_all_resolved():
    """With every issue resolved, the tile must not lie: no '0 open · N in
    total' next to an empty state that still invites a fresh ingest."""
    open_path = _wiki / "issues" / "ISS-001-open.md"
    saved = open_path.read_text(encoding="utf-8")
    open_path.unlink()
    try:
        app._PARSE_CACHE.clear()
        body = app.app.test_client().get("/").get_data(as_text=True)
        assert "No open issues" in body, body
        assert "No issues yet" not in body, body
    finally:
        open_path.write_text(saved, encoding="utf-8")


def test_scope_tile_counts_one_issue_once():
    """One open issue linking both a context page and an external-interface
    page must count once on the Scope tile, not twice (union, not sum, over
    the folders it spans)."""
    written = [
        (_wiki / "context" / "CTX-001-system.md"),
        (_wiki / "external-interfaces" / "EIF-001-a.md"),
        (_wiki / "issues" / "ISS-003-scope.md"),
    ]
    written[0].write_text(CTX, encoding="utf-8")
    written[1].write_text(EIF, encoding="utf-8")
    written[2].write_text(ISS_SCOPE, encoding="utf-8")
    try:
        app._PARSE_CACHE.clear()
        body = app.app.test_client().get("/").get_data(as_text=True)
        scope = body[body.index("tile-scope"):body.index("tile-backlog")]
        assert "1 open issue" in scope, scope
        assert "2 open issue" not in scope, scope
    finally:
        for f in written:
            f.unlink()


if __name__ == "__main__":
    test_open_issue_counts_by_folder()
    test_tile_flag_and_plural()
    test_issues_page_preselects_open_filter()
    test_issues_tile_says_no_open_when_all_resolved()
    test_scope_tile_counts_one_issue_once()
    print("OK: issue flags")
