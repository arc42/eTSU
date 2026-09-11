---
id: DM-002
type: data-model
title: Show
status: draft
created: 2026-09-09
updated: 2026-09-09
sources:
  - "[[SRC-007-tsu-brief]]"
related:
  - "[[GLO-002-show]]"
  - "[[ISS-025-data-model-attributes-unsourced]]"
tags: [data-model]
stereotype: entity
parent: []
bounded-context: Gallery Touring
source-of-truth: eTSU
relationships:
  - { verb: takes place at, target: "[[GLO-015-gallery]]", cardinality: "1", kind: association }
  - { verb: displays, target: "[[DM-003-piece]]", cardinality: "0..*", kind: association }
---

# Show

**Purpose.** One stop of a tour at a single gallery: the window in which that tour's pieces are on display and for sale there.

**Identity.** `id`.

**Attributes.**
- `id` : text — stable show reference
- `opens-on` : date — first day on display
- `closes-on` : date — last day on display

**Relationships.**
- takes place at → [[GLO-015-gallery]] · 1 · association
- displays → [[DM-003-piece]] · 0..* · association

**Invariants / rules.**
- A show belongs to exactly one tour and one gallery.
- The agreed price of a piece is fixed for the duration of a show, and may move between shows.

> [!assumption]
> The attribute list is derived from the glossary definition, not from a
> source that enumerates fields. Names and types are a first cut for the
> team to correct — see [[ISS-025-data-model-attributes-unsourced]].
