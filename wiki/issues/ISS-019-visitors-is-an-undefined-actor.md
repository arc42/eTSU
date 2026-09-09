---
id: ISS-019
type: issue
title: "\"Visitors\" is drawn as a primary actor but is defined nowhere"
status: open
created: 2026-09-09
updated: 2026-09-09
sources:
  - "[[SRC-006-workshop-etsu-context-sketch]]"
related:
  - "[[ISS-018-competing-context-diagrams]]"
  - "[[ISS-013-three-way-buyer-segmentation]]"
  - "[[ISS-006-buyer-versus-art-collector]]"
  - "[[STK-004-buyer]]"
  - "[[GLO-002-show]]"
tags: [issue]
severity: major
kind: ambiguity
raised-by: agent
resolved: null
---

# "Visitors" is drawn as a primary actor but is defined nowhere

**What's unresolved.** The sketch gives Visitors one of only two human actor
positions on the diagram, which makes them a primary user of eTSU. No source
says who they are. Three readings are live and they imply three different
products.

**Affects.** [[STK-004-buyer]], which may or may not be the same party;
[[ISS-013-three-way-buyer-segmentation]], which now has a candidate fourth cut;
and any use case that starts with someone arriving.

**Context / evidence.** The card wall drawn in the same session
([[SRC-005-workshop-capability-card-wall]]) says **Customer** and **Museum**, not
Visitor. Earlier sources say **buyer**, **art collector**, and **individual /
global online / institutional**. Visitor is the fifth word for a party in this
area and the first one that does not imply a purchase.

The readings:

1. **Gallery visitor** — a person physically at a [[GLO-002-show|Show]]. Then
   eTSU has an on-site surface (kiosk, catalogue, QR) that no other source
   mentions, and most visitors never buy.
2. **Website visitor** — an anonymous browser of an online catalogue. Then eTSU
   is public-facing, which is Reading B of
   [[ISS-004-scope-inflation-marketplace-vs-back-office]].
3. **A loose synonym for buyer** — the sketch's word for
   [[STK-004-buyer]]. Then nothing new is being claimed and the term should be
   dropped in favour of the glossary's.

The arrow direction is itself evidence and it is thin: Visitors point *into*
eTSU, and nothing points back. Taken literally, eTSU returns nothing to a
visitor, which cannot be the intent for readings 1 or 2.

**Options.**
1. **Ask the room which reading they drew, then either add a glossary term and a
   stakeholder page, or strike the word.** Recommended — the three readings are
   distinguished by one sentence from whoever held the pen, and the cost of
   guessing is a stakeholder page that describes nobody.
2. Assume reading 3 and treat Visitor as an alias on [[STK-004-buyer]] under
   [[0010-stakeholder-aliases-field|ADR-0010]]. Cheap, and wrong if the group
   meant a non-buying audience.
3. Create a Visitor stakeholder now with the definition left open. Fills the gap
   with a page that asserts nothing.

**Resolution.** *Open.*
