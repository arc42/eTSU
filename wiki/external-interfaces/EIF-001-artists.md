---
id: EIF-001
type: external-interface
title: Artists
status: draft
created: 2026-09-09
updated: 2026-09-09
sources:
  - "[[SRC-004-ulrich-stuerzlinger-context-diagram]]"
related:
  - "[[CTX-001-etsu-system-context]]"
  - "[[STK-002-artist]]"
  - "[[ISS-011-context-flows-inferred-not-sourced]]"
tags: [external-interface]
partner: Artists — individual creators who submit work
tier: supply
short_title: Artists
flows:
  - { data: artwork submissions and tour participation, direction: inbound, format: unknown, trigger: "artist submits; unconfirmed", label: artwork }
  - { data: sale notifications and commission statements, direction: outbound, format: unknown, trigger: "on sale; unconfirmed", label: sales }
---

# Artists

**Purpose.** The supply side of the platform: creators submit work that becomes
the content of a [[GLO-001-tour|Tour]]. The diagram labels this node
**"Create & submit"** and places it in the SUPPLY tier.

**Flows.** Solid (outbound from the artist into eTSU) and dashed (return) arrows
are both drawn, so the relationship is bidirectional. The payloads above are
**read off the box label, not off the arrows** — the diagram labels no arrow.
See [[ISS-011-context-flows-inferred-not-sourced]].

**Belongs to.** [[CTX-001-etsu-system-context]]

> [!note] Also a stakeholder
> The same actor is held as the persona [[STK-002-artist]]. Per this ingest's
> decision (ADR-0026) the **edge lives here**; the stakeholder keeps the persona
> and is hidden from the context projection via `context_role: none` (ADR-0014).
