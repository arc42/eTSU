---
id: EIF-008
type: external-interface
title: Individual Buyers
status: draft
created: 2026-09-09
updated: 2026-09-09
sources:
  - "[[SRC-004-ulrich-stuerzlinger-context-diagram]]"
related:
  - "[[CTX-001-etsu-system-context]]"
  - "[[STK-004-buyer]]"
  - "[[ISS-013-three-way-buyer-segmentation]]"
tags: [external-interface]
partner: Individual retail buyers
tier: demand
short_title: Individual buyers
flows:
  - { data: purchase intent, deposit and balance payment, direction: inbound, format: unknown, trigger: "buyer signs intent to purchase; unconfirmed", label: orders }
  - { data: listings, prices, purchase confirmation and provenance record, direction: outbound, format: unknown, trigger: unknown, label: listings }
---

# Individual Buyers

**Purpose.** The diagram labels this **"Retail purchases"** in the DEMAND tier.

**Flows.** Bidirectional as drawn; payloads inferred —
[[ISS-011-context-flows-inferred-not-sourced]].

**Belongs to.** [[CTX-001-etsu-system-context]]

> [!note] Also a stakeholder; and a third segmentation
> Held as the persona [[STK-004-buyer]] (hidden from the projection via
> `context_role: none`). The diagram splits buyers three ways — individual /
> global online / institutional — which is a **third** cut, different from both
> the brief ("buyer") and the workshop list ("buyers" + "art collectors").
> [[ISS-013-three-way-buyer-segmentation]].
