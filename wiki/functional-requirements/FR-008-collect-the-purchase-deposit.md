---
id: FR-008
type: functional-requirement
title: Collect the purchase deposit
status: draft
created: 2026-09-09
updated: 2026-09-09
sources:
  - "[[SRC-007-tsu-brief]]"
related:
  - "[[FR-007-settlement-and-compliance]]"
  - "[[FR-009-collect-the-purchase-balance]]"
  - "[[GOAL-006-settlement-correct-and-on-time]]"
  - "[[GLO-022-intent-to-purchase]]"
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
order: 50
goal:
  - "[[GOAL-006-settlement-correct-and-on-time]]"
---

# Collect the purchase deposit

## Story

As [[STK-001-gus-renoir]] **Head Office** I want **the 10% deposit tracked
against its deadline from the moment an
[[GLO-022-intent-to-purchase|intent to purchase]] is signed**, so that **a
[[GLO-011-piece|piece]] is never held off the market by a
[[GLO-013-buyer|buyer]] who has not paid**.

**Acceptance criteria.**

- **Given** an intent to purchase signed on a Sunday through Thursday, **when**
  24 hours pass without the deposit, **then** the piece becomes available for
  sale again and nothing is owed by either side.
- **Given** an intent signed on a Friday or a Saturday, **when** the deposit
  arrives by the same time on the following Monday, **then** it counts as on
  time.
- **Given** an [[GLO-019-agreed-price|agreed price]], **when** the deposit is
  calculated, **then** it is exactly 10% of that price.

## Hierarchy

- **Parent:** [[FR-007-settlement-and-compliance]].
- **Children:** none.

> [!note] Open points
> - **The weekend rule is stated only for the deposit.** Whether "the same time
>   on Monday" means a public holiday moves it further, no source says.
> - `priority: Should` is the template default. Nobody has applied [[MoSCoW]],
>   though this is a candidate `Must` if any story is.

## History

> Split out of [[FR-002-settle-finances-and-legal-obligations]] on 2026-09-09.
> The rule is quoted from [[SRC-007-tsu-brief]]; the "so that" clause is
> **derived** from the brief's stated consequence, not quoted from it.
