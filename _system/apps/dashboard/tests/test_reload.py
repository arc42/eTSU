"""The footer's "Reload" control — dropping every server-side cache on demand.

Wiki edits normally appear on a plain browser refresh: `_parse` is keyed by
(path, mtime), and the folder listings are re-globbed per request, so a new,
edited or deleted page shows up by itself. Two things do not follow, and they
are what the button is for:

  * a rewrite that lands on the same mtime — an ingest restoring a file, a
    checkout, a copy that preserves timestamps — is a cache hit forever;
  * Jinja compiles each template once per worker, so an edited template
    otherwise needs the process restarted.

Both are cleared by POST /reload. Static assets are handled differently, by
`static_url` stamping the file's own mtime into the query string, so an
edited stylesheet arrives without anyone pressing anything.

Run from the dashboard dir:
    .venv/bin/python tests/test_reload.py
"""
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
# without a browser heartbeat the watchdog SIGTERMs this process (ADR-0022)
os.environ["DASH_STARTUP_GRACE"] = "3600"
os.environ["DASH_HEARTBEAT_GRACE"] = "3600"

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))  # import app.py

import app  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
BASE = (ROOT / "templates" / "base.html").read_text(encoding="utf-8")
CSS = (ROOT / "static" / "style.css").read_text(encoding="utf-8")

TERM = _wiki / "glossary" / "GLO-001-provenance.md"


def _write_term(title, keep_mtime=False):
    """Write the one glossary page these tests read back. `keep_mtime` restores
    the previous timestamp, which is the whole point: it reproduces the only
    edit the mtime-keyed parse cache cannot see by itself."""
    before = TERM.stat().st_mtime_ns if keep_mtime and TERM.exists() else None
    TERM.write_text(
        "---\n"
        "id: GLO-001\n"
        "type: glossary-term\n"
        f"title: {title}\n"
        "status: accepted\n"
        "created: 2026-09-09\n"
        "updated: 2026-09-09\n"
        "sources: []\n"
        "related: []\n"
        "tags: [glossary]\n"
        "---\n\n"
        f"# {title}\n\n**Definition.** A term.\n",
        encoding="utf-8",
    )
    if before is not None:
        os.utime(TERM, ns=(before, before))


def test_reload_route_reports_ok():
    _write_term("Alpha")
    with app.app.test_client() as client:
        r = client.post("/reload")
        assert r.status_code == 200, r.status_code
        assert r.get_json() == {"ok": True}, r.get_json()


def test_reload_is_post_only():
    """A GET must not clear caches — a crawler, a prefetch or a stray link
    would otherwise flush the whole vault on someone else's behalf."""
    with app.app.test_client() as client:
        assert client.get("/reload").status_code == 405


def test_reload_empties_the_parse_cache():
    _write_term("Alpha")
    with app.app.test_client() as client:
        client.get("/glossary")
        assert app._PARSE_CACHE, "expected the page render to populate the cache"
        client.post("/reload")
        assert app._PARSE_CACHE == {}, app._PARSE_CACHE


def test_reload_empties_the_jinja_template_cache():
    with app.app.test_client() as client:
        client.get("/glossary")
        assert app.app.jinja_env.cache, "expected rendering to cache a template"
        client.post("/reload")
        assert not app.app.jinja_env.cache, app.app.jinja_env.cache


def test_a_rewrite_that_keeps_its_mtime_is_only_seen_after_reload():
    """The gap the button exists to close."""
    _write_term("Alpha")
    with app.app.test_client() as client:
        client.post("/reload")
        assert b"Alpha" in client.get("/glossary").data

        _write_term("Betamax", keep_mtime=True)
        assert b"Betamax" not in client.get("/glossary").data, \
            "same mtime should still be served from the parse cache"

        client.post("/reload")
        assert b"Betamax" in client.get("/glossary").data


def test_static_url_stamps_the_files_mtime():
    expected = int((ROOT / "static" / "style.css").stat().st_mtime)
    with app.app.test_request_context("/"):
        url = app.static_url("style.css")
    assert url.endswith(f"?v={expected}"), url


def test_static_url_leaves_a_missing_file_unversioned():
    with app.app.test_request_context("/"):
        url = app.static_url("no-such-file.css")
    assert "?" not in url, url


def test_the_stylesheet_link_is_versioned():
    assert re.search(r"static_url\(\s*['\"]style\.css['\"]\s*\)", BASE), \
        "base.html should load the stylesheet through static_url"


def test_the_footer_carries_the_reload_button():
    button = re.search(r'<button[^>]*id="reload-data"[^>]*>', BASE)
    assert button, "no reload button in base.html"
    # visible to every viewer, unlike the facilitator-only disconnect control
    assert "hidden" not in button.group(0), button.group(0)


def test_the_reload_button_posts_to_the_reload_route():
    assert re.search(r'fetch\(\s*"/reload"', BASE), BASE
    assert "location.reload()" in BASE


def test_the_reload_button_is_styled():
    assert ".reload-data {" in CSS
    assert ".reload-data:disabled" in CSS


if __name__ == "__main__":
    test_reload_route_reports_ok()
    test_reload_is_post_only()
    test_reload_empties_the_parse_cache()
    test_reload_empties_the_jinja_template_cache()
    test_a_rewrite_that_keeps_its_mtime_is_only_seen_after_reload()
    test_static_url_stamps_the_files_mtime()
    test_static_url_leaves_a_missing_file_unversioned()
    test_the_stylesheet_link_is_versioned()
    test_the_footer_carries_the_reload_button()
    test_the_reload_button_posts_to_the_reload_route()
    test_the_reload_button_is_styled()
    print("all reload tests passed")
