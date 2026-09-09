---
id: ISS-017
type: issue
title: Twelve candidate capabilities were named on cards, none of them defined
status: open
created: 2026-09-09
updated: 2026-09-09
sources:
  - "[[SRC-005-workshop-capability-card-wall]]"
related:
  - "[[ISS-004-scope-inflation-marketplace-vs-back-office]]"
  - "[[ISS-007-cleaner-versus-restorer]]"
  - "[[ISS-013-three-way-buyer-segmentation]]"
  - "[[ISS-021-authentication-card-ambiguous]]"
  - "[[GLO-001-tour]]"
  - "[[GOAL-003-operational-excellence]]"
  - "[[GOAL-004-trust-and-authentication]]"
tags: [issue]
severity: major
kind: gap
raised-by: agent
resolved: null
---

# Twelve candidate capabilities were named on cards, none of them defined

**What's unresolved.** The workshop produced twelve capability names on cards and
stopped there. Not one card carries a definition, an owner, a boundary, or a
reason for existing. They are held here as a candidate list rather than promoted
to [[req42]] Product Backlog items, because a name alone is not a functional
requirement — it cannot be sized, prioritised under [[MoSCoW]], or tested. The
list is the finding; converting it is the next session's work.

**Affects.** The `wiki/functional-requirements/` folder, which stays empty until
this closes. Several cards also touch open questions already on the board, marked
in the table below.

**Context / evidence.** Transcribed verbatim from
[[SRC-005-workshop-capability-card-wall]]. The photograph shows two distinct
print sizes and no drawn grouping, lines, or clusters.

| # | Card, as written | Print | Nearest existing page | Note |
|---|---|---|---|---|
| 1 | Artist Management | large | [[STK-002-artist]], [[EIF-001-artists]] | |
| 2 | Artwork Management | large | [[GLO-003-provenance]] | no page covers the piece itself |
| 3 | Museum Purchasing Process | large | [[STK-008-museum]], [[EIF-010-institutional-buyers]] | feeds [[ISS-013-three-way-buyer-segmentation]] |
| 4 | Customer Purchasing Process | large | [[STK-004-buyer]], [[EIF-008-individual-buyers]] | feeds [[ISS-013-three-way-buyer-segmentation]] |
| 5 | Cleaning & Restorations | large | [[STK-009-conservator]] | fuses two roles — [[ISS-007-cleaner-versus-restorer]] |
| 6 | tour planning | small | [[GLO-001-tour]], [[GOAL-003-operational-excellence]] | |
| 7 | contract handling | small | [[STK-010-legal-and-accounting]], [[STK-006-insurer]] | lending agreements vs. sales contracts unclear |
| 8 | payment handling | small | [[EIF-013-technology-and-infrastructure]] | |
| 9 | shipping handling | small | [[STK-005-shipper]], [[EIF-012-logistics-and-fulfillment]] | |
| 10 | insurance claim handling | small | [[STK-006-insurer]], [[EIF-012-logistics-and-fulfillment]] | first mention of *claims*, not just cover |
| 11 | authentication | small | [[GOAL-004-trust-and-authentication]], [[EIF-003-appraisers-and-authenticators]] | ambiguous — [[ISS-021-authentication-card-ambiguous]] |
| 12 | *(struck out)* communication | small | [[EIF-004-customer-support-and-marketing]] | first word deleted on the card and illegible; who communicates with whom is unknown |

Two further observations that are evidence, not interpretation:

- **The print sizes look like two levels, but nothing on the table says so.** The
  five large cards read as domains, the seven small ones as activities within
  them. No card is placed under another, and no line connects any pair. Any
  Epic → Feature hierarchy would be invented, so none is recorded.
- **The list is back-office in character.** Cleaning, shipping, insurance claims
  and tour planning are TSU's own operations. Nothing on the table describes a
  public marketplace. This is evidence for Reading A of
  [[ISS-004-scope-inflation-marketplace-vs-back-office]] and it points the
  opposite way from [[SRC-006-workshop-etsu-context-sketch]], drawn in the same
  session.

**Options.**
1. **Run a definition pass over the twelve, then convert.** Each card gets a
   one-sentence purpose, an owning stakeholder, and a [[MoSCoW]] priority; the
   survivors become Functional requirements with `stereotype: epic`. Recommended:
   it is the cheapest way to find out which of the twelve are real, and the
   [[INVEST]] test cannot run against a bare noun.
2. Promote all twelve to draft epics now and define them later. Fast, but it
   fills the backlog with twelve unfalsifiable items and makes the wiki look
   further along than it is.
3. Wait for [[ISS-004-scope-inflation-marketplace-vs-back-office]] to close
   first. Defensible, since scope decides which cards survive at all, but it
   leaves the backlog empty for an unknown stretch.

**Resolution.** *Open.*
