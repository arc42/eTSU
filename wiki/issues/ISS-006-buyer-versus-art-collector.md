---
id: ISS-006
type: issue
title: Are "buyer" and "art collector" one role or two?
status: resolved
created: 2026-09-09
updated: 2026-09-09
sources:
  - "[[SRC-002-georg-mayrhauser-vision-goals-stakeholders]]"
related:
  - "[[ISS-013-three-way-buyer-segmentation]]"
  - "[[STK-004-buyer]]"
  - "[[STK-014-art-collector]]"
  - "[[STK-008-museum]]"
tags: [issue]
severity: minor
kind: ambiguity
raised-by: agent
resolved: 2026-09-09
---

# Are "buyer" and "art collector" one role or two?

**What's unresolved.** The workshop list names **buyers** and **art collectors**
as separate entries. The brief only ever says "buyer" (and once "customer").
They were merged into [[STK-004-buyer]] with *art collector* as an alias — but
merging is a decision, and it may be the wrong one.

**Affects.** [[STK-004-buyer]]; any future data model of the purchasing party;
pricing rules.

**Context / evidence.** There is a real distinction available if the group wants
it: a **buyer** is whoever signs an intent to purchase on a given piece; a
**collector** is a recurring relationship the business cultivates over years,
across tours. The brief's pricing rules already prove the buying party's
*identity* changes the deal — a [[STK-008-museum|museum]] buys at the minimum
museum sale price, which is almost always below the minimum customer price. If
institutional status changes price, collector status might too (preferential
access to a tour, early viewing, negotiated terms).

Left unresolved, this surfaces later as a data-model question: one Party with
roles, or separate types?

**Options.**
1. One role, `art collector` as an alias (current state) — simplest; loses the
   relationship dimension.
2. Two stakeholders — collector as a distinct persona with its own goals
   (access, relationship, portfolio) alongside the transactional buyer.
3. One party type with a **segment** attribute (private / collector /
   institutional) driving pricing and access — probably where the data model
   lands, but that is a modelling decision, not a stakeholder one.

**Resolution.** **Resolved 2026-09-09** by [[STK-001-gus-renoir]], along option 2:
**two roles.** [[STK-004-buyer]] is the transactional party who signs an intent
to purchase on one piece; [[STK-014-art-collector]] is the recurring relationship
TSU cultivates across tours. The `art collector` alias was removed from the buyer
page and the new persona created.

This closes the two-way question only. **How the buying party segments overall
stays open** in [[ISS-013-three-way-buyer-segmentation]] — that Issue holds the
individual / global-online / institutional cut, which is a different dimension
and now has a fourth candidate in the *Customer* vs *Museum* cards of
[[SRC-005-workshop-capability-card-wall]].
