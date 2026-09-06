---
type: anchor
title: Acceptance Criteria (Given/When/Then)
aliases: [acceptance-criteria, gherkin, given-when-then]
tags: [anchor, testability]
applies-to: [functional-requirement (story stereotype), use-case special requirements]
---

# Acceptance Criteria (Given/When/Then)

Testable **conditions of satisfaction** for a backlog item — the check that says "done
and correct." Written in **Gherkin** form so they're unambiguous and verifiable:

> **Given** &lt;context / precondition&gt;
> **When** &lt;action / event&gt;
> **Then** &lt;observable, checkable outcome&gt;.

One scenario per distinct rule. Cover the **happy path plus the key alternates/errors**
the story implies. Phrase outcomes as **user-observable**, not implementation detail.

## Checklist (audit / grill)
- [ ] Each criterion is observable and testable — no "works well" / "is fast" (that's a
      [[quality-requirement|Qualitätsanforderung]] with a measure, not an AC).
- [ ] Happy path covered, plus at least the obvious alternate/error path.
- [ ] Written from the outside (what the user/system observes), not how it's built.
- [ ] Together they fully decide whether the story is satisfied.

A story with no acceptance criteria → not [[INVEST|testable]] → raise an `ISS-NNN`.

> Cite as `[[acceptance-criteria]]` (aliases `[[gherkin]]`, `[[given-when-then]]`).
