---
id: ISS-024
type: issue
title: Close-out fires when a Show ends, but the brief puts both actions at tour close
status: open
created: 2026-09-09
updated: 2026-09-09
sources:
  - "[[SRC-008-sandra-mayer-beneficiary-stories]]"
  - "[[SRC-007-tsu-brief]]"
related:
  - "[[GLO-002-show]]"
  - "[[GLO-001-tour]]"
  - "[[GLO-006-conservator]]"
  - "[[GLO-021-lending-agreement]]"
  - "[[GLO-011-piece]]"
  - "[[GLO-013-buyer]]"
  - "[[FR-001-view-piece-inventory-and-status]]"
  - "[[ISS-022-tsu-brief-only-partially-ingested]]"
  - "[[FR-006-tour-visibility]]"
  - "[[DM-001-tour]]"
  - "[[FR-029-keep-a-bought-piece-safe-until-handover]]"
tags: [issue]
severity: major
kind: contradiction
raised-by: agent
resolved: null
---

# Close-out fires when a Show ends, but the brief puts both actions at tour close

**What's unresolved.** *Exhibition* now means [[GLO-002-show|Show]], decided by
Gernot Starke on 2026-09-09. That settles the **word** and, in doing so, exposes
a **contradiction** the word had been hiding: Sandra Mayer's close-out event
fires at the end of a Show, while the brief puts both of its actions at the end
of the **[[GLO-001-tour|Tour]]**.

**Affects.** [[GLO-002-show]], [[GLO-001-tour]],
[[FR-001-view-piece-inventory-and-status]] and the piece state model behind it,
[[GLO-021-lending-agreement]], and whatever activity model eventually describes
close-out.

**Context / evidence.** Two actions, two sources, two different moments:

| Action | [[SRC-008-sandra-mayer-beneficiary-stories]] | [[SRC-007-tsu-brief]] |
|---|---|---|
| Conservation | "Send art to cleaners and restorers" when the exhibition ends, i.e. **per Show** | the lending agreement covers "the cleaning at the end of the tour", i.e. **once per Tour** |
| Release to buyer | "Check what art can be sent to buyers" when the exhibition ends, i.e. **per Show** | "We don't let the buyer take the piece until the tour is over" — explicit, and **per Tour** |

The second row is the sharp one. The brief does not merely imply tour-close
delivery; it states it as a rule of the business. If close-out really runs at
every Show, then a piece sold at the first stop of a six-stop tour goes to its
buyer immediately, and the brief's rule is wrong or has changed.

The first row costs money rather than contradicting a rule. Conservation per
Show means engaging a [[GLO-006-conservator|conservator]] at every stop instead
of once, against a [[GLO-021-lending-agreement|lending agreement]] that
provides for one treatment at tour close.

A third reading exists and neither source states it: **close-out runs at every
Show but does different things** — condition checks and repacking at each stop,
conservation and delivery only at the last one. That would reconcile both
sources, which is exactly why it should not be adopted without someone
confirming it.

**Options.**
1. **Ask Sandra Mayer whether she meant one stop or the whole tour.** Recommended
   — it is one question to a known author, and the answer decides a business rule
   rather than a wording preference.
2. Adopt the third reading, one close-out procedure per Show whose steps depend
   on whether it is the last one. Plausible and tidy, but invented here.
3. Treat the brief as authoritative and the story as loose phrasing. Cheap, and
   it discards a workshop contribution on the agent's say-so.

**Resolution.** *Open.* Note the naming half is already decided: *exhibition* is
an alias on [[GLO-002-show]]. Only the timing is in dispute.
