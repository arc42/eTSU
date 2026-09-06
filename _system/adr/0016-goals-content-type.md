# ADR-0016: Content type **Goal** for req42 block 01 "Objective setting"

- **Status:** accepted
- **Date:** 2026-05-28

## Context
req42 block 01, **Objective setting** (vision + sub-goals), had no place in the
wiki so far. The draft vision for the system (`raw/vision-draft.md`,
2026-05-27) — one vision plus four [[PAM]] sub-goals — therefore sat outside
the typed structure and could neither be linked nor projected in the graph.

None of the existing twelve types fits: `functional-requirements/` is
solution space (backlog), `quality-requirements/` are ATAM-style scenarios
against ISO-25010 attributes, `constraints/` are limitations, `context/`
outlines the system boundary. Goals are their own category — the **why**
space that motivates the solution space.

Secondary question: **vision vs. sub-goals — one type or two?** Both are
statements about intended outcomes but differ in form (an umbrella narrative
vs. [[PAM]] structure). The pattern from [[ADR-0012]] (one type, Functional
requirement, stereotypes `epic|feature|story`) has proven itself.

## Decision
**A new content type `goal`** (`wiki/goals/`, IDs `GOAL-NNN`) with field
**`stereotype: vision | objective`**:

- **vision** — the umbrella narrative, exactly one per system; formatted per
  Geoffrey Moore ("For …, who …, the <system> is a … that …. Unlike …").
- **objective** — a sub-goal in **[[PAM]]** format (Purpose · Advantage · *one*
  metric); promoted to **[[SMART]]** once `horizon` (a time horizon) is set.

Hierarchy via **`parent:`** wikilinks (objectives point to the vision; the
vision has no parent). Additional frontmatter fields: `beneficiary:`
(`[[STK-...]]` — PAM's "Advantage"), `metric:`/`baseline:`/`target:` (exactly
one indicator), `horizon:` (empty → PAM, filled in → SMART-capable).

Title grammar per [[ADR-0015]]: **a noun phrase with a clear outcome** (goals
name outcomes, not activities). Language: see ADR-0005 — at the time of this
ADR (2026-05-28) German, since the 2026-09-06 rewrite, English.

This grows the type table from **12 to 13 types**.

## Consequences
The vision and sub-goals from `raw/vision-draft.md` can now be carried into
the wiki (a follow-up step, not part of this ADR). Updated: the `CLAUDE.md`
type table plus the folder list, `_system/index.md` (a new **Goals** section
between Glossary and Stakeholders, matching req42's ordering), a new template
`_templates/goal.md`. **No migration** — there are no `GOAL-…` instances yet.

Deliberately **not** modelled: separate types for vision and sub-goal
(a stereotype is used instead, matching [[ADR-0012]]); priority (MoSCoW fits
backlog items, not goals — with few goals the hierarchy alone is enough).
`beneficiary:` is its own field (not just prose) so stakeholder connections
stay discoverable in the graph and in reports.
