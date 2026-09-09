---
id: EIF-012
type: external-interface
title: Logistics & Fulfillment
status: draft
created: 2026-09-09
updated: 2026-09-09
sources:
  - "[[SRC-004-ulrich-stuerzlinger-context-diagram]]"
related:
  - "[[CTX-001-etsu-system-context]]"
  - "[[STK-005-shipper]]"
  - "[[STK-006-insurer]]"
  - "[[STK-009-conservator]]"
  - "[[ISS-012-bundled-eif-nodes-hide-partners]]"
tags: [external-interface]
partner: Shipping, insurance and restoration providers
tier: core-operations
short_title: Logistics
flows:
  - { data: tour manifests, routing schedules, insured values, restoration obligations, direction: outbound, format: unknown, trigger: "tour goes ahead; unconfirmed", label: manifests }
  - { data: shipment status, insurance policies and claim settlements, condition reports, direction: inbound, format: unknown, trigger: unknown, label: status }
---

# Logistics & Fulfillment

**Purpose.** The diagram labels this **"Shipping, insurance, restoration"** —
everything that physically moves and protects a piece for the duration of a
[[GLO-001-tour|Tour]].

**Flows.** Bidirectional as drawn; payloads inferred —
[[ISS-011-context-flows-inferred-not-sourced]].

**Belongs to.** [[CTX-001-etsu-system-context]]

> [!note] Three distinct partners fused into one node
> This box collapses [[STK-005-shipper]], [[STK-006-insurer]] and
> [[STK-009-conservator]] — three separate companies under three separate
> contracts. It matters that they are separate: the brief fixes **one shipper
> and one insurer per entire Tour** (those companies demand to work that way),
> while the restorer is engaged **per lending agreement, at tour close**.
> Different counterparts, different cardinality, different triggers. `partner:`
> is supposed to name one neighbour (ADR-0013) —
> [[ISS-012-bundled-eif-nodes-hide-partners]] tracks the split into three nodes.
