---
id: FR-027
type: functional-requirement
title: Reserve gallery space for a piece
status: draft
created: 2026-09-09
updated: 2026-09-09
sources:
  - "[[SRC-010-workshop-example-mapping-stories]]"
related:
  - "[[FR-015-tour-scheduling]]"
  - "[[GOAL-003-operational-excellence]]"
  - "[[GLO-015-gallery]]"
  - "[[GLO-002-show]]"
  - "[[GLO-011-piece]]"
  - "[[GLO-013-buyer]]"
  - "[[STK-003-gallery-manager]]"
tags: [functional-requirement]
stereotype: story
parent:
  - "[[FR-015-tour-scheduling]]"
priority: Should
release: backlog
lane: backbone
order: 109
goal:
  - "[[GOAL-003-operational-excellence]]"
---

# Reserve gallery space for a piece

## Story

As [[STK-003-gallery-manager]] **a gallery** I want **to reserve space to show a
[[GLO-011-piece|piece]]**, so that **potential [[GLO-013-buyer|buyers]] can view
it in real life on tour**.

**Acceptance criteria.** *None given.* Nothing says what a unit of space is, or
what happens when a [[GLO-002-show|Show]] is over-subscribed.

**This introduces a constraint no earlier source has.** Until now a
[[GLO-015-gallery|gallery]] was a venue that a tour visits. This card says
galleries have **finite capacity** that must be booked per piece. If true, tour
assembly is a fitting problem, not just a scheduling one, and the number of
pieces a tour can carry is bounded by its smallest venue.

**The role is drawn as the gallery itself**, not a person. Mapped here to
[[STK-003-gallery-manager]] as the only human who runs a gallery, **which is the
agent's mapping**; the card may mean the gallery as an organisation.

## Hierarchy

- **Parent:** [[FR-015-tour-scheduling]].

> [!note] Open points
> - **Capacity is unquantified.** No source gives gallery dimensions or a
>   piece-count limit.
> - **Who reserves?** Head Office allocating pieces to galleries, or a gallery
>   claiming pieces, are opposite flows.

## History

> Transcribed 2026-09-09 from [[SRC-010-workshop-example-mapping-stories]].
> Benefit clause supplied by the card, which reads "in real life / on tour" with
> an earlier word struck out.
