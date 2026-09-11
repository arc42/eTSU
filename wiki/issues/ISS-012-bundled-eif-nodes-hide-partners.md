---
id: ISS-012
type: issue
title: Five EIF nodes each bundle two or more distinct partners
status: open
created: 2026-09-09
updated: 2026-09-09
sources:
  - "[[SRC-004-ulrich-stuerzlinger-context-diagram]]"
related:
  - "[[EIF-002-museums-and-owners]]"
  - "[[EIF-003-appraisers-and-authenticators]]"
  - "[[GLO-007-appraiser]]"
  - "[[GLO-008-lender]]"
  - "[[GLO-009-logistics-partner]]"
  - "[[GLO-010-aml-screening]]"
  - "[[EIF-012-logistics-and-fulfillment]]"
  - "[[EIF-013-technology-and-infrastructure]]"
  - "[[EIF-014-regulatory-and-compliance]]"
  - "[[EIF-005-fraud-and-security-prevention]]"
  - "[[STK-007-customs-authority]]"
tags: [issue]
severity: major
kind: ambiguity
raised-by: agent
resolved: null
---

# Five EIF nodes each bundle two or more distinct partners

**What's unresolved.** ADR-0013 specifies **one neighbour per `EIF` node**. Five
nodes captured from the diagram break that, each fusing counterparts with
different contracts, different cardinality and different triggers.

**Affects.** [[EIF-002-museums-and-owners]],
[[EIF-003-appraisers-and-authenticators]], [[EIF-012-logistics-and-fulfillment]],
[[EIF-013-technology-and-infrastructure]], [[EIF-014-regulatory-and-compliance]].

**Context / evidence.**

| Node | Fuses | Why the split matters |
|---|---|---|
| [[EIF-012-logistics-and-fulfillment]] | shipper, insurer, restorer | The brief fixes **one shipper and one insurer per whole Tour** — those companies demand it. The restorer is engaged **per lending agreement, at tour close**. Different cardinality, different trigger. |
| [[EIF-013-technology-and-infrastructure]] | cloud, payments, security, CDN | Only **payments** is a neighbour. Cloud/CDN/security are how eTSU is *deployed* — a context diagram shows what a system exchanges data **with**, not what it **runs on**. |
| [[EIF-014-regulatory-and-compliance]] | tax authorities, AML/KYC, law enforcement | Three regulators with three interfaces. AML also appears separately as [[EIF-005-fraud-and-security-prevention]] — the same concern drawn twice. |
| [[EIF-003-appraisers-and-authenticators]] | appraiser, authenticator | An **appraiser** says what a piece is worth; an **authenticator** says whether it is genuine. Different judgments, different evidence, usually different specialists. Surfaced on 2026-09-09 while writing [[GLO-007-appraiser]]. |
| [[EIF-002-museums-and-owners]] | museums, private owners | Different lending agreements. And a museum is **also** a buyer, appearing again in the DEMAND tier as [[EIF-010-institutional-buyers]] — one party split across two tiers without the diagram saying so. |

**Also a gap: customs is absent entirely.** [[STK-007-customs-authority]] holds
`influence: high` — a border hold stops a [[GLO-002-show|Show]] — and the brief
explicitly has each gallery start customs paperwork ahead of its show. No box in
the diagram covers it, unless it is meant to hide inside "Regulatory &
Compliance".

**Options.**
1. Split each bundle into one node per partner, merge the duplicate AML node,
   and add a customs node. Recommended, and **now unblocked**:
   [[ISS-010-system-boundary-undefined]] closed on 2026-09-09, which already
   dropped cloud, CDN and security from [[EIF-013-technology-and-infrastructure]]
   and took the boundary from fourteen nodes to ten.
2. Keep the bundles as capability groupings and model the real partners one level
   down. Preserves the diagram's readability; `partner:` then names a group,
   not a neighbour, and ADR-0013's rule is abandoned rather than deferred.

**Resolution.** *Open.* Four preliminary glossary terms were written on
2026-09-09 while these partners were being named —
[[GLO-007-appraiser]], [[GLO-008-lender]], [[GLO-009-logistics-partner]] and
[[GLO-010-aml-screening]]. Each states plainly which counterparts its node
fuses, so the split proposed above can be argued in the ubiquitous language
rather than only on the diagram.
