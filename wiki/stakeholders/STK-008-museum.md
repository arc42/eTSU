---
id: STK-008
type: stakeholder
title: Museum
status: draft
created: 2026-09-09
updated: 2026-09-09
sources:
  - "[[SRC-004-ulrich-stuerzlinger-context-diagram]]"
  - "[[SRC-002-georg-mayrhauser-vision-goals-stakeholders]]"
related:
  - "[[EIF-002-museums-and-owners]]"
  - "[[GOAL-002-global-market-expansion]]"
  - "[[GOAL-004-trust-and-authentication]]"
  - "[[STK-004-buyer]]"
  - "[[STK-013-private-owner]]"
  - "[[GLO-008-lender]]"
  - "[[EIF-010-institutional-buyers]]"
  - "[[GLO-003-provenance]]"
  - "[[GLO-014-museum]]"
  - "[[ISS-006-buyer-versus-art-collector]]"
  - "[[ISS-013-three-way-buyer-segmentation]]"
  - "[[STK-009-conservator]]"
  - "[[DM-008-museum]]"
tags: [stakeholder]
aliases: [institutional buyer]
role: Lends pieces to a Tour and buys pieces at the museum price
influence: medium
interest: high
provides: []
receives: []
nature: organization
context_role: none
---

# Museum

**Snapshot.** A museum plays **two roles at once**, and eTSU has to hold both.
As a *lender* it owns pieces that appear on a [[GLO-001-tour|Tour]] under a
lending agreement (insurance amount, loan duration, professional cleaning at the
end of the tour). As a *buyer* it purchases pieces at the **minimum museum sale
price**, which is almost always below the minimum price offered to a private
[[STK-004-buyer|buyer]] — artists will discount heavily to hang in a collection.

**Goals.** [[PAM]] (light)
- Acquire work for the collection at institutional terms.
- Transact only where [[GLO-003-provenance|provenance]] is documented — the
  2029 narrative in [[SRC-001-ulrich-stuerzlinger-goals-and-newspaper]] has
  museums at 30% of transaction volume, contingent on exactly that.

**Concerns / pains.**
- Acquisition committees cannot approve a purchase without a verified chain of
  ownership.
- Lent pieces must come back in documented condition, professionally cleaned.

**Interactions.** No [[UC-...]] or [[FR-...]] captured yet.

> [!note] Dual role
> Modelling a museum as *either* a buyer *or* a lender will produce the wrong
> data model. The two-price rule (customer minimum vs. museum minimum) means the
> buyer's institutional status materially changes the transaction — it is not
> just a customer attribute.

> [!assumption]
> The minimum museum sale price and lending-agreement terms come from
> `raw/TSU-brief.md.md`, still un-ingested.

> [!note] Context edges live on the interface node
> This role is also drawn as a box in the workshop context diagram, so its
> boundary edges are held on [[EIF-002-museums-and-owners]] and [[EIF-010-institutional-buyers]] (ADR-0026). `context_role: none` keeps it out
> of the projection so the actor renders exactly once (ADR-0014); `provides:`
> and `receives:` stay empty here on purpose.
