---
id: FR-009
type: functional-requirement
title: Collect the purchase balance
status: draft
created: 2026-09-09
updated: 2026-09-09
sources:
  - "[[SRC-007-tsu-brief]]"
related:
  - "[[FR-007-settlement-and-compliance]]"
  - "[[FR-008-collect-the-purchase-deposit]]"
  - "[[FR-010-settle-a-failed-purchase]]"
  - "[[FR-011-pay-artist-commission]]"
  - "[[GOAL-006-settlement-correct-and-on-time]]"
  - "[[GLO-022-intent-to-purchase]]"
  - "[[GLO-019-agreed-price]]"
  - "[[GLO-011-piece]]"
  - "[[STK-001-gus-renoir]]"
  - "[[FR-002-settle-finances-and-legal-obligations]]"
tags: [functional-requirement]
stereotype: story
parent:
  - "[[FR-007-settlement-and-compliance]]"
priority: Should
release: backlog
lane: backbone
order: 60
goal:
  - "[[GOAL-006-settlement-correct-and-on-time]]"
---

# Collect the purchase balance

## Story

As [[STK-001-gus-renoir]] **Head Office** I want **the remaining 90% tracked
against its own 14-day deadline**, so that **a sale either completes on schedule
or fails cleanly, without anyone chasing it by hand**.

**Acceptance criteria.**

- **Given** an [[GLO-022-intent-to-purchase|intent to purchase]], **when** 14
  days from **signing** pass without the remaining 90%, **then** the sale fails
  and [[FR-010-settle-a-failed-purchase]] applies.
- **Given** any weekday of signing, **when** the 14 days are counted, **then**
  no weekend or holiday extension applies. The deadline runs from signing
  regardless of the day, unlike the deposit's.
- **Given** the full [[GLO-019-agreed-price|agreed price]] has been received,
  **when** the payment clears, **then** the [[GLO-011-piece|piece]] counts as
  sold and [[FR-011-pay-artist-commission]] is triggered.

## Hierarchy

- **Parent:** [[FR-007-settlement-and-compliance]].
- **Children:** none.

> [!note] Open points
> - **The two clocks run concurrently, not in sequence.** Both start at signing,
>   so a buyer who pays the deposit on day 13 still owes the balance on day 14.
>   The brief implies this; no source states it outright.
> - A sold piece **stays on tour** until the tour closes. Completing payment does
>   not release the piece — see [[ISS-024-close-out-timing-show-versus-tour]].

## History

> Split out of [[FR-002-settle-finances-and-legal-obligations]] on 2026-09-09.
> Rule from [[SRC-007-tsu-brief]]; the "so that" clause is derived from it, not
> quoted.
