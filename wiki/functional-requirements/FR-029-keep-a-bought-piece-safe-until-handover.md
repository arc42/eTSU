---
id: FR-029
type: functional-requirement
title: Keep a bought piece safe until handover
status: draft
created: 2026-09-09
updated: 2026-09-09
sources:
  - "[[SRC-010-workshop-example-mapping-stories]]"
related:
  - "[[FR-016-piece-protection]]"
  - "[[FR-012-settle-a-loss-claim-on-a-sold-piece]]"
  - "[[GOAL-008-pieces-come-home-intact]]"
  - "[[GLO-011-piece]]"
  - "[[GLO-001-tour]]"
  - "[[GLO-013-buyer]]"
  - "[[STK-004-buyer]]"
  - "[[ISS-024-close-out-timing-show-versus-tour]]"
tags: [functional-requirement]
stereotype: story
parent:
  - "[[FR-016-piece-protection]]"
priority: Should
release: backlog
lane: backbone
order: 111
goal:
  - "[[GOAL-008-pieces-come-home-intact]]"
---

# Keep a bought piece safe until handover

## Story

As [[STK-004-buyer]] **a buyer** I want **my bought
[[GLO-011-piece|piece]] to stay safe for the rest of the
[[GLO-001-tour|Tour]]**, so that **its value remains**.

**Acceptance criteria.** *None given.*

**This card is the buyer's side of the same gap.** A buyer pays in full and then
waits, sometimes for months, because the piece stays on tour until the tour
closes. During that wait TSU holds an object the buyer owns. The brief's only
provision for that period is a refund if something happens, which returns the
money and not the painting. The card says plainly that the buyer wants the
painting.

**"So that its value remains" is worth reading literally.** It is not only about
loss. A piece that tours for six months and arrives with a scuff is worth less
than the one that was bought, and no source addresses condition at handover.

## Hierarchy

- **Parent:** [[FR-016-piece-protection]].

> [!note] Open points
> - **Who bears the risk once a piece is paid for but not delivered?** Legally
>   this is custody, and no source names the answer.
> - **Handover timing is itself contested** —
>   [[ISS-024-close-out-timing-show-versus-tour]] holds whether release happens
>   at Show close or Tour close.
> - **Condition at handover is unmodelled**, which is exactly what
>   [[GOAL-008-pieces-come-home-intact]] measures.

## History

> Transcribed 2026-09-09 from [[SRC-010-workshop-example-mapping-stories]].
> Benefit clause supplied by the card.
