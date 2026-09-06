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

# Absolute paths to the mounted layers, consumed by compose.yaml.
export WIKI_DIR="$ROOT/wiki"
export ADR_DIR="$ROOT/_system/adr"
export CONFIG_FILE="$ROOT/_system/wiki.yaml"

# Open a URL in the default browser (a normal tab is fine — the server stops
# itself when the tab/window is closed, so nothing needs to close the window
# programmatically). See ADR-0022. Shared by every mode below.
open_browser_at() {
  local url="$1"
  if command -v open >/dev/null 2>&1; then open "$url"
  elif command -v xdg-open >/dev/null 2>&1; then xdg-open "$url"
  fi
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
    echo "✓ Dashboard running at $URL"
    open_browser_at "$URL"
    ;;
  rebuild)
    docker compose -f "$COMPOSE_FILE" build --no-cache
    docker compose -f "$COMPOSE_FILE" up -d
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
      python3 -m venv .venv
      .venv/bin/pip install -q -r requirements.txt
    fi
    export WIKI_DIR ADR_DIR CONFIG_FILE
    export WIKI_CONFIG="$CONFIG_FILE"
    echo "✓ Dashboard (local, no Docker) on http://localhost:8000"
    open_browser_at "http://localhost:8000"
    exec .venv/bin/python app.py
    ;;
  *)
    echo "Unknown command: $cmd" >&2
    echo "Usage: ./dashboard.sh [up|down|logs|rebuild|local]" >&2
    exit 2
    ;;
esac
