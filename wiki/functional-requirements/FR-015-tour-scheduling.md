---
id: FR-015
type: functional-requirement
title: Tour Scheduling
status: draft
created: 2026-09-09
updated: 2026-09-09
sources:
  - "[[SRC-009-workshop-inventory-decomposition]]"
  - "[[SRC-010-workshop-example-mapping-stories]]"
  - "[[SRC-005-workshop-capability-card-wall]]"
related:
  - "[[FR-027-reserve-gallery-space-for-a-piece]]"
  - "[[GOAL-003-operational-excellence]]"
  - "[[GLO-001-tour]]"
  - "[[GLO-002-show]]"
  - "[[GLO-015-gallery]]"
  - "[[GLO-016-home-gallery]]"
  - "[[STK-003-gallery-manager]]"
  - "[[ISS-017-twelve-candidate-capabilities-undefined]]"
tags: [functional-requirement]
stereotype: epic
parent: []
priority: Should
release: backlog
lane: backbone
order: 60
goal:
  - "[[GOAL-003-operational-excellence]]"
---

# Tour Scheduling

## Epic: Summary

For [[STK-001-gus-renoir|Head Office]] and
[[STK-003-gallery-manager|gallery managers]], **which
[[GLO-011-piece|pieces]] hang where and when** across a
[[GLO-001-tour|Tour]]'s sequence of [[GLO-002-show|Shows]].

**PROBLEM / GOAL**

Once a tour is a "Go", each [[GLO-015-gallery|gallery]] must be told its dates,
when details follow, when to start customs paperwork and when to begin local
publicity. The workshop added a constraint no earlier source mentions: a gallery
has **finite wall space**, and space has to be reserved for a piece before it can
be shown.

**Success metric(s).** Inherited from
[[GOAL-003-operational-excellence]]: tour setup lead time.

**Scope.** in: show dates, per-gallery lead times, space reservation, the
[[GLO-016-home-gallery|home gallery]] as start and end point · out: physical
movement between shows, and contracts.

## Hierarchy

- **Parent:** none.
- **Children:** [[FR-027-reserve-gallery-space-for-a-piece]].

> [!note] Open points
> - Named from the green **Schedule Mechanism** card (written "SCHDULE") in
>   [[SRC-009-workshop-inventory-decomposition]]. Related to card 6 of
>   [[ISS-017-twelve-candidate-capabilities-undefined]], "tour planning", which
>   stays held because planning and scheduling may not be the same capability.
> - **Gallery capacity is a new fact.** No source states how much space a gallery
>   has, and the "6 locations" figure is itself unconfirmed.

## History

> Created 2026-09-09 from the Schedule Mechanism card and the gallery
> space-reservation story in [[SRC-010-workshop-example-mapping-stories]]. It
> gives [[GOAL-003-operational-excellence]] its first backlog.
