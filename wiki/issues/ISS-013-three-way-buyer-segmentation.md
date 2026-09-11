---
id: ISS-013
type: issue
title: A third buyer segmentation appears — individual / global online / institutional
status: open
created: 2026-09-09
updated: 2026-09-09
sources:
  - "[[SRC-004-ulrich-stuerzlinger-context-diagram]]"
  - "[[SRC-005-workshop-capability-card-wall]]"
  - "[[SRC-006-workshop-etsu-context-sketch]]"
related:
  - "[[ISS-006-buyer-versus-art-collector]]"
  - "[[STK-004-buyer]]"
  - "[[STK-014-art-collector]]"
  - "[[STK-008-museum]]"
  - "[[EIF-008-individual-buyers]]"
  - "[[EIF-009-global-online-buyers]]"
  - "[[EIF-010-institutional-buyers]]"
  - "[[GLO-013-buyer]]"
  - "[[GLO-014-museum]]"
  - "[[GLO-018-minimum-museum-sale-price]]"
  - "[[ISS-017-twelve-candidate-capabilities-undefined]]"
  - "[[ISS-019-visitors-is-an-undefined-actor]]"
  - "[[DM-008-museum]]"
  - "[[DM-009-buyer]]"
tags: [issue]
severity: major
kind: contradiction
raised-by: agent
resolved: null
---

# A third buyer segmentation appears — individual / global online / institutional

**What's unresolved.** Three sources now cut the buying party three different
ways, and no two agree. This is no longer a naming quibble: the brief already
proves that *who the buyer is* changes *what they pay*, so the segmentation is a
pricing rule, and it will land in the data model.

**Affects.** [[STK-004-buyer]], [[STK-008-museum]],
[[EIF-008-individual-buyers]], [[EIF-009-global-online-buyers]],
[[EIF-010-institutional-buyers]], and [[ISS-006-buyer-versus-art-collector]],
which this supersedes in scope.

**Context / evidence.**

| Source | Segmentation | Cut along |
|---|---|---|
| `raw/TSU-brief.md.md` | buyer · museum | **price tier** — the minimum museum sale price is almost always below the minimum customer price |
| [[SRC-002-georg-mayrhauser-vision-goals-stakeholders]] | buyers · art collectors | **relationship** — transactional vs. cultivated |
| [[SRC-004-ulrich-stuerzlinger-context-diagram]] | individual · global online · institutional | **channel and geography** for the first two, **institution type** for the third |
| [[SRC-005-workshop-capability-card-wall]] | customer · museum | **process** — two separate purchasing processes were carded, implying the flows differ, not just the price |
| [[SRC-006-workshop-etsu-context-sketch]] | visitors | **none** — one undifferentiated actor ([[ISS-019-visitors-is-an-undefined-actor]]) |

The three cuts are not alternatives to choose between — they are three
*different dimensions*, and the diagram mixes two of them within one row:
"Individual" and "Institutional" describe *who the party is*, while "Global
Online" describes *how they arrived*. A museum buying through the website is
both "global online" and "institutional", so the three boxes are not mutually
exclusive as drawn.

Note also that "corps" (corporate collections) in
[[EIF-010-institutional-buyers]] appears in **no other source**.

**Options.**
1. Model **one buying party with independent attributes** — `segment`
   (private / collector / institutional), `channel` (in-gallery / online),
   `region`. Pricing keys off `segment`, [[GOAL-002-global-market-expansion]]'s
   metric keys off `channel`. Recommended: it is the only option under which the
   three sources stop contradicting each other, because each was describing a
   different attribute all along.
2. Adopt the diagram's three types as-is and accept the overlap.
3. Defer until the data model is written and let it force the answer.

**Resolution.** *Open,* and now the only open part of the question.
[[ISS-006-buyer-versus-art-collector]] **closed on 2026-09-09**: buyer and
collector are two roles, and [[STK-014-art-collector]] exists. That settled the
*relationship* dimension only. The **segment**, **channel** and **process**
dimensions above are still unresolved, and the card wall added a fifth cut —
two separate purchasing processes for customer and museum, which claims the
*flows* differ and not merely the price.
