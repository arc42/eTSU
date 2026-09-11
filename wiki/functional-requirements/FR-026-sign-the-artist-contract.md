---
id: FR-026
type: functional-requirement
title: Sign the artist contract
status: draft
created: 2026-09-09
updated: 2026-09-09
sources:
  - "[[SRC-010-workshop-example-mapping-stories]]"
  - "[[SRC-007-tsu-brief]]"
related:
  - "[[FR-014-contract-management]]"
  - "[[GOAL-003-operational-excellence]]"
  - "[[GLO-012-artist]]"
  - "[[GLO-020-commission]]"
  - "[[GLO-017-minimum-sale-price]]"
  - "[[GLO-018-minimum-museum-sale-price]]"
  - "[[GLO-011-piece]]"
  - "[[STK-001-gus-renoir]]"
  - "[[STK-010-legal-and-accounting]]"
tags: [functional-requirement]
stereotype: story
parent:
  - "[[FR-014-contract-management]]"
priority: Should
release: backlog
lane: backbone
order: 108
goal:
  - "[[GOAL-003-operational-excellence]]"
---

# Sign the artist contract

## Story

As [[STK-001-gus-renoir]] **TSU** I want **to sign a contract with the
[[GLO-012-artist|artist]]**, so that **legal obligations, terms and conditions
are accepted and agreed between all parties**.

**Acceptance criteria.** Partly derivable, because
[[SRC-007-tsu-brief]] states what the contract has to settle first.

- **Given** a tour concept, **when** the contract is prepared, **then** it names
  which [[GLO-011-piece|pieces]] travel, the [[GLO-020-commission|commission]]
  percentage, the [[GLO-017-minimum-sale-price|minimum sale price]] per piece and
  the [[GLO-018-minimum-museum-sale-price|minimum museum sale price]] per piece.
- **Given** those four terms are agreed **and** lending agreements are in place,
  **when** the formal contract is signed, **then** the tour counts as a "Go".

**Sequence matters and the brief is explicit about it.** Artist terms come first,
lending agreements second, and only then the formal contract, "because we know
that the tour is a Go". A system that lets the contract be signed first would
invert the business.

## Hierarchy

- **Parent:** [[FR-014-contract-management]].

> [!note] Open points
> - **"All parties" is undefined.** The artist contract is bilateral; lenders,
>   insurers and shippers sign separate instruments.
> - **Signature is not modelled.** Wet ink, e-signature, or a record that
>   somebody signed elsewhere.

## History

> Transcribed 2026-09-09 from [[SRC-010-workshop-example-mapping-stories]];
> criteria added from [[SRC-007-tsu-brief]]. Together with
> [[FR-014-contract-management]] this closes the *contract* part of the legals
> gap left when [[FR-002-settle-finances-and-legal-obligations]] was split.
