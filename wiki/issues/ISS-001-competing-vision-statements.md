---
id: ISS-001
type: issue
title: Two competing vision statements for eTSU — Moore format vs. the "new Picasso" line
status: open
created: 2026-09-09
updated: 2026-09-09
sources:
  - "[[SRC-002-georg-mayrhauser-vision-goals-stakeholders]]"
related:
  - "[[GOAL-001-eTSU-vision]]"
  - "[[ISS-015-a-new-picasso-is-undefined]]"
  - "[[ISS-016-moore-format-cited-without-an-anchor]]"
  - "[[ISS-004-scope-inflation-marketplace-vs-back-office]]"
tags: [issue]
severity: major
kind: contradiction
raised-by: agent
resolved: null
---

# Two competing vision statements for eTSU — Moore format vs. the "new Picasso" line

**What's unresolved.** [[GOAL-001-eTSU-vision]] holds a Geoffrey Moore–format
vision written during bootstrap. The Req4Arc Linz workshop independently
produced a one-liner. ADR-0016 allows exactly one vision per system, so one of
these has to win — or they have to merge.

**Affects.** [[GOAL-001-eTSU-vision]] and, through `parent:`, all four
objectives: [[GOAL-002-global-market-expansion]],
[[GOAL-003-operational-excellence]], [[GOAL-004-trust-and-authentication]],
[[GOAL-005-frictionless-global-art-trade]].

**Context / evidence.**
- *Bootstrap (GOAL-001):* "For **gallery tour operators** who coordinate
  multi-stop art tours … **eTSU** is a **digital tour and gallery management
  platform** that gives real-time visibility into every piece's status …"
- *Workshop ([[SRC-002-georg-mayrhauser-vision-goals-stakeholders]]):* "If there
  is a new Picasso we will have shown and sold it over our Platform."

These are not merely different wordings. The Moore text scopes eTSU as an
**operational tool for tour operators**; the Picasso line scopes it as **the
channel through which significant art reaches the world** — an ambition much
closer to the marketplace reading in
[[ISS-004-scope-inflation-marketplace-vs-back-office]].

**Options.**
1. Keep the Moore text, demote the Picasso line to `tile_claim:` — retains
   structure and the target-group/category/benefit discipline; loses the line
   people will actually remember.
2. Adopt the Picasso line as the vision, keep the Moore text as an explanatory
   paragraph beneath it — memorable and workshop-owned, but a vision with no
   named target group or category is harder to derive objectives from.
3. Merge: Picasso line as the headline, Moore structure as the body — likely the
   best of both, but needs the group present to agree the wording.

**Update 2026-09-09 — neither candidate is currently legible.**
Both sides of this choice rest on an undefined term:
- *"a new Picasso"* is never defined and cannot be evaluated —
  [[ISS-015-a-new-picasso-is-undefined]];
- *"the Moore format"* is cited by `_templates/goal.md` but has no anchor in
  `_system/anchors/`, so nobody can look up what choosing it commits them to —
  [[ISS-016-moore-format-cited-without-an-anchor]].

Settle those two first; the choice here gets much easier once both options mean
something specific.

**Resolution.** *Open.* Deliberately not decided by the agent — this belongs to
the workshop group.
