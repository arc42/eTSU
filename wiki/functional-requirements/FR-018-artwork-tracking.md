---
id: FR-018
type: functional-requirement
title: Artwork Tracking
status: draft
created: 2026-09-09
updated: 2026-09-09
sources:
  - "[[SRC-009-workshop-inventory-decomposition]]"
related:
  - "[[FR-006-tour-visibility]]"
  - "[[FR-022-display-current-piece-information]]"
  - "[[FR-023-modify-piece-location]]"
  - "[[FR-024-list-filter-search-and-sort-pieces]]"
  - "[[FR-017-artwork-inventory]]"
  - "[[GLO-011-piece]]"
  - "[[ISS-009-real-time-metric-untestable]]"
  - "[[FR-001-view-piece-inventory-and-status]]"
tags: [functional-requirement]
stereotype: feature
parent:
  - "[[FR-006-tour-visibility]]"
priority: Should
release: backlog
lane: backbone
order: 22
goal:
  - "[[GOAL-005-frictionless-global-art-trade]]"
---

# Artwork Tracking

## Story

For anyone with a stake in a tour, **finding a [[GLO-011-piece|piece]] and
seeing its current state** — where it is now, and what has changed.

**PROBLEM / GOAL**

An inventory nobody can query is a list. This feature is the read side: current
information, location, and the means to find one piece among many.

**Success metric(s).** Inherited from
[[GOAL-005-frictionless-global-art-trade]], whose metric is not yet testable —
[[ISS-009-real-time-metric-untestable]].

**Scope.** in: display, location updates, listing and finding · out: creating
entries, and status transitions at close-out.

## Hierarchy

- **Parent:** [[FR-006-tour-visibility]].
- **Children:** [[FR-022-display-current-piece-information]],
  [[FR-023-modify-piece-location]],
  [[FR-024-list-filter-search-and-sort-pieces]].

> [!note] Open points
> - **"Modify location data" is the only write on this side**, which suggests
>   location is maintained by hand rather than derived from shipping. Nobody
>   said which.
> - Card title kept as drawn: **"Tracking of artworks"**.

## History

> Created 2026-09-09 from the grouping card in
> [[SRC-009-workshop-inventory-decomposition]].
