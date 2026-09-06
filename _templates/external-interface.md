---
id: EIF-NNN
type: external-interface
title: <Interface / neighbour name>
status: draft        # draft | review | accepted | deprecated
created: {{date}}
updated: {{date}}
sources: []
related: []          # [[CTX-...]] it belongs to, [[UC-...]], [[DM-...]], [[STK-...]]
tags: [external-interface]
partner: <neighbouring SYSTEM on the other side>   # EIF is for real external systems; human roles carry their flows on the [[STK-...]] (ADR-0013)
flows:               # one entry per data flow; a neighbour may have several and/or both directions
  - { data: <payload>, direction: inbound, format: <protocol / format, if known>, trigger: <who initiates & when, optional> }
---

# {{title}}

**Purpose.** <Why this interface exists; what it enables.>

**Flows.** <Narrative on the flows in frontmatter: key payload / fields, who initiates and when.>

**Belongs to.** [[CTX-...]]

> [!note] Open points
> <ambiguities → raise as [[ISS-...]]>
