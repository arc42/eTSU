"""render_markdown / _unwrap_prose contract: hard-wrapped prose (agents write
wiki pages wrapped at ~80 columns) renders as one paragraph, not one <br> per
source line — while lists, fenced code, and explicit two-space breaks are
left untouched. No pytest.

Run from the dashboard dir:
    .venv/bin/python tests/test_markdown.py
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


def test_hard_wrapped_prose_is_one_paragraph():
    html = app.render_markdown("First line of a\nwrapped paragraph.\n\nSecond.", {})
    assert "<br" not in html, html
    assert "<p>First line of a wrapped paragraph.</p>" in html, html


def test_list_directly_after_prose_line_is_a_list():
    html = app.render_markdown("**Goals.** PAM (light)\n- one thing\n- two things", {})
    assert "<ul>" in html and "<li>one thing</li>" in html, html


def test_wrapped_list_item_stays_one_item():
    html = app.render_markdown("- Replace the ad-hoc\n  coordination.\n- Second item", {})
    assert html.count("<li>") == 2, html
    assert "ad-hoc coordination" in html.replace("\n", " "), html


def test_fenced_code_is_untouched():
    html = app.render_markdown("```\nline a\nline b\n```", {})
    assert "line a\nline b" in html, html


def test_explicit_two_space_break_is_kept():
    html = app.render_markdown("roses are red  \nviolets are blue", {})
    assert "<br" in html, html


if __name__ == "__main__":
    test_hard_wrapped_prose_is_one_paragraph()
    test_list_directly_after_prose_line_is_a_list()
    test_wrapped_list_item_stays_one_item()
    test_fenced_code_is_untouched()
    test_explicit_two_space_break_is_kept()
    print("OK: markdown unwrap contract")
