---
id: GLO-008
type: glossary-term
title: Lender
status: draft
created: 2026-09-09
updated: 2026-09-09
sources:
  - "[[SRC-004-ulrich-stuerzlinger-context-diagram]]"
related:
  - "[[EIF-002-museums-and-owners]]"
  - "[[STK-008-museum]]"
  - "[[STK-013-private-owner]]"
  - "[[STK-009-conservator]]"
  - "[[GLO-001-tour]]"
  - "[[ISS-012-bundled-eif-nodes-hide-partners]]"
  - "[[GLO-011-piece]]"
  - "[[GLO-012-artist]]"
  - "[[GLO-014-museum]]"
  - "[[GLO-021-lending-agreement]]"
tags: [glossary, preliminary]
aliases: [owner, lending party]
bounded-context: Gallery Touring
agreed: false
stereotype: entity
---

# Lender

**Definition.** *Preliminary.* The party that puts a piece it owns on a
[[GLO-001-tour|Tour]] **without selling it**, under a lending agreement that
fixes the insured value, the loan duration and the conservation owed at tour
close.

**In context.** Lenders are why not every piece on tour is for sale, and the
lending agreement is where three obligations that reach into eTSU are written
down at once: what the piece is insured for, how long it may travel, and that a
[[GLO-006-conservator|conservator]] treats it before it goes home. Two kinds of
lender are known, [[STK-008-museum|museums]] and
[[STK-013-private-owner|private owners]], and they sign different agreements.

**Distinguish from.** *Seller* — a lender's piece returns; a seller's does not.
And a museum is often **both** lender and buyer, which is why the same party
appears on two sides of the context diagram.
[[ISS-013-three-way-buyer-segmentation]] holds that overlap.

> [!note] Preliminary
> `tags: [preliminary]` and `agreed: false` — the agent's wording, from the
> "Lend artwork" box on the workshop diagram and the brief's lending-agreement
> terms. *Lender* is a **union term** covering two distinct counterparts;
> [[ISS-012-bundled-eif-nodes-hide-partners]] proposes splitting the interface
> node in two, and this entry should not be read as an argument against that.
