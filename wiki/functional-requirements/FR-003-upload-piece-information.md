---
id: FR-003
type: functional-requirement
title: Upload piece information
status: draft
created: 2026-09-09
updated: 2026-09-09
sources:
  - "[[SRC-008-sandra-mayer-beneficiary-stories]]"
  - "[[SRC-010-workshop-example-mapping-stories]]"
related:
  - "[[STK-002-artist]]"
  - "[[GLO-012-artist]]"
  - "[[GLO-011-piece]]"
  - "[[GLO-003-provenance]]"
  - "[[EIF-001-artists]]"
  - "[[ISS-023-sandra-stories-lack-benefit-and-criteria]]"
  - "[[ISS-004-scope-inflation-marketplace-vs-back-office]]"
  - "[[FR-005-piece-management]]"
  - "[[GOAL-007-artist-self-service]]"
  - "[[FR-021-upload-piece-images]]"
  - "[[FR-020-add-piece-details]]"
tags: [functional-requirement]
stereotype: story
parent:
  - "[[FR-005-piece-management]]"
priority: Should
release: backlog
lane: backbone
order: 30
goal:
  - "[[GOAL-007-artist-self-service]]"
---

# Upload piece information

## Story

As [[STK-002-artist]] **an artist** I want **to upload information about my
[[GLO-011-piece|pieces]]**, so that **my work can be displayed and sold without
me being there**.

> [!note] Benefit supplied 2026-09-09 by three later cards
> Sandra Mayer's original stopped at "upload information about my artwork" with
> no "so that". Three cards in [[SRC-010-workshop-example-mapping-stories]] ask
> for the same capability and each states a reason: *"so it can be presented
> online"*, *"so that my pictures can be displayed and sold"*, and *"so I can
> sell them"*. The clause above merges those three; it is **the workshop's
> reason, in the agent's words**. The three cards are recorded here rather than
> given pages of their own.

**Acceptance criteria.** *None given.* Nothing says what information, in what
format, or who may change it after upload.

- **Given** … **when** … **then** …

**This is the first artist-facing surface in the wiki, and that matters.** Every
earlier source has artists as a *counterparty* TSU negotiates with. The card
wall's "Artist Management" means TSU managing artists. This story reverses the
direction: the artist logs in and maintains their own catalogue entries. A
back-office tool does not need that, so it is evidence bearing on
[[ISS-004-scope-inflation-marketplace-vs-back-office]].

It also touches [[GLO-003-provenance|provenance]]. If artists supply the
catalogue information themselves, artist-supplied data becomes part of the
evidence chain, which is exactly the material an appraiser or authenticator
would be checking.

## Hierarchy

- **Parent:** [[FR-005-piece-management]], the card wall's "Artwork Management"
  named in the ubiquitous language.
- **Children:** none.

> [!note] Open points
> - **What information?** Title, dimensions, medium, year, images, price
>   expectations, provenance documents — the source says none of these.
> - **Who may edit it afterwards?** An artist changing their own catalogue entry
>   mid-tour has pricing and provenance consequences.
> - The `goal:` link to [[GOAL-002-global-market-expansion]] was **removed** on
>   2026-09-09: that objective measures digital revenue share, which artist data
>   entry touches only at two removes.
>   [[GOAL-007-artist-self-service]] was written for it instead, and is itself
>   unconfirmed with Gus Renoir's team.

## History

> Transcribed 2026-09-09 from [[SRC-008-sandra-mayer-beneficiary-stories]].
> Wording normalised (artwork → [[GLO-011-piece|piece]], of which *artwork* is a
> recorded alias).
