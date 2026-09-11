---
id: STK-004
type: stakeholder
title: Buyer
status: draft
created: 2026-09-09
updated: 2026-09-09
sources:
  - "[[SRC-004-ulrich-stuerzlinger-context-diagram]]"
  - "[[SRC-002-georg-mayrhauser-vision-goals-stakeholders]]"
related:
  - "[[EIF-008-individual-buyers]]"
  - "[[GOAL-002-global-market-expansion]]"
  - "[[GOAL-004-trust-and-authentication]]"
  - "[[GLO-003-provenance]]"
  - "[[STK-014-art-collector]]"
  - "[[ISS-013-three-way-buyer-segmentation]]"
  - "[[EIF-009-global-online-buyers]]"
  - "[[GLO-013-buyer]]"
  - "[[ISS-005-ungrounded-stakeholder-entries]]"
  - "[[ISS-006-buyer-versus-art-collector]]"
  - "[[ISS-019-visitors-is-an-undefined-actor]]"
  - "[[ISS-022-tsu-brief-only-partially-ingested]]"
  - "[[STK-008-museum]]"
  - "[[GOAL-006-settlement-correct-and-on-time]]"
  - "[[FR-029-keep-a-bought-piece-safe-until-handover]]"
  - "[[GOAL-008-pieces-come-home-intact]]"
  - "[[DM-009-buyer]]"
tags: [stakeholder]
aliases: [customer]
role: Purchases a piece from a Show
influence: low
interest: high
provides: []
receives: []
nature: person
context_role: none
---

# Buyer

**Snapshot.** Buys a piece while it is on tour, signs an intent to purchase, and
then works through a fixed payment sequence: 10% within 24 hours (until Monday
if signed on a Friday or Saturday), the remaining 90% within 14 days. The piece
stays on tour regardless — the buyer takes possession only after the tour closes.

**Goals.** [[PAM]] (light)
- Buy with confidence that the piece is what it is claimed to be —
  [[GOAL-004-trust-and-authentication]]; verified pieces reportedly carry a
  10–15% premium precisely because buyers will pay for that certainty.
- Discover and buy without being physically present at a
  [[GLO-002-show|Show]] — [[GOAL-002-global-market-expansion]].

**Concerns / pains.**
- Forfeiting half the deposit ("The Insult") by missing the 14-day deadline.
- Paying in full and then waiting until the tour ends to take the piece home.
- Buying a forgery or a piece with a broken chain of
  [[GLO-003-provenance|provenance]].

**Interactions.** No [[UC-...]] or [[FR-...]] captured yet.

> [!assumption]
> The payment sequence and "The Insult" come from `raw/TSU-brief.md.md`, still
> un-ingested.

> [!note] Collector is a separate role
> *Art collector* was an alias here until 2026-09-09, when
> [[STK-001-gus-renoir]] decided the two are distinct roles
> ([[ISS-006-buyer-versus-art-collector]]). This page is now the transactional
> buyer only; the cultivated relationship lives on [[STK-014-art-collector]].
> How the buying party segments overall is still open in
> [[ISS-013-three-way-buyer-segmentation]].

> [!note] Context edges live on the interface node
> This role is also drawn as a box in the workshop context diagram, so its
> boundary edges are held on [[EIF-008-individual-buyers]], [[EIF-009-global-online-buyers]], [[EIF-010-institutional-buyers]] (ADR-0026). `context_role: none` keeps it out
> of the projection so the actor renders exactly once (ADR-0014); `provides:`
> and `receives:` stay empty here on purpose.
