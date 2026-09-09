---
id: CTX-001
type: context
title: eTSU system context
status: draft
created: 2026-09-09
updated: 2026-09-09
sources:
  - "[[SRC-004-ulrich-stuerzlinger-context-diagram]]"
related:
  - "[[EIF-001-artists]]"
  - "[[EIF-002-museums-and-owners]]"
  - "[[EIF-003-appraisers-and-authenticators]]"
  - "[[EIF-004-customer-support-and-marketing]]"
  - "[[EIF-005-fraud-and-security-prevention]]"
  - "[[EIF-006-business-growth-and-content]]"
  - "[[EIF-007-data-and-analytics]]"
  - "[[EIF-008-individual-buyers]]"
  - "[[EIF-009-global-online-buyers]]"
  - "[[EIF-010-institutional-buyers]]"
  - "[[EIF-011-gallery-operations]]"
  - "[[EIF-012-logistics-and-fulfillment]]"
  - "[[EIF-013-technology-and-infrastructure]]"
  - "[[EIF-014-regulatory-and-compliance]]"
  - "[[ISS-010-system-boundary-undefined]]"
  - "[[ISS-004-scope-inflation-marketplace-vs-back-office]]"
  - "[[ISS-018-competing-context-diagrams]]"
  - "[[ISS-019-visitors-is-an-undefined-actor]]"
  - "[[ISS-020-sketch-boxes-untyped]]"
tags: [context]
kind: business
diagram: generated
---

# eTSU system context

**Diagram.** _Projected_ — generated from `EIF.flows` (ADR-0013), one labelled
line per neighbour, clustered by `tier:` (ADR-0026). All ten edges live on
the `EIF` nodes; stakeholders with an `EIF` twin are hidden via
`context_role: none` (ADR-0014), so each actor renders exactly once.

**In scope.** *Not yet agreed.* The source diagram names the system
**"TSU / eTSU — Gallery platform & digital marketplace"** and surrounds it with
supply, demand, support and operations. Taken at face value that describes a
two-sided marketplace: artists and lenders supply work, three buyer segments
consume it, and the gallery network, logistics chain and compliance apparatus
run underneath. **This wiki does not yet assert that as the scope** — see
*Out of scope* and [[ISS-004-scope-inflation-marketplace-vs-back-office]].

**Out of scope.** *Nothing is yet an agreed non-goal.* This is itself the
finding. The brief asks for "a digital product supporting the gallery's
business"; the diagram draws a global marketplace. Until
[[ISS-004-scope-inflation-marketplace-vs-back-office]] closes, no non-goal can
be stated honestly, and this section stays deliberately empty rather than
inventing a boundary the group has not drawn.

**External interfaces.** Ten, grouped by the source diagram's tiers. The
dashboard renders them as one labelled line each, with both directions listed in
the flow table beneath the diagram (ADR-0026) — not repeated here, so the two
cannot drift apart.

| Tier | Neighbours |
|---|---|
| Supply | [[EIF-001-artists\|Artists]] · [[EIF-002-museums-and-owners\|Lenders]] · [[EIF-003-appraisers-and-authenticators\|Appraisers]] |
| Support | [[EIF-005-fraud-and-security-prevention\|AML screening]] |
| Demand | [[EIF-008-individual-buyers\|Individual buyers]] · [[EIF-009-global-online-buyers\|Online buyers]] · [[EIF-010-institutional-buyers\|Institutional buyers]] |
| Core operations | [[EIF-012-logistics-and-fulfillment\|Logistics]] · [[EIF-013-technology-and-infrastructure\|Payments]] · [[EIF-014-regulatory-and-compliance\|Regulators]] |

Four nodes were **deprecated on 2026-09-09** when
[[ISS-010-system-boundary-undefined]] closed —
[[EIF-004-customer-support-and-marketing]], [[EIF-006-business-growth-and-content]],
[[EIF-007-data-and-analytics]] and [[EIF-011-gallery-operations]] are inside the
boundary, and [[EIF-013-technology-and-infrastructure]] was narrowed to the
payment provider alone.

**User roles.** Each human counterpart is also a persona; the context edge lives
on the `EIF` node, the persona keeps goals, concerns and influence/interest.

| Stakeholder | Interface |
|---|---|
| [[STK-002-artist]] | [[EIF-001-artists]] |
| [[STK-004-buyer]] | [[EIF-008-individual-buyers]], [[EIF-009-global-online-buyers]], [[EIF-010-institutional-buyers]] |
| [[STK-008-museum]] | [[EIF-002-museums-and-owners]] *and* [[EIF-010-institutional-buyers]] — lender and buyer |
| [[STK-013-private-owner]] | [[EIF-002-museums-and-owners]] |
| [[STK-005-shipper]], [[STK-006-insurer]], [[STK-009-conservator]] | [[EIF-012-logistics-and-fulfillment]] |
| [[STK-014-art-collector]] | **no node** — split from [[STK-004-buyer]] on 2026-09-09, not drawn anywhere |
| [[STK-003-gallery-manager]] | **internal** — a user of eTSU, not a boundary counterpart |
| [[STK-007-customs-authority]] | **no node** — customs is absent from the diagram |
| [[STK-001-gus-renoir]], [[STK-010-legal-and-accounting]], [[STK-011-development-team]], [[STK-012-creative-genius]] | internal; no boundary edge drawn |

**Explanation.** The source is a **business ecosystem diagram**, not a system
context diagram, and the difference is not cosmetic. A context diagram's job is
to draw one line — inside the system, outside the system — and show what crosses
it. This diagram draws four thematic tiers instead, and placed TSU's own
galleries, analytics and support function *outside* the box under a heading that
calls them **CORE OPERATIONS**. That placement was confirmed on 2026-09-09 to be
a **drawing mistake** ([[ISS-010-system-boundary-undefined]]): the line runs
around eTSU the product, and those four nodes are inside it.

Captured here as drawn (ADR-0026) so the workshop's artefact is preserved
verbatim and can be worked on directly. Three Issues still carry cleanup:
[[ISS-012-bundled-eif-nodes-hide-partners]] (several nodes fuse 2–3 partners),
[[ISS-011-context-flows-inferred-not-sourced]] (no arrow carries a payload), and
[[ISS-013-three-way-buyer-segmentation]].

> [!warning] A second, competing diagram exists
> The same Linz workshop also produced a hand-drawn sketch
> ([[SRC-006-workshop-etsu-context-sketch]]) showing `eTSU` with **six**
> neighbours — Visitors, Artist, Payment, Invoice, Delivery, Social Media — that
> shares only two of them with the ten above and adds Social Media, which appears
> in no other source. This page still records the ecosystem diagram only.
> [[ISS-018-competing-context-diagrams]] holds the choice; nothing here changes
> until it closes.

> [!note] Open points
> - **[[ISS-004-scope-inflation-marketplace-vs-back-office]] is now the blocker
>   for this page.** Neither *In scope* nor *Out of scope* can be written until
>   the marketplace question is settled. The boundary question that used to sit
>   here, [[ISS-010-system-boundary-undefined]], closed on 2026-09-09.
> - **Customs is missing** ([[STK-007-customs-authority]]) though the brief names
>   it explicitly and a border hold stops a [[GLO-002-show|Show]].
> - **"6 locations" is new** — no earlier source gives the gallery count.
> - The system box merges [[GLO-004-tsu|TSU]] and [[GLO-005-etsu|eTSU]] into one
>   node, though the glossary keeps them distinct: TSU is the business, eTSU the
>   product. At the context level the *system* is eTSU alone.
