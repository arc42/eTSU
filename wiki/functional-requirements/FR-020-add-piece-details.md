---
id: FR-020
type: functional-requirement
title: Add piece details
status: draft
created: 2026-09-09
updated: 2026-09-09
sources:
  - "[[SRC-009-workshop-inventory-decomposition]]"
related:
  - "[[FR-017-artwork-inventory]]"
  - "[[FR-003-upload-piece-information]]"
  - "[[GLO-011-piece]]"
  - "[[GLO-012-artist]]"
  - "[[GLO-017-minimum-sale-price]]"
  - "[[GLO-019-agreed-price]]"
  - "[[STK-001-gus-renoir]]"
  - "[[FR-022-display-current-piece-information]]"
tags: [functional-requirement]
stereotype: story
parent:
  - "[[FR-017-artwork-inventory]]"
priority: Should
release: backlog
lane: backbone
order: 102
goal:
  - "[[GOAL-005-frictionless-global-art-trade]]"
---

# Add piece details

## Story

As [[STK-001-gus-renoir]] **Head Office** I want **to record a
[[GLO-011-piece|piece]]'s title, description, artist name and selling price**,
so that **&lt;benefit not stated&gt;**.

> [!assumption] Fields quoted, benefit absent
> The card lists the four fields verbatim: *title, description, artist name,
> selling price*. It states no benefit —
> [[ISS-023-sandra-stories-lack-benefit-and-criteria]].

**Acceptance criteria.** *None given.*

**This is the first field list in the wiki**, and it is thinner than the business
needs. It has no medium, no dimensions, no year, no provenance documents, and
**one** price where the brief has three:
[[GLO-017-minimum-sale-price|minimum sale price]],
[[GLO-018-minimum-museum-sale-price|minimum museum sale price]] and the floating
[[GLO-019-agreed-price|agreed price]]. Which of the three "selling price" means
is undetermined, and the answer is a pricing rule.

## Hierarchy

- **Parent:** [[FR-017-artwork-inventory]].

> [!note] Open points
> - **"Selling price" is ambiguous across three defined price terms.**
> - Overlaps [[FR-003-upload-piece-information]], where the artist supplies the
>   same data. Who writes which field is undecided.

## History

> Transcribed 2026-09-09 from [[SRC-009-workshop-inventory-decomposition]].
