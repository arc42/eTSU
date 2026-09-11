---
id: FR-012
type: functional-requirement
title: Settle a loss claim on a sold piece
status: draft
created: 2026-09-09
updated: 2026-09-09
sources:
  - "[[SRC-007-tsu-brief]]"
related:
  - "[[FR-007-settlement-and-compliance]]"
  - "[[FR-011-pay-artist-commission]]"
  - "[[GOAL-006-settlement-correct-and-on-time]]"
  - "[[GLO-020-commission]]"
  - "[[GLO-011-piece]]"
  - "[[GLO-013-buyer]]"
  - "[[GLO-001-tour]]"
  - "[[STK-006-insurer]]"
  - "[[STK-001-gus-renoir]]"
  - "[[FR-002-settle-finances-and-legal-obligations]]"
  - "[[FR-016-piece-protection]]"
  - "[[FR-028-insure-a-piece-against-damage]]"
  - "[[FR-029-keep-a-bought-piece-safe-until-handover]]"
tags: [functional-requirement]
stereotype: story
parent:
  - "[[FR-007-settlement-and-compliance]]"
priority: Should
release: backlog
lane: backbone
order: 90
goal:
  - "[[GOAL-006-settlement-correct-and-on-time]]"
---

# Settle a loss claim on a sold piece

## Story

As [[STK-001-gus-renoir]] **Head Office** I want **the three-way unwind applied
when a sold [[GLO-011-piece|piece]] is lost or damaged while still on tour**, so
that **the [[GLO-013-buyer|buyer]] is made whole and the artist keeps what they
were already paid**.

**Acceptance criteria.**

- **Given** a piece paid for in full and still on [[GLO-001-tour|Tour]],
  **when** it is lost or damaged, **then** the buyer is refunded the **entire**
  amount received.
- **Given** the same event, **when** the [[GLO-020-commission|commission]] is
  reconsidered, **then** the artist **keeps** the half already paid and it is
  not reclaimed.
- **Given** the same event, **when** TSU accounts for the loss, **then** the
  half-commission already paid is absorbed from the
  [[STK-006-insurer|insurance]] payout, not billed to anyone.

## Hierarchy

- **Parent:** [[FR-007-settlement-and-compliance]].
- **Children:** none.

> [!note] Open points
> - **The second half of the commission is unaddressed.** The brief says the
>   artist keeps the half already paid; whether the half due five days after
>   tour close is still owed, it does not say. Real money, and genuinely open.
> - **Loss before full payment is unaddressed.** The rule as written assumes the
>   buyer has paid in full.
> - **Who declares a piece lost, and when**, no source says.

## History

> Split out of [[FR-002-settle-finances-and-legal-obligations]] on 2026-09-09.
> Every rule is quoted from [[SRC-007-tsu-brief]]; the "so that" clause is
> derived from it.
