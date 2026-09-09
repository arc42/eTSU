---
id: ISS-009
type: issue
title: "GOAL-005's \"real time\" metric is untestable, and the objective overlaps two others"
status: open
created: 2026-09-09
updated: 2026-09-09
sources:
  - "[[SRC-002-georg-mayrhauser-vision-goals-stakeholders]]"
related:
  - "[[GOAL-005-frictionless-global-art-trade]]"
  - "[[GOAL-002-global-market-expansion]]"
  - "[[GOAL-003-operational-excellence]]"
tags: [issue]
severity: major
kind: ambiguity
raised-by: agent
resolved: null
---

# GOAL-005's "real time" metric is untestable, and the objective overlaps two others

**What's unresolved.** Two separate problems with the same goal, kept together
because fixing one probably reshapes the other.

**1. The metric carries no number.** [[GOAL-005-frictionless-global-art-trade]]
measures success as artwork information "shown in **real time**". No latency, no
freshness window, no measurement point. Per the anchors, a quality target
without a measure is untestable — the goal cannot pass or fail. It stays
[[PAM]] and cannot promote to [[SMART]] until quantified, and `horizon:` is
empty as well.

**2. It overlaps [[GOAL-002-global-market-expansion]] and
[[GOAL-003-operational-excellence]].** Its purpose ("selling of art **globally**")
restates GOAL-002; its advantage ("instant overview of shows, art work and
**selling processes**") restates GOAL-003. The three arrived from two authors on
the same day with no reconciliation between them.

**Affects.** [[GOAL-005-frictionless-global-art-trade]],
[[GOAL-002-global-market-expansion]], [[GOAL-003-operational-excellence]].

**Context / evidence.** From
[[SRC-002-georg-mayrhauser-vision-goals-stakeholders]] verbatim:

> P: Enable frictionless showing and selling of art globally
> A: Instant overview of shows, art work and selling processes
> M: Information on the art work (where it is shown, if it is sold, what's the
> current price) is shown in real time

The three facts named — location, sale status, current price — are precise and
genuinely useful; it is only the timeliness that is unquantified. Note that
"real time" matters most exactly where it is hardest: a price floated by Head
Office between tour stops must reach a [[STK-003-gallery-manager|gallery
manager]] before they quote the old one to a buyer standing in the room.

**Options.**
1. **Quantify and keep.** Give it a latency budget — e.g. "a price or status
   change is visible in every gallery within 5 seconds" — and keep it as the
   distinct *timeliness* objective the other two lack. Recommended: it is the
   only goal that names timeliness, and the stale-price scenario above is a real
   business risk.
2. **Fold into GOAL-003** as a secondary indicator of operational excellence, and
   retire GOAL-005. Fewer goals; loses the specific promise.
3. **Restate as a quality requirement** rather than a goal — "real-time
   visibility" is arguably a `QR-` performance scenario (stimulus: price change;
   response: propagated; measure: ≤ N seconds), not a business objective.

**Resolution.** *Open.*
