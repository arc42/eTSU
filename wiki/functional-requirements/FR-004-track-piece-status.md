---
id: FR-004
type: functional-requirement
title: Track piece status
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
  - "[[FR-001-view-piece-inventory-and-status]]"
  - "[[ISS-023-sandra-stories-lack-benefit-and-criteria]]"
  - "[[ISS-009-real-time-metric-untestable]]"
  - "[[ISS-004-scope-inflation-marketplace-vs-back-office]]"
  - "[[FR-006-tour-visibility]]"
  - "[[GOAL-007-artist-self-service]]"
tags: [functional-requirement]
stereotype: story
parent:
  - "[[FR-006-tour-visibility]]"
priority: Should
release: backlog
lane: backbone
order: 40
goal:
  - "[[GOAL-005-frictionless-global-art-trade]]"
  - "[[GOAL-007-artist-self-service]]"
---

# Track piece status

## Story

As [[STK-002-artist]] **an artist** I want **an up-to-date status of my
[[GLO-011-piece|pieces]]**, so that **I can tell whether a
[[GLO-001-tour|Tour]] is paying off**.

> [!note] Benefit supplied 2026-09-09 by two later cards
> Sandra Mayer's original had no "so that". Two cards in
> [[SRC-010-workshop-example-mapping-stories]] supply reasons, and they are
> different from each other: *"I want to be informed about a successful sale so
> that I get a feeling whether a tour pays off or not"*, used above, and *"I want
> to check my sellings so I can prepare my tax statements"*.
>
> **The tax reason is a second, separate need**, and arguably a second story: an
> artist preparing a tax statement wants a period summary, not a live status.
> Recorded here rather than split, because splitting it is the group's call.

**Acceptance criteria.** *None given.* "Updated" carries no frequency and no
latency, which is the same defect [[ISS-009-real-time-metric-untestable]]
records against [[GOAL-005-frictionless-global-art-trade]].

- **Given** … **when** … **then** …

**Same status model as [[FR-001-view-piece-inventory-and-status]], different
audience.** Gus wants the whole inventory; the artist wants only their own
pieces. That is one state machine with two views over it, and the difference
that matters is **what an artist may see**: their own sales, certainly, but
whether they see the [[GLO-019-agreed-price|agreed price]] a piece fetched, or
another artist's pieces on a group tour, nobody has said.

The brief gives the artist a concrete reason to care that no source states
outright. Half the [[GLO-020-commission|commission]] is paid on sale and half
five days after the tour closes, so an artist tracking status is also tracking
when they get paid.

## Hierarchy

- **Parent:** [[FR-006-tour-visibility]].
- **Children:** none.

> [!note] Open points
> - **Visibility rules are undefined.** Own pieces only, presumably, but the
>   group-tour case is unaddressed.
> - **"Updated" needs a number.** Live, daily, on change? Untestable as written.
> - Artist-facing, like [[FR-003-upload-piece-information]] — evidence for
>   [[ISS-004-scope-inflation-marketplace-vs-back-office]].

## History

> Transcribed 2026-09-09 from [[SRC-008-sandra-mayer-beneficiary-stories]].
