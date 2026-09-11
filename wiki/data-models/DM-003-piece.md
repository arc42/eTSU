---
id: DM-003
type: data-model
title: Piece
status: draft
created: 2026-09-09
updated: 2026-09-09
sources:
  - "[[SRC-007-tsu-brief]]"
related:
  - "[[GLO-011-piece]]"
  - "[[ISS-025-data-model-attributes-unsourced]]"
tags: [data-model]
stereotype: sum-type
parent: []
bounded-context: Gallery Touring
source-of-truth: eTSU
relationships:
  - { verb: created by, target: "[[DM-004-artist]]", cardinality: "1", kind: association }
  - { verb: documented by, target: "[[GLO-003-provenance]]", cardinality: "0..1", kind: composition }
  - { verb: returns to, target: "[[GLO-016-home-gallery]]", cardinality: "1", kind: association }
---

# Piece

**Purpose.** A single work of art travelling on a tour. Every piece is either for sale or on loan, never both, and that one bit decides almost everything else about it — which is why this is a sum type and not a status flag.

**Identity.** `id`.

**Attributes.**
- `id` : text — stable piece reference
- `title` : text — the work's title
- `year` : number — year of creation
- `medium` : text — material / technique
- `dimensions` : text — height x width x depth
- `current-location` : text — gallery or transit leg the piece is at

**Relationships.**
- created by → [[DM-004-artist]] · 1 · association
- documented by → [[GLO-003-provenance]] · 0..1 · composition
- returns to → [[GLO-016-home-gallery]] · 1 · association

**Invariants / rules.**
- For sale and on loan are exclusive and exhaustive: the variants below are the only two.
- A piece belongs to exactly one tour at a time.

> [!assumption]
> The attribute list is derived from the glossary definition, not from a
> source that enumerates fields. Names and types are a first cut for the
> team to correct — see [[ISS-025-data-model-attributes-unsourced]].
