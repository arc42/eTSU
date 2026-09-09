---
id: STK-002
type: stakeholder
title: Artist
status: draft
created: 2026-09-09
updated: 2026-09-09
sources:
  - "[[SRC-004-ulrich-stuerzlinger-context-diagram]]"
  - "[[SRC-002-georg-mayrhauser-vision-goals-stakeholders]]"
related:
  - "[[EIF-001-artists]]"
  - "[[GOAL-002-global-market-expansion]]"
  - "[[GOAL-003-operational-excellence]]"
  - "[[GOAL-004-trust-and-authentication]]"
  - "[[GLO-001-tour]]"
tags: [stakeholder]
aliases: [up-and-coming artist]
role: Creator whose work is shown and sold on a Tour
influence: medium
interest: high
provides: []
receives: []
nature: person
context_role: none
---

# Artist

**Snapshot.** A young, up-and-coming creator whose body of work forms a
[[GLO-001-tour|Tour]] — usually alone, occasionally pooled into a group tour
when no single artist has enough work for a full [[GLO-002-show|Show]].
Negotiates which pieces travel, the commission percentage, and the minimum sale
price (and a separate, lower minimum museum sale price, because a museum
placement is worth more to an artist than the money).

**Goals.** [[PAM]] (light)
- Reach buyers beyond the gallery circuit — [[GOAL-002-global-market-expansion]]
  targets 2.5× the legacy-model earnings by 2029.
- Be paid promptly. Today half the commission arrives on full buyer payment and
  half five days after the tour closes; [[GOAL-003-operational-excellence]] aims
  at near-immediate settlement.

**Concerns / pains.**
- Waiting on money that is already earned while a tour runs on for weeks.
- Loss of control once pieces are travelling: where they hang, what they are
  priced at after a float, what condition they come back in.
- Authenticity — [[GOAL-004-trust-and-authentication]] protects an artist's
  market as much as a buyer's purchase.

**Interactions.** No [[UC-...]] or [[FR-...]] captured yet.

> [!assumption]
> The commission mechanics, minimum museum sale price and the "big egos"
> motivation come from `raw/TSU-brief.md.md`, which is still un-ingested and so
> cannot yet be cited in `sources:`.

> [!note] Context edges live on the interface node
> This role is also drawn as a box in the workshop context diagram, so its
> boundary edges are held on [[EIF-001-artists]] (ADR-0026). `context_role: none` keeps it out
> of the projection so the actor renders exactly once (ADR-0014); `provides:`
> and `receives:` stay empty here on purpose.
