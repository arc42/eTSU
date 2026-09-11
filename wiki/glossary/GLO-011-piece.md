---
id: GLO-011
type: glossary-term
title: Piece
status: draft
created: 2026-09-09
updated: 2026-09-09
sources:
  - "[[SRC-007-tsu-brief]]"
  - "[[SRC-009-workshop-inventory-decomposition]]"
  - "[[SRC-010-workshop-example-mapping-stories]]"
related:
  - "[[GLO-012-artist]]"
  - "[[GLO-001-tour]]"
  - "[[GLO-002-show]]"
  - "[[GLO-008-lender]]"
  - "[[GLO-021-lending-agreement]]"
  - "[[GLO-017-minimum-sale-price]]"
  - "[[GLO-019-agreed-price]]"
  - "[[GLO-003-provenance]]"
  - "[[GLO-006-conservator]]"
  - "[[GLO-013-buyer]]"
  - "[[GLO-016-home-gallery]]"
  - "[[GLO-018-minimum-museum-sale-price]]"
  - "[[GLO-020-commission]]"
  - "[[GLO-022-intent-to-purchase]]"
  - "[[GLO-023-the-insult]]"
  - "[[FR-001-view-piece-inventory-and-status]]"
  - "[[FR-003-upload-piece-information]]"
  - "[[FR-004-track-piece-status]]"
  - "[[ISS-024-close-out-timing-show-versus-tour]]"
  - "[[FR-005-piece-management]]"
  - "[[FR-006-tour-visibility]]"
  - "[[GOAL-007-artist-self-service]]"
  - "[[FR-008-collect-the-purchase-deposit]]"
  - "[[FR-009-collect-the-purchase-balance]]"
  - "[[FR-010-settle-a-failed-purchase]]"
  - "[[FR-011-pay-artist-commission]]"
  - "[[FR-012-settle-a-loss-claim-on-a-sold-piece]]"
  - "[[DM-003-piece]]"
  - "[[DM-005-piece-for-sale]]"
  - "[[DM-006-piece-on-loan]]"
  - "[[FR-016-piece-protection]]"
  - "[[FR-017-artwork-inventory]]"
  - "[[FR-018-artwork-tracking]]"
  - "[[FR-019-create-the-piece-inventory]]"
  - "[[FR-020-add-piece-details]]"
  - "[[FR-021-upload-piece-images]]"
  - "[[FR-022-display-current-piece-information]]"
  - "[[FR-023-modify-piece-location]]"
  - "[[FR-024-list-filter-search-and-sort-pieces]]"
  - "[[FR-026-sign-the-artist-contract]]"
  - "[[FR-027-reserve-gallery-space-for-a-piece]]"
  - "[[FR-028-insure-a-piece-against-damage]]"
  - "[[FR-029-keep-a-bought-piece-safe-until-handover]]"
  - "[[GOAL-008-pieces-come-home-intact]]"
tags: [glossary]
aliases: [artwork, work, art piece, item, art, picture]
bounded-context: Gallery Touring
agreed: false
stereotype: entity
---

# Piece

**Definition.** A single work of art travelling on a [[GLO-001-tour|Tour]]. Every
piece is either **for sale** or **on loan**, never both, and that one bit decides
almost everything else about it.

**In context.** The piece is the unit the whole business turns on. For sale, it
carries a [[GLO-017-minimum-sale-price|minimum sale price]], a
[[GLO-018-minimum-museum-sale-price|minimum museum sale price]] and a
[[GLO-020-commission|commission]] percentage, all agreed with the
[[GLO-012-artist|artist]] before the tour is a "Go". On loan, it carries a
[[GLO-021-lending-agreement|lending agreement]] instead, and returns to its
[[GLO-008-lender|lender]] by way of a [[GLO-006-conservator|conservator]].

A sold piece **stays on tour**. The buyer takes possession only after the tour
closes, which means a piece can be sold, insured, paid for in full and still
hanging in a gallery two countries away.

**Distinguish from.** Nothing, and that is the problem. *Artwork* is carried as
an alias, not a second term: the brief says "piece" throughout and never once
says artwork, while the card wall says "Artwork Management". The Linz workshop
then used **six more words for it across two photographs** — *item*, *art*,
*painting*, *picture*, *print* and *artwork* — sometimes in one sentence.
*Painting* and *print* are media rather than synonyms and are deliberately **not**
aliased; *item*, *art* and *picture* are. Retitle this page if the group prefers
the workshop's word over the brief's.

> [!note] Notes
> `agreed: false` — sourced from the brief, never confirmed with Gus Renoir's
> team. Open: pieces can be **added mid-tour** when an artist is selling well,
> and some artists create new work for later tour stops while the tour is
> underway. Nothing yet says whether such a piece joins the same tour record or
> starts a new one.
