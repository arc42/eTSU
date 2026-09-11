---
id: ISS-025
type: issue
title: Data-model attribute lists are derived, not sourced
status: open
created: 2026-09-09
updated: 2026-09-09
sources:
  - "[[SRC-007-tsu-brief]]"
related:
  - "[[DM-001-tour]]"
  - "[[DM-002-show]]"
  - "[[DM-003-piece]]"
  - "[[DM-004-artist]]"
  - "[[DM-005-piece-for-sale]]"
  - "[[DM-006-piece-on-loan]]"
  - "[[DM-007-lending-agreement]]"
  - "[[DM-008-museum]]"
  - "[[DM-009-buyer]]"
  - "[[DM-010-intent-to-purchase]]"
tags: [issue, data-model]
kind: gap
---

# Data-model attribute lists are derived, not sourced

**What.** The ten `DM-` pages were written by projecting the glossary onto the
data-model type. Their *relationships* are sourced: every one of them restates
something a glossary definition already says, and those definitions cite
[[SRC-007-tsu-brief]]. Their **attributes** are not. No source enumerates the
fields of a Piece or an Intent to Purchase, so the attribute names, types and
optionality on every DM page are a first cut, marked inline as
`> [!assumption]`.

**Why it matters.** The attribute list is the half a development team will read
as a specification. Provenance rules say a claim with no source is flagged, not
quietly promoted, and a plausible-looking field list is exactly the kind of
thing that stops being questioned once it renders in a table.

**What would close this.** Someone who knows the business walks the ten pages
and either confirms each field or strikes it. Likely sharpest on:

- `Piece.current-location` — is a location a field on the piece, or the tail of
  a movement history the system holds separately?
- `IntentToPurchase.state` — the four states are inferred from the payment
  clock in [[GLO-013-buyer]], never stated as a lifecycle.
- `Museum.country` — assumed because customs and compliance need it
  ([[GLO-010-aml-screening]]), not because a source says a museum record has it.
- Money types throughout: currency is nowhere in the material, and a global
  tour business plainly has more than one.

**Not blocking.** The relationships and the sum-type split carry the modelling
decisions and stand on their own. This is about field-level detail.
