---
id: GLO-009
type: glossary-term
title: Logistics partner
status: draft
created: 2026-09-09
updated: 2026-09-09
sources:
  - "[[SRC-004-ulrich-stuerzlinger-context-diagram]]"
related:
  - "[[EIF-012-logistics-and-fulfillment]]"
  - "[[STK-005-shipper]]"
  - "[[STK-006-insurer]]"
  - "[[STK-009-conservator]]"
  - "[[GLO-001-tour]]"
  - "[[ISS-012-bundled-eif-nodes-hide-partners]]"
  - "[[GLO-016-home-gallery]]"
tags: [glossary, preliminary]
aliases: [logistics, fulfillment]
bounded-context: Gallery Touring
agreed: false
stereotype: entity
---

# Logistics partner

**Definition.** *Preliminary.* A **collective term** for the external companies
that physically move and protect a piece for the duration of a
[[GLO-001-tour|Tour]]: the [[STK-005-shipper|shipper]] that transports it, the
[[STK-006-insurer|insurer]] that covers it, and the
[[GLO-006-conservator|conservator]] that treats it at tour close.

**In context.** The three are contracted differently and that difference is a
requirement, not trivia. One shipper and one insurer are fixed **for an entire
Tour**, because those companies will not work any other way. The conservator is
engaged **per lending agreement**, and only when the tour ends. Different
cardinality, different trigger, different paperwork.

**Distinguish from.** Any single company. Nobody is "the logistics partner" —
the phrase names a category with at least three members, and using it as if it
were one counterpart is exactly the mistake
[[ISS-012-bundled-eif-nodes-hide-partners]] records against
[[EIF-012-logistics-and-fulfillment]]. Distinguish also from **Delivery**, the
outbound box on the workshop sketch, which may mean getting a sold piece to its
buyer rather than moving a tour between galleries
([[ISS-020-sketch-boxes-untyped]]).

> [!note] Preliminary
> `tags: [preliminary]` and `agreed: false` — the agent's wording, taken from
> the "Shipping, insurance, restoration" box. The term is recorded so the bundle
> has a name while it is being argued about; if
> [[ISS-012-bundled-eif-nodes-hide-partners]] splits the node into three, this
> entry stays useful only as an umbrella and should say so explicitly then.
