---
id: DM-001
type: data-model
title: Tour
status: draft
created: 2026-09-09
updated: 2026-09-09
sources:
  - "[[SRC-007-tsu-brief]]"
related:
  - "[[GLO-001-tour]]"
  - "[[ISS-024-close-out-timing-show-versus-tour]]"
  - "[[ISS-025-data-model-attributes-unsourced]]"
tags: [data-model]
stereotype: entity
parent: []
bounded-context: Gallery Touring
source-of-truth: eTSU
relationships:
  - { verb: contains, target: "[[DM-002-show]]", cardinality: "1..*", kind: composition }
  - { verb: starts and ends at, target: "[[GLO-016-home-gallery]]", cardinality: "1", kind: association }
  - { verb: presents, target: "[[DM-004-artist]]", cardinality: "1..*", kind: association }
  - { verb: carries, target: "[[DM-003-piece]]", cardinality: "1..*", kind: aggregation }
---

# Tour

**Purpose.** The travelling exhibition that is TSU's whole operating unit: one artist's work, a sequence of shows, one home gallery at each end.

**Identity.** `id`.

**Attributes.**
- `id` : text — stable tour reference
- `title` : text — how the tour is billed
- `start-date` : date — first show opens
- `end-date` : date — last show closes
- `status` : enum — planned | go | running | closed

**Relationships.**
- contains → [[DM-002-show]] · 1..* · composition
- starts and ends at → [[GLO-016-home-gallery]] · 1 · association
- presents → [[DM-004-artist]] · 1..* · association
- carries → [[DM-003-piece]] · 1..* · aggregation

**Invariants / rules.**
- A tour usually presents one artist; several are allowed only when no single artist has enough work.
- Every piece a tour carries returns to the home gallery when the tour ends.

> [!assumption]
> The attribute list is derived from the glossary definition, not from a
> source that enumerates fields. Names and types are a first cut for the
> team to correct — see [[ISS-025-data-model-attributes-unsourced]].
