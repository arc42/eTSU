#!/usr/bin/env bash
#
# Launch the Requirements-Wiki dashboard (Docker, no local install needed).
#
#   ./dashboard.sh          build + start, open browser at http://localhost:8080
#   ./dashboard.sh up       same as above
#   ./dashboard.sh down     stop and remove the container
#   ./dashboard.sh logs     follow container logs
#   ./dashboard.sh rebuild  force a clean rebuild, then start
#   ./dashboard.sh local    run Flask directly (no Docker) at http://localhost:8000
#
# The dashboard stops itself a few seconds after you close its browser tab/window
# (ADR-0022), so it won't linger as an orphan. `down` stays available to remove a
# stopped container or stop a still-running one manually. `local` is a fallback
# for machines where Docker will not start (e.g. a workshop laptop).
#
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COMPOSE_FILE="$ROOT/_system/apps/dashboard/compose.yaml"
URL="http://localhost:8080"
LOCAL_URL="http://localhost:8000"

# Absolute paths to the mounted layers, consumed by compose.yaml.
export WIKI_DIR="$ROOT/wiki"
export ADR_DIR="$ROOT/_system/adr"
export CONFIG_FILE="$ROOT/_system/wiki.yaml"

# Footer time in the host's zone, not UTC: Docker containers default to UTC.
if [ -z "${TZ:-}" ] && [ -L /etc/localtime ]; then
  TZ="$(readlink /etc/localtime | sed 's#.*/zoneinfo/##')"
fi
export TZ="${TZ:-UTC}"

# Open a URL in the default browser (a normal tab is fine — the server stops
# itself when the tab/window is closed, so nothing needs to close the window
# programmatically). See ADR-0022. Shared by every mode below.
open_browser_at() {
  local url="$1"
  if command -v open >/dev/null 2>&1; then open "$url"
  elif command -v xdg-open >/dev/null 2>&1; then xdg-open "$url"
  fi
}

# Wait (up to ~30 s) until the dashboard actually answers. Opening the browser
# first gives the facilitator a connection-refused page and a manual reload —
# guaranteed on the first run, which builds the venv or the image.
wait_for_url() {
  local url="$1" tries=60
  command -v curl >/dev/null 2>&1 || return 0   # nothing to poll with; don't stall
  while [ "$tries" -gt 0 ]; do
    if curl -sf --max-time 1 -o /dev/null "$url/"; then return 0; fi
    tries=$((tries - 1))
    sleep 0.5
  done
  return 1
}

cmd="${1:-up}"

# Docker is required for every mode except `local`, which is the escape hatch
# for machines where Docker will not start.
if [ "$cmd" != "local" ] && ! command -v docker >/dev/null 2>&1; then
  echo "✗ Docker is not installed or not on PATH." >&2
  exit 1
fi

case "$cmd" in
  up)
    docker compose -f "$COMPOSE_FILE" up --build -d
    wait_for_url "$URL" || echo "… still starting; reload the page if it does not answer."
    echo "✓ Dashboard running at $URL"
    open_browser_at "$URL"
    ;;
  rebuild)
    docker compose -f "$COMPOSE_FILE" build --no-cache
    docker compose -f "$COMPOSE_FILE" up -d
    wait_for_url "$URL" || echo "… still starting; reload the page if it does not answer."
    echo "✓ Dashboard rebuilt, running at $URL"
    open_browser_at "$URL"
    ;;
  down)
    docker compose -f "$COMPOSE_FILE" down
    echo "✓ Dashboard stopped."
    ;;
  logs)
    docker compose -f "$COMPOSE_FILE" logs -f
    ;;
  local)
    cd "$ROOT/_system/apps/dashboard"
    if [ ! -d .venv ]; then
      echo "→ First run: building the virtualenv and installing requirements (~20 s)…"
      python3 -m venv .venv
      .venv/bin/pip install -q --disable-pip-version-check -r requirements.txt
    fi
    export WIKI_DIR ADR_DIR CONFIG_FILE
    export WIKI_CONFIG="$CONFIG_FILE"
    # Start the server first, then open the browser once it actually answers.
    .venv/bin/python app.py &
    server_pid=$!
    wait_for_url "$LOCAL_URL" || echo "… server did not answer yet; reload if the page fails."
    echo "✓ Dashboard (local, no Docker) on $LOCAL_URL"
    open_browser_at "$LOCAL_URL"
    wait "$server_pid" || true
    ;;
  *)
    echo "Unknown command: $cmd" >&2
    echo "Usage: ./dashboard.sh [up|down|logs|rebuild|local]" >&2
    exit 2
    ;;
esac
