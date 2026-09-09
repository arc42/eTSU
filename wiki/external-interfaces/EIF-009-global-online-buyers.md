---
id: EIF-009
type: external-interface
title: Global Online Buyers
status: draft
created: 2026-09-09
updated: 2026-09-09
sources:
  - "[[SRC-004-ulrich-stuerzlinger-context-diagram]]"
related:
  - "[[CTX-001-etsu-system-context]]"
  - "[[STK-004-buyer]]"
  - "[[GOAL-002-global-market-expansion]]"
  - "[[ISS-004-scope-inflation-marketplace-vs-back-office]]"
  - "[[ISS-013-three-way-buyer-segmentation]]"
tags: [external-interface]
partner: Buyers in new geographic markets, transacting online
tier: demand
short_title: Online buyers
flows:
  - { data: online purchase intent and payment, direction: inbound, format: unknown, trigger: unknown, label: orders }
  - { data: listings, prices, confirmation and provenance record, direction: outbound, format: unknown, trigger: unknown, label: listings }
---

# Global Online Buyers

**Purpose.** The diagram labels this **"New markets"** — the demand side of
[[GOAL-002-global-market-expansion]] (5,000+ online buyers in Year 1).

**Flows.** Bidirectional as drawn; payloads inferred —
[[ISS-011-context-flows-inferred-not-sourced]].

**Belongs to.** [[CTX-001-etsu-system-context]]

> [!note] This node presumes the marketplace reading
> A buyer who transacts online, unseen, in a new market **only exists under
> Reading B** of [[ISS-004-scope-inflation-marketplace-vs-back-office]]. Under
> Reading A (back-office digitisation) this node does not exist at all — the
> brief's sale happens in person, over champagne, in a gallery back office.
> The diagram's own system box reading *"Gallery platform & digital
> marketplace"* is corroborating evidence for Reading B, but one participant's
> drawing is not the group's decision.
