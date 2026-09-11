---
id: GLO-002
type: glossary-term
title: Show
status: draft
created: 2026-09-06
updated: 2026-09-09
sources:
  - "[[SRC-007-tsu-brief]]"
  - "[[SRC-008-sandra-mayer-beneficiary-stories]]"
related:
  - "[[GLO-001-tour]]"
  - "[[EIF-011-gallery-operations]]"
  - "[[GLO-011-piece]]"
  - "[[GLO-015-gallery]]"
  - "[[GLO-019-agreed-price]]"
  - "[[ISS-019-visitors-is-an-undefined-actor]]"
  - "[[STK-003-gallery-manager]]"
  - "[[STK-007-customs-authority]]"
  - "[[ISS-024-close-out-timing-show-versus-tour]]"
  - "[[FR-001-view-piece-inventory-and-status]]"
  - "[[FR-006-tour-visibility]]"
  - "[[DM-002-show]]"
  - "[[FR-015-tour-scheduling]]"
  - "[[FR-023-modify-piece-location]]"
  - "[[FR-027-reserve-gallery-space-for-a-piece]]"
tags: [glossary]
aliases: [tour stop, exhibition]
bounded-context: Gallery Touring
agreed: false
stereotype: entity
---

# Show

**Definition.** One stop of a [[GLO-001-tour|Tour]] at a single gallery: the
period during which that tour's pieces are on display and for sale at that
gallery's location.

**In context.** Each Show has its own fixed price per piece for the duration
of the stop (the price may be re-set between Shows as the Tour moves), and
its own local customs paperwork and publicity lead time.

**Distinguish from.** [[GLO-001-tour|Tour]] — the Tour is the whole
multi-stop sequence; a Show is a single stop within it.

> [!note] Notes
> Captured verbatim from the brief ([[SRC-007-tsu-brief]]) — not yet confirmed
> (`agreed: false`). Easy to conflate with "Tour" in casual conversation;
> flagged here precisely because that confusion is likely in a workshop.

> [!warning] "Exhibition" resolves here, and that creates a contradiction
> Added as an alias on 2026-09-09 by decision of [[STK-001-gus-renoir]]:
> *exhibition* means one Show, not the whole Tour.
>
> That settles the word and immediately exposes a business-rule conflict.
> [[SRC-008-sandra-mayer-beneficiary-stories]] fires close-out "when the
> exhibition ends" — sending pieces to a [[GLO-006-conservator|conservator]] and
> releasing them to [[GLO-013-buyer|buyers]]. The brief puts **both** at
> [[GLO-001-tour|Tour]] close, and is explicit that a buyer may not take a piece
> until the tour is over. [[ISS-024-close-out-timing-show-versus-tour]] holds it;
> nothing is decided.
