---
id: ISS-002
type: issue
title: Objective baselines and targets are asserted with no source
status: open
created: 2026-09-09
updated: 2026-09-09
sources:
  - "[[SRC-001-ulrich-stuerzlinger-goals-and-newspaper]]"
related:
  - "[[GOAL-002-global-market-expansion]]"
  - "[[GOAL-003-operational-excellence]]"
  - "[[GOAL-004-trust-and-authentication]]"
tags: [issue]
severity: major
kind: gap
raised-by: agent
resolved: null
---

# Objective baselines and targets are asserted with no source

**What's unresolved.** Every quantitative figure in the three objectives arrived
as a bare number. None appears in `raw/TSU-brief.md.md`, and no measurement,
interview or system extract is cited. Without a real baseline, none of these
objectives can be evaluated — a target of "≤ 1 week" means nothing if nobody has
measured that setup currently takes 3–4 weeks.

**Affects.** [[GOAL-002-global-market-expansion]],
[[GOAL-003-operational-excellence]], [[GOAL-004-trust-and-authentication]].

**Context / evidence.** Figures asserted in
[[SRC-001-ulrich-stuerzlinger-goals-and-newspaper]] with no provenance:

| Figure | Used as | Where does it come from? |
|---|---|---|
| 3–4 weeks tour setup | baseline, GOAL-003 | unknown |
| $8–12K cost per tour | baseline, GOAL-003 | unknown |
| Buyer checkout completion → 85% | target, GOAL-003 | no checkout exists today |
| 5,000+ online buyers in Year 1 | target, GOAL-002 | unknown |
| 15–20% digital revenue Year 1 | target, GOAL-002 | unknown |
| 90%+ provenance coverage | target, GOAL-004 | current coverage unmeasured |
| < 0.5% fraud rate | target, GOAL-004 | current rate unmeasured |
| 10–15% price premium | advantage, GOAL-004 | unknown |

The one figure that *is* grounded is the five-day artist payment delay, which
comes from the brief.

**Options.**
1. Measure before committing — run a baseline study on the three that matter
   most (setup lead time, cost per tour, provenance coverage) and revise. Slow,
   but makes the objectives real.
2. Mark them as **hypotheses** with an explicit review date, and proceed. Keeps
   momentum; risks the whole goal tree resting on invented numbers.
3. Ask [[STK-001-gus-renoir]] to confirm or correct each figure from experience.
   Cheapest, and probably the right first move.

**Resolution.** *Open.*
