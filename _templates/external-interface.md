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
tier:                # optional: supply | support | demand | core-operations — band of the source context diagram this node came from (ADR-0026)
short_title:         # optional: SHORT label for the projected diagram's node (`partner` is a sentence and would swamp it). Empty -> `title`.
flows:               # one entry per data flow; a neighbour may have several and/or both directions
  - { data: <payload>, direction: inbound, format: <protocol / format, if known>, trigger: <who initiates & when, optional>, label: <one or two words for the diagram edge, optional> }
# A neighbour with flows in BOTH directions draws ONE line on the projected
# diagram, labelled with the `label:` values in the order written (duplicates
# collapse); both directions are spelled out in the flow table beneath it
# (ADR-0026). Omit `label:` and the edge falls back to a clipped `data`.
---

# {{title}}

**Purpose.** <Why this interface exists; what it enables.>

**Flows.** <Narrative on the flows in frontmatter: key payload / fields, who initiates and when.>

**Belongs to.** [[CTX-...]]

> [!note] Open points
> <ambiguities → raise as [[ISS-...]]>
