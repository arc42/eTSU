"""Multi-client presence tracking and the "Yoda" facilitator.

Covers the addendum to ADR-0022: presence moved from a single "last seen"
scalar to a per-client_id dict; the facilitator ("Yoda") is whichever
currently-connected client has the earliest first_seen — no token, no
cookie, just connection order (see `_facilitator_client_id` in app.py).

Run from the dashboard dir:
    .venv/bin/python tests/test_presence.py
"""
import json
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
# without a browser heartbeat the watchdog SIGTERMs this process (ADR-0022)
os.environ["DASH_STARTUP_GRACE"] = "3600"
os.environ["DASH_HEARTBEAT_GRACE"] = "3600"

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))  # import app.py

import app  # noqa: E402


def _ping(client, client_id, **kw):
    return client.post("/ping", data=json.dumps({"client_id": client_id}),
                        content_type="application/json", **kw)


def _reset_presence():
    """Presence state is module-global (mirrors production); each test
    starts from a clean slate rather than depending on run order."""
    with app._lifecycle_lock:
        app._clients.clear()
        app._leaving.clear()
        app._first_seen.clear()
        app._user_agents.clear()


def test_ping_without_a_body_does_not_500():
    # Real pages always send a client_id, but a bare POST (curl, a stale
    # client) must not crash the presence dict.
    _reset_presence()
    client = app.app.test_client()
    resp = client.post("/ping")
    assert resp.status_code == 200
    assert resp.get_json()["nickname"]


def test_presence_count_reflects_distinct_clients():
    _reset_presence()
    client = app.app.test_client()
    _ping(client, "alice")
    _ping(client, "bob")
    _ping(client, "alice")  # a second tab load from the same tab: no double count
    resp = client.get("/presence/count")
    assert resp.status_code == 200
    assert resp.get_json()["count"] == 1, resp.get_json()  # alice is Yoda (first); bob is the 1 client


def test_presence_count_excludes_clients_outside_the_active_window():
    _reset_presence()
    client = app.app.test_client()
    _ping(client, "carol")
    with app._lifecycle_lock:
        app._clients["carol"] = app.time.monotonic() - (app._PRESENCE_WINDOW + 5)
    assert client.get("/presence/count").get_json()["count"] == 0


def test_leaving_then_repinging_the_same_client_cancels_the_leave():
    _reset_presence()
    client = app.app.test_client()
    _ping(client, "dana")
    client.post("/leaving", data=json.dumps({"client_id": "dana"}),
                content_type="application/json")
    _ping(client, "dana")  # same tab, in-page navigation
    with app._lifecycle_lock:
        assert "dana" not in app._leaving


def test_first_client_is_the_facilitator_not_the_second():
    # The bug report this fixes: every localhost tab used to get the
    # "Disconnect all" button (a shared token, claimed by any tab that ever
    # loaded the link). Now only the earliest-still-connected client is.
    _reset_presence()
    client = app.app.test_client()
    first = _ping(client, "yoda").get_json()
    second = _ping(client, "luke").get_json()
    assert first["is_facilitator"] is True
    assert second["is_facilitator"] is False


def test_the_facilitator_is_literally_named_yoda_not_a_random_nickname():
    _reset_presence()
    client = app.app.test_client()
    first = _ping(client, "first-in").get_json()
    second = _ping(client, "second-in").get_json()
    assert first["nickname"] == "Yoda"
    assert second["nickname"] != "Yoda" and second["nickname"]


def test_a_stale_earliest_client_does_not_block_the_facilitator_role():
    # Regression: _facilitator_client_id() used to consider every id still in
    # _first_seen, evicted only after the 90s heartbeat grace — so a tab gone
    # for, say, 40s (past the 30s presence window, but not yet evicted) kept
    # "holding" the role, and the genuinely-active first client never passed
    # `cid == _facilitator_client_id()` at all: nobody got the button.
    _reset_presence()
    client = app.app.test_client()
    _ping(client, "long-gone")  # first ever, but about to go stale
    with app._lifecycle_lock:
        app._clients["long-gone"] = app.time.monotonic() - (app._PRESENCE_WINDOW + 5)
    resp = _ping(client, "yoda").get_json()  # the only *currently* connected client
    assert resp["is_facilitator"] is True


