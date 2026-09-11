---
id: FR-014
type: functional-requirement
title: Contract Management
status: draft
created: 2026-09-09
updated: 2026-09-09
sources:
  - "[[SRC-009-workshop-inventory-decomposition]]"
  - "[[SRC-010-workshop-example-mapping-stories]]"
  - "[[SRC-005-workshop-capability-card-wall]]"
related:
  - "[[FR-026-sign-the-artist-contract]]"
  - "[[FR-007-settlement-and-compliance]]"
  - "[[GOAL-003-operational-excellence]]"
  - "[[GLO-021-lending-agreement]]"
  - "[[GLO-017-minimum-sale-price]]"
  - "[[GLO-020-commission]]"
  - "[[STK-010-legal-and-accounting]]"
  - "[[STK-002-artist]]"
  - "[[ISS-017-twelve-candidate-capabilities-undefined]]"
tags: [functional-requirement]
stereotype: epic
parent: []
priority: Should
release: backlog
lane: backbone
order: 50
goal:
  - "[[GOAL-003-operational-excellence]]"
---

# Contract Management

## Epic: Summary

For [[STK-001-gus-renoir|Head Office]] and
[[STK-010-legal-and-accounting|legal]], **every instrument a tour is built on**,
from first agreement to signature.

**PROBLEM / GOAL**

A tour is a stack of contracts negotiated in a fixed order, and the tour is not a
"Go" until they all hold: terms with the [[GLO-012-artist|artist]] (which pieces
travel, the [[GLO-020-commission|commission]] percentage, the two price floors),
then [[GLO-021-lending-agreement|lending agreements]] with owners and museums,
then the formal artist contract, then shipping and insurance for the whole tour.
Four instruments, four counterparties, four moments.

**Success metric(s).** Inherited from
[[GOAL-003-operational-excellence]]: tour setup lead time, currently 3–4 weeks
against a target of one week. Contracts are most of that elapsed time.

**Scope.** in: contract content, sequence, parties and signature · out: the money
those contracts later oblige ([[FR-007-settlement-and-compliance]]).

## Hierarchy

- **Parent:** none.
- **Children:** [[FR-026-sign-the-artist-contract]].

> [!note] Open points
> - **Moved out of [[FR-007-settlement-and-compliance]] on 2026-09-09.** Card 7
>   of [[ISS-017-twelve-candidate-capabilities-undefined]], "contract handling",
>   was absorbed into the settlement epic that morning; the workshop's own
>   **Contract Management** card says it is a capability in its own right, and
>   contracts run through artists, lenders, insurers and shippers rather than
>   only through money.
> - **Only the artist contract has a story.** Lending agreements, the shipping
>   and insurance arrangement, and anything about amendment or termination have
>   none.

## History

> Created 2026-09-09 from the green **Contract Management** capability card in
> [[SRC-009-workshop-inventory-decomposition]] and the TSU contract story in
> [[SRC-010-workshop-example-mapping-stories]]. This also closes the *contract*
> part of the legals gap left by the [[FR-002-settle-finances-and-legal-obligations]]
> split; tax and AML screening remain uncovered.
