---
type: anchor
title: Story Mapping
aliases: [story-mapping, story-map, user-story-map]
tags: [anchor, technique, backlog]
applies-to: [product backlog (req42 block 04), epics, features, user-stories]
---

# Story Mapping

A technique (Jeff Patton) for arranging the Product Backlog as a **2-D map** instead of
a flat, context-free list — so you can explain the whole system, find gaps, and slice
releases. It is the way req42 recommends *maintaining* the functional-requirements
hierarchy (Hruschka cites Patton).

- **Backbone** (top row, left→right in **narrative / time order**): **epics only** in
  this vault (`stereotype: epic`). "The order you'd explain the system" is the correct order.
- **Ribs** (down each column, ordered by **priority**): the finer items — **features and
  stories** under each epic.
- **Swim-lanes** = releases. The top row across the whole map is the **walking skeleton /
  MVP** — the smallest end-to-end system. You don't prioritise the backbone against
  itself; you prioritise the ribs.
- **Naming (convention A, ADR-0015):** backbone items (epics) and features are **noun
  phrases** naming an outcome; the ribs (stories) and use cases are **verb + object**
  (active goal). The word class signals the granularity.

**In this vault.** A story map is a **projection / report over the Epic → Feature →
Story tree**, not a separate content type. The tree gives membership; the map adds two
things, so the backlog nodes must carry them: **sibling order** (backbone narrative
order) and **priority / release** ([[MoSCoW]] + a release tag). With those, the map is
fully derivable — render it as a report; don't store it as data.

## Representation (markdown)

A map is **generated from the FR nodes**, never hand-authored as a second source (that
would drift). Two output shapes — same data, different strengths:

- **Nested lists** — per epic, release sub-lists, stories beneath. Best for editing /
  diffing and many stories; scales vertically; but doesn't show the cross-epic MVP row.
- **Table** — columns = epics (backbone), rows = release swim-lanes; closest to Patton's
  2-D board and shows the **walking skeleton across the whole backbone** at a glance.
  Best for presentation/review; awkward when the backbone is wide.

Optionally derive a rough **Mermaid** sketch. The default rendering (table vs list) is a
generator choice, made when a story-map view/export is actually built. Worked
examples: `docs/methods/story-mapping.md`.

## Checklist (audit / grill)
- [ ] Backbone identified — coarse items in narrative order?
- [ ] Walking skeleton sliced — top row is a coherent end-to-end MVP?
- [ ] Narrative gaps — any step a user would expect that's missing?
- [ ] Every rib traces up to its backbone item (`parent:` set) **and** to one or
      more goals (`goal: [[GOAL-...]]`) — **or** is an explicit Enabler
      (`goal: []` with `lane: platform`/`display`). Goal-Coverage projects from
      this field (ADR-0018); missing goals on a backbone/feature item ⇒ flag as
      `[[ISS-...]]`.
- [ ] Naming grammar — epics/features noun phrases, stories/use-cases verb+object (convention A, ADR-0015)?

A backlog that is a flat list with no backbone → suggest mapping it; raise an `ISS-NNN`
if scope-completeness is in doubt.

> Cite as `[[story-mapping]]`. Distilled from Jeff Patton, *"The New Backlog is a Map"*
> (2008) — fuller attributed reference in `docs/methods/story-mapping.md`.
