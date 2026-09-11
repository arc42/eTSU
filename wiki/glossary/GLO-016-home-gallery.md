---
id: GLO-016
type: glossary-term
title: Home gallery
status: draft
created: 2026-09-09
updated: 2026-09-09
sources:
  - "[[SRC-007-tsu-brief]]"
related:
  - "[[GLO-015-gallery]]"
  - "[[GLO-001-tour]]"
  - "[[GLO-009-logistics-partner]]"
  - "[[STK-005-shipper]]"
  - "[[GLO-011-piece]]"
  - "[[FR-015-tour-scheduling]]"
tags: [glossary]
aliases: []
bounded-context: Gallery Touring
agreed: false
stereotype: entity
---

# Home gallery

**Definition.** The one [[GLO-015-gallery|gallery]] where a
[[GLO-001-tour|Tour]] begins and where every [[GLO-011-piece|piece]] returns
when it ends.

**In context.** This is a **per-tour role**, not a property of a gallery: the
same venue may be home for one tour and an ordinary stop on the next. It matters
because shipping and insurance are arranged **from and to the home gallery for
the entire tour**, so it is the fixed point the whole logistics contract is
written against ([[GLO-009-logistics-partner]]).

**Distinguish from.** The Head Office in New York, where Gus Renoir works. The
brief never says the two are the same place, and nothing suggests the head
office holds pieces.

> [!note] Notes
> `agreed: false` — sourced from the brief. Open: whether a sold piece also
> returns to the home gallery before going to its buyer, or ships directly from
> wherever the tour ended. The brief says only that the buyer waits until the
> tour is over.
