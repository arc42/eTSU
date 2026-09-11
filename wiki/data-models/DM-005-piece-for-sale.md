---
id: DM-005
type: data-model
title: Piece for sale
status: draft
created: 2026-09-09
updated: 2026-09-09
sources:
  - "[[SRC-007-tsu-brief]]"
related:
  - "[[GLO-011-piece]]"
  - "[[ISS-025-data-model-attributes-unsourced]]"
tags: [data-model]
stereotype: entity
parent:
  - "[[DM-003-piece]]"
bounded-context: Gallery Touring
source-of-truth: eTSU
relationships:
  - { verb: floored by, target: "[[GLO-017-minimum-sale-price]]", cardinality: "1", kind: composition }
  - { verb: floored for museums by, target: "[[GLO-018-minimum-museum-sale-price]]", cardinality: "0..1", kind: composition }
  - { verb: earns, target: "[[GLO-020-commission]]", cardinality: "1", kind: composition }
---

# Piece for sale

**Purpose.** The variant of a piece that TSU may sell: it carries price floors and an artist commission, and none of the lending machinery.

**Identity.** Inherited from [[DM-003-piece]].

**Attributes.**
- `minimum-sale-price` : money — floor for an ordinary buyer
- `minimum-museum-sale-price` : money — lower floor, museums only
- `commission-rate` : percent — artist's share, typically 20-40%

**Relationships.**
- floored by → [[GLO-017-minimum-sale-price]] · 1 · composition
- floored for museums by → [[GLO-018-minimum-museum-sale-price]] · 0..1 · composition
- earns → [[GLO-020-commission]] · 1 · composition

**Invariants / rules.**
- May not be sold below the minimum sale price, or below the museum floor when the buyer is a museum.
- The museum floor is almost always lower than the ordinary floor.

> [!assumption]
> The attribute list is derived from the glossary definition, not from a
> source that enumerates fields. Names and types are a first cut for the
> team to correct — see [[ISS-025-data-model-attributes-unsourced]].
