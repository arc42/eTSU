---
id: GLO-010
type: glossary-term
title: AML screening
status: draft
created: 2026-09-09
updated: 2026-09-09
sources:
  - "[[SRC-004-ulrich-stuerzlinger-context-diagram]]"
related:
  - "[[EIF-005-fraud-and-security-prevention]]"
  - "[[EIF-014-regulatory-and-compliance]]"
  - "[[GOAL-004-trust-and-authentication]]"
  - "[[STK-010-legal-and-accounting]]"
  - "[[ISS-012-bundled-eif-nodes-hide-partners]]"
  - "[[FR-007-settlement-and-compliance]]"
tags: [glossary, preliminary]
aliases: [anti-money-laundering screening, AML, KYC]
bounded-context: Gallery Touring
agreed: false
---

# AML screening

**Definition.** *Preliminary.* Anti-money-laundering screening: checking a
transaction and the parties behind it against sanctions, politically-exposed-person
and blocked-party lists before a sale is allowed to complete, and raising an
alert when there is a hit.

**In context.** High-value art is a recognised money-laundering channel, which is
why this sits on the boundary at all. It is the operational counterpart to the
"< 0.5% fraud rate" and "zero compliance incidents" targets in
[[GOAL-004-trust-and-authentication]] — neither number is measurable without it.

**Distinguish from.** *Authentication*, which asks whether the **piece** is
genuine; AML screening asks whether the **buyer** is acceptable
([[ISS-021-authentication-card-ambiguous]] turns on the same confusion). And
*KYC* is carried here as an alias, though strictly it is the identity-verification
step that feeds screening rather than screening itself. That looseness is
inherited from the source and should be tightened when the term is agreed.

> [!note] Preliminary
> `tags: [preliminary]` and `agreed: false` — the agent's wording, expanded from
> the two words "AML detection" on the workshop diagram. **Whether this is even
> external is unsettled:** bought from a screening provider it is a real
> neighbour; built into eTSU it is a security Quality requirement plus backlog,
> and the diagram does not say which. The same concern is also drawn a second
> time inside [[EIF-014-regulatory-and-compliance]] —
> [[ISS-012-bundled-eif-nodes-hide-partners]].
