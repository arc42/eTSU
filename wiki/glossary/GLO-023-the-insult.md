---
id: GLO-023
type: glossary-term
title: The Insult
status: draft
created: 2026-09-09
updated: 2026-09-09
sources:
  - "[[SRC-007-tsu-brief]]"
related:
  - "[[GLO-022-intent-to-purchase]]"
  - "[[GLO-013-buyer]]"
  - "[[GLO-019-agreed-price]]"
  - "[[GLO-011-piece]]"
  - "[[ISS-022-tsu-brief-only-partially-ingested]]"
  - "[[FR-007-settlement-and-compliance]]"
  - "[[GOAL-006-settlement-correct-and-on-time]]"
  - "[[FR-010-settle-a-failed-purchase]]"
tags: [glossary]
aliases: []
bounded-context: Settlement
agreed: false
stereotype: value-object
---

# The Insult

**Definition.** The half of the deposit **returned** to a
[[GLO-013-buyer|buyer]] who paid the 10% and then failed to pay the remaining
90% within 14 days. TSU keeps the other half; the returned half is what the
business calls The Insult.

**In context.** In-house jargon, and worth an entry precisely because it names
the **refund**, not the forfeit. Anyone reading it the other way round will
compute the wrong number: 5% of the [[GLO-019-agreed-price|agreed price]] goes
back to the failed buyer, 5% stays with TSU, and the
[[GLO-011-piece|piece]] returns to the market.

**Distinguish from.** Missing the **first** deadline, the 10% within 24 hours.
That costs nothing at all: no money has changed hands, so the piece simply
becomes available again with no Insult to pay.

> [!note] Notes
> `agreed: false` — sourced from the brief, in Gus Renoir's own words: "This
> returned money is known in our business as 'The Insult.'" Kept with its
> capital letters because it is a proper name in the ubiquitous language, not a
> description.
