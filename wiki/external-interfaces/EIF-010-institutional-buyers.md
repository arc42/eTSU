---
id: EIF-010
type: external-interface
title: Institutional Buyers
status: draft
created: 2026-09-09
updated: 2026-09-09
sources:
  - "[[SRC-004-ulrich-stuerzlinger-context-diagram]]"
related:
  - "[[CTX-001-etsu-system-context]]"
  - "[[STK-008-museum]]"
  - "[[EIF-002-museums-and-owners]]"
  - "[[GOAL-004-trust-and-authentication]]"
  - "[[ISS-013-three-way-buyer-segmentation]]"
tags: [external-interface]
partner: Institutional buyers — museums and corporate collections
tier: demand
short_title: Institutional buyers
flows:
  - { data: institutional purchase intent and acquisition approval, direction: inbound, format: unknown, trigger: unknown, label: orders }
  - { data: institutional pricing and provenance dossier, direction: outbound, format: unknown, trigger: unknown, label: pricing }
---

# Institutional Buyers

**Purpose.** The diagram labels this **"Museums, corps"**. The 2029 narrative
puts museums at 30% of transaction volume, contingent on the verification
coverage in [[GOAL-004-trust-and-authentication]].

**Flows.** Bidirectional as drawn; payloads inferred —
[[ISS-011-context-flows-inferred-not-sourced]].

**Belongs to.** [[CTX-001-etsu-system-context]]

> [!note] The same museum appears twice in this diagram
> A museum lends pieces ([[EIF-002-museums-and-owners]], SUPPLY tier) **and**
> buys them (here, DEMAND tier) — and buys at the *minimum museum sale price*,
> which is below the private-buyer minimum. The diagram splits one party across
> two tiers without saying they are the same counterpart.
> [[ISS-012-bundled-eif-nodes-hide-partners]] and [[STK-008-museum]] both carry
> this. "Corporate collections" is new and appears in no other source.
