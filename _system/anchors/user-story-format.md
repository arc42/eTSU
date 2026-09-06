---
type: anchor
title: User-Story Format
aliases: [user-story-format, story-format]
tags: [anchor, user-story]
applies-to: [user-story]
---

# User-Story Format

The canonical shape of a user story. Quality of a story is judged separately by
[[INVEST]]; priority by [[MoSCoW]].

**Role–goal–benefit:**
> **As a** \<role / [[STK-...]]\> **I want** \<capability\> **so that** \<benefit\>.

**Acceptance criteria** use Given–When–Then:
> **Given** \<context\>, **when** \<action\>, **then** \<outcome\>.

## Checklist (audit / grill)
- [ ] Role is a real stakeholder ([[STK-...]]), not "user" by default.
- [ ] Benefit ("so that") is present and non-circular — it states *why*, not a restated *what*.
- [ ] At least one acceptance criterion, in Given–When–Then form.
- [ ] Criteria are observable/verifiable, not opinions.
