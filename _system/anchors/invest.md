---
type: anchor
title: INVEST
aliases: [INVEST]
tags: [anchor, user-story]
applies-to: [user-story]
---

# INVEST

Quality criteria for a user story (complements the [[user-story-format]] shape).

- **Independent** — minimal coupling to other stories; can be built in any order.
- **Negotiable** — a basis for conversation, not a rigid contract.
- **Valuable** — delivers value to a stakeholder ([[STK-...]]).
- **Estimable** — clear enough to size.
- **Small** — fits comfortably in one iteration; if not, split it.
- **Testable** — has acceptance criteria that can pass or fail.

## Checklist (audit / grill)
- [ ] No hidden dependency that forces sequencing; if there is → note it or split.
- [ ] Value to a named stakeholder is explicit.
- [ ] Story is estimable; if not, what's missing? → [[ISS-...]].
- [ ] Small enough for one iteration; oversize → propose a split.
- [ ] Testable — acceptance criteria present and verifiable.

A story failing Estimable/Testable is not "ready"; raise an Issue.
