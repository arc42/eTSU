---
id: FR-007
type: functional-requirement
title: Settlement and Compliance
status: draft
created: 2026-09-09
updated: 2026-09-09
sources:
  - "[[SRC-005-workshop-capability-card-wall]]"
  - "[[SRC-008-sandra-mayer-beneficiary-stories]]"
related:
  - "[[FR-002-settle-finances-and-legal-obligations]]"
  - "[[FR-008-collect-the-purchase-deposit]]"
  - "[[FR-009-collect-the-purchase-balance]]"
  - "[[FR-010-settle-a-failed-purchase]]"
  - "[[FR-011-pay-artist-commission]]"
  - "[[FR-012-settle-a-loss-claim-on-a-sold-piece]]"
  - "[[GOAL-006-settlement-correct-and-on-time]]"
  - "[[GLO-020-commission]]"
  - "[[GLO-019-agreed-price]]"
  - "[[GLO-022-intent-to-purchase]]"
  - "[[GLO-023-the-insult]]"
  - "[[GLO-021-lending-agreement]]"
  - "[[GLO-010-aml-screening]]"
  - "[[STK-001-gus-renoir]]"
  - "[[STK-010-legal-and-accounting]]"
  - "[[ISS-017-twelve-candidate-capabilities-undefined]]"
  - "[[ISS-022-tsu-brief-only-partially-ingested]]"
  - "[[GOAL-006-settlement-correct-and-on-time]]"
  - "[[ISS-023-sandra-stories-lack-benefit-and-criteria]]"
  - "[[FR-014-contract-management]]"
tags: [functional-requirement]
stereotype: epic
parent: []
priority: Should
release: backlog
lane: backbone
order: 30
goal:
  - "[[GOAL-006-settlement-correct-and-on-time]]"
---

# Settlement and Compliance

## Epic: Summary

For [[STK-001-gus-renoir|Head Office]] and
[[STK-010-legal-and-accounting|accounting]], **every obligation that a sale or a
loan creates**, executed for the right amount, to the right party, on time.

**PROBLEM / GOAL**

The money rules are precise, dated and currently tracked by hand: a deposit due
in 24 hours with a weekend exception, a balance in 14 days,
[[GLO-020-commission|commission]] split across two clocks,
[[GLO-023-the-insult|The Insult]] on default, and a refund rule if a sold piece
is lost while still on tour. Each is an amount that can be computed wrongly and a
deadline that can pass unnoticed.

**Success metric(s).**

Inherited from [[GOAL-006-settlement-correct-and-on-time]]: share of payment
obligations settled within their contractual deadline.

**Scope.** in: payment obligations and their deadlines, commission settlement,
contract and lending-agreement obligations, tax and
[[GLO-010-aml-screening|AML screening]] duties · out: pricing decisions, and the
purchase ceremony itself.

## Hierarchy

- **Parent:** none. This is a top-level epic.
- **Children:** [[FR-008-collect-the-purchase-deposit]],
  [[FR-009-collect-the-purchase-balance]], [[FR-010-settle-a-failed-purchase]],
  [[FR-011-pay-artist-commission]],
  [[FR-012-settle-a-loss-claim-on-a-sold-piece]].
  [[FR-002-settle-finances-and-legal-obligations]] was **retired** into these
  five on 2026-09-09.

> [!note] Open points
> - **Created to give the story a parent**, 2026-09-09, at Gernot Starke's
>   request. It absorbs **card 8, *payment handling***, of the twelve in
>   [[ISS-017-twelve-candidate-capabilities-undefined]].
> - **It briefly absorbed two more and gave them back the same day.**
>   *contract handling* went to [[FR-014-contract-management]], because the
>   workshop drew Contract Management as a capability of its own and contracts
>   run through lenders, insurers and shippers as well as money.
>   *insurance claim handling* went to [[FR-016-piece-protection]] under Gernot
>   Starke's "we need to protect both". The two epics meet at
>   [[FR-012-settle-a-loss-claim-on-a-sold-piece]], which stays here because it
>   is about money.
> - **The finance half is covered; contracts have moved out; tax and AML remain
>   uncovered.** All five children are money rules from [[SRC-007-tsu-brief]],
>   which states them precisely enough to write criteria against. Contracts now
>   have [[FR-014-contract-management]] and [[FR-026-sign-the-artist-contract]].
>   **Tax and [[GLO-010-aml-screening|AML screening]] still have no story**,
>   because no source states a rule for them — the brief mentions the formal artist contract and
>   the lending agreements only in passing, and tax and AML come from a workshop
>   diagram box rather than from any rule. That gap is real and unfiled.
> - **Two open money questions surfaced during the split**, both on
>   [[FR-012-settle-a-loss-claim-on-a-sold-piece]]: whether the *second* half of
>   the commission is still owed after a loss, and what happens when a piece is
>   lost before the buyer has paid in full.
> - **Compliance may not belong with settlement.** AML screening and tax are
>   grouped here because both are obligations with deadlines, which is an agent's
>   judgment, not anyone's decision.

## History

> Created 2026-09-09 to resolve the orphaned-requirements finding on the
> dashboard backlog page, alongside
> [[GOAL-006-settlement-correct-and-on-time]], which had no epic to serve it.
