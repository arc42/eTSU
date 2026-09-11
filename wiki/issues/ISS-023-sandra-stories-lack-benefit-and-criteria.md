---
id: ISS-023
type: issue
title: Backlog stories still lack acceptance criteria; the benefit clauses are now settled
status: open
created: 2026-09-09
updated: 2026-09-09
sources:
  - "[[SRC-008-sandra-mayer-beneficiary-stories]]"
  - "[[SRC-009-workshop-inventory-decomposition]]"
  - "[[SRC-010-workshop-example-mapping-stories]]"
related:
  - "[[FR-001-view-piece-inventory-and-status]]"
  - "[[FR-002-settle-finances-and-legal-obligations]]"
  - "[[FR-003-upload-piece-information]]"
  - "[[FR-004-track-piece-status]]"
  - "[[ISS-017-twelve-candidate-capabilities-undefined]]"
  - "[[FR-007-settlement-and-compliance]]"
  - "[[FR-005-piece-management]]"
  - "[[FR-006-tour-visibility]]"
  - "[[FR-019-create-the-piece-inventory]]"
  - "[[FR-022-display-current-piece-information]]"
  - "[[FR-024-list-filter-search-and-sort-pieces]]"
tags: [issue]
severity: major
kind: gap
raised-by: agent
resolved: null
---

# Backlog stories still lack acceptance criteria; the benefit clauses are now settled

**What's unresolved.** Four stories entered the backlog on 2026-09-09 in
role-and-want form. **None states why**, and **none is testable.** Under
[[user-story-format]] a story needs a non-circular "so that" and at least one
Given-When-Then criterion; all four fail both checks. Enforcement here is
advisory, so the stories were written as given and the gap recorded rather than
filled in — the benefit lines are deliberately empty on the pages.

**Affects.** [[FR-001-view-piece-inventory-and-status]],
[[FR-002-settle-finances-and-legal-obligations]],
[[FR-003-upload-piece-information]], [[FR-004-track-piece-status]] — the entire
backlog as it currently stands.

**Context / evidence.** Verbatim from
[[SRC-008-sandra-mayer-beneficiary-stories]], with the [[INVEST]] letters each
one fails:

| Page | As written | Fails |
|---|---|---|
| ~~[[FR-001-view-piece-inventory-and-status]]~~ | "As Gus I want an overview of an inventory and status of each item." | **retired 2026-09-09**, decomposed into two features |
| ~~[[FR-002-settle-finances-and-legal-obligations]]~~ | "As Gus I want finances and legals taken care of" | **V**aluable, **T**estable, **S**mall, **E**stimable — **retired 2026-09-09** |
| [[FR-003-upload-piece-information]] | "As an artist I want to upload information about my artwork" | ~~**V**aluable~~ **settled 2026-09-09**; still **T**estable |
| [[FR-004-track-piece-status]] | "As artist I want an updated status of my artwork" | ~~**V**aluable~~ **settled 2026-09-09**; still **T**estable |

Two problems are worse than the common one.

- **[[FR-002-settle-finances-and-legal-obligations]] was retired on
  2026-09-09**, on Gernot Starke's instruction, into five stories under
  [[FR-007-settlement-and-compliance]]. Those five carry real Given-When-Then
  criteria, because [[SRC-007-tsu-brief]] states the money rules precisely.
  **Only the money rules split cleanly** — contracts, tax and AML had no rule to
  write against, so the "legals" half of the original story is now uncovered;
  that gap is recorded on the epic. The other three stories in this Issue are
  unaffected and still lack both a benefit clause and criteria.
- **Every priority is the template default.** All four carry `priority: Should`
  because the template says so, not because anyone applied [[MoSCoW]]. A backlog
  whose priorities were never set is not prioritised, and the default should not
  be mistaken for a decision.

> [!note] Narrowed 2026-09-09 — benefits settled, criteria still missing
> [[SRC-010-workshop-example-mapping-stories]] carries ten cards in **full
> role-goal-benefit form**, and two of them supply the "so that" that
> [[FR-003-upload-piece-information]] and [[FR-004-track-piece-status]] were
> missing. With [[FR-001-view-piece-inventory-and-status]] and
> [[FR-002-settle-finances-and-legal-obligations]] both retired, **the benefit
> half of this Issue is closed.**
>
> **Acceptance criteria are still missing, and the problem got bigger.**
> [[SRC-009-workshop-inventory-decomposition]] added six stories that are bare
> operation cards with neither a role nor a reason —
> [[FR-019-create-the-piece-inventory]], [[FR-020-add-piece-details]],
> [[FR-021-upload-piece-images]], [[FR-022-display-current-piece-information]],
> [[FR-023-modify-piece-location]] and
> [[FR-024-list-filter-search-and-sort-pieces]]. Only the five settlement
> stories and [[FR-026-sign-the-artist-contract]] carry real Given-When-Then
> criteria, because only [[SRC-007-tsu-brief]] states rules precise enough to
> write them against.

**Options.**
1. **Take the four back to Sandra Mayer for the "so that" and one criterion
   each.** Recommended — the author is known and reachable, the benefit is one
   sentence per story, and everything else here follows from having it. Split
   [[FR-002-settle-finances-and-legal-obligations]] in the same pass.
2. Draft the benefits in-house from the goals already in the wiki, marked as
   assumptions. Faster, and it makes four stories look agreed that are not.
3. Leave them as placeholders until an epic structure exists
   ([[ISS-017-twelve-candidate-capabilities-undefined]]), then rewrite top-down.

**Resolution.** *Open.*
