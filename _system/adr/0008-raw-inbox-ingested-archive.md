# ADR-0008: `raw/` as inbox, ingested originals move to `raw/ingested/`

- **Status:** accepted
- **Date:** 2026-05-24

## Context
After ADR-0006, human source files sat flat in `raw/`, mixed with sources
already processed and sources not yet processed. As the number of sources
grows, this makes it hard to see *what still needs to be ingested*. The
original files themselves must not be deleted (drift detection via sha256,
re-derivation, provenance), but they do not need to permanently occupy the
"inbox".

## Decision
The **top level of `raw/` is the inbox**: only *new, not-yet-ingested*
sources. Once a source is ingested, its original is moved to
**`raw/ingested/`**, and the corresponding `SRC-NNN` `origin:` is updated to
the new path.

That gives `raw/` the following shape:
- **top level** — inbox (new, unprocessed sources)
- **`raw/ingested/`** — archived originals after ingest (human, immutable)
- **`raw/sources/`** — agent-generated provenance records `SRC-NNN` (ADR-0006)

The ingest workflow gets a closing step for this (step 8); the audit workflow
checks sha256 drift against the file at the `origin:` path.

## Consequences
The inbox shows outstanding ingest work at a glance; processed originals
remain preserved and checkable. Because files are only moved (not modified),
all sha256 baselines stay valid. Cost: one extra move step per ingest and
upkeep of the `origin:` path. Trade-off of the chosen **flat** layout:
`sources/` (records) and `ingested/` (files) are similarly named siblings —
accepted deliberately, to keep human originals out of the agent-owned
`raw/sources/` (clear ownership).
