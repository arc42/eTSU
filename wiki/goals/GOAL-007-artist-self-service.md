---
id: GOAL-007
type: goal
title: Artists maintain and follow their own work
status: draft
created: 2026-09-09
updated: 2026-09-09
sources:
  - "[[SRC-008-sandra-mayer-beneficiary-stories]]"
related:
  - "[[GOAL-001-eTSU-vision]]"
  - "[[GOAL-002-global-market-expansion]]"
  - "[[GOAL-003-operational-excellence]]"
  - "[[GOAL-005-frictionless-global-art-trade]]"
  - "[[FR-003-upload-piece-information]]"
  - "[[FR-004-track-piece-status]]"
  - "[[FR-005-piece-management]]"
  - "[[FR-006-tour-visibility]]"
  - "[[GLO-012-artist]]"
  - "[[GLO-011-piece]]"
  - "[[GLO-020-commission]]"
  - "[[STK-002-artist]]"
  - "[[EIF-001-artists]]"
  - "[[ISS-004-scope-inflation-marketplace-vs-back-office]]"
  - "[[DM-004-artist]]"
  - "[[FR-013-artist-management]]"
  - "[[FR-025-register-as-an-artist]]"
tags: [goal]
stereotype: objective
parent:
  - "[[GOAL-001-eTSU-vision]]"
beneficiary:
  - "[[STK-002-artist]]"
metric: share of catalogue pieces whose information was supplied by the artist
baseline: 0% (no artist-facing surface exists today)
target: "60%"
horizon: Year 1
short_title: Artist self-service
tile_claim:
---

# Artists maintain and follow their own work

## Objective   > follows [[PAM]]; promotes to [[SMART]] once `horizon` is set

- **Purpose.** [[GLO-012-artist|Artists]] describe their own
  [[GLO-011-piece|pieces]] and follow what happens to them, directly, instead of
  through Head Office.
- **Advantage.** Head Office stops being the data-entry bottleneck on the tour
  setup path, the catalogue is richer and earlier because the person who made the
  work wrote the entry, and the artist can see when a piece sold and therefore
  when the [[GLO-020-commission|commission]] falls due.
- **Metric.** Share of catalogue pieces whose information was supplied by the
  artist — see `metric:` / `baseline:` / `target:` / `horizon:`.

**Why this needs its own objective.** Every source before
[[SRC-008-sandra-mayer-beneficiary-stories]] puts artists on the far side of a
negotiation: TSU agrees terms *with* them, and the card wall's "Artist
Management" means TSU managing artists. Two of Sandra Mayer's stories reverse
that direction and make the artist a **user**. No existing objective measures
anything an artist does, and [[GOAL-002-global-market-expansion]] names artists
as beneficiaries only through buyers reaching them.

**Parent.** [[GOAL-001-eTSU-vision]].

## Impact

- **Addressed stakeholders:** see `beneficiary:`.
- **Served by:** projected from **FR backlinks** (ADR-0018) —
  [[FR-005-piece-management]], [[FR-006-tour-visibility]],
  [[FR-003-upload-piece-information]], [[FR-004-track-piece-status]].

> [!note] Open points
> - **Proposed by the agent on 2026-09-09**, at Gernot Starke's request. Derived
>   from two stories, **not from any stated goal**, and not confirmed with Gus
>   Renoir's team.
> - **This is a scope commitment, and it should be read as one.** An objective
>   naming artists as users of eTSU is the first goal-level statement that eTSU
>   has a surface outside Head Office and the galleries. It leans towards
>   Reading B of [[ISS-004-scope-inflation-marketplace-vs-back-office]]. If the
>   group settles on the back-office reading, this objective should be withdrawn
>   rather than quietly narrowed.
> - **`target: 60%` is a placeholder** with no reasoning behind it. So is the
>   Year-1 horizon.
> - The metric measures **supply** of information, not the quality of it. An
>   artist filling in a form badly still counts. A second indicator on
>   completeness may be needed.
