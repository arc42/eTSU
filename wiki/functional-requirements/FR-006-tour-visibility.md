---
id: FR-006
type: functional-requirement
title: Tour Visibility
status: draft
created: 2026-09-09
updated: 2026-09-09
sources:
  - "[[SRC-008-sandra-mayer-beneficiary-stories]]"
  - "[[SRC-009-workshop-inventory-decomposition]]"
related:
  - "[[FR-017-artwork-inventory]]"
  - "[[FR-018-artwork-tracking]]"
  - "[[FR-001-view-piece-inventory-and-status]]"
  - "[[FR-004-track-piece-status]]"
  - "[[GLO-011-piece]]"
  - "[[GLO-001-tour]]"
  - "[[GLO-002-show]]"
  - "[[STK-001-gus-renoir]]"
  - "[[STK-002-artist]]"
  - "[[STK-003-gallery-manager]]"
  - "[[ISS-009-real-time-metric-untestable]]"
  - "[[ISS-024-close-out-timing-show-versus-tour]]"
  - "[[ISS-023-sandra-stories-lack-benefit-and-criteria]]"
  - "[[GOAL-007-artist-self-service]]"
tags: [functional-requirement]
stereotype: epic
parent: []
priority: Should
release: backlog
lane: backbone
order: 20
goal:
  - "[[GOAL-005-frictionless-global-art-trade]]"
  - "[[GOAL-007-artist-self-service]]"
---

# Tour Visibility

## Epic: Summary

For everyone with a stake in a [[GLO-001-tour|Tour]], **where every
[[GLO-011-piece|piece]] is and what state it is in**, without phoning the gallery
that happens to be holding it.

**PROBLEM / GOAL**

A tour scatters pieces across galleries for weeks. A piece may be on display,
sold but still touring, awaiting conservation, or releasable to its buyer, and
today the only way to find out is to ask someone. That makes close-out slow and
makes it possible to lose track of a piece that has already been paid for.

**Success metric(s).**

Inherited from [[GOAL-005-frictionless-global-art-trade]]: staleness of a
piece's location, sale status and current price. That metric is **not yet
testable** — [[ISS-009-real-time-metric-untestable]].

**Scope.** in: the piece state model, who may see which pieces, and the
close-out sequence that moves pieces between states · out: the piece record
itself (that is [[FR-005-piece-management]]), and money.

## Hierarchy

- **Parent:** none. This is a top-level epic.
- **Children:** two features, [[FR-017-artwork-inventory]] and
  [[FR-018-artwork-tracking]], carrying six stories between them; plus the story
  [[FR-004-track-piece-status]] directly.
  [[FR-001-view-piece-inventory-and-status]] was **retired** into the two
  features on 2026-09-09.

> [!note] Open points
> - The workshop decomposed this epic's own statement into two groups,
>   **Inventory of artworks** and **Tracking of artworks**, which are now its two
>   features. That is corroboration the epic boundary was roughly right.
> - **Created to give the stories a parent**, 2026-09-09, at Gernot Starke's
>   request. **Not on the card wall** — the twelve cards contain no visibility
>   capability. The name derives from
>   [[GOAL-005-frictionless-global-art-trade]] instead.
> - **The state model is undefined and contested.** The states come from an
>   unfinished list in [[SRC-008-sandra-mayer-beneficiary-stories]], and when the
>   close-out transition fires is disputed —
>   [[ISS-024-close-out-timing-show-versus-tour]].
> - **Visibility rules are undefined.** Gus sees everything; what an artist sees
>   of a group tour, or of another artist's prices, nobody has said.

## History

> Created 2026-09-09 to resolve the orphaned-requirements finding on the
> dashboard backlog page. Its two children were the only stories in the wiki that
> already served [[GOAL-005-frictionless-global-art-trade]].
