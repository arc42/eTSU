---
id: EIF-007
type: external-interface
title: Data & Analytics
status: deprecated
created: 2026-09-09
updated: 2026-09-09
sources:
  - "[[SRC-004-ulrich-stuerzlinger-context-diagram]]"
related:
  - "[[CTX-001-etsu-system-context]]"
  - "[[ISS-010-system-boundary-undefined]]"
tags: [external-interface]
partner: Business intelligence and analytics function
tier: support
short_title: Analytics
flows:
  - { data: operational, catalogue and transaction data, direction: outbound, format: unknown, trigger: unknown, label: data }
  - { data: BI reports and insights, direction: inbound, format: unknown, trigger: unknown, label: insights }
---

# Data & Analytics

**Purpose.** The diagram labels this **"BI, insights"**.

**Flows.** Bidirectional as drawn; payloads inferred —
[[ISS-011-context-flows-inferred-not-sourced]].

**Belongs to.** [[CTX-001-etsu-system-context]]

> [!note] Most likely a capability, not a neighbour
> Of all fourteen boxes this is the least interface-shaped: analytics over eTSU's
> own data is normally *part of* eTSU. Modelled as an interface only because the
> diagram draws it outside the box. Strongest candidate for reclassification
> under [[ISS-010-system-boundary-undefined]] — and note that the metrics in
> [[GOAL-002-global-market-expansion]] and [[GOAL-003-operational-excellence]]
> cannot be measured *at all* without whatever this turns out to be.

> [!warning] Deprecated 2026-09-09 — inside the boundary
> [[STK-001-gus-renoir]] confirmed that placing TSU's own operations outside the
> system boundary was a **drawing mistake** in
> [[SRC-004-ulrich-stuerzlinger-context-diagram]], closing
> [[ISS-010-system-boundary-undefined]]. Analytics over eTSU's own data is an eTSU capability. Every metric in `wiki/goals/` depends on it, which makes it internal by definition.
>
> This page is kept, not deleted, so the workshop artefact stays readable and the
> decision is traceable. Its requirements belong in `FR`/`QR` pages, not here.
