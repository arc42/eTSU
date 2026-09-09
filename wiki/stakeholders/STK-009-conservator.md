---
id: STK-009
type: stakeholder
title: Conservator
status: draft
created: 2026-09-09
updated: 2026-09-09
sources:
  - "[[SRC-004-ulrich-stuerzlinger-context-diagram]]"
  - "[[SRC-002-georg-mayrhauser-vision-goals-stakeholders]]"
related:
  - "[[GLO-006-conservator]]"
  - "[[EIF-012-logistics-and-fulfillment]]"
  - "[[STK-013-private-owner]]"
  - "[[STK-008-museum]]"
  - "[[ISS-007-cleaner-versus-restorer]]"
tags: [stakeholder]
aliases: [cleaner, restorator, restorer, professional cleaner]
role: Cleans and conserves borrowed pieces when a Tour closes
influence: low
interest: medium
provides: []
receives: []
nature: person
context_role: none
---

# Conservator

**Snapshot.** A professional cleaner/restorer engaged at the end of a
[[GLO-001-tour|Tour]] to clean borrowed pieces. This is not goodwill: it is a
**contractual obligation written into the lending agreements** with
[[STK-013-private-owner|private owners]] and [[STK-008-museum|museums]],
alongside the insurance amount and the loan duration.

**Goals.** [[PAM]] (light)
- Know which pieces are due for treatment, under which lending agreement, and by
  when.

**Concerns / pains.**
- Condition changes during a tour that go unrecorded until the piece arrives.

**Interactions.** No [[UC-...]] or [[FR-...]] captured yet.

> [!note] Naming settled
> **Conservator** is the canonical term ([[GLO-006-conservator]]). *Cleaner* and
> *restorator* are aliases for the same role, and *restorer* was a typo for
> restorator, kept as an alias so older references still resolve. There is no
> separate janitorial stakeholder. Decided 2026-09-09, closing
> [[ISS-007-cleaner-versus-restorer]].

> [!note] Context edges live on the interface node
> This role is also drawn as a box in the workshop context diagram, so its
> boundary edges are held on [[EIF-012-logistics-and-fulfillment]] (ADR-0026). `context_role: none` keeps it out
> of the projection so the actor renders exactly once (ADR-0014); `provides:`
> and `receives:` stay empty here on purpose.
