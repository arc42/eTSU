---
id: EIF-004
type: external-interface
title: Customer Support & Marketing
status: deprecated
created: 2026-09-09
updated: 2026-09-09
sources:
  - "[[SRC-004-ulrich-stuerzlinger-context-diagram]]"
related:
  - "[[CTX-001-etsu-system-context]]"
  - "[[ISS-010-system-boundary-undefined]]"
tags: [external-interface]
partner: Customer support and marketing function (24/7, SEO, social)
tier: support
short_title: Support/marketing
flows:
  - { data: campaign, SEO and social content; inbound support cases, direction: inbound, format: unknown, trigger: unknown, label: campaigns }
  - { data: catalogue, tour and customer data for campaigns and case handling, direction: outbound, format: unknown, trigger: unknown, label: cases }
---

# Customer Support & Marketing

**Purpose.** The diagram's SUPPORT & ENABLEMENT tier, labelled **"24/7, SEO,
social"**.

**Flows.** Bidirectional as drawn; payloads inferred —
[[ISS-011-context-flows-inferred-not-sourced]].

**Belongs to.** [[CTX-001-etsu-system-context]]

> [!note] Is this actually external?
> "24/7 support, SEO, social" reads as a **TSU function or an eTSU capability**,
> not a neighbouring system — it is modelled as an interface because the diagram
> draws it outside the box. If it is internal, "24/7" is a
> [[QR-...]] availability requirement and the rest is backlog, not an interface.
> [[ISS-010-system-boundary-undefined]].

> [!warning] Deprecated 2026-09-09 — inside the boundary
> [[STK-001-gus-renoir]] confirmed that placing TSU's own operations outside the
> system boundary was a **drawing mistake** in
> [[SRC-004-ulrich-stuerzlinger-context-diagram]], closing
> [[ISS-010-system-boundary-undefined]]. Customer support and marketing are TSU functions, not neighbouring systems. Any 24/7 availability claim belongs in a Quality requirement and any SEO or social-media reach target in a Goal.
>
> This page is kept, not deleted, so the workshop artefact stays readable and the
> decision is traceable. Its requirements belong in `FR`/`QR` pages, not here.
