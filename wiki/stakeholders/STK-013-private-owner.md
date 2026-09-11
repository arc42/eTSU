---
id: STK-013
type: stakeholder
title: Private owner
status: draft
created: 2026-09-09
updated: 2026-09-09
sources:
  - "[[SRC-004-ulrich-stuerzlinger-context-diagram]]"
related:
  - "[[EIF-002-museums-and-owners]]"
  - "[[STK-008-museum]]"
  - "[[STK-006-insurer]]"
  - "[[STK-009-conservator]]"
  - "[[GLO-001-tour]]"
  - "[[GLO-008-lender]]"
  - "[[GLO-021-lending-agreement]]"
tags: [stakeholder]
aliases: [lender, private lender]
role: Owns a piece and lends it to a Tour under a lending agreement
influence: low
interest: medium
provides: []
receives: []
nature: person
context_role: none
---

# Private owner

**Snapshot.** A private individual who already owns a piece and lends it to a
[[GLO-001-tour|Tour]]. Not every piece on tour is for sale — some are on loan
from the artist, from a private owner, or from a [[STK-008-museum|museum]]. The
lending agreement fixes the insurance amount, the loan duration, and the
professional cleaning by a [[STK-009-conservator|restorer]] once the tour closes.

**Goals.** [[PAM]] (light)
- Lend without risk: adequately insured, returned on time, returned clean.
- Know where the piece is at any point in the tour.

**Concerns / pains.**
- A tour that overruns its agreed loan duration.
- Damage or condition drift with no documented custody trail.

**Interactions.** No [[UC-...]] or [[FR-...]] captured yet.

> [!assumption]
> This role appears in `raw/TSU-brief.md.md` (still un-ingested) and is
> **absent** from the Req4Arc Linz stakeholder list — surfaced by grilling that
> list against the brief. `sources:` stays empty until the brief is ingested.

> [!note] Context edges live on the interface node
> This role is also drawn as a box in the workshop context diagram, so its
> boundary edges are held on [[EIF-002-museums-and-owners]] (ADR-0026). `context_role: none` keeps it out
> of the projection so the actor renders exactly once (ADR-0014); `provides:`
> and `receives:` stay empty here on purpose.
