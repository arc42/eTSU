---
id: ISS-021
type: issue
title: "The \"authentication\" card could mean artwork authentication or user log-in"
status: open
created: 2026-09-09
updated: 2026-09-09
sources:
  - "[[SRC-005-workshop-capability-card-wall]]"
related:
  - "[[ISS-017-twelve-candidate-capabilities-undefined]]"
  - "[[GOAL-004-trust-and-authentication]]"
  - "[[EIF-003-appraisers-and-authenticators]]"
  - "[[GLO-003-provenance]]"
tags: [issue]
severity: major
kind: ambiguity
raised-by: agent
resolved: null
---

# The "authentication" card could mean artwork authentication or user log-in

**What's unresolved.** One card reads `authentication`, with nothing else on it.
In this domain the word has two established and unrelated meanings, and the two
land in different parts of the wiki.

**Affects.** [[ISS-017-twelve-candidate-capabilities-undefined]] card 11, and
[[GOAL-004-trust-and-authentication]], whose measurable target assumes the first
reading.

**Context / evidence.**

- **Artwork authentication** — establishing that a piece is genuine and its
  [[GLO-003-provenance|provenance]] holds. This is the sense in
  [[GOAL-004-trust-and-authentication]] ("≥ 90% verification coverage") and the
  sense behind [[EIF-003-appraisers-and-authenticators]]. It is a
  Functional requirement with a whole workflow behind it: request, expert
  opinion, certificate, chain of custody.
- **User authentication** — logging a person into eTSU. That is a
  Quality requirement under ISO 25010 security, not a backlog epic, and it would
  be unremarkable enough that nobody would card it.

The card's neighbours on the table are `payment handling`, `contract handling`
and `insurance claim handling` — all business process cards, none of them
technical. That is weak evidence for the artwork reading, but it is evidence,
and it is the reading this wiki would otherwise assume by default. Recording it
rather than assuming it, because the cost of guessing wrong is a missing security
requirement.

**Options.**
1. **Confirm the artwork reading and rename the capability "Artwork
   Authentication".** Recommended — it removes the collision with the security
   sense permanently, and the glossary should gain the term either way.
2. Both were meant, on one card. Split into a Functional requirement and a
   Quality requirement.
3. The security reading was meant, and artwork authentication is simply missing
   from the card wall — which would itself be a gap worth recording.

**Resolution.** *Open.*
