---
id: FR-028
type: functional-requirement
title: Insure a piece against damage
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
  - "[[GLO-021-lending-agreement]]"
  - "[[STK-002-artist]]"
  - "[[STK-006-insurer]]"
tags: [functional-requirement]
stereotype: story
parent:
  - "[[FR-016-piece-protection]]"
priority: Should
release: backlog
lane: backbone
order: 110
goal:
  - "[[GOAL-008-pieces-come-home-intact]]"
---

# Insure a piece against damage

## Story

As [[STK-002-artist]] **an artist** I want **my [[GLO-011-piece|piece]]
insured**, so that **I am compensated if it is damaged**.

**Acceptance criteria.** *None given, and none can be written yet* — the business
rule this asks for does not exist in any source.

**The brief covers a different case.** It handles a piece **already sold** and
then lost on tour: the buyer is refunded in full, the artist keeps the
half-commission already paid, and TSU absorbs that from the insurance payout
([[FR-012-settle-a-loss-claim-on-a-sold-piece]]). It says nothing about an
**unsold** piece of the artist's own being damaged, which is what this card asks
about, and in that case the artist has earned no commission to keep.

Two adjacent facts, neither of which answers it. Insurance is arranged **once per
whole tour** with a single insurer. Insured **values** are fixed in
[[GLO-021-lending-agreement|lending agreements]] — but a lending agreement covers
a *borrowed* piece, and an artist's own piece for sale is not borrowed.

## Hierarchy

- **Parent:** [[FR-016-piece-protection]].

> [!note] Open points
> - **Is an unsold piece insured at all, and for how much?** Nothing states it.
> - **Who is the beneficiary of a claim** on an unsold piece, the artist or TSU?
> - Gernot Starke settled the principle on 2026-09-09 — "we need to protect
>   both" — which makes this a requirement. The rule behind it still has to be
>   written by the business.

## History

> Transcribed 2026-09-09 from [[SRC-010-workshop-example-mapping-stories]].
> Benefit clause supplied by the card.
