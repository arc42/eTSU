---
id: DM-008
type: data-model
title: Museum
status: draft
created: 2026-09-09
updated: 2026-09-09
sources:
  - "[[SRC-007-tsu-brief]]"
related:
  - "[[GLO-014-museum]]"
  - "[[ISS-013-three-way-buyer-segmentation]]"
  - "[[ISS-025-data-model-attributes-unsourced]]"
  - "[[STK-008-museum]]"
tags: [data-model]
stereotype: entity
parent: []
bounded-context: Gallery Touring
source-of-truth: eTSU
relationships:
  - { verb: lends as, target: "[[GLO-008-lender]]", cardinality: "0..1", kind: association }
  - { verb: buys as, target: "[[DM-009-buyer]]", cardinality: "0..1", kind: association }
---

# Museum

**Purpose.** An institution with a permanent collection, appearing on both sides of the business: it lends pieces to a tour, and it buys them at its own lower floor.

**Identity.** `id`.

**Attributes.**
- `id` : text — stable museum reference
- `name` : text — institution name
- `country` : text — jurisdiction, which drives customs and compliance

**Relationships.**
- lends as → [[GLO-008-lender]] · 0..1 · association
- buys as → [[DM-009-buyer]] · 0..1 · association

**Invariants / rules.**
- Lending and buying are roles a museum plays, not what it is — a museum may do both, either or neither.
- As a buyer it pays the minimum museum sale price, not the ordinary floor.

> [!assumption]
> The attribute list is derived from the glossary definition, not from a
> source that enumerates fields. Names and types are a first cut for the
> team to correct — see [[ISS-025-data-model-attributes-unsourced]].
