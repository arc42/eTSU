---
id: EIF-005
type: external-interface
title: Fraud & Security Prevention
status: draft
created: 2026-09-09
updated: 2026-09-09
sources:
  - "[[SRC-004-ulrich-stuerzlinger-context-diagram]]"
related:
  - "[[CTX-001-etsu-system-context]]"
  - "[[GOAL-004-trust-and-authentication]]"
  - "[[EIF-014-regulatory-and-compliance]]"
  - "[[ISS-010-system-boundary-undefined]]"
  - "[[GLO-010-aml-screening]]"
  - "[[ISS-012-bundled-eif-nodes-hide-partners]]"
tags: [external-interface]
partner: Fraud detection and AML screening capability
tier: support
short_title: AML screening
flows:
  - { data: transaction and counterparty data for screening, direction: outbound, format: unknown, trigger: "per transaction; unconfirmed", label: screening }
  - { data: risk scores, alerts, blocked-party hits, direction: inbound, format: unknown, trigger: unknown, label: screening }
---

# Fraud & Security Prevention

**Purpose.** The diagram labels this **"AML detection"**. It is the operational
counterpart to the "< 0.5% fraud rate" and "zero compliance incidents" targets
in [[GOAL-004-trust-and-authentication]].

**Flows.** Bidirectional as drawn; payloads inferred —
[[ISS-011-context-flows-inferred-not-sourced]].

**Belongs to.** [[CTX-001-etsu-system-context]]

> [!note] Bought service or own capability?
> If AML screening is bought from a provider, this is a genuine external system
> and one of the few real `EIF` nodes in the diagram. If it is built into eTSU,
> it is a security [[QR-...]] plus backlog. The diagram does not say, and the
> answer changes the architecture. Note it also overlaps the "AML/KYC" listed
> inside [[EIF-014-regulatory-and-compliance]] —
> [[ISS-012-bundled-eif-nodes-hide-partners]].
