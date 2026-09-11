---
id: STK-005
type: stakeholder
title: Shipper
status: draft
created: 2026-09-09
updated: 2026-09-09
sources:
  - "[[SRC-004-ulrich-stuerzlinger-context-diagram]]"
  - "[[SRC-002-georg-mayrhauser-vision-goals-stakeholders]]"
related:
  - "[[EIF-012-logistics-and-fulfillment]]"
  - "[[GOAL-003-operational-excellence]]"
  - "[[GLO-001-tour]]"
  - "[[STK-006-insurer]]"
  - "[[GLO-009-logistics-partner]]"
  - "[[GLO-016-home-gallery]]"
  - "[[FR-016-piece-protection]]"
  - "[[FR-023-modify-piece-location]]"
tags: [stakeholder]
aliases: [logistics provider, fine-art shipper]
role: Moves the Tour's pieces between galleries and back to the home gallery
influence: medium
interest: medium
provides: []
receives: []
nature: organization
context_role: none
---

# Shipper

**Snapshot.** A specialist fine-art logistics company. Crucially, **one shipper
covers an entire [[GLO-001-tour|Tour]]** — from the home gallery, through every
[[GLO-002-show|Show]], and back. These companies demand to work that way, so the
shipper is chosen once per tour, not per leg.

**Goals.** [[PAM]] (light)
- Receive a complete, stable manifest and schedule early enough to plan the
  whole route.

**Concerns / pains.**
- Pieces added mid-tour (the brief notes that a strongly selling artist may have
  new work added while the tour is underway) invalidating an agreed manifest.
- Schedule changes propagating late.

**Interactions.** No [[UC-...]] or [[FR-...]] captured yet.

> [!assumption]
> The one-shipper-per-tour rule and mid-tour additions come from
> `raw/TSU-brief.md.md`, still un-ingested.

> [!note] Context edges live on the interface node
> This role is also drawn as a box in the workshop context diagram, so its
> boundary edges are held on [[EIF-012-logistics-and-fulfillment]] (ADR-0026). `context_role: none` keeps it out
> of the projection so the actor renders exactly once (ADR-0014); `provides:`
> and `receives:` stay empty here on purpose.
