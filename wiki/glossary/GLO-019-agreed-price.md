---
id: GLO-019
type: glossary-term
title: Agreed price
status: draft
created: 2026-09-09
updated: 2026-09-09
sources:
  - "[[SRC-007-tsu-brief]]"
related:
  - "[[GLO-017-minimum-sale-price]]"
  - "[[GLO-018-minimum-museum-sale-price]]"
  - "[[GLO-002-show]]"
  - "[[GLO-022-intent-to-purchase]]"
  - "[[GLO-023-the-insult]]"
  - "[[GLO-020-commission]]"
  - "[[GLO-011-piece]]"
  - "[[GLO-013-buyer]]"
  - "[[FR-002-settle-finances-and-legal-obligations]]"
  - "[[FR-007-settlement-and-compliance]]"
  - "[[GOAL-006-settlement-correct-and-on-time]]"
  - "[[FR-008-collect-the-purchase-deposit]]"
  - "[[FR-009-collect-the-purchase-balance]]"
  - "[[FR-010-settle-a-failed-purchase]]"
  - "[[FR-020-add-piece-details]]"
tags: [glossary]
aliases: [floating price, sale price]
bounded-context: Settlement
agreed: false
stereotype: value-object
---

# Agreed price

**Definition.** The price a [[GLO-013-buyer|buyer]] actually pays for a
[[GLO-011-piece|piece]], named in the
[[GLO-022-intent-to-purchase|intent to purchase]]. It **floats as the tour
proceeds** but is **fixed for the duration of each [[GLO-002-show|Show]]**.

**In context.** Fixed within a stop, resettable between stops. That single rule
is a data-model invariant and a source of real questions: two buyers at two
different stops on the same tour can legitimately pay different amounts for
comparable pieces, and the 10% deposit and 90% balance are both computed against
the price at signing.

**Distinguish from.** The [[GLO-017-minimum-sale-price|minimum sale price]],
which is the floor it may not fall below. The floor is contractual and per
piece; the agreed price is commercial and per show.

> [!note] Notes
> `agreed: false` — sourced from the brief. Open: whether a price reset mid-tour
> can move **downwards**, and what happens to a piece whose price is reset while
> an intent to purchase is still inside its 14-day window. Nothing in the brief
> answers either.
