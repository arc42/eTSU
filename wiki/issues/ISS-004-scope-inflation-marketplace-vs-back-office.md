---
id: ISS-004
type: issue
title: Is eTSU a back-office tool or a global consumer marketplace?
status: open
created: 2026-09-09
updated: 2026-09-09
sources:
  - "[[SRC-001-ulrich-stuerzlinger-goals-and-newspaper]]"
  - "[[SRC-002-georg-mayrhauser-vision-goals-stakeholders]]"
  - "[[SRC-004-ulrich-stuerzlinger-context-diagram]]"
  - "[[SRC-005-workshop-capability-card-wall]]"
  - "[[SRC-006-workshop-etsu-context-sketch]]"
related:
  - "[[GLO-005-etsu]]"
  - "[[CTX-001-etsu-system-context]]"
  - "[[ISS-010-system-boundary-undefined]]"
  - "[[GOAL-001-eTSU-vision]]"
  - "[[GOAL-002-global-market-expansion]]"
  - "[[GOAL-003-operational-excellence]]"
  - "[[GOAL-004-trust-and-authentication]]"
  - "[[ISS-001-competing-vision-statements]]"
  - "[[ISS-017-twelve-candidate-capabilities-undefined]]"
  - "[[ISS-018-competing-context-diagrams]]"
  - "[[ISS-019-visitors-is-an-undefined-actor]]"
tags: [issue]
severity: blocker
kind: risk
raised-by: agent
resolved: null
---

# Is eTSU a back-office tool or a global consumer marketplace?

**What's unresolved.** The brief and the workshop emails describe two different
systems under one name. Nearly every downstream decision — data model, external
interfaces, use cases, the entire backlog — depends on which one eTSU is. This
is the blocker of this ingest.

**Affects.** [[GLO-005-etsu]], [[GOAL-001-eTSU-vision]] and every objective
beneath it; will affect all Context, External interface, Use case and Functional
requirement pages once those exist.

**Context / evidence.**

*Reading A — back-office digitisation.* `raw/TSU-brief.md.md`: "submit a proposal
to Gus Renoir for the **digitization of his business**"; "a digital product
**supporting the gallery's business**." The whole brief is internal process:
tour assembly, lending agreements, shipping, and a sale ritual that is
deliberately face-to-face — champagne in the back office while paperwork is
signed. Users are Head Office and gallery staff.

*Reading B — a public global marketplace.*
[[SRC-001-ulrich-stuerzlinger-goals-and-newspaper]]: "make TSU art available
**24/7 globally**"; "**5,000+ online buyers** in Year 1"; "improve **buyer
checkout completion** to 85%+"; "48% of revenue" digital; "expanded into 150+
countries"; blockchain provenance verification against the Art Loss Register and
Interpol; regulatory approval across 47 jurisdictions.
[[SRC-002-georg-mayrhauser-vision-goals-stakeholders]] agrees: "shown and **sold
it over our Platform**", "selling of art **globally**."

The gap is not one of degree. Reading B requires a public product surface, a
payment system, an identity/KYC regime, multi-jurisdiction compliance, and
external register integrations — **none of which exist in Reading A**, and one
of which (online checkout) directly contradicts the brief's sale ritual, where a
buyer signs an intent to purchase in person and then has 24 hours to transfer
10%.

**Update 2026-09-09 — a third source, still not a decision.**
[[SRC-004-ulrich-stuerzlinger-context-diagram]] names the system box
**"TSU / eTSU — Gallery platform & digital marketplace"** and draws a whole
DEMAND tier including [[EIF-009-global-online-buyers|Global Online Buyers — "New
markets"]]. That is Reading B, stated more plainly than anywhere else. It is
corroboration, not resolution: all three sources pointing at Reading B come from
the same two workshop participants, and **no source from the client side —
Gus Renoir, the brief — has said anything but Reading A.** The party who has to
pay for it has not been asked.

Note the dependency: [[ISS-010-system-boundary-undefined]] cannot close until
this does, and roughly half of `wiki/external-interfaces/` depends on that.

**Options.**
1. **Reading A only.** Digitise the back office; treat every marketplace goal as
   out of scope and record it as a non-goal in the Context page. Matches the
   brief and what the client actually asked for.
2. **Reading B, phased.** Back office first, marketplace as a later phase — which
   is exactly the sequence the 2029 narrative describes ("operational excellence
   first … global expansion followed naturally"). Requires the group to accept a
   multi-year programme, not a product.
3. **Reading B directly.** Build the marketplace. Fastest to the workshop's
   ambition; ignores that the sale ritual, the two-tier museum pricing and the
   deposit/forfeit rules are not yet modelled at all.

> [!note] New evidence 2026-09-09 — the Linz workshop split on this too
> Both photographed artefacts bear on the question and they point opposite ways.
> [[SRC-005-workshop-capability-card-wall]] is back-office throughout: cleaning,
> shipping, insurance claims, contract handling, tour planning — TSU's own
> operations, with no public surface named on any of the twelve cards
> ([[ISS-017-twelve-candidate-capabilities-undefined]]). Yet
> [[SRC-006-workshop-etsu-context-sketch]], drawn in the same session, gives
> eTSU **Visitors** as a primary actor and **Social Media** as an outbound
> neighbour, which only make sense if eTSU faces the public
> ([[ISS-019-visitors-is-an-undefined-actor]],
> [[ISS-018-competing-context-diagrams]]).
>
> The disagreement is therefore not between sources of different vintage. It is
> inside one workshop, on one day, between two artefacts made side by side.

**Resolution.** *Open.* Note that option 2 is what the sources themselves imply
if the 2029 narrative is read as a roadmap — but no source states it as a
decision, so the agent is not treating it as one.
