---
id: FR-016
type: functional-requirement
title: Piece Protection
status: draft
created: 2026-09-09
updated: 2026-09-09
sources:
  - "[[SRC-010-workshop-example-mapping-stories]]"
  - "[[SRC-005-workshop-capability-card-wall]]"
related:
  - "[[FR-028-insure-a-piece-against-damage]]"
  - "[[FR-029-keep-a-bought-piece-safe-until-handover]]"
  - "[[FR-012-settle-a-loss-claim-on-a-sold-piece]]"
  - "[[GOAL-008-pieces-come-home-intact]]"
  - "[[GLO-011-piece]]"
  - "[[GLO-021-lending-agreement]]"
  - "[[GLO-006-conservator]]"
  - "[[STK-006-insurer]]"
  - "[[STK-005-shipper]]"
  - "[[ISS-017-twelve-candidate-capabilities-undefined]]"
tags: [functional-requirement]
stereotype: epic
parent: []
priority: Should
release: backlog
lane: backbone
order: 70
goal:
  - "[[GOAL-008-pieces-come-home-intact]]"
---

# Piece Protection

## Epic: Summary

For [[STK-002-artist|artists]], [[STK-004-buyer|buyers]] and lenders, **the
physical safety of a [[GLO-011-piece|piece]] while it travels** — insurance
cover, custody, condition, and what happens when something goes wrong.

**PROBLEM / GOAL**

Every rule the brief states about damage protects **money**: the buyer is
refunded, the artist keeps their half-commission, TSU absorbs the rest from
insurance. Two workshop cards ask instead that the **work** be protected, and
Gernot Starke settled it on 2026-09-09 with "we need to protect both". A
[[GLO-021-lending-agreement|lending agreement]] makes the same demand
contractually: a borrowed piece must go home, conserved, and a refund does not
discharge that.

**Success metric(s).** Inherited from
[[GOAL-008-pieces-come-home-intact]]: share of pieces completing a tour with no
loss and no unrecorded condition change.

**Scope.** in: insurance cover per piece, custody and condition at each
hand-over, damage and loss handling · out: the **money** consequences of a loss,
which stay on [[FR-012-settle-a-loss-claim-on-a-sold-piece]] under settlement.

## Hierarchy

- **Parent:** none.
- **Children:** [[FR-028-insure-a-piece-against-damage]],
  [[FR-029-keep-a-bought-piece-safe-until-handover]].

> [!note] Open points
> - **Moved out of [[FR-007-settlement-and-compliance]] on 2026-09-09.** Card 10
>   of [[ISS-017-twelve-candidate-capabilities-undefined]], "insurance claim
>   handling", was absorbed into settlement that morning. Under "protect both" it
>   belongs here, and the money half stays there. The two epics meet at
>   [[FR-012-settle-a-loss-claim-on-a-sold-piece]].
> - **No source describes condition recording**, which the goal's metric assumes.
> - **Insurance is fixed per whole tour**, one insurer, with insured values set
>   in lending agreements. Whether cover is really per piece or per tour changes
>   this epic's shape and no source says.

## History

> Created 2026-09-09 from the artist and buyer protection cards in
> [[SRC-010-workshop-example-mapping-stories]], on Gernot Starke's "we need to
> protect both".
