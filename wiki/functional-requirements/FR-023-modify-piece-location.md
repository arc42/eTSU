---
id: FR-023
type: functional-requirement
title: Modify piece location
status: draft
created: 2026-09-09
updated: 2026-09-09
sources:
  - "[[SRC-009-workshop-inventory-decomposition]]"
related:
  - "[[FR-018-artwork-tracking]]"
  - "[[GLO-011-piece]]"
  - "[[GLO-015-gallery]]"
  - "[[GLO-002-show]]"
  - "[[STK-005-shipper]]"
  - "[[EIF-012-logistics-and-fulfillment]]"
  - "[[STK-001-gus-renoir]]"
tags: [functional-requirement]
stereotype: story
parent:
  - "[[FR-018-artwork-tracking]]"
priority: Should
release: backlog
lane: backbone
order: 105
goal:
  - "[[GOAL-005-frictionless-global-art-trade]]"
---

# Modify piece location

## Story

As [[STK-001-gus-renoir]] **Head Office** I want **to change where a
[[GLO-011-piece|piece]] currently is**, so that **&lt;benefit not stated&gt;**.

> [!assumption] Bare operation card
> Reads "Modify location data".

**Acceptance criteria.** *None given.*

**The card implies location is typed in, not derived.** A tour moves pieces
between [[GLO-015-gallery|galleries]] under one shipper for the whole tour
([[EIF-012-logistics-and-fulfillment]]), so location could come from the
shipper's own tracking. Making it a manual edit is a design choice nobody has
argued for, and it puts the freshness of the whole tracking feature in the hands
of whoever remembers to update it.

## Hierarchy

- **Parent:** [[FR-018-artwork-tracking]].

> [!note] Open points
> - **Manual or derived?** This decides whether
>   [[GOAL-005-frictionless-global-art-trade]] is achievable at all.
> - **What is a location** — a gallery, a [[GLO-002-show|Show]], a crate in
>   transit, or a customs hold? No source says.

## History

> Transcribed 2026-09-09 from [[SRC-009-workshop-inventory-decomposition]].
