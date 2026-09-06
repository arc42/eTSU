"""Plain-assert test for wiki_config() — no pytest dependency.

Run from the dashboard dir inside a venv that has the app's requirements:
    .venv/bin/python tests/test_wiki_config.py
"""
import os
import sys
import tempfile
from pathlib import Path

_tmp = Path(tempfile.mkdtemp())
(_tmp / "wiki").mkdir()
(_tmp / "adr").mkdir()
os.environ["WIKI_DIR"] = str(_tmp / "wiki")
os.environ["ADR_DIR"] = str(_tmp / "adr")
os.environ["WIKI_CONFIG"] = str(_tmp / "wiki.yaml")
# the dashboard SIGTERMs itself without a browser heartbeat (ADR-0022)
os.environ["DASH_STARTUP_GRACE"] = "3600"
os.environ["DASH_HEARTBEAT_GRACE"] = "3600"

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))  # import app.py

import app  # noqa: E402

CONFIG = Path(os.environ["WIKI_CONFIG"])


def test_missing_config_falls_back():
    if CONFIG.exists():
        CONFIG.unlink()
    cfg = app.wiki_config()
    assert cfg["system_name"] == "Requirements Wiki", cfg
    assert cfg["system_name_set"] is False, cfg
    assert cfg["tagline"] == "", cfg


def test_blank_config_falls_back():
    CONFIG.write_text('system_name: ""\ntagline: ""\n', encoding="utf-8")
    cfg = app.wiki_config()
    assert cfg["system_name"] == "Requirements Wiki", cfg
    assert cfg["system_name_set"] is False, cfg


def test_filled_config_is_used():
    CONFIG.write_text('system_name: "Bookshelf"\ntagline: "Lending, tracked"\n',
                      encoding="utf-8")
    cfg = app.wiki_config()
    assert cfg["system_name"] == "Bookshelf", cfg
    assert cfg["system_name_set"] is True, cfg
    assert cfg["tagline"] == "Lending, tracked", cfg


def test_config_is_read_live_not_cached():
    CONFIG.write_text('system_name: "First"\n', encoding="utf-8")
    assert app.wiki_config()["system_name"] == "First"
    CONFIG.write_text('system_name: "Second"\n', encoding="utf-8")
    assert app.wiki_config()["system_name"] == "Second", \
        "config must be re-read per call so the workshop can rename live"


def test_shipped_default_name_is_flagged_so_the_home_page_can_prompt():
    """The vault ships named `eTSU`; bootstrap.md step 1 is to replace it.
    `system_name_set` alone cannot see that state — it is True the moment the
    file is non-empty — so the home page lost its "run bootstrap" affordance
    when the starter gained a shipped name."""
    CONFIG.write_text(f'system_name: "{app.SHIPPED_SYSTEM_NAME}"\n', encoding="utf-8")
    cfg = app.wiki_config()
    assert cfg["system_name_set"] is True, cfg
    assert cfg["system_name_is_shipped"] is True, cfg

    CONFIG.write_text('system_name: "Their Own System"\n', encoding="utf-8")
    cfg = app.wiki_config()
    assert cfg["system_name_is_shipped"] is False, cfg

    CONFIG.unlink()
    assert app.wiki_config()["system_name_is_shipped"] is False, "unnamed is not shipped-default"


def test_malformed_config_does_not_crash():
    CONFIG.write_text("system_name: [unclosed\n", encoding="utf-8")
    cfg = app.wiki_config()
    assert cfg["system_name"] == "Requirements Wiki", cfg


def test_non_dict_yaml_falls_back():
    """`system_name: [a, b]` is valid YAML that parses to a list, not a dict —
    the guard for it existed but was never exercised."""
    CONFIG.write_text("- just\n- a\n- list\n", encoding="utf-8")
    cfg = app.wiki_config()
    assert cfg["system_name"] == "Requirements Wiki", cfg
    assert cfg["system_name_set"] is False, cfg
    assert cfg["tagline"] == "", cfg

    CONFIG.write_text("just a bare string\n", encoding="utf-8")
    assert app.wiki_config()["system_name"] == "Requirements Wiki"


if __name__ == "__main__":
    test_missing_config_falls_back()
    test_blank_config_falls_back()
    test_filled_config_is_used()
    test_config_is_read_live_not_cached()
    test_shipped_default_name_is_flagged_so_the_home_page_can_prompt()
    test_malformed_config_does_not_crash()
    test_non_dict_yaml_falls_back()
    print("OK: wiki_config()")
