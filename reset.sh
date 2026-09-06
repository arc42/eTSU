#!/usr/bin/env bash
#
# Restore the naked state: delete all captured content, keep all machinery.
# Use between workshop runs, or to recover from a live ingest that went wrong.
#
#   ./reset.sh           ask for confirmation, then reset
#   ./reset.sh --force    skip the confirmation
#
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ "${1:-}" != "--force" ]; then
  echo "This deletes every page in wiki/, every source in raw/, and empties"
  echo "_system/index.md, _system/log.md and _system/wiki.yaml."
  read -r -p "Reset $ROOT to the naked state? [y/N] " reply
  [ "$reply" = "y" ] || { echo "Aborted."; exit 1; }
fi

find "$ROOT/wiki" -name '*.md' -delete
find "$ROOT/raw" -maxdepth 1 -type f -delete
find "$ROOT/raw/sources" "$ROOT/raw/ingested" -name '*.md' -delete
git -C "$ROOT" checkout -- _system/index.md _system/log.md _system/wiki.yaml
echo "✓ Reset. wiki/ is empty; machinery untouched."
