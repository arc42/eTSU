---
id: GLO-012
type: glossary-term
title: Artist
status: draft
created: 2026-09-09
updated: 2026-09-09
sources:
  - "[[SRC-007-tsu-brief]]"
related:
  - "[[STK-002-artist]]"
  - "[[GLO-011-piece]]"
  - "[[GLO-001-tour]]"
  - "[[GLO-020-commission]]"
  - "[[GLO-017-minimum-sale-price]]"
  - "[[GLO-018-minimum-museum-sale-price]]"
  - "[[GLO-008-lender]]"
  - "[[FR-003-upload-piece-information]]"
  - "[[FR-004-track-piece-status]]"
  - "[[FR-005-piece-management]]"
  - "[[GOAL-007-artist-self-service]]"
  - "[[DM-004-artist]]"
  - "[[FR-013-artist-management]]"
  - "[[FR-020-add-piece-details]]"
  - "[[FR-025-register-as-an-artist]]"
  - "[[FR-026-sign-the-artist-contract]]"
tags: [glossary]
aliases: [up-and-coming artist]
bounded-context: Gallery Touring
agreed: false
stereotype: entity
---

# Artist

**Definition.** The creator whose work a [[GLO-001-tour|Tour]] presents. TSU
specialises in the young and up-and-coming, found by the Creative Genius, and a
tour usually shows one artist alone.

**In context.** The artist is a **counterparty before being a beneficiary**.
Four things are negotiated with them before a tour is a "Go": which
[[GLO-011-piece|pieces]] travel, the [[GLO-020-commission|commission]]
percentage, the [[GLO-017-minimum-sale-price|minimum sale price]] per piece and
the [[GLO-018-minimum-museum-sale-price|minimum museum sale price]] per piece.
Agreement on all four turns into a formal contract.

An artist may also be a [[GLO-008-lender|lender]], since some pieces on tour are
on loan from the artist rather than for sale.

**Distinguish from.** A *group tour* shows several artists at once, put together
when no one artist has a large enough body of work. The tour has one concept;
the artist count is not fixed at one.

> [!note] Notes
> `agreed: false` — sourced from the brief. The persona is
> [[STK-002-artist]]. The brief is blunt that artists "all have big egos, and
> will do most anything to have a piece hang in a museum's collection", which is
> the stated reason the museum price sits below the customer price. That is
> motive, and it belongs on the persona rather than in the definition.
