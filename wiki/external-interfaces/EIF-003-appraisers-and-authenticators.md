---
id: EIF-003
type: external-interface
title: Appraisers & Authenticators
status: draft
created: 2026-09-09
updated: 2026-09-09
sources:
  - "[[SRC-004-ulrich-stuerzlinger-context-diagram]]"
related:
  - "[[CTX-001-etsu-system-context]]"
  - "[[GOAL-004-trust-and-authentication]]"
  - "[[GLO-003-provenance]]"
tags: [external-interface]
partner: Independent appraisers and authentication bodies
tier: supply
short_title: Appraisers
flows:
  - { data: verification request — piece identity and supporting documentation, direction: outbound, format: unknown, trigger: "piece enters the catalogue; unconfirmed", label: verification }
  - { data: provenance verification result / certificate of authenticity, direction: inbound, format: unknown, trigger: unknown, label: verification }
---

# Appraisers & Authenticators

**Purpose.** The node the whole of [[GOAL-004-trust-and-authentication]] depends
on: an independent party that establishes whether a piece's
[[GLO-003-provenance|provenance]] holds. The diagram labels it **"Verify
provenance"**.

**Flows.** Bidirectional as drawn. Payloads inferred —
[[ISS-011-context-flows-inferred-not-sourced]].

**Belongs to.** [[CTX-001-etsu-system-context]]

> [!note] New party, no stakeholder page
> This actor appears in **no earlier source** — not in the TSU brief, not in the
> Req4Arc Linz stakeholder list. It is the first concrete counterpart for the
> ≥ 90% verification-coverage target in [[GOAL-004-trust-and-authentication]].
>
> Open: is this a **service TSU buys** (an appraiser firm), or the **register
> lookup** the 2029 narrative names — Art Loss Register, Interpol? Those are
> different neighbours with very different interfaces, and no source says which.
