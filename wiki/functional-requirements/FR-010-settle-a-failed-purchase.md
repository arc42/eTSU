---
id: FR-010
type: functional-requirement
title: Settle a failed purchase
status: draft
created: 2026-09-09
updated: 2026-09-09
sources:
  - "[[SRC-007-tsu-brief]]"
related:
  - "[[FR-007-settlement-and-compliance]]"
  - "[[FR-009-collect-the-purchase-balance]]"
  - "[[GOAL-006-settlement-correct-and-on-time]]"
  - "[[GLO-023-the-insult]]"
  - "[[GLO-019-agreed-price]]"
  - "[[GLO-011-piece]]"
  - "[[GLO-013-buyer]]"
  - "[[STK-001-gus-renoir]]"
  - "[[FR-002-settle-finances-and-legal-obligations]]"
tags: [functional-requirement]
stereotype: story
parent:
  - "[[FR-007-settlement-and-compliance]]"
priority: Should
release: backlog
lane: backbone
order: 70
goal:
  - "[[GOAL-006-settlement-correct-and-on-time]]"
---

# Settle a failed purchase

## Story

As [[STK-001-gus-renoir]] **Head Office** I want **[[GLO-023-the-insult|The
Insult]] computed and paid automatically when a buyer misses the balance**, so
that **the split is always right and the [[GLO-011-piece|piece]] returns to the
market the same day**.

**Acceptance criteria.**

- **Given** a [[GLO-013-buyer|buyer]] who paid the deposit and missed the
  14-day balance, **when** the deadline passes, **then** half the deposit is
  returned to that buyer and half is retained by TSU.
- **Given** the same failure, **when** it is settled, **then** the piece becomes
  available for sale again.
- **Given** an [[GLO-019-agreed-price|agreed price]], **when** the returned
  amount is computed, **then** it is 5% of that price, being half of the 10%
  deposit.
- **Given** a buyer who missed the **deposit** instead, **when** that deadline
  passes, **then** the piece returns to the market and **no Insult arises**,
  because no money changed hands.

## Hierarchy

- **Parent:** [[FR-007-settlement-and-compliance]].
- **Children:** none.

> [!note] Open points
> - **[[GLO-023-the-insult|The Insult]] names the returned half, not the
>   retained half.** A reader who inverts it computes the wrong payment, which
>   is why the term has a glossary entry.
> - **When the piece is re-priced after returning to the market, nobody says.**
>   The [[GLO-019-agreed-price|agreed price]] is fixed within a
>   [[GLO-002-show|Show]] but floats between Shows, so a piece failing mid-Show
>   may or may not go back at the same price.

## History

> Split out of [[FR-002-settle-finances-and-legal-obligations]] on 2026-09-09.
> Every figure is quoted from [[SRC-007-tsu-brief]]; the "so that" clause is
> derived from it.
