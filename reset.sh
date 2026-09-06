#!/usr/bin/env bash
#
# Restore the naked state: delete all captured content, keep all machinery.
# Use between workshop runs, or to recover from a live ingest that went wrong.
#
#   ./reset.sh           ask for confirmation, then reset
#   ./reset.sh --force    skip the confirmation
#
# What counts as "captured content" is decided by git, not by file extension:
# everything the repo ships under wiki/ and raw/ is tracked (the .gitkeep files,
# the eTSU brand artwork in raw/assets/, the worked example), so anything a
# workshop added is exactly the untracked rest — .txt transcripts, .pdf specs,
# whiteboard photos and .md pages alike. raw/examples/ is left alone entirely.
#
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# git is the discriminator below, so fail fast (and clearly) without it.
if ! git -C "$ROOT" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "reset.sh needs this vault to be a git repository: it uses git to tell" >&2
  echo "the files the repo ships from the content a workshop added. Clone the" >&2
  echo "repo rather than downloading a zip, or run 'git init && git add -A &&" >&2
  echo "git commit -m baseline' here first." >&2
  exit 1
fi

if [ "${1:-}" != "--force" ]; then
  echo "This deletes every page in wiki/, every source in raw/ (inbox, sources/,"
  echo "ingested/ and any files you added to assets/), and empties"
  echo "_system/index.md, _system/log.md and _system/wiki.yaml."
  echo "It is irreversible for anything you have not committed."
  # `read` returns non-zero on EOF; without the `|| reply=` guard `set -e`
  # would kill the script before "Aborted." is printed.
  read -r -p "Reset $ROOT to the naked state? [y/N] " reply || reply=""
  [ "$reply" = "y" ] || { echo "Aborted."; exit 1; }
fi

# A managed directory deleted outright would otherwise abort the run under
# `set -e` before the restore below ever happens.
mkdir -p "$ROOT/wiki" "$ROOT/raw/sources" "$ROOT/raw/ingested" \
         "$ROOT/raw/assets" "$ROOT/raw/examples"

# Delete everything under wiki/ and raw/ that the repo does not ship.
# -x so ignored files go too; raw/examples/ is excluded so a facilitator's own
# seed material survives between runs.
git -C "$ROOT" clean -q -f -d -x -- wiki raw ':(exclude)raw/examples'

# Restore the shipped files: the scaffolds, plus anything tracked under wiki/
# or raw/ that was edited or deleted during the session.
git -C "$ROOT" checkout -- _system/index.md _system/log.md _system/wiki.yaml \
                           wiki raw

echo "✓ Reset. wiki/ and raw/ hold only what the repo ships; machinery untouched."
