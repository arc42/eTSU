---
id: GOAL-008
type: goal
title: Every piece comes home intact
status: draft
created: 2026-09-09
updated: 2026-09-09
sources:
  - "[[SRC-010-workshop-example-mapping-stories]]"
related:
  - "[[GOAL-001-eTSU-vision]]"
  - "[[GOAL-006-settlement-correct-and-on-time]]"
  - "[[FR-016-piece-protection]]"
  - "[[GLO-011-piece]]"
  - "[[GLO-021-lending-agreement]]"
  - "[[GLO-006-conservator]]"
  - "[[STK-002-artist]]"
  - "[[STK-004-buyer]]"
  - "[[STK-006-insurer]]"
  - "[[FR-028-insure-a-piece-against-damage]]"
  - "[[FR-029-keep-a-bought-piece-safe-until-handover]]"
tags: [goal]
stereotype: objective
parent:
  - "[[GOAL-001-eTSU-vision]]"
beneficiary:
  - "[[STK-002-artist]]"
  - "[[STK-004-buyer]]"
  - "[[STK-013-private-owner]]"
metric: share of pieces that complete a tour with no loss and no unrecorded condition change
baseline: not measured
target: "100% no loss; ≥ 98% no unrecorded condition change"
horizon: Year 1
short_title: Pieces intact
tile_claim:
---

# Every piece comes home intact

## Objective   > follows [[PAM]]; promotes to [[SMART]] once `horizon` is set

- **Purpose.** The physical [[GLO-011-piece|piece]] survives the tour, and its
  condition at every hand-over is recorded rather than remembered.
- **Advantage.** [[STK-002-artist|Artists]] and
  [[STK-004-buyer|buyers]] both said, in their own words, that they want the
  **work** protected. Money already has an objective. The object did not.
- **Metric.** Share of pieces completing a tour with no loss and no unrecorded
  condition change — see `metric:` / `baseline:` / `target:` / `horizon:`.

**Why the money objective does not already cover this.**
[[GOAL-006-settlement-correct-and-on-time]] makes people financially whole. Every
rule in the brief works that way: a lost piece means the buyer is refunded, the
artist keeps their half-commission, and TSU absorbs the difference from
insurance. Nobody is out of pocket, and the painting is still gone. Two cards in
[[SRC-010-workshop-example-mapping-stories]] ask for something the brief never
promises — that the artwork itself arrives safely — and Gernot Starke settled it
on 2026-09-09 with **"we need to protect both"**. This objective is the second
half of that pair.

It also has a lender edge. A [[GLO-021-lending-agreement|lending agreement]]
obliges TSU to return a borrowed piece, conserved by a
[[GLO-006-conservator|conservator]]. A refund does not discharge that.

**Parent.** [[GOAL-001-eTSU-vision]].

## Impact

- **Addressed stakeholders:** see `beneficiary:`.
- **Served by:** projected from **FR backlinks** (ADR-0018) —
  [[FR-016-piece-protection]] and its stories.

> [!note] Open points
> - **Written 2026-09-09 from Gernot Starke's "protect both".** The decision is
>   his; the metric, the target and the wording are the agent's and are confirmed
>   by nobody.
> - **"Unrecorded condition change" needs a definition.** It presumes condition
>   is recorded at hand-over, which no source describes today.
> - **The target is split across two numbers**, which breaks the one-indicator
>   rule these objectives follow. Loss and condition may need separating into two
>   objectives.
