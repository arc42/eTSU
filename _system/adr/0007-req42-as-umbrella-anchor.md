# ADR-0007: req42 as umbrella anchor and methodological reference

- **Status:** accepted
- **Date:** 2026-05-24

## Context
The content types of this wiki (glossary, stakeholders, use cases, user
stories, features, quality requirements, constraints, issues …) are in effect
the building blocks of the **req42 framework** (Hruschka & Meuten); the
smaller anchors ([[SMART]], [[PAM]], [[INVEST]], [[MoSCoW]],
[[user-story-format]]) are standards that req42 applies *within* those
building blocks. Until now this methodological origin was recorded nowhere.
ADR-0004 established that adding an anchor is a deliberate, ADR-worthy act.

## Decision
req42 is added as an **umbrella anchor** `_system/anchors/req42.md` (citable as
`[[req42]]`), kept slim, and given a **mapping table** from req42 block to
content type/anchor. A more detailed, human-readable reference lives as a
**mirror** under `docs/req42/`. req42 is *method, not domain* — it is **not**
read by the ingest workflow and produces no `wiki/` pages.

Source and license: req42 is published under **CC BY-SA 4.0** (Hruschka &
Meuten). Both files name the authors, license, and canonical source; the
mirror is an adapted summary (not a verbatim copy) and is itself published
under CC BY-SA 4.0.

## Consequences
The methodological foundation of the taxonomy is now explicit, citable, and
checkable (a coverage checklist lives in the anchor). This also makes a
**gap** visible: req42 block 03 *Scope & boundaries* has no content type yet
(relevant once `raw/context-diagram.md` is ingested) — to be decided
separately. Cost: whenever req42 has a major update, both the anchor and the
mirror must be brought up to date (drift against upstream); license
obligations (attribution, share-alike) must be honoured.
