---
id: FR-002
type: functional-requirement
title: Settle finances and legal obligations
status: deprecated
created: 2026-09-09
updated: 2026-09-09
sources:
  - "[[SRC-008-sandra-mayer-beneficiary-stories]]"
related:
  - "[[STK-001-gus-renoir]]"
  - "[[STK-010-legal-and-accounting]]"
  - "[[GLO-020-commission]]"
  - "[[GLO-021-lending-agreement]]"
  - "[[GLO-019-agreed-price]]"
  - "[[ISS-023-sandra-stories-lack-benefit-and-criteria]]"
  - "[[ISS-022-tsu-brief-only-partially-ingested]]"
  - "[[FR-007-settlement-and-compliance]]"
  - "[[GOAL-006-settlement-correct-and-on-time]]"
  - "[[FR-008-collect-the-purchase-deposit]]"
  - "[[FR-009-collect-the-purchase-balance]]"
  - "[[FR-010-settle-a-failed-purchase]]"
  - "[[FR-011-pay-artist-commission]]"
  - "[[FR-012-settle-a-loss-claim-on-a-sold-piece]]"
tags: [functional-requirement]
stereotype: story
parent:
  - "[[FR-007-settlement-and-compliance]]"
priority: Should
release: backlog
lane: backbone
order: 20
goal:
  - "[[GOAL-006-settlement-correct-and-on-time]]"
---

# Settle finances and legal obligations

> [!warning] Retired 2026-09-09 — split into five stories
> Split on Gernot Starke's instruction into [[FR-008-collect-the-purchase-deposit]], [[FR-009-collect-the-purchase-balance]],
[[FR-010-settle-a-failed-purchase]], [[FR-011-pay-artist-commission]] and
[[FR-012-settle-a-loss-claim-on-a-sold-piece]],
> all under [[FR-007-settlement-and-compliance]]. This page is kept, not deleted,
> so the story as Sandra Mayer wrote it stays readable and the split is
> traceable. **Nothing should be planned from it.**
>
> **The "legals" half did not survive the split.** All five successors are money
> rules from the brief. Contracts, tax and AML screening had no rule to write a
> criterion against, so no story covers them — recorded on
> [[FR-007-settlement-and-compliance]].

## Story

As [[STK-001-gus-renoir]] **the business owner** I want **finances and legal
matters taken care of**, so that **&lt;benefit not stated&gt;**.

> [!assumption] No benefit clause in the source
> Arrived as "As Gus I want finances and legals taken care of" and stops there —
> [[ISS-023-sandra-stories-lack-benefit-and-criteria]].

**Acceptance criteria.** *None given, and none can be written as the story
stands.*

- **Given** … **when** … **then** …

**This is the weakest of the four, and it is worth saying why.** "Finances and
legals taken care of" names an entire department, not a capability. It fails
[[INVEST]] on **Small** and **Estimable** outright: nothing bounds it, so no two
readers would size it the same way. Kept as written rather than silently split,
because splitting it is a decision the group has not made.

The brief already supplies the material any split would draw on, none of which
is ingested yet ([[ISS-022-tsu-brief-only-partially-ingested]]):
[[GLO-020-commission|commission]] settlement in two halves on two clocks, the
[[GLO-019-agreed-price|agreed price]] and its deposit-and-balance sequence,
[[GLO-021-lending-agreement|lending agreements]], and the tax and compliance
work owned by [[STK-010-legal-and-accounting]].

## Hierarchy

- **Parent:** [[FR-007-settlement-and-compliance]] — which now largely
  duplicates it, because this story is itself epic-sized.
- **Children:** none.

> [!note] Open points
> - **Wrong altitude, and now visibly so.** This story is epic-sized, and its
>   parent [[FR-007-settlement-and-compliance]] says nearly the same thing one
>   level up. The likely correction is to split this into real stories under that
>   epic and retire this page —
>   [[ISS-023-sandra-stories-lack-benefit-and-criteria]].
> - A `goal:` link to [[GOAL-003-operational-excellence]] was **removed** on
>   2026-09-09; settlement does not move tour setup lead time.
>   [[GOAL-006-settlement-correct-and-on-time]] was written for it instead.
> - `priority: Should` is the template default; nobody has prioritised it.

## History

> Transcribed 2026-09-09 from [[SRC-008-sandra-mayer-beneficiary-stories]].
> Title given verb-first per [[0015-backlog-naming-convention|ADR-0015]]; the
> source phrasing was "finances and legals taken care of".
