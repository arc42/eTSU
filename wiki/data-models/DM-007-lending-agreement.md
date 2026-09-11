---
id: DM-007
type: data-model
title: Lending agreement
status: draft
created: 2026-09-09
updated: 2026-09-09
sources:
  - "[[SRC-007-tsu-brief]]"
related:
  - "[[GLO-021-lending-agreement]]"
  - "[[ISS-025-data-model-attributes-unsourced]]"
tags: [data-model]
stereotype: entity
parent: []
bounded-context: Gallery Touring
source-of-truth: Legal & Accounting
relationships:
  - { verb: made with, target: "[[GLO-008-lender]]", cardinality: "1", kind: association }
  - { verb: covers, target: "[[DM-006-piece-on-loan]]", cardinality: "1..*", kind: association }
  - { verb: obliges, target: "[[GLO-006-conservator]]", cardinality: "0..1", kind: association }
---

# Lending agreement

**Purpose.** The contract under which a lender puts a piece on a tour without selling it. It fixes the insured value, the loan duration and the conservation obligation at once.

**Identity.** `id`.

**Attributes.**
- `id` : text — stable agreement reference
- `insured-value` : money — agreed cover
- `duration` : text — loan period
- `conservation-obligation` : text — what is owed when the tour closes

**Relationships.**
- made with → [[GLO-008-lender]] · 1 · association
- covers → [[DM-006-piece-on-loan]] · 1..* · association
- obliges → [[GLO-006-conservator]] · 0..1 · association

**Invariants / rules.**
- All three terms are fixed in one document; none of them stands alone.

> [!assumption]
> The attribute list is derived from the glossary definition, not from a
> source that enumerates fields. Names and types are a first cut for the
> team to correct — see [[ISS-025-data-model-attributes-unsourced]].
