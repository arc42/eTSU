---
id: EIF-014
type: external-interface
title: Regulatory & Compliance
status: draft
created: 2026-09-09
updated: 2026-09-09
sources:
  - "[[SRC-004-ulrich-stuerzlinger-context-diagram]]"
related:
  - "[[CTX-001-etsu-system-context]]"
  - "[[STK-007-customs-authority]]"
  - "[[STK-010-legal-and-accounting]]"
  - "[[GOAL-004-trust-and-authentication]]"
  - "[[EIF-005-fraud-and-security-prevention]]"
  - "[[ISS-012-bundled-eif-nodes-hide-partners]]"
tags: [external-interface]
partner: Tax authorities, AML/KYC providers and law enforcement
tier: core-operations
short_title: Regulators
flows:
  - { data: tax filings, KYC identity data, suspicious activity reports, direction: outbound, format: unknown, trigger: unknown, label: filings }
  - { data: clearances, rulings, watchlist and enforcement notices, direction: inbound, format: unknown, trigger: unknown, label: clearances }
---

# Regulatory & Compliance

**Purpose.** The diagram labels this **"Tax, AML/KYC, law enforcement"** — the
regulatory surface behind [[GOAL-004-trust-and-authentication]]'s "zero
compliance incidents" and the 2029 narrative's 47 jurisdictions.

**Flows.** Bidirectional as drawn; payloads inferred —
[[ISS-011-context-flows-inferred-not-sourced]].

**Belongs to.** [[CTX-001-etsu-system-context]]

> [!note] Three counterparts, and one missing one
> Tax authorities, an AML/KYC provider and law enforcement are three different
> partners with three different interfaces — and AML also appears separately as
> [[EIF-005-fraud-and-security-prevention]], so the same concern is drawn twice.
> [[ISS-012-bundled-eif-nodes-hide-partners]].
>
> **Customs is absent from this diagram entirely.** Yet the brief is explicit
> that each gallery starts customs paperwork ahead of its show, and
> [[STK-007-customs-authority]] holds high influence — a border hold stops a
> [[GLO-002-show|Show]]. Either customs is meant to sit inside this box, or the
> diagram has a gap on the one regulatory interface the brief actually names.
