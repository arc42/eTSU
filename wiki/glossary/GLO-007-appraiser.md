---
id: GLO-007
type: glossary-term
title: Appraiser
status: draft
created: 2026-09-09
updated: 2026-09-09
sources:
  - "[[SRC-004-ulrich-stuerzlinger-context-diagram]]"
related:
  - "[[EIF-003-appraisers-and-authenticators]]"
  - "[[GLO-003-provenance]]"
  - "[[GOAL-004-trust-and-authentication]]"
  - "[[ISS-021-authentication-card-ambiguous]]"
  - "[[ISS-012-bundled-eif-nodes-hide-partners]]"
tags: [glossary, preliminary]
aliases: [valuer]
bounded-context: Gallery Touring
agreed: false
stereotype: entity
---

# Appraiser

**Definition.** *Preliminary.* An independent expert engaged to state what a
piece is **worth**, producing a valuation TSU can put in front of an insurer, a
lender or a buyer.

**In context.** Valuation is load-bearing well before any sale. Insured values
are fixed in lending agreements, and the minimum museum sale price sits below
the minimum customer price, so both numbers rest on somebody's assessment of
worth. [[EIF-003-appraisers-and-authenticators]] is the boundary node.

**Distinguish from.** *Authenticator* — the expert who states whether a piece is
**genuine**. Value and genuineness are different judgments, made by different
specialists, on different evidence. The two are fused into one interface node,
which is why they are separated here; see
[[ISS-012-bundled-eif-nodes-hide-partners]]. Distinguish both from
[[GLO-003-provenance|provenance]], which is the documentary evidence the
authenticator reasons over, not a judgment at all.

> [!note] Preliminary
> `tags: [preliminary]` and `agreed: false` — this definition is the agent's, not
> the group's. The party appears in **no source before the workshop context
> diagram**: not in the TSU brief, not in the Linz stakeholder list. Two things
> are open beyond the wording. Is this a firm TSU buys a service from, or the
> register lookup the 2029 narrative names (Art Loss Register, Interpol)? And
> does the same counterpart do both valuation and authentication, or are these
> two neighbours drawn as one? No stakeholder page exists for the role yet.
