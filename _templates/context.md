---
id: CTX-NNN
type: context
title: <System context name>
status: draft        # draft | review | accepted | deprecated
created: {{date}}
updated: {{date}}
sources: []
related: []          # [[EIF-...]] interfaces, [[STK-...]] roles
tags: [context]
kind: business       # business | technical
diagram: generated   # projected on-the-fly from EIF.flows + STK.provides/receives; not stored (ADR-0013, ISS-010)
---

# {{title}}

**Diagram.** _Projected_ — generated from the external interfaces (`EIF.flows`) and the
user roles' `provides:`/`receives:` edges (ADR-0013, [[ISS-010-context-diagram-projection-audit-loop]]);
not hand-maintained here.

**In scope.** <One paragraph: what the system IS responsible for delivering.>

**Out of scope.** <What the system is explicitly NOT supposed to do or
deliver. State each non-goal plainly; this is the delimitation, not a wish list.>
- <non-goal>

**External interfaces.** <each neighbour is its own node>
- [[EIF-...]] — <partner · direction · what flows>

**User roles.** <external human actors of the system; link existing stakeholders>
- [[STK-...]] — <how they interact with the system>

**Explanation.** <Narrative tying the diagram together: which neighbours matter and why.>

> [!note] Open points
> <ambiguities or missing neighbours → raise as [[ISS-...]]>
