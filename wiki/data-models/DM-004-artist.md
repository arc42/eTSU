---
id: DM-004
type: data-model
title: Artist
status: draft
created: 2026-09-09
updated: 2026-09-09
sources:
  - "[[SRC-007-tsu-brief]]"
related:
  - "[[GLO-012-artist]]"
  - "[[GOAL-007-artist-self-service]]"
  - "[[ISS-025-data-model-attributes-unsourced]]"
  - "[[STK-002-artist]]"
tags: [data-model]
stereotype: entity
parent: []
bounded-context: Gallery Touring
source-of-truth: eTSU
relationships:
  - { verb: earns, target: "[[GLO-020-commission]]", cardinality: "0..*", kind: association }
---

# Artist

**Purpose.** The creator whose work a tour presents. TSU specialises in the young and up-and-coming, and a tour usually shows one artist alone.

**Identity.** `id`.

**Attributes.**
- `id` : text — stable artist reference
- `name` : text — display name
- `represented-since` : date — start of the TSU relationship

**Relationships.**
- earns → [[GLO-020-commission]] · 0..* · association

**Invariants / rules.**
- Commission and both price floors are agreed per piece with the artist before a tour is a Go.

> [!assumption]
> The attribute list is derived from the glossary definition, not from a
> source that enumerates fields. Names and types are a first cut for the
> team to correct — see [[ISS-025-data-model-attributes-unsourced]].