def test_facilitator_role_transfers_when_yoda_disconnects():
    _reset_presence()
    client = app.app.test_client()
    _ping(client, "yoda")
    _ping(client, "luke")
    with app._lifecycle_lock:
        app._forget_client("yoda")  # yoda's tab is gone (evicted by the watchdog)
    resp = _ping(client, "luke").get_json()
    assert resp["is_facilitator"] is True


def test_presence_count_excludes_the_current_facilitator():
    # Regression: the facilitator's own already-open tab pings too (it's the
    # same base.html script). If it counted, two real clients would
    # show as "3 connected" — confusing, and exactly what was reported.
    _reset_presence()
    client = app.app.test_client()
    _ping(client, "yoda")             # connects first -> becomes facilitator
    _ping(client, "alice")
    _ping(client, "bob")
    assert client.get("/presence/count").get_json()["count"] == 2


def test_presence_list_reports_nickname_browser_and_duration():
    _reset_presence()
    client = app.app.test_client()
    _ping(client, "yoda")  # connects first -> facilitator, excluded from the list
    _ping(client, "erin",
          headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                                  "Chrome/120.0 Safari/537.36"})
    resp = client.get("/presence/list").get_json()
    assert len(resp["clients"]) == 1, resp
    p = resp["clients"][0]
    assert p["browser"] == "Chrome" and p["os"] == "macOS", p
    assert isinstance(p["connected_seconds"], int)
    assert p["nickname"]  # non-empty, and stable for the same client_id


def test_nickname_is_stable_for_the_same_client_id():
    assert app._nickname("same-id") == app._nickname("same-id")


def test_presence_list_excludes_the_facilitator():
    _reset_presence()
    client = app.app.test_client()
    _ping(client, "yoda")   # connects first -> the only client -> facilitator
    resp = client.get("/presence/list").get_json()
    assert resp["clients"] == []


def test_disconnect_all_rejects_a_non_facilitator():
    _reset_presence()
    client = app.app.test_client()
    _ping(client, "yoda")
    resp = client.post("/disconnect-all", data=json.dumps({"client_id": "luke"}),
                        content_type="application/json")
    assert resp.status_code == 403
    with app._lifecycle_lock:
        assert app._shutting_down is False


def test_disconnect_all_accepts_the_facilitator():
    _reset_presence()
    client = app.app.test_client()
    _ping(client, "yoda")
    resp = client.post("/disconnect-all", data=json.dumps({"client_id": "yoda"}),
                        content_type="application/json")
    assert resp.status_code == 204
    with app._lifecycle_lock:
        assert app._shutting_down is True
    # undo, so later tests in this process aren't affected by the shutdown flag
    app._shutting_down = False


if __name__ == "__main__":
    test_ping_without_a_body_does_not_500()
    test_presence_count_reflects_distinct_clients()
    test_presence_count_excludes_clients_outside_the_active_window()
    test_leaving_then_repinging_the_same_client_cancels_the_leave()
    test_first_client_is_the_facilitator_not_the_second()
    test_the_facilitator_is_literally_named_yoda_not_a_random_nickname()
    test_a_stale_earliest_client_does_not_block_the_facilitator_role()
    test_facilitator_role_transfers_when_yoda_disconnects()
    test_presence_count_excludes_the_current_facilitator()
    test_presence_list_reports_nickname_browser_and_duration()
    test_nickname_is_stable_for_the_same_client_id()
    test_presence_list_excludes_the_facilitator()
    test_disconnect_all_rejects_a_non_facilitator()
    test_disconnect_all_accepts_the_facilitator()
    print("all presence/disconnect-all tests passed")
