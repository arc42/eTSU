---
id: STK-011
type: stakeholder
title: Development team
status: draft
created: 2026-09-09
updated: 2026-09-09
sources:
  - "[[SRC-002-georg-mayrhauser-vision-goals-stakeholders]]"
related:
  - "[[GOAL-001-eTSU-vision]]"
tags: [stakeholder]
aliases: [PO, architects, developers, designers, QA]
role: Designs, builds and assures eTSU
influence: high
interest: high
provides: []
receives: []
nature: organization
context_role: none
---

# Development team

**Snapshot.** Product owner, architects, developers, designers and QA — the team
building [[GLO-005-etsu|eTSU]]. Named explicitly in the Req4Arc Linz workshop
list. High influence over how the system takes shape; not a user of the running
system.

**Goals.** [[PAM]] (light)
- Requirements precise enough to build and test against — which is what this
  wiki is for.
- Scope that is decided rather than assumed; see
  [[ISS-004-scope-inflation-marketplace-vs-back-office]].

**Concerns / pains.**
- Goals stated as solutions (blockchain, Interpol integration) arriving before
  the problem is agreed.
- Untestable quality targets — "real time", "zero incidents".

**Interactions.** No [[UC-...]] or [[FR-...]] captured yet.

> [!note] Hidden from the context diagram
> `context_role: none` (ADR-0014) — the build team is not an actor at the system
> boundary, so it is deliberately excluded from the context projection.
