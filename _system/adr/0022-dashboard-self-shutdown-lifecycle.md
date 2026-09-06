# ADR-0022: The dashboard shuts itself down once the browser tab is closed

- **Status:** accepted
- **Date:** 2026-06-22

## Context

The requirements dashboard (`_system/apps/dashboard/`) is a read-only Flask
app that used to run under gunicorn (2 workers) in a Docker container in the
background: `dashboard.sh up` → `docker compose up -d`, restart policy
`unless-stopped`, after which the script opens the browser.

That created two problems:

- **No clean stop from the UI.** Shutting it down only worked via
  `./dashboard.sh down` or `docker stop` — nothing in the running web UI.
- **Browser closed ≠ server closed.** Closing the window/tab left the
  container running unnoticed (no WebSocket/SSE/heartbeat detects the
  closing), occupying port 8080, and — thanks to `unless-stopped` — even
  surviving reboots: a forgotten orphan. No data loss threatens (read-only),
  but the container hangs around as a zombie.

A naive `/stop` endpoint alone doesn't solve this: the gunicorn master
(PID 1 in the container) restarts terminated workers, and
`restart: unless-stopped` brings the container straight back up after a
self-stop — the restart policy actively fights any self-shutdown from
inside.

On top of that, in-memory state (who is currently watching?) fragments across
several processes once there is more than one worker.

A **first iteration** tied presence to a permanently open SSE stream
(`/events`) per tab — chosen because background tabs throttle/freeze
`setInterval`, so naive JS heartbeat polling can produce false signals (the
server shuts down even though the tab is merely hidden). That turned out to
be the wrong call: **every open stream occupies a worker thread for its
entire lifetime.** Clicking through subpages accumulated short-lived
"zombie" connections (the old page disconnects, but the server only notices
at the next keepalive) until the thread pool was exhausted — at which point
**not even `/stop` could be served any more** (the overlay appeared, but the
server never died). A cap plus a thread reserve only eased the symptom. The
real question — *why hold connections open at all?* — led to the
simplification below.

A **"stop server" button** in the UI also turned out to be a dead end: a web
page **cannot** close its own tab under browser security rules
(`window.close()` only works on windows that were opened by script). The
button could terminate the server, but left the dead tab open — worse than
simply closing the tab. The button was therefore removed again; **closing
the tab is the shutdown gesture.**

## Decision

We treat the dashboard as a **short-lived, on-demand viewer** (the Jupyter
pattern) and tie the server's lifecycle to "is a browser watching?".

1. **Presence via a lightweight heartbeat — no held connections.** Every open
   page sends a `POST /ping` every 20 s; server-side this only updates a
   `last seen` timestamp and returns immediately. **A `/ping` holds no
   worker thread** — this fully eliminates the thread-pool exhaustion of the
   SSE approach; a handful of threads is enough. The throttling problem (the
   original reason for SSE) is solved via a generous grace period that
   outlasts background throttling (point 2), rather than via an open
   connection.
2. **A watchdog with two grace periods.** A background thread shuts things
   down once no `/ping` has arrived for longer than `_HEARTBEAT_GRACE`
   (90 s). The period is **deliberately larger than the browser's background
   throttling (~60 s)**: a merely hidden tab keeps pinging at a throttled
   rate (~1×/min) and so stays alive; only a genuinely closed tab stops
   pinging entirely and triggers shutdown once the period elapses. It also
   comfortably bridges the brief gap of in-page navigation. If no ping ever
   arrives at startup, shutdown likewise kicks in after `_STARTUP_GRACE`
   (90 s), so a failed browser launch doesn't leave an orphan behind. Both
   periods can be overridden via environment variables
   (`DASH_HEARTBEAT_GRACE`, `DASH_STARTUP_GRACE`).
3. **Shutdown = close the tab, no button.** On leaving the page, a
   `pagehide` beacon fires `POST /leaving`. If it is only **navigation**
   between pages, the following page immediately pings again and cancels the
   signal (a "settle" ping after 2.5 s covers a late-arriving `/leaving` from
   the previous page). If the **tab/window is genuinely closed**, no further
   ping arrives and the watchdog shuts down after `_LEAVE_GRACE` (~5 s) —
   noticeably faster than the plain heartbeat period. That way the gesture
   users already know (close the tab) is enough to shut down; a web page
   never has to close its own tab (which browsers forbid). The lifecycle
   script (heartbeat + `pagehide` beacon) lives in `base.html` and runs on
   every page. `dashboard.sh` simply opens a tab in the default browser (no
   app mode, no `--app`).
4. **A clean shutdown = SIGTERM to the master.** `_shutdown()` signals the
   gunicorn master (`os.getppid()`); all workers exit, PID 1 returns, the
   container ends. In the dev server (`python app.py`) the process
   terminates itself via SIGTERM to itself (NOT the parent — that's the
   shell): a SIGINT sent from a background thread is swallowed by the
   Werkzeug dev server (Werkzeug 3.x), whereas SIGTERM goes through the
   default action.
5. **Restart policy → `no`.** This is the only way the container stays down
   after a self-stop. Resilience across reboots is deliberately given up — a
   local viewer is not a service that needs to survive a restart.
6. **One worker, a small thread pool** (`gunicorn --worker-class gthread
   --workers 1 --threads 4`). A single process keeps `last seen` and the
   watchdog coherent. Since **no request is held open any more** (the
   heartbeat replaces the SSE stream), a handful of threads is enough and
   the pool can no longer be exhausted — a few threads suffice for a page
   load plus the occasional `/ping` alongside it. That was the core of the
   bug, and is now structurally fixed by removing the held connection.

## Consequences

- Closing the tab/window shuts down the server (~5 s via the `pagehide`
  beacon, at the latest after the heartbeat period elapses): no more orphaned
  container, no more port held indefinitely. That was the core concern.
- No UI controls, no pool that can be blocked, no browser-specific window
  tricks — the shutdown gesture is "close the tab," which every browser
  supports.
- **Trade-off:** navigating between pages relies on the immediate reconnect
  ping for liveness; if that fails to happen (e.g. JS disabled), the server
  stops after `_LEAVE_GRACE`. Not an issue for normal operation.
- **Trade-off:** if the tab is closed only briefly, the server may be gone
  when you come back and needs restarting via `./dashboard.sh up`.
  Deliberately accepted.
- **Trade-off:** if the machine sleeps longer than the grace period,
  heartbeats stop and the server shuts down — the same restart path applies.
  Acceptable for a local viewer.
- `dashboard.sh down`/`up` remain valid as a manual fallback; `down` cleans
  up an already-stopped container.
- Reversal would mean: restart policy back to `unless-stopped`,
  `/ping`+`/leaving`+watchdog removed — hence this record.
