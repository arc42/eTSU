---
id: ISS-020
type: issue
title: "PAYMENT, INVOICE, DELIVERY and SOCIAL MEDIA are drawn as boxes but never typed"
status: open
created: 2026-09-09
updated: 2026-09-09
sources:
  - "[[SRC-006-workshop-etsu-context-sketch]]"
related:
  - "[[ISS-018-competing-context-diagrams]]"
  - "[[ISS-011-context-flows-inferred-not-sourced]]"
  - "[[EIF-012-logistics-and-fulfillment]]"
  - "[[EIF-013-technology-and-infrastructure]]"
tags: [issue]
severity: minor
kind: ambiguity
raised-by: agent
resolved: null
---

# PAYMENT, INVOICE, DELIVERY and SOCIAL MEDIA are drawn as boxes but never typed

**What's unresolved.** Four of the sketch's six neighbours are drawn as plain
rectangles with a single noun inside. A rectangle on a context diagram normally
means *an external system*, but three of these nouns read as **documents or
activities**, not systems. Which they are decides whether each becomes an
`EIF` page or a `DM` entity, and the two are not interchangeable.

**Affects.** Whatever [[ISS-018-competing-context-diagrams]] settles on. Under
[[0013-data-flows-as-edges-context-diagram-as-projection|ADR-0013]] only real
external systems may be `EIF` nodes, so a mistyped box would put a document on
the boundary.

**Context / evidence.**

| Box | Arrows | Reads as a system if… | Reads as data if… |
|---|---|---|---|
| PAYMENT | both directions | a payment service provider — matches [[EIF-013-technology-and-infrastructure]] | "payment" is the transaction record eTSU stores |
| INVOICE | both directions | an accounting or billing system eTSU exchanges documents with | the invoice is a document eTSU *produces*, in which case the return arrow makes no sense |
| DELIVERY | outbound only | a carrier or fulfilment provider — overlaps [[EIF-012-logistics-and-fulfillment]] | "delivery" is a shipment record |
| SOCIAL MEDIA | outbound only | Instagram, Facebook and similar, published to | a marketing channel, not a system at all |

INVOICE is the sharpest case. It is the only box drawn bidirectionally that
plausibly is not a system: eTSU issuing an invoice is an output, and nothing
obvious flows back. Either an external accounting system is in play and nobody
named it, or the return arrow means something else entirely.

No arrow on the sketch carries a label, so none of this can be read off the
drawing — the same defect [[ISS-011-context-flows-inferred-not-sourced]] records
against the other diagram.

**Options.**
1. **Ask which four systems were meant and name the vendors or system classes.**
   Recommended — one sentence per box, and it settles the `EIF`-vs-`DM` question
   for all four at once.
2. Type them by default as systems, since they are drawn as boxes. Fast, but it
   would create an "Invoice" external interface that may not exist.
3. Leave all four untyped until [[ISS-018-competing-context-diagrams]] closes.

**Resolution.** *Open.*
