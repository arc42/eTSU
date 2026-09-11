---
id: GLO-020
type: glossary-term
title: Commission
status: draft
created: 2026-09-09
updated: 2026-09-09
sources:
  - "[[SRC-007-tsu-brief]]"
related:
  - "[[GLO-012-artist]]"
  - "[[GLO-019-agreed-price]]"
  - "[[GLO-001-tour]]"
  - "[[GLO-011-piece]]"
  - "[[STK-010-legal-and-accounting]]"
  - "[[GLO-017-minimum-sale-price]]"
  - "[[FR-002-settle-finances-and-legal-obligations]]"
  - "[[FR-007-settlement-and-compliance]]"
  - "[[GOAL-006-settlement-correct-and-on-time]]"
  - "[[GOAL-007-artist-self-service]]"
  - "[[FR-011-pay-artist-commission]]"
  - "[[FR-012-settle-a-loss-claim-on-a-sold-piece]]"
  - "[[FR-014-contract-management]]"
  - "[[FR-026-sign-the-artist-contract]]"
tags: [glossary]
aliases: [artist commission]
bounded-context: Settlement
agreed: false
stereotype: value-object
---

# Commission

**Definition.** The share of a sale owed to the [[GLO-012-artist|artist]],
agreed per piece before the tour and typically **20% to 40%**.

**In context.** How TSU makes money, and it settles in **two halves on two
different clocks**. Half is paid to the artist as soon as the full
[[GLO-019-agreed-price|agreed price]] has been received. The other half is paid
**five days after the close of the [[GLO-001-tour|Tour]]**, not five days after
the sale.

There is a loss rule that matters more than its length suggests: if a sold piece
is damaged or destroyed while still on tour, the buyer is refunded in full, the
artist **keeps** the half-commission already paid, and TSU absorbs that cost out
of the insurance payment.

**Distinguish from.** The commission *percentage*, agreed with the artist up
front, and the commission *amount*, which depends on the price the piece
eventually fetched. The brief negotiates the first and settles the second.

> [!note] Notes
> `agreed: false` — sourced from the brief. Open: how commission works on a
> group tour, and whether the 20–40% band is a rule or an observation.
