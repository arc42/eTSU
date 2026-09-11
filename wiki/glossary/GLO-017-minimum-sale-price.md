---
id: GLO-017
type: glossary-term
title: Minimum sale price
status: draft
created: 2026-09-09
updated: 2026-09-09
sources:
  - "[[SRC-007-tsu-brief]]"
related:
  - "[[GLO-018-minimum-museum-sale-price]]"
  - "[[GLO-019-agreed-price]]"
  - "[[GLO-011-piece]]"
  - "[[GLO-012-artist]]"
  - "[[GLO-020-commission]]"
  - "[[FR-014-contract-management]]"
  - "[[FR-020-add-piece-details]]"
  - "[[FR-026-sign-the-artist-contract]]"
tags: [glossary]
aliases: [minimum customer price, floor price]
bounded-context: Settlement
agreed: false
stereotype: value-object
---

# Minimum sale price

**Definition.** The floor below which a [[GLO-011-piece|piece]] may not be sold
to an ordinary buyer, agreed **per piece** with the
[[GLO-012-artist|artist]] before the tour is a "Go".

**In context.** It is a contractual floor, not a price tag. The
[[GLO-019-agreed-price|agreed price]] floats above it as the tour proceeds and
is what a buyer actually pays. The floor is set once; the price moves.

**Distinguish from.** The [[GLO-018-minimum-museum-sale-price|minimum museum
sale price]], a separate floor for the same piece that is almost always lower.
Two floors per piece, not one.

> [!note] Notes
> `agreed: false` — sourced from the brief. Open: what happens to the floor when
> a piece is **added mid-tour**, and whether a floor can be renegotiated once the
> formal contract is signed. The brief says the price floats but never says the
> floor does.
