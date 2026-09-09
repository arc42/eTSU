---
id: EIF-011
type: external-interface
title: Gallery Operations
status: deprecated
created: 2026-09-09
updated: 2026-09-09
sources:
  - "[[SRC-004-ulrich-stuerzlinger-context-diagram]]"
related:
  - "[[CTX-001-etsu-system-context]]"
  - "[[STK-003-gallery-manager]]"
  - "[[GLO-004-tsu]]"
  - "[[GLO-002-show]]"
  - "[[ISS-010-system-boundary-undefined]]"
tags: [external-interface]
partner: TSU's own gallery network — 6 locations, staff and events
tier: core-operations
short_title: Galleries
flows:
  - { data: show schedules, price lists, piece assignments, customs and publicity lead times, direction: outbound, format: unknown, trigger: "tour confirmed; unconfirmed", label: schedules }
  - { data: local sales, piece status, event and footfall data, direction: inbound, format: unknown, trigger: unknown, label: sales }
---

# Gallery Operations

**Purpose.** The diagram labels this **"6 locations, staff, events"** — the
physical gallery network where every [[GLO-002-show|Show]] happens.

**Flows.** Bidirectional as drawn; payloads inferred —
[[ISS-011-context-flows-inferred-not-sourced]].

**Belongs to.** [[CTX-001-etsu-system-context]]

> [!note] New fact: six locations
> **No earlier source states how many galleries TSU has.** The brief says only
> "one of our galleries" and "each TSU gallery". This diagram is the first to
> give a number — **6** — and it should be confirmed before anything depends on
> it (tour length, shipping legs, rollout scope).

> [!note] This is TSU itself, drawn as a neighbour
> [[GLO-004-tsu|TSU]] *is* the gallery network. Modelling it as an external
> interface says eTSU is a system that the galleries talk *to* rather than a
> system the galleries *use* — which is the opposite of the brief's premise.
> Retained because the diagram draws it outside the box under a heading that
> calls it CORE. This is the sharpest instance of
> [[ISS-010-system-boundary-undefined]].

> [!warning] Deprecated 2026-09-09 — inside the boundary
> [[STK-001-gus-renoir]] confirmed that placing TSU's own operations outside the
> system boundary was a **drawing mistake** in
> [[SRC-004-ulrich-stuerzlinger-context-diagram]], closing
> [[ISS-010-system-boundary-undefined]]. [[GLO-004-tsu|TSU]] *is* the gallery network. The galleries **use** eTSU; they do not exchange data with it across a boundary. The "6 locations" figure is still the only source for the gallery count and is preserved here rather than lost with the node.
>
> This page is kept, not deleted, so the workshop artefact stays readable and the
> decision is traceable. Its requirements belong in `FR`/`QR` pages, not here.
