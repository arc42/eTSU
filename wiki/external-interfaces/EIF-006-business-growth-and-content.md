---
id: EIF-006
type: external-interface
title: Business Growth & Content
status: deprecated
created: 2026-09-09
updated: 2026-09-09
sources:
  - "[[SRC-004-ulrich-stuerzlinger-context-diagram]]"
related:
  - "[[CTX-001-etsu-system-context]]"
  - "[[ISS-010-system-boundary-undefined]]"
  - "[[FR-021-upload-piece-images]]"
tags: [external-interface]
partner: Content production — photography and 3D capture
tier: support
short_title: Content production
flows:
  - { data: photography, 3D captures and media assets for pieces, direction: inbound, format: unknown, trigger: "piece enters a tour; unconfirmed", label: media assets }
  - { data: piece lists and shoot briefs, direction: outbound, format: unknown, trigger: unknown, label: shoot briefs }
---

# Business Growth & Content

**Purpose.** The diagram labels this **"Photography, 3D"** — producing the
imagery a remote buyer would need in order to buy a piece they cannot stand in
front of.

**Flows.** Bidirectional as drawn; payloads inferred —
[[ISS-011-context-flows-inferred-not-sourced]].

**Belongs to.** [[CTX-001-etsu-system-context]]

> [!note] Two things in one box
> "Business growth" (a commercial objective) and "photography / 3D" (a content
> production service) are unrelated. Only the second is interface-shaped — a
> photography studio is a plausible external supplier. The first belongs in
> `wiki/goals/`. [[ISS-010-system-boundary-undefined]].

> [!warning] Deprecated 2026-09-09 — inside the boundary
> [[STK-001-gus-renoir]] confirmed that placing TSU's own operations outside the
> system boundary was a **drawing mistake** in
> [[SRC-004-ulrich-stuerzlinger-context-diagram]], closing
> [[ISS-010-system-boundary-undefined]]. "Business growth" is an objective, not a neighbour, and content production is an internal function. The one genuinely external part — a photography and 3D capture supplier — is *not* carried forward by this page; whether it deserves its own node is held in [[ISS-012-bundled-eif-nodes-hide-partners]].
>
> This page is kept, not deleted, so the workshop artefact stays readable and the
> decision is traceable. Its requirements belong in `FR`/`QR` pages, not here.
