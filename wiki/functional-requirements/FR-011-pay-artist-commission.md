---
id: FR-011
type: functional-requirement
title: Pay artist commission
status: draft
created: 2026-09-09
updated: 2026-09-09
sources:
  - "[[SRC-007-tsu-brief]]"
  - "[[SRC-010-workshop-example-mapping-stories]]"
related:
  - "[[FR-007-settlement-and-compliance]]"
  - "[[FR-009-collect-the-purchase-balance]]"
  - "[[FR-012-settle-a-loss-claim-on-a-sold-piece]]"
  - "[[GOAL-006-settlement-correct-and-on-time]]"
  - "[[GLO-020-commission]]"
  - "[[GLO-001-tour]]"
  - "[[GLO-011-piece]]"
  - "[[STK-002-artist]]"
  - "[[STK-001-gus-renoir]]"
  - "[[FR-002-settle-finances-and-legal-obligations]]"
tags: [functional-requirement]
stereotype: story
parent:
  - "[[FR-007-settlement-and-compliance]]"
priority: Should
release: backlog
lane: backbone
order: 80
goal:
  - "[[GOAL-006-settlement-correct-and-on-time]]"
---

# Pay artist commission

## Story

As [[STK-002-artist]] **an artist** I want **both halves of my
[[GLO-020-commission|commission]] paid on their own clocks without my asking**,
so that **I know when a [[GLO-011-piece|piece]] sold and when the money follows**.

**Acceptance criteria.**

- **Given** a piece whose full [[GLO-019-agreed-price|agreed price]] has been
  received, **when** the payment clears, **then** the artist is told the piece
  has sold and **half** the due commission is paid immediately.
- **Given** the same piece, **when** five days have passed since the close of
  the [[GLO-001-tour|Tour]], **then** the **second half** is paid.
- **Given** a commission percentage agreed with the artist before the tour,
  **when** the amount is computed, **then** it uses the price the piece actually
  fetched, not the [[GLO-017-minimum-sale-price|minimum sale price]].

## Hierarchy

- **Parent:** [[FR-007-settlement-and-compliance]].
- **Children:** none.

> [!note] Open points
> - **The second clock is the tour's, not the sale's.** A piece sold at the
>   first [[GLO-002-show|Show]] of a long tour waits for the whole tour to close
>   before its second half is paid. That is what the brief says, and it is the
>   kind of rule an artist would want to renegotiate.
> - **Group tours are unaddressed.** How commission works when several artists
>   share a tour, no source says.
> - **The artist asked for the sale notification independently.** A card in
>   [[SRC-010-workshop-example-mapping-stories]] reads *"I want to be informed
>   about a successful sale so that I get a feeling whether a tour pays off"*,
>   which matches the brief's "we tell the artist that the piece has been sold"
>   from the other side. The notification is carried on
>   [[FR-004-track-piece-status]]; here it stays a payment trigger.
> - [[GOAL-003-operational-excellence]] carries a *secondary* indicator about
>   paying commission in real time. It is not linked in `goal:` here, because
>   that objective's own metric is tour setup lead time.

## History

> Split out of [[FR-002-settle-finances-and-legal-obligations]] on 2026-09-09.
> Both clocks are quoted from [[SRC-007-tsu-brief]]; the "so that" clause is
> derived from it.
