---
id: GLO-022
type: glossary-term
title: Intent to purchase
status: draft
created: 2026-09-09
updated: 2026-09-09
sources:
  - "[[SRC-007-tsu-brief]]"
related:
  - "[[GLO-013-buyer]]"
  - "[[GLO-019-agreed-price]]"
  - "[[GLO-023-the-insult]]"
  - "[[GLO-011-piece]]"
  - "[[GLO-015-gallery]]"
  - "[[STK-003-gallery-manager]]"
  - "[[FR-007-settlement-and-compliance]]"
  - "[[GOAL-006-settlement-correct-and-on-time]]"
  - "[[FR-008-collect-the-purchase-deposit]]"
  - "[[FR-009-collect-the-purchase-balance]]"
  - "[[DM-010-intent-to-purchase]]"
tags: [glossary]
aliases: [signed intent, purchase intent]
bounded-context: Settlement
agreed: false
stereotype: entity
---

# Intent to purchase

**Definition.** The signed document that turns a visitor into a
[[GLO-013-buyer|buyer]]. Drawn up in a
[[STK-003-gallery-manager|gallery manager's]] back office, over champagne, and
signed there.

**In context.** Signing **starts both clocks**: 10% of the
[[GLO-019-agreed-price|agreed price]] within 24 hours, extended to the same time
on Monday if the signature falls on a Friday or Saturday, and the remaining 90%
within 14 days of signing regardless of the day. Miss the first and the
[[GLO-011-piece|piece]] simply goes back on the market. Miss the second and it
also costs the buyer [[GLO-023-the-insult|The Insult]].

The ceremony is not decoration. The brief is explicit that buying art "is
supposed to be a genteel activity", and the back-office signing is described as
a tradition TSU has to follow. Any digital purchase flow has to reckon with
that, not design it away.

**Distinguish from.** A completed sale. The piece is not sold until all the
money has arrived, and even then it **stays on tour** until the tour closes.

> [!note] Notes
> `agreed: false` — sourced from the brief. Open: whether an intent to purchase
> can be signed anywhere other than a gallery back office, which is precisely
> what a digital product would want to change —
> [[ISS-004-scope-inflation-marketplace-vs-back-office]].
