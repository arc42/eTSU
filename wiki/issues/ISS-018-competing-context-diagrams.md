---
id: ISS-018
type: issue
title: Two competing context diagrams — a 14-node ecosystem and a 6-neighbour eTSU sketch
status: open
created: 2026-09-09
updated: 2026-09-09
sources:
  - "[[SRC-006-workshop-etsu-context-sketch]]"
  - "[[SRC-004-ulrich-stuerzlinger-context-diagram]]"
related:
  - "[[CTX-001-etsu-system-context]]"
  - "[[ISS-010-system-boundary-undefined]]"
  - "[[ISS-004-scope-inflation-marketplace-vs-back-office]]"
  - "[[ISS-019-visitors-is-an-undefined-actor]]"
  - "[[ISS-020-sketch-boxes-untyped]]"
  - "[[GLO-004-tsu]]"
  - "[[GLO-005-etsu]]"
tags: [issue]
severity: blocker
kind: contradiction
raised-by: agent
resolved: null
---

# Two competing context diagrams — a 14-node ecosystem and a 6-neighbour eTSU sketch

**What's unresolved.** The workshop produced two drawings of the same thing that
disagree about almost everything: what the system is, where its boundary runs,
and who its neighbours are. They are not two views of one agreement. They are two
answers, and [[CTX-001-etsu-system-context]] currently records only the first.

**Affects.** [[CTX-001-etsu-system-context]] and all fourteen `EIF` pages
beneath it. Under Side B, roughly ten of those fourteen stop being interfaces
altogether.

**Context / evidence.**

| | Side A — [[SRC-004-ulrich-stuerzlinger-context-diagram]] | Side B — [[SRC-006-workshop-etsu-context-sketch]] |
|---|---|---|
| System box | "TSU / eTSU — Gallery platform & digital marketplace" | `eTSU` alone |
| Neighbours | 14 as drawn, 10 after [[ISS-010-system-boundary-undefined]] closed | 6 |
| Human actors | none drawn as actors | VISITORS, ARTIST, as stick figures |
| External systems | none typed as systems | PAYMENT, INVOICE, DELIVERY, SOCIAL MEDIA |
| TSU's own galleries | drawn *outside*, as "CORE OPERATIONS" | not drawn at all |
| Arrow payloads | none labelled | none labelled |

Side B's six neighbours are **Visitors, Artist, Payment, Invoice, Delivery,
Social Media**. Read against Side A:

- **Social Media appears in neither the fourteen nodes nor any earlier source.**
  It is a genuinely new outbound neighbour.
- **Invoice is drawn as a neighbour of eTSU**, which Side A does not do at any
  point. See [[ISS-020-sketch-boxes-untyped]].
- **Visitors is a new party** with no stakeholder page. See
  [[ISS-019-visitors-is-an-undefined-actor]].
- **Ten of Side A's fourteen have no counterpart in Side B** — museums, lenders,
  appraisers, support, AML screening, content production, analytics, the
  institutional and online buyer segments, the gallery network, the logistics
  chain and the regulators. Side B keeps only artists, buyers-as-visitors,
  payments and delivery.

The sketch is also, structurally, the better context diagram of the two. It draws
one boundary, separates human actors from systems by shape as
[[0014-context-diagram-actor-roles-and-shapes|ADR-0014]] requires, and never
places the system's own operations outside itself — which is the defect Side A
was corrected for on the same day, when
[[ISS-010-system-boundary-undefined]] closed and four of its nodes were
deprecated as internal. That correction shrank Side A from fourteen neighbours to
ten; it did not make the two drawings agree. Side B still shares only **artists**
and **buyers-as-visitors** with the surviving ten. Both were drawn in the same
room on the same day, and the wiki does not pick a side.

Note that [[GLO-004-tsu]] and [[GLO-005-etsu]] keep the business and the product
distinct. Side A merges them into one box; Side B names only the product. On the
glossary's own terms, Side B is the one using the ubiquitous language correctly.

**Options.**
1. **Take Side B as the system context and re-cast Side A as a business
   ecosystem view.** The two then stop competing: one answers "what is eTSU
   connected to", the other "who is in TSU's market". Recommended — it is the
   only option that keeps both artefacts and explains why they differ. Cost:
   most of the ten surviving `EIF` pages are demoted to the ecosystem view, and
   Side B's four untyped boxes must be resolved first
   ([[ISS-020-sketch-boxes-untyped]]).
2. Keep Side A and treat the sketch as one participant's partial recollection.
   Cheap, but it leaves [[ISS-010-system-boundary-undefined]] open and discards
   Social Media, which no other source contains.
3. Draw a third diagram in the next session with both in front of the group.
   Honest, but pays for the same conversation twice.

**Resolution.** *Open.* [[CTX-001-etsu-system-context]] is deliberately left
unchanged until this closes.
