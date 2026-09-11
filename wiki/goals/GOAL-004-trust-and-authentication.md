---
id: GOAL-004
type: goal
title: Authenticated provenance as a market differentiator
status: draft
created: 2026-09-09
updated: 2026-09-09
sources:
  - "[[SRC-001-ulrich-stuerzlinger-goals-and-newspaper]]"
related:
  - "[[GOAL-001-eTSU-vision]]"
  - "[[GLO-003-provenance]]"
  - "[[ISS-002-unsourced-objective-baselines]]"
  - "[[ISS-003-year-one-vs-2029-target-divergence]]"
  - "[[ISS-004-scope-inflation-marketplace-vs-back-office]]"
  - "[[EIF-003-appraisers-and-authenticators]]"
  - "[[EIF-005-fraud-and-security-prevention]]"
  - "[[EIF-010-institutional-buyers]]"
  - "[[EIF-014-regulatory-and-compliance]]"
  - "[[GLO-007-appraiser]]"
  - "[[GLO-010-aml-screening]]"
  - "[[ISS-017-twelve-candidate-capabilities-undefined]]"
  - "[[ISS-021-authentication-card-ambiguous]]"
  - "[[STK-002-artist]]"
  - "[[STK-004-buyer]]"
  - "[[STK-007-customs-authority]]"
  - "[[STK-008-museum]]"
  - "[[STK-010-legal-and-accounting]]"
  - "[[STK-014-art-collector]]"
tags: [goal]
stereotype: objective
parent:
  - "[[GOAL-001-eTSU-vision]]"
beneficiary:
  - "[[STK-004-buyer]]"
  - "[[STK-008-museum]]"
  - "[[STK-002-artist]]"
metric: share of catalogue pieces with verified provenance
baseline: not measured
target: ≥ 90%
horizon: Year 1
short_title: Trust & authentication
tile_claim:
---

# Authenticated provenance as a market differentiator

## Objective   > follows [[PAM]]; promotes to [[SMART]] once `horizon` is set

- **Purpose.** Treat authentication and fraud prevention as something eTSU
  competes on, not as a compliance chore bolted on afterwards.
- **Advantage.** Verified pieces sell at a 10–15% premium; as art-market
  regulation tightens, the compliance capability becomes a moat rather than a
  cost; institutional buyers — [[STK-008-museum|museums]] above all — will only
  transact where [[GLO-003-provenance|provenance]] is documented.
- **Metric.** Provenance verification coverage — see `metric:` / `target:` / `horizon:`.

**Secondary indicators.** Fraud rate < 0.5%; zero regulatory compliance incidents.

**Five-year ambition** (September 2029 narrative): 99% verification coverage via
blockchain integration with the Art Loss Register and Interpol databases; a
sustained 12–15% price premium; museums at 30% of transaction volume; eTSU
endorsed as a model across 47 jurisdictions.

**Parent.** [[GOAL-001-eTSU-vision]].

## Impact

- **Addressed stakeholders:** see `beneficiary:`.
- **Served by:** projected from **FR backlinks** (ADR-0018) — none captured yet.

> [!note] Open points
> - `baseline: not measured` — no source states today's verification coverage.
> - "Zero regulatory compliance incidents" is an absolute with no named
>   regulation behind it. Which jurisdictions and which rules (AML, KYC, cultural
>   property export) actually bind TSU? Untestable until named.
> - Blockchain, the Art Loss Register and Interpol are named as *solutions* in a
>   goal. Kept here as quoted ambition only; if the group commits to them they
>   belong in [[ISS-004-scope-inflation-marketplace-vs-back-office|Constraints]],
>   not in the goal space (ADR-0016 keeps goals out of the solution space).
