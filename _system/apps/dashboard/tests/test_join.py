"""QR "scan to join" contract: `public_url()`, `qr_svg()`, and the `/join`
page that projects the code full-size. No pytest.

Run from the dashboard dir:
    .venv/bin/python tests/test_join.py
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
# DASH_PUBLIC_URL must be set before `import app` — public_url() reads it via
# os.environ.get() at call time, but setting it here matches how dashboard.sh
# actually launches the process (env fixed before the app ever starts).
os.environ["DASH_PUBLIC_URL"] = "http://192.0.2.7:8080/"

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE))

import app  # noqa: E402


def test_public_url_prefers_env_and_strips_slash():
    with app.app.test_request_context("/"):
        assert app.public_url() == "http://192.0.2.7:8080"


def test_qr_svg_is_inline_and_theme_aware():
    svg = app.qr_svg("http://192.0.2.7:8080")
    assert svg.startswith("<svg") and "currentColor" in svg


def test_home_and_join_show_the_code():
    c = app.app.test_client()
    home = c.get("/").get_data(as_text=True)
    assert 'class="hero-join"' in home and "<svg" in home and "192.0.2.7:8080" in home
    join = c.get("/join").get_data(as_text=True)
    # Exactly one <svg> inside .join-qr — the page-wide count is 2 because
    # base.html's footer carries its own unrelated "Python/Flask" badge icon
    # on every page.
    qr_start = join.index('class="join-qr"')
    qr_section = join[qr_start:join.index("</div>", qr_start)]
    assert qr_section.count("<svg") == 1
    assert "192.0.2.7:8080" in join and "Who" in join


def test_public_url_falls_back_when_env_is_unset():
    saved = os.environ.pop("DASH_PUBLIC_URL")
    try:
        with app.app.test_request_context("/", base_url="http://[::1]:8080"):
            url = app.public_url()
            assert url.startswith("http://"), url
            assert url.endswith(":8080"), url
            assert "]" not in url.split("//", 1)[1].split(":8080")[0] or url.startswith("http://[::1]"), url
    finally:
        os.environ["DASH_PUBLIC_URL"] = saved


def test_public_url_falls_back_to_the_request_origin_without_a_lan_ip():
    """No routable interface (an offline laptop, a locked-down container):
    the QR must still encode a working address — the request's own origin."""
    saved_env = os.environ.pop("DASH_PUBLIC_URL")
    saved_ip = app._lan_ip
    app._lan_ip = lambda: None
    try:
        with app.app.test_request_context("/", base_url="http://127.0.0.1:8000"):
            assert app.public_url() == "http://127.0.0.1:8000"
    finally:
        app._lan_ip = saved_ip
        os.environ["DASH_PUBLIC_URL"] = saved_env


if __name__ == "__main__":
    test_public_url_prefers_env_and_strips_slash()
    test_qr_svg_is_inline_and_theme_aware()
    test_home_and_join_show_the_code()
    test_public_url_falls_back_when_env_is_unset()
    test_public_url_falls_back_to_the_request_origin_without_a_lan_ip()
    print("OK: QR join code")
