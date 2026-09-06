---
id: GOAL-NNN
type: goal
title: <Name>           # Noun phrase, outcome-oriented (e.g. "Real-time transparency for families"), EN (ADR-0005)
status: draft           # draft | review | accepted | deprecated
created: {{date}}
updated: {{date}}
sources: []
related: []             # [[STK-...]], [[FR-...]], [[QR-...]], [[CON-...]]
tags: [goal]
stereotype: objective   # vision | objective  (vision = the overarching narrative; objective = a PAM sub-goal)
parent: []              # [[GOAL-...]] — the vision has no parent; objectives point to the vision
beneficiary: []         # [[STK-...]] — who gets the benefit (PAM "Advantage")
metric:                 # a single indicator (PAM); empty for a vision
baseline:               # current value, once measured/estimated — otherwise empty
target:                 # target value (e.g. "≤ 50%", "< 15 min")
horizon:                # time horizon (e.g. "from season 2027"); empty → still PAM, filled → [[SMART]]-ready
short_title:            # optional: a shorter label for diagram nodes and tile rows
                        # (the goal tree and the backlog map are tight). Empty -> `title`.
tile_claim:             # vision only: ONE short line (≤ ~90 chars) for the dashboard's
                        # Vision tile and the req42 block-01 sub-headline. The tile is small —
                        # this is the pitch, not the full Moore paragraph below. Empty → no claim shown.
---

# {{title}}

<!-- One type, two stereotypes — mirrors ADR-0012 (FR with epic|feature|story).
     Vision = the roof (exactly one GOAL per system); Objectives = sub-goals under
     the vision. Hierarchy via `parent:` wikilinks. Title grammar: noun phrase with
     a clear outcome (ADR-0015). English ubiquitous language (ADR-0005). -->

## Vision  — when `stereotype: vision`   > follows the Geoffrey Moore format (contrast clause optional)

For **<target group>** who **<need / problem>**, **<system>** is a
**<category>** that **<key benefit>**.

*Optional:* `Unlike <alternative>, <differentiator>.` — include only when
market positioning against concrete alternatives is part of the vision; for a
positive, inviting vision, **omit it**.

**Objectives.** see `parent:` backlinks (objectives that point to this vision).

## Objective  — when `stereotype: objective`   > follows [[PAM]]; promotes to [[SMART]] once `horizon` is set

- **Purpose.** <the outcome sought, not an activity>
- **Advantage.** <for whom (see `beneficiary:`), what concrete benefit — "so what?">
- **Metric.** <the one indicator (see `metric:` / `baseline:` / `target:`)>

**Parent.** see `parent:` (usually the vision).

## Impact

- **Addressed stakeholders:** see `beneficiary:` (plus any further ones under `related:`).
- **Served by:** projected from the **FR backlinks** (Obsidian backlink pane / dashboard coverage matrix). Every `[[FR-...]]` that names this goal in its `goal:` field appears here automatically — **do not** maintain this by hand (projection principle, ADR-0018).

> [!note] Open points
> <missing baseline, untestable metric, unclear horizon → capture as [[ISS-...]]>

<!-- Goals cover req42 block 01 "Business Goals" (ADR-0016). They are the goal
     space (why), not the solution space (how); FR/QR/CON carry the latter. -->
