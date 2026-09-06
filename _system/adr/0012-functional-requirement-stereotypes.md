# ADR-0012: Functional requirements as one type with a stereotype (epic|feature|story)

- **Status:** accepted
- **Date:** 2026-05-25

## Context
We had **Feature** and **User story** as separate content types. But req42's
product backlog (block 04) is really **one** hierarchy of functional
requirements at three granularities — **Epic → Feature → Story** — which gets
projected as a story map. Separate types splinter this family and carry no
unified parent/child graph. The sponsor wants to be able to "mark a functional
requirement as an epic, story, or feature, to enable a hierarchy (or a
graph)".

## Decision
One content type, **Functional requirement**
(`wiki/functional-requirements/`, `FR-NNN`), with a field
**`stereotype: epic | feature | story`**. The hierarchy is built via
**`parent:`** wikilinks (more than one allowed ⇒ a graph, not just a tree).
For the story-map projection ([[story-mapping]]), nodes additionally carry
**`order`** (backbone sequence), **`priority`** ([[MoSCoW]]), and **`release`**
(swim lane).

The previous, **instance-less** types Feature and User story are absorbed
into this one (13 → 12 content types). Acceptance criteria are captured via
the new anchor **[[acceptance-criteria]]** (Given/When/Then) — harvested from
the retired templates. The use-case template was enriched (Cockburn style)
but remains its **own** type. **Estimate/owner** are deliberately not modelled
in the wiki (that belongs to the tracker, e.g. JIRA); the wiki holds
requirement facts: stereotype, hierarchy, priority, release, order.

## Consequences
A unified, graph-capable backlog; the story map is a pure projection. All
cross-references are now `[[FR-...]]` (instead of `[[FEAT-...]]`/`[[US-...]]`).
Updated: the `CLAUDE.md` type table, the req42 anchor + `docs/req42/`, the
index, the dashboard app. Migration: none — both retired types were
instance-less.
