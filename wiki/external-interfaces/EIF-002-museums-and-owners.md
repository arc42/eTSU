---
id: EIF-002
type: external-interface
title: Museums & Owners
status: draft
created: 2026-09-09
updated: 2026-09-09
sources:
  - "[[SRC-004-ulrich-stuerzlinger-context-diagram]]"
related:
  - "[[CTX-001-etsu-system-context]]"
  - "[[STK-008-museum]]"
  - "[[STK-013-private-owner]]"
  - "[[ISS-012-bundled-eif-nodes-hide-partners]]"
tags: [external-interface]
partner: Museums and private owners who lend artwork
tier: supply
short_title: Lenders
flows:
  - { data: artwork lent to a tour, plus lending-agreement terms, direction: inbound, format: unknown, trigger: "lending agreement signed; unconfirmed", label: loans }
  - { data: loan status, location, condition and insurance confirmation, direction: outbound, format: unknown, trigger: unknown, label: loan status }
---

# Museums & Owners

**Purpose.** Not every piece on tour is for sale; some are on loan. The diagram
labels this node **"Lend artwork"**.

**Flows.** Bidirectional as drawn. Payloads inferred from the box label —
[[ISS-011-context-flows-inferred-not-sourced]].

**Belongs to.** [[CTX-001-etsu-system-context]]

> [!note] Two partners in one node
> This box fuses [[STK-008-museum|museums]] and
> [[STK-013-private-owner|private owners]] — different parties with different
> agreements, and a museum is *also* a buyer (see [[EIF-010-institutional-buyers]]).
> `partner:` should name one neighbour (ADR-0013);
> [[ISS-012-bundled-eif-nodes-hide-partners]] tracks the split.
