---
id: STK-006
type: stakeholder
title: Insurer
status: draft
created: 2026-09-09
updated: 2026-09-09
sources:
  - "[[SRC-004-ulrich-stuerzlinger-context-diagram]]"
  - "[[SRC-002-georg-mayrhauser-vision-goals-stakeholders]]"
related:
  - "[[EIF-012-logistics-and-fulfillment]]"
  - "[[GLO-001-tour]]"
  - "[[STK-005-shipper]]"
  - "[[STK-013-private-owner]]"
tags: [stakeholder]
aliases: [insurance company]
role: Insures the Tour's pieces for the duration of the Tour
influence: medium
interest: medium
provides: []
receives: []
nature: organization
context_role: none
---

# Insurer

**Snapshot.** Like the [[STK-005-shipper|shipper]], **one insurer covers the
entire [[GLO-001-tour|Tour]]**. Insurance amounts for borrowed pieces are fixed
in the lending agreements with owners and museums. The insurance payout is what
makes the business whole when a sold piece is damaged before the tour ends: the
buyer is fully refunded, the artist keeps the half-commission already paid, and
TSU absorbs that from the settlement.

**Goals.** [[PAM]] (light)
- Accurate, current valuations and an auditable record of where each piece is.

**Concerns / pains.**
- Floating prices during a tour drifting away from the insured values.
- Incomplete condition or custody records at claim time.

**Interactions.** No [[UC-...]] or [[FR-...]] captured yet.

> [!assumption]
> The one-insurer rule, lending-agreement insurance amounts and the
> damage/refund settlement come from `raw/TSU-brief.md.md`, still un-ingested.

> [!note] Context edges live on the interface node
> This role is also drawn as a box in the workshop context diagram, so its
> boundary edges are held on [[EIF-012-logistics-and-fulfillment]] (ADR-0026). `context_role: none` keeps it out
> of the projection so the actor renders exactly once (ADR-0014); `provides:`
> and `receives:` stay empty here on purpose.
