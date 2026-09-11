---
id: DM-009
type: data-model
title: Buyer
status: draft
created: 2026-09-09
updated: 2026-09-09
sources:
  - "[[SRC-007-tsu-brief]]"
related:
  - "[[GLO-013-buyer]]"
  - "[[ISS-013-three-way-buyer-segmentation]]"
  - "[[ISS-025-data-model-attributes-unsourced]]"
  - "[[STK-004-buyer]]"
tags: [data-model]
stereotype: entity
parent: []
bounded-context: Settlement
source-of-truth: Legal & Accounting
relationships:
  - { verb: signs, target: "[[DM-010-intent-to-purchase]]", cardinality: "0..*", kind: association }
---

# Buyer

**Purpose.** Whoever signs an intent to purchase and then owes money against a fixed clock: a tenth of the agreed price within a day, the rest within a fortnight.

**Identity.** `id`.

**Attributes.**
- `id` : text — stable buyer reference
- `name` : text — legal name on the intent
- `kind` : enum — individual | museum | institution

**Relationships.**
- signs → [[DM-010-intent-to-purchase]] · 0..* · association

**Invariants / rules.**
- A visitor becomes a buyer only by signing an intent to purchase.
- Missing the balance deadline forfeits half the deposit; the other half is returned.

> [!assumption]
> The attribute list is derived from the glossary definition, not from a
> source that enumerates fields. Names and types are a first cut for the
> team to correct — see [[ISS-025-data-model-attributes-unsourced]].
