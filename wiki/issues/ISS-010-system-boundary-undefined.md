---
id: ISS-010
type: issue
title: The context diagram draws TSU's own operations outside the system boundary
status: resolved
created: 2026-09-09
updated: 2026-09-09
sources:
  - "[[SRC-004-ulrich-stuerzlinger-context-diagram]]"
related:
  - "[[CTX-001-etsu-system-context]]"
  - "[[EIF-004-customer-support-and-marketing]]"
  - "[[EIF-006-business-growth-and-content]]"
  - "[[EIF-007-data-and-analytics]]"
  - "[[EIF-011-gallery-operations]]"
  - "[[EIF-013-technology-and-infrastructure]]"
  - "[[ISS-004-scope-inflation-marketplace-vs-back-office]]"
  - "[[ISS-018-competing-context-diagrams]]"
tags: [issue]
severity: blocker
kind: ambiguity
raised-by: agent
resolved: 2026-09-09
---

# The context diagram draws TSU's own operations outside the system boundary

**What's unresolved.** Where does eTSU end? The source diagram places four boxes
outside the system that read as TSU's own functions or eTSU's own capabilities —
one of them under a heading that literally calls it **CORE**. A system cannot
have its core operations outside its own boundary. Until the line is drawn,
[[CTX-001-etsu-system-context]] cannot state *in scope* or *out of scope*, and
roughly half the `EIF` nodes are provisional.

**Affects.** [[CTX-001-etsu-system-context]] and, directly,
[[EIF-011-gallery-operations]], [[EIF-007-data-and-analytics]],
[[EIF-004-customer-support-and-marketing]],
[[EIF-006-business-growth-and-content]],
[[EIF-013-technology-and-infrastructure]]. Indirectly: every use case, data model
and backlog item that has not been written yet.

**Context / evidence.** The four contested boxes, and why each is doubtful:

| Box | Diagram sub-label | Why it may not be external |
|---|---|---|
| Gallery Operations | "6 locations, staff, events" | This **is** [[GLO-004-tsu\|TSU]]. Modelling it as a neighbour says the galleries talk *to* eTSU rather than *use* it — the opposite of the brief's premise. |
| Data & Analytics | "BI, insights" | Analytics over eTSU's own data is normally part of eTSU. Also: no metric in `wiki/goals/` is measurable without it. |
| Customer Support & Marketing | "24/7, SEO, social" | A TSU function. "24/7" is an availability [[QR-...]], not an interface. |
| Business Growth & Content | "Photography, 3D" | "Business growth" is an objective; "photography/3D" is a supplier. Two unrelated things in one box. |

A fifth, [[EIF-013-technology-and-infrastructure]], mixes a real neighbour
(payments) with deployment concerns (cloud, CDN, security) that are not
neighbours at all.

Per ADR-0026 all fourteen were captured as drawn rather than silently
reinterpreted — this Issue is where the correction happens.

**Options.**
1. **Draw the line at eTSU the product.** Gallery Operations, Data & Analytics,
   Customer Support and Business Growth become *internal*: their requirements
   move to `FR`/`QR` and their `EIF` pages are retired. Leaves roughly 8–9
   genuine boundary nodes. Recommended — it is the only reading in which the
   phrase "core operations" is not self-contradictory.
2. **Draw the line at eTSU as a marketplace platform**, with TSU's galleries as
   one participant among many — then Gallery Operations legitimately *is*
   external, and the brief's premise is what changes. Coherent, but it is a much
   bigger decision than a diagram can carry, and it depends on
   [[ISS-004-scope-inflation-marketplace-vs-back-office]].
3. **Keep all fourteen** and accept that `wiki/external-interfaces/` means
   "boxes drawn outside the system" rather than "neighbouring systems".

**Resolution.** **Resolved 2026-09-09** by [[STK-001-gus-renoir]], along option 1.
Drawing TSU's own operations outside the system boundary **was a mistake**, not a
position. The line runs around eTSU the product, and the four contested boxes are
**inside** it:

| Node | Now |
|---|---|
| [[EIF-011-gallery-operations]] | deprecated — this is [[GLO-004-tsu\|TSU]] itself; the galleries *use* eTSU |
| [[EIF-007-data-and-analytics]] | deprecated — an eTSU capability every goal metric depends on |
| [[EIF-004-customer-support-and-marketing]] | deprecated — a TSU function; "24/7" is a Quality requirement |
| [[EIF-006-business-growth-and-content]] | deprecated — an objective plus an internal function |
| [[EIF-013-technology-and-infrastructure]] | narrowed to the payment provider; cloud, CDN and security dropped as internal |

Ten boundary nodes remain. The four deprecated pages are kept rather than
deleted so the workshop artefact stays readable and the correction is traceable;
their content belongs in `FR`/`QR` pages from here on.

**Two things this does *not* settle.** It does not decide
[[ISS-004-scope-inflation-marketplace-vs-back-office]] — eTSU may still turn out
to be a marketplace rather than a back-office tool, and that would move the line
again. And it does not choose between the two competing context drawings from the
Linz workshop, which is now [[ISS-018-competing-context-diagrams]].
