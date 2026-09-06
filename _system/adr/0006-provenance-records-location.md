# ADR-0006: Slim provenance records in `raw/sources/`

- **Status:** accepted
- **Date:** 2026-05-24

## Context
Source/provenance records (`SRC-NNN`) were created flat in `raw/` — as siblings
of the actual, human-curated source files (e.g. `glossary.md`). They also
carried extensive prose (`Summary`, `Key takeaways`, `Provenance`). That had
two drawbacks:

1. **Mixed ownership.** Agent-generated metadata sat next to the immutable
   human sources — confusing, "why are these files here?".
2. **Duplication with the log.** The prose repeated the chronological
   narrative that already lives in `_system/log.md`.

The content-type table in `CLAUDE.md` already said "frontmatter only" anyway;
practice had drifted from that. But an SRC record is **not** a log entry — it
is a node in the graph: the target of `sources:` wikilinks, the carrier of the
`sha256` used for drift detection, and the reverse manifest (`ingested-pages` /
backlinks). Those functions cannot be replaced by log lines.

## Decision
Provenance records remain **one node per source**, but are kept **slim**
(frontmatter plus at most a one-line summary) and live in their own folder,
**`raw/sources/`**, separate from the human source files at the top level of
`raw/`.

- **Narrative** (what happened, when) belongs exclusively in `_system/log.md`.
- **Provenance/traceability** (source, hash, affected pages) belongs in the
  SRC record.
- `_system/index.md` gets a **`## Sources`** section as the registry of all
  ingested sources (matching every other content type).

## Consequences
Clean separation: human raw sources (`raw/`, immutable) versus agent-generated
provenance (`raw/sources/`). Lightweight records, one clear place for the
registry (index) and one for the narrative (log). Cost: existing `sources:`
links were repointed to `raw/sources/…`; `CLAUDE.md`, the source template, and
the ingest workflow were updated. Open refinement: full-path links break on a
future move — basename links (`[[SRC-001-…]]`) would be more move-resilient
and could be introduced later.
