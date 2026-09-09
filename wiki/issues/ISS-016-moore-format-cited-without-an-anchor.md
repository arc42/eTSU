---
id: ISS-016
type: issue
title: The Moore vision format is cited by the template but has no semantic anchor
status: open
created: 2026-09-09
updated: 2026-09-09
sources: []
related:
  - "[[GOAL-001-eTSU-vision]]"
  - "[[ISS-001-competing-vision-statements]]"
  - "[[ISS-014-legacy-issue-ids-referenced-by-starter-adrs]]"
tags: [issue]
severity: minor
kind: gap
raised-by: agent
resolved: null
---

# The Moore vision format is cited by the template but has no semantic anchor

**What's unresolved.** `_templates/goal.md` instructs that a vision *"follows the
Geoffrey Moore format"*, and [[GOAL-001-eTSU-vision]] is written in it. But
**"Moore" is never defined anywhere in the vault.** There is no
`_system/anchors/moore.md`, so a reader meeting the instruction has nothing to
follow, and the agent applying it is working from memory rather than from the
wiki.

This is the exact gap `_system/anchors/` exists to close. ADR-0004 established
that reusable methodological standards live there and are **cited by alias**
rather than restated — `[[SMART]]`, `[[PAM]]`, `[[INVEST]]`, `[[MoSCoW]]`,
`[[user-story-format]]`, `[[acceptance-criteria]]`, `[[story-mapping]]` all have
anchors. Moore is cited the same way and has none.

**Affects.** `_templates/goal.md`, [[GOAL-001-eTSU-vision]], and
[[ISS-001-competing-vision-statements]] — that Issue asks the group to choose
between "the Moore text" and "the Picasso line" without either side being able
to look up what the first one commits them to.

**Context / evidence.** **Geoffrey Moore**, *Crossing the Chasm* (1991),
positioning / value-proposition statement:

> For **&lt;target customer&gt;** who **&lt;statement of need or opportunity&gt;**,
> the **&lt;product name&gt;** is a **&lt;product category&gt;** that
> **&lt;key benefit, compelling reason to buy&gt;**.
> Unlike **&lt;primary competitive alternative&gt;**, our product
> **&lt;statement of primary differentiation&gt;**.

The template already encodes one local adaptation — it marks the *Unlike* clause
optional and advises omitting it "for a positive, inviting vision". That
adaptation is itself undocumented reasoning that belongs in an anchor rather
than in a template comment.

**Options.**
1. **Write `_system/anchors/moore.md`** with the format, the optional-contrast
   convention, a worked eTSU example and a short checklist (is the target group
   named? the category? one key benefit?), then cite it as `[[Moore]]` from the
   goal template and from `GOAL-001`. Recommended — anchors are authored, not
   ingested (ADR-0004), so this needs no source and is a small, self-contained fix.
2. Fold it into the existing [[req42]] anchor as a sub-section on Block 01
   visions. Fewer files; less discoverable.
3. Drop the citation and inline the format in the template. Contradicts ADR-0004's
   cite-don't-restate principle.

**Resolution.** *Open.*

> [!note] ID collision, as predicted
> `ADR-0020` cites an `ISS-016-remove-active-soft-delete` from the starter's own
> history. Per the policy stated in
> [[ISS-014-legacy-issue-ids-referenced-by-starter-adrs]], this vault's sequence
> is not being routed around those ghosts; filenames differ, so nothing
> mis-resolves.
