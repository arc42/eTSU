---
id: DM-006
type: data-model
title: Piece on loan
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
  - { verb: covered by, target: "[[DM-007-lending-agreement]]", cardinality: "1", kind: association }
  - { verb: conserved by, target: "[[GLO-006-conservator]]", cardinality: "0..1", kind: association }
---

# Piece on loan

**Purpose.** The variant of a piece that travels without being sellable: it exists on a tour under a lending agreement and goes home when the tour closes.

**Identity.** Inherited from [[DM-003-piece]].

**Attributes.**
- `insured-value` : money — value fixed in the lending agreement
- `loan-start` : date — when the loan period opens
- `loan-end` : date — when the piece must be back

**Relationships.**
- covered by → [[DM-007-lending-agreement]] · 1 · association
- conserved by → [[GLO-006-conservator]] · 0..1 · association

**Invariants / rules.**
- Carries no sale price and no commission; it is not for sale at any price.
- Conservation is owed when the tour closes, per the lending agreement.

> [!assumption]
> The attribute list is derived from the glossary definition, not from a
> source that enumerates fields. Names and types are a first cut for the
> team to correct — see [[ISS-025-data-model-attributes-unsourced]].
