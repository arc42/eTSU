---
id: FR-001
type: functional-requirement
title: View piece inventory and status
status: deprecated
created: 2026-09-09
updated: 2026-09-09
sources:
  - "[[SRC-008-sandra-mayer-beneficiary-stories]]"
  - "[[SRC-009-workshop-inventory-decomposition]]"
related:
  - "[[STK-001-gus-renoir]]"
  - "[[GLO-011-piece]]"
  - "[[GLO-002-show]]"
  - "[[GLO-006-conservator]]"
  - "[[GLO-013-buyer]]"
  - "[[ISS-023-sandra-stories-lack-benefit-and-criteria]]"
  - "[[ISS-024-close-out-timing-show-versus-tour]]"
  - "[[ISS-009-real-time-metric-untestable]]"
  - "[[FR-006-tour-visibility]]"
  - "[[FR-017-artwork-inventory]]"
  - "[[FR-018-artwork-tracking]]"
  - "[[FR-004-track-piece-status]]"
tags: [functional-requirement]
stereotype: story
parent:
  - "[[FR-006-tour-visibility]]"
priority: Should
release: backlog
lane: backbone
order: 10
goal:
  - "[[GOAL-005-frictionless-global-art-trade]]"
---

# View piece inventory and status

> [!warning] Retired 2026-09-09 — decomposed into two features
> The workshop wrote this card verbatim at the head of a decomposition table
> ([[SRC-009-workshop-inventory-decomposition]]) and hung nine operations off it
> in two groups. It was therefore being used as an **epic-level** statement, and
> it says the same thing as [[FR-006-tour-visibility]] above it. Replaced by
> [[FR-017-artwork-inventory]] and [[FR-018-artwork-tracking]] and their six
> stories. Kept, not deleted, so Sandra Mayer's original wording stays readable.
>
> **This was the agent's call.** It was put to Gernot Starke as question 1 of a
> grill round and he did not answer it.

## Story

As [[STK-001-gus-renoir]] **the business owner** I want **an overview of the
inventory and the status of each [[GLO-011-piece|piece]]**, so that **&lt;benefit
not stated&gt;**.

> [!assumption] No benefit clause in the source
> The story arrived as "As Gus I want an overview of an inventory and status of
> each item" and stops there. The "so that" is deliberately left empty rather
> than invented — [[ISS-023-sandra-stories-lack-benefit-and-criteria]].

**Acceptance criteria.** *None given.* The source states no observable outcome,
so this story is not yet testable ([[user-story-format]], [[INVEST]]).

- **Given** … **when** … **then** …

**Context — what "status" has to cover.** The same email supplies an unfinished
close-out event that shows what states a piece moves through:

> **Event: When the exhibition ends**
> - Send art to cleaners and restorers
> - Check what art can be sent to buyers
> - …

Read with the rest of the wiki, that implies at least: on display, sold but still
touring, awaiting conservation ([[GLO-006-conservator]]), and releasable to a
[[GLO-013-buyer|buyer]]. The list ends in an ellipsis in the source, so it is
incomplete by the sender's own admission.

**When the event fires is contested.** Gernot Starke read "exhibition" as
[[GLO-002-show|Show]], one gallery stop. The brief puts both actions at **tour**
close instead. That conflict is real and is carried in
[[ISS-024-close-out-timing-show-versus-tour]], not resolved here.

## Hierarchy

- **Parent:** [[FR-006-tour-visibility]].
- **Children:** none.

> [!note] Open points
> - `priority: Should` is the template default. **Nobody has prioritised this**
>   under [[MoSCoW]].
> - The source says "item"; this wiki says [[GLO-011-piece|piece]].
> - Serves [[GOAL-005-frictionless-global-art-trade]], whose "real time"
>   metric is itself untestable — [[ISS-009-real-time-metric-untestable]].
> - A `goal:` link to [[GOAL-003-operational-excellence]] was **removed** on
>   2026-09-09: that objective measures tour *setup* lead time, which an
>   inventory view cannot move.

## History

> Transcribed 2026-09-09 from [[SRC-008-sandra-mayer-beneficiary-stories]],
> subject "Beneficiary stories". Wording normalised to the ubiquitous language
> (item → piece); nothing else added.
