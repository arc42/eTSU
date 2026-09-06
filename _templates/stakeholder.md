---
id: STK-NNN
type: stakeholder
title: <Role / persona name>
status: draft
created: {{date}}
updated: {{date}}
sources: []
related: []
tags: [stakeholder]
aliases: []          # alternative names / user-category labels, e.g. "Backoffice" (ADR-0010)
role: <job title or system role>
influence: medium    # high | medium | low  (power to shape the system)
interest: medium     # high | medium | low  (stake in the outcome)
provides: []         # data this role supplies INTO the system — inbound context edges (ADR-0013)
receives: []         # data this role gets FROM the system — outbound context edges (ADR-0013)
nature: person       # person | organization — context-diagram shape: person→actor symbol, organization→box (ADR-0014)
context_role:        # context-diagram label / merge key; empty→title, shared value→merged node, 'none'→hidden (ADR-0014)
---

# {{title}}

**Snapshot.** <One-paragraph simplified persona. Not a biography.>

**Goals.** <frame each with [[PAM]] (light) or [[SMART]] (full)>
- <what they want the system to achieve>

**Concerns / pains.**
- <what they fear, dislike, or are blocked by>

**Interactions.** <[[UC-...]] use cases and [[FR-...]] functional requirements they touch.>
