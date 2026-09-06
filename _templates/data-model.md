---
id: DM-NNN
type: data-model
title: <Entity / value-object / sum-type name>
status: draft
created: {{date}}
updated: {{date}}
sources: []
related: []           # [[GLO-...]] glossary anchor(s) for the same concept; [[STK-...]] / [[FR-...]] consumers
tags: [data-model]
stereotype: entity    # entity | value-object | sum-type   (product types vs. tagged union, ADR-0019)
parent: []            # [[DM-...]] — used by sum-type variants to point at their sum-type; empty for top-level
bounded-context: <context name>
source-of-truth: <system/owner of this data>
---

# {{title}}

<!-- One file = one entity / value-object / sum-type (ADR-0019). NOT a whole aggregate.
     Stereotypes:
       entity       — product type WITH identity (lifecycle, key)
       value-object — product type WITHOUT identity (equality by value)
       sum-type     — tagged union; variants live as separate DM files with `parent:` ↑
     Enum-style sums with no payload (e.g. `Start.status ∈ {geplant, …}`) stay INLINE
     as attribute types — don't create stand-alone DM files for them. -->

**Purpose.** <What this represents and why it exists.>

**Identity.** <Key attribute(s); omit for value-object and sum-type.>

**Attributes.**
- <name> : <type> <mandatory?> — <note>

**Relationships.**
- <verb> → [[DM-...]] · <cardinality> · <association | aggregation | composition | inheritance> · <mandatory?>

**Invariants / rules.**
- <business rule the data must satisfy>

> [!note] Open points
> <ambiguities → raise as [[ISS-...]]>
