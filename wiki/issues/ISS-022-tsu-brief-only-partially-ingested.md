---
id: ISS-022
type: issue
title: The TSU brief is the primary source and is still only partially ingested
status: open
created: 2026-09-09
updated: 2026-09-09
sources:
  - "[[SRC-007-tsu-brief]]"
related:
  - "[[ISS-017-twelve-candidate-capabilities-undefined]]"
  - "[[ISS-004-scope-inflation-marketplace-vs-back-office]]"
  - "[[STK-004-buyer]]"
  - "[[GLO-023-the-insult]]"
  - "[[FR-007-settlement-and-compliance]]"
  - "[[GOAL-006-settlement-correct-and-on-time]]"
  - "[[FR-002-settle-finances-and-legal-obligations]]"
  - "[[ISS-024-close-out-timing-show-versus-tour]]"
  - "[[FR-007-settlement-and-compliance]]"
  - "[[GOAL-006-settlement-correct-and-on-time]]"
tags: [issue]
severity: major
kind: gap
raised-by: agent
resolved: null
---

# The TSU brief is the primary source and is still only partially ingested

**What's unresolved.** `raw/TSU-brief.md.md` is the founding account of the
business and the only source that describes how TSU actually operates. On
2026-09-09 thirteen glossary terms were extracted from it, and later the same day
its **settlement rules** became five stories under
[[FR-007-settlement-and-compliance]] plus
[[GOAL-006-settlement-correct-and-on-time]]. **The rest is still uningested**,
and several pages still lean on it informally with `> [!assumption]` callouts
rather than a `sources:` link.

**Affects.** [[STK-004-buyer]], whose payment sequence comes from the brief with
no source record until now. More broadly: the empty
`wiki/activity-models/`, `wiki/use-cases/`, `wiki/data-models/` and
`wiki/functional-requirements/` folders, all of which the brief could populate.

**Context / evidence.** What the brief contains that no page yet captures:

| Material | Would become |
|---|---|
| Tour assembly: concept → artist terms → lending agreements → formal contract → shipping and insurance → gallery notification | an Activity model, and the spine of the backlog |
| ~~The deposit-and-balance sequence: 10% in 24 h, 90% in 14 days, forfeiture rules~~ | **done 2026-09-09** — [[FR-008-collect-the-purchase-deposit]], [[FR-009-collect-the-purchase-balance]], [[FR-010-settle-a-failed-purchase]] |
| ~~Commission settlement: half on sale, half 5 days after tour close~~ | **done 2026-09-09** — [[FR-011-pay-artist-commission]] |
| ~~Loss of a sold piece on tour: full refund, artist keeps half the commission, TSU absorbs it from insurance~~ | **done 2026-09-09** — [[FR-012-settle-a-loss-claim-on-a-sold-piece]], which surfaced two open money questions |
| One shipper and one insurer **per whole tour**, because those companies demand it | a Constraint |
| Price floats between tour stops but is fixed within one | a Constraint, and a Data model invariant |
| Adding new pieces mid-tour when an artist sells well | a Functional requirement |

**Options.**
1. **Run a full grill-gated ingest of the brief next.** Recommended — it is the
   richest source in the vault and the only one that would fill four empty
   folders. It also outranks the workshop material, which is second-hand by
   comparison.
2. Ingest it piecemeal, as each empty folder is needed. Spreads the cost, but
   risks the same contradiction being rediscovered several times.
3. Leave it. Only defensible if the workshop supersedes the brief, which nobody
   has claimed.

**Resolution.** *Open.* The file deliberately stays in the `raw/` inbox rather
than moving to `raw/ingested/` (ADR-0008), because it is not ingested yet.
