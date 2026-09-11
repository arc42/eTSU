---
id: FR-005
type: functional-requirement
title: Piece Management
status: draft
created: 2026-09-09
updated: 2026-09-09
sources:
  - "[[SRC-005-workshop-capability-card-wall]]"
  - "[[SRC-008-sandra-mayer-beneficiary-stories]]"
related:
  - "[[FR-003-upload-piece-information]]"
  - "[[GLO-011-piece]]"
  - "[[GLO-012-artist]]"
  - "[[GLO-003-provenance]]"
  - "[[STK-002-artist]]"
  - "[[ISS-017-twelve-candidate-capabilities-undefined]]"
  - "[[ISS-023-sandra-stories-lack-benefit-and-criteria]]"
  - "[[GOAL-007-artist-self-service]]"
tags: [functional-requirement]
stereotype: epic
parent: []
priority: Should
release: backlog
lane: backbone
order: 10
goal:
  - "[[GOAL-007-artist-self-service]]"
  - "[[GOAL-004-trust-and-authentication]]"
---

# Piece Management

## Epic: Summary

For [[STK-002-artist|artists]] and Head Office, **the record of every
[[GLO-011-piece|piece]]** — what it is, who made it, what documents back it, and
who may change any of that.

**PROBLEM / GOAL**

A [[GLO-001-tour|Tour]] cannot be assembled, priced, insured or verified without
a trustworthy record of each piece. Today that record is assembled by Head Office
from whatever the artist sends, which makes Head Office the bottleneck and the
single point of transcription error.

**Success metric(s).**

Inherited from [[GOAL-007-artist-self-service]]: share of catalogue pieces whose
information was supplied by the artist. Provenance completeness is measured by
[[GOAL-004-trust-and-authentication]] instead.

**Scope.** in: the piece record, who supplies it, who may amend it, and the
documents attached to it · out: status while on tour (that is
[[FR-006-tour-visibility]]), and anything to do with price or money.

## Hierarchy

- **Parent:** none. This is a top-level epic.
- **Children:** [[FR-003-upload-piece-information]].

> [!note] Open points
> - **This epic was created to give the stories a parent**, on 2026-09-09 at
>   Gernot Starke's request, not because anyone specified it. It corresponds to
>   the card-wall capability **"Artwork Management"**, card 2 of the twelve held
>   in [[ISS-017-twelve-candidate-capabilities-undefined]] — that Issue stays
>   open for the other eleven.
> - **Named in the ubiquitous language.** The card says *Artwork*; this wiki says
>   [[GLO-011-piece|Piece]], of which *artwork* is a recorded alias.
> - One child only. Thin for an epic, and it will stay thin until the brief is
>   ingested — [[ISS-022-tsu-brief-only-partially-ingested]].

## History

> Created 2026-09-09 to resolve the orphaned-requirements finding on the
> dashboard backlog page. Derived from the card wall plus
> [[FR-003-upload-piece-information]]; no source describes it directly.
