---
id: DM-010
type: data-model
title: Intent to purchase
status: draft
created: 2026-09-09
updated: 2026-09-09
sources:
  - "[[SRC-007-tsu-brief]]"
related:
  - "[[GLO-022-intent-to-purchase]]"
  - "[[GOAL-006-settlement-correct-and-on-time]]"
  - "[[ISS-025-data-model-attributes-unsourced]]"
tags: [data-model]
stereotype: entity
parent: []
bounded-context: Settlement
source-of-truth: Legal & Accounting
relationships:
  - { verb: for, target: "[[DM-005-piece-for-sale]]", cardinality: "1", kind: association }
  - { verb: names, target: "[[GLO-019-agreed-price]]", cardinality: "1", kind: composition }
  - { verb: signed at, target: "[[GLO-015-gallery]]", cardinality: "1", kind: association }
  - { verb: refunds, target: "[[GLO-023-the-insult]]", cardinality: "0..1", kind: association }
---

# Intent to purchase

**Purpose.** The signed document that turns a visitor into a buyer, names the agreed price, and starts both payment clocks.

**Identity.** `id`.

**Attributes.**
- `id` : text — stable intent reference
- `signed-on` : datetime — starts the deposit clock
- `deposit-due` : datetime — 24 hours after signing
- `balance-due` : datetime — 14 days after signing
- `state` : enum — signed | deposit-paid | settled | failed

**Relationships.**
- for → [[DM-005-piece-for-sale]] · 1 · association
- names → [[GLO-019-agreed-price]] · 1 · composition
- signed at → [[GLO-015-gallery]] · 1 · association
- refunds → [[GLO-023-the-insult]] · 0..1 · association

**Invariants / rules.**
- The agreed price is fixed for the duration of the show in which it is signed.
- The Insult exists only on a failed intent, never on a settled one.

> [!assumption]
> The attribute list is derived from the glossary definition, not from a
> source that enumerates fields. Names and types are a first cut for the
> team to correct — see [[ISS-025-data-model-attributes-unsourced]].
