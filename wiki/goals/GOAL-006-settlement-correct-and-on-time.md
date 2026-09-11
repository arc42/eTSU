---
id: GOAL-006
type: goal
title: Settlement that is correct and on time
status: draft
created: 2026-09-09
updated: 2026-09-09
sources:
  - "[[SRC-007-tsu-brief]]"
  - "[[SRC-008-sandra-mayer-beneficiary-stories]]"
related:
  - "[[GOAL-001-eTSU-vision]]"
  - "[[GOAL-003-operational-excellence]]"
  - "[[FR-008-collect-the-purchase-deposit]]"
  - "[[FR-009-collect-the-purchase-balance]]"
  - "[[FR-010-settle-a-failed-purchase]]"
  - "[[FR-011-pay-artist-commission]]"
  - "[[FR-012-settle-a-loss-claim-on-a-sold-piece]]"
  - "[[FR-007-settlement-and-compliance]]"
  - "[[GLO-020-commission]]"
  - "[[GLO-019-agreed-price]]"
  - "[[GLO-022-intent-to-purchase]]"
  - "[[GLO-023-the-insult]]"
  - "[[GLO-021-lending-agreement]]"
  - "[[STK-001-gus-renoir]]"
  - "[[STK-002-artist]]"
  - "[[STK-004-buyer]]"
  - "[[STK-010-legal-and-accounting]]"
  - "[[ISS-022-tsu-brief-only-partially-ingested]]"
  - "[[FR-002-settle-finances-and-legal-obligations]]"
  - "[[DM-010-intent-to-purchase]]"
  - "[[GOAL-008-pieces-come-home-intact]]"
tags: [goal]
stereotype: objective
parent:
  - "[[GOAL-001-eTSU-vision]]"
beneficiary:
  - "[[STK-001-gus-renoir]]"
  - "[[STK-002-artist]]"
  - "[[STK-010-legal-and-accounting]]"
metric: share of payment obligations settled within their contractual deadline
baseline: not measured
target: "≥ 99%"
horizon: Year 1
short_title: Settlement accuracy
tile_claim:
---

# Settlement that is correct and on time

## Objective   > follows [[PAM]]; promotes to [[SMART]] once `horizon` is set

- **Purpose.** Every money obligation a sale or a loan creates is executed for
  the right amount, to the right party, before its deadline, without anyone
  holding the schedule in their head.
- **Advantage.** The obligations are unforgiving and dated, and the business
  currently tracks them manually. An artist paid late is a relationship lost;
  a deposit deadline missed by TSU rather than by the
  [[STK-004-buyer|buyer]] is money the business cannot claim; a lending
  obligation missed is a lender who does not lend again.
- **Metric.** Share of payment obligations settled within their contractual
  deadline — see `metric:` / `baseline:` / `target:` / `horizon:`.

**Why this needs its own objective.** Four obligations run on four different
clocks, and no existing goal measures whether any of them is met:

| Obligation | Deadline | Source |
|---|---|---|
| Buyer deposit, 10% of the [[GLO-019-agreed-price\|agreed price]] | 24 h from signing, Monday if signed Friday or Saturday | [[SRC-007-tsu-brief]] |
| Buyer balance, the remaining 90% | 14 days from signing, any weekday | [[SRC-007-tsu-brief]] |
| First half of the [[GLO-020-commission\|commission]] | on receipt of full payment | [[SRC-007-tsu-brief]] |
| Second half of the commission | 5 days after tour close | [[SRC-007-tsu-brief]] |

Two further cases are settlement rather than sales.
[[GLO-023-the-insult|The Insult]] returns half the deposit to a failed buyer and
keeps half. And if a sold piece is lost while still on tour, the buyer is
refunded in full, the artist keeps the half-commission already paid, and TSU
absorbs that from the insurance payout. Every one of these is an amount that can
be computed wrongly.

**Parent.** [[GOAL-001-eTSU-vision]].

## Impact

- **Addressed stakeholders:** see `beneficiary:`.
- **Served by:** projected from **FR backlinks** (ADR-0018) —
  [[FR-007-settlement-and-compliance]] and its five stories:
  [[FR-008-collect-the-purchase-deposit]], [[FR-009-collect-the-purchase-balance]],
  [[FR-010-settle-a-failed-purchase]], [[FR-011-pay-artist-commission]],
  [[FR-012-settle-a-loss-claim-on-a-sold-piece]].

> [!note] Open points
> - **Proposed by the agent on 2026-09-09**, at Gernot Starke's request, because
>   [[FR-002-settle-finances-and-legal-obligations]] had no goal that its metric
>   could serve. Not from any source, and **not yet confirmed with Gus Renoir's
>   team.**
> - **The baseline is unmeasured**, like every other objective here —
>   [[ISS-002-unsourced-objective-baselines]]. Unusually, this one is
>   *measurable in principle from historical records*, since the deadlines and
>   the payment dates both exist on paper today.
> - **`target: ≥ 99%` is a placeholder.** The honest target may be 100%, since
>   these are contractual deadlines rather than service levels. The group should
>   set it.
> - Distinguish from [[GOAL-003-operational-excellence]], which measures how fast
>   a tour is *set up*. This one measures whether money moves *correctly*, which
>   is a different outcome on a different part of the timeline.
