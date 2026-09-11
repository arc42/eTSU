---
id: EIF-013
type: external-interface
title: Technology & Infrastructure
status: draft
created: 2026-09-09
updated: 2026-09-09
sources:
  - "[[SRC-004-ulrich-stuerzlinger-context-diagram]]"
related:
  - "[[CTX-001-etsu-system-context]]"
  - "[[ISS-010-system-boundary-undefined]]"
  - "[[ISS-012-bundled-eif-nodes-hide-partners]]"
  - "[[ISS-011-context-flows-inferred-not-sourced]]"
  - "[[ISS-020-sketch-boxes-untyped]]"
tags: [external-interface]
partner: Payment service provider
tier: core-operations
short_title: Payments
flows:
  - { data: payment authorisation and settlement requests, direction: outbound, format: unknown, trigger: "buyer pays deposit or balance; unconfirmed", label: payments }
  - { data: payment confirmations, failures and chargebacks, direction: inbound, format: unknown, trigger: unknown, label: payments }
---

# Technology & Infrastructure

**Purpose.** The diagram labels this **"Cloud, payments, security, CDN"**.

**Flows.** Only the *payment* flows are modelled above, because they are the
only ones that are interface-shaped. Payloads inferred —
[[ISS-011-context-flows-inferred-not-sourced]].

**Belongs to.** [[CTX-001-etsu-system-context]]

> [!note] One real neighbour hidden inside three non-neighbours
> **Payments** is a genuine external system — a payment service provider eTSU
> must integrate with, and the one that makes the brief's deposit/balance
> sequence (10% within 24 h, 90% within 14 days, half the deposit forfeited on
> default) actually enforceable.
>
> **Cloud, CDN and security** are not neighbours at all — they are *how eTSU is
> deployed*. A context diagram shows what the system exchanges data **with**,
> not what it **runs on**; putting infrastructure at the boundary is a category
> error that would propagate into the architecture if left.
> [[ISS-012-bundled-eif-nodes-hide-partners]].

> [!note] Narrowed 2026-09-09 — payments only
> Under the same decision that closed [[ISS-010-system-boundary-undefined]], the
> cloud, CDN and security halves of this box are **inside** the boundary and were
> dropped. `partner:` is now the payment service provider alone, which is what
> the flows above already described. The node survives where the other three
> core-operations nodes did not, because a payment provider is a real external
> system.
