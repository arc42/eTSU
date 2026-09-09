---
id: GOAL-005
type: goal
title: Real-time visibility of every piece on tour
status: draft
created: 2026-09-09
updated: 2026-09-09
sources:
  - "[[SRC-002-georg-mayrhauser-vision-goals-stakeholders]]"
related:
  - "[[GOAL-001-eTSU-vision]]"
  - "[[GOAL-002-global-market-expansion]]"
  - "[[GOAL-003-operational-excellence]]"
  - "[[ISS-009-real-time-metric-untestable]]"
tags: [goal]
stereotype: objective
parent:
  - "[[GOAL-001-eTSU-vision]]"
beneficiary:
  - "[[STK-001-gus-renoir]]"
  - "[[STK-003-gallery-manager]]"
  - "[[STK-002-artist]]"
  - "[[STK-004-buyer]]"
metric: staleness of a piece's location, sale status and current price
baseline: not measured
target: "\"real time\" — not yet quantified, see [[ISS-009-real-time-metric-untestable]]"
horizon:
short_title: Real-time visibility
tile_claim:
---

# Real-time visibility of every piece on tour

## Objective   > follows [[PAM]]; promotes to [[SMART]] once `horizon` is set

- **Purpose.** Enable frictionless showing and selling of art globally.
- **Advantage.** Anyone with a stake in a [[GLO-001-tour|Tour]] gets an instant
  overview of shows, artworks and the state of each sale, instead of phoning the
  gallery holding the piece.
- **Metric.** For any piece: where it is currently shown, whether it is sold, and
  its current price — all reflected without perceptible delay.

**Parent.** [[GOAL-001-eTSU-vision]].

## Impact

- **Addressed stakeholders:** see `beneficiary:`.
- **Served by:** projected from **FR backlinks** (ADR-0018) — none captured yet.

> [!note] Open points
> - **The metric is not testable as stated.** "Real time" carries no number.
>   A latency budget (e.g. "price change visible in every gallery within 5 s")
>   would make this [[SMART]]. See [[ISS-009-real-time-metric-untestable]].
> - `horizon:` is empty — this stays [[PAM]] rather than [[SMART]] until the
>   group sets one.
> - The purpose overlaps [[GOAL-002-global-market-expansion]] ("globally") and
>   the advantage overlaps [[GOAL-003-operational-excellence]] ("instant overview
>   of selling processes"). These arrived from two different authors on the same
>   day and have not been reconciled — also tracked in
>   [[ISS-009-real-time-metric-untestable]].
