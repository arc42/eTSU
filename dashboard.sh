#!/usr/bin/env bash
#
# Launch the Requirements-Wiki dashboard (Docker, no local install needed).
#
#   ./dashboard.sh          build + start, open browser at http://localhost:8080
#   ./dashboard.sh up       same as above
#   ./dashboard.sh down     stop and remove the container
#   ./dashboard.sh logs     follow container logs
#   ./dashboard.sh rebuild  force a clean rebuild, then start
#
# The dashboard stops itself a few seconds after you close its browser tab/window
# (ADR-0022), so it won't linger as an orphan. `down` stays available to remove a
# stopped container or stop a still-running one manually.
#
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COMPOSE_FILE="$ROOT/_system/apps/dashboard/compose.yaml"
URL="http://localhost:8080"

# Absolute paths to the mounted layers, consumed by compose.yaml.
export WIKI_DIR="$ROOT/wiki"
export ADR_DIR="$ROOT/_system/adr"

if ! command -v docker >/dev/null 2>&1; then
  echo "✗ Docker ist nicht installiert oder nicht im PATH." >&2
  exit 1
fi

# Open the dashboard in the default browser (a normal tab is fine — the server
# stops itself when the tab/window is closed, so nothing needs to close the
# window programmatically). See ADR-0022.
open_browser() {
  if command -v open >/dev/null 2>&1; then open "$URL"
  elif command -v xdg-open >/dev/null 2>&1; then xdg-open "$URL"
  fi
}

cmd="${1:-up}"
case "$cmd" in
  up)
    docker compose -f "$COMPOSE_FILE" up --build -d
    echo "✓ Dashboard läuft auf $URL"
    open_browser
    ;;
  rebuild)
    docker compose -f "$COMPOSE_FILE" build --no-cache
    docker compose -f "$COMPOSE_FILE" up -d
    echo "✓ Dashboard neu gebaut, läuft auf $URL"
    open_browser
    ;;
  down)
    docker compose -f "$COMPOSE_FILE" down
    echo "✓ Dashboard gestoppt."
    ;;
  logs)
    docker compose -f "$COMPOSE_FILE" logs -f
    ;;
  *)
    echo "Unbekannter Befehl: $cmd" >&2
    echo "Benutzung: ./dashboard.sh [up|down|logs|rebuild]" >&2
    exit 2
    ;;
esac
