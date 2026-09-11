---
id: GLO-013
type: glossary-term
title: Buyer
status: draft
created: 2026-09-09
updated: 2026-09-09
sources:
  - "[[SRC-007-tsu-brief]]"
related:
  - "[[STK-004-buyer]]"
  - "[[STK-014-art-collector]]"
  - "[[GLO-022-intent-to-purchase]]"
  - "[[GLO-019-agreed-price]]"
  - "[[GLO-023-the-insult]]"
  - "[[GLO-011-piece]]"
  - "[[GLO-014-museum]]"
  - "[[ISS-013-three-way-buyer-segmentation]]"
  - "[[FR-001-view-piece-inventory-and-status]]"
  - "[[ISS-024-close-out-timing-show-versus-tour]]"
  - "[[FR-008-collect-the-purchase-deposit]]"
  - "[[FR-010-settle-a-failed-purchase]]"
  - "[[FR-012-settle-a-loss-claim-on-a-sold-piece]]"
  - "[[DM-009-buyer]]"
  - "[[FR-027-reserve-gallery-space-for-a-piece]]"
  - "[[FR-029-keep-a-bought-piece-safe-until-handover]]"
tags: [glossary]
aliases: [customer]
bounded-context: Settlement
agreed: false
stereotype: entity
---

# Buyer

**Definition.** Whoever signs an [[GLO-022-intent-to-purchase|intent to
purchase]] on a [[GLO-011-piece|piece]] and then owes money against a fixed
clock: 10% of the [[GLO-019-agreed-price|agreed price]] within 24 hours, the
remaining 90% within 14 days of signing.

**In context.** Becoming a buyer is a **moment, not a status**. Before signing,
a person is a visitor with a glass of champagne in a gallery manager's back
office. After signing, they are on a clock, and missing either deadline puts the
piece back on the market. Missing the second one also costs them half the
deposit, which the business calls [[GLO-023-the-insult|The Insult]].

**Distinguish from.** A [[GLO-014-museum|museum]] buying at the
[[GLO-018-minimum-museum-sale-price|minimum museum sale price]] is a buyer on
different terms, and an [[STK-014-art-collector|art collector]] is a
relationship rather than a transaction. How the buying party segments overall is
still open in [[ISS-013-three-way-buyer-segmentation]].

> [!note] Notes
> `agreed: false` — sourced from the brief. The persona is
> [[STK-004-buyer]]. The 24-hour clock has a stated exception: a purchase signed
> on a Friday or Saturday runs until the same time on Monday. The 14-day clock
> has no such exception and runs regardless of the day.
