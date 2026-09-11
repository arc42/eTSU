---
id: FR-017
type: functional-requirement
title: Artwork Inventory
status: draft
created: 2026-09-09
updated: 2026-09-09
sources:
  - "[[SRC-009-workshop-inventory-decomposition]]"
related:
  - "[[FR-006-tour-visibility]]"
  - "[[FR-019-create-the-piece-inventory]]"
  - "[[FR-020-add-piece-details]]"
  - "[[FR-021-upload-piece-images]]"
  - "[[FR-018-artwork-tracking]]"
  - "[[GLO-011-piece]]"
  - "[[STK-001-gus-renoir]]"
  - "[[FR-001-view-piece-inventory-and-status]]"
tags: [functional-requirement]
stereotype: feature
parent:
  - "[[FR-006-tour-visibility]]"
priority: Should
release: backlog
lane: backbone
order: 21
goal:
  - "[[GOAL-005-frictionless-global-art-trade]]"
---

# Artwork Inventory

## Story

For [[STK-001-gus-renoir|Head Office]], **getting every
[[GLO-011-piece|piece]] on a tour into the record in the first place** — the
list itself, what each entry holds, and its images.

**PROBLEM / GOAL**

There is no overview of what is on tour until something creates and populates the
inventory. This is the write side; [[FR-018-artwork-tracking]] is the read side.

**Success metric(s).** Inherited from
[[GOAL-005-frictionless-global-art-trade]].

**Scope.** in: creating the inventory, the fields on a piece, images · out:
querying it, and location.

## Hierarchy

- **Parent:** [[FR-006-tour-visibility]].
- **Children:** [[FR-019-create-the-piece-inventory]],
  [[FR-020-add-piece-details]], [[FR-021-upload-piece-images]].

> [!note] Open points
> - The card reads **"Inventory of artworks"**; renamed here into the ubiquitous
>   language only for the child pages, since *artwork* is a recorded alias of
>   [[GLO-011-piece|piece]]. The feature keeps the workshop's own title.
> - Overlaps [[FR-005-piece-management]], which also owns the piece record. The
>   boundary between "the catalogue entry" and "the tour inventory" is undrawn.

## History

> Created 2026-09-09 from the grouping card in
> [[SRC-009-workshop-inventory-decomposition]]. The wiki's first feature.
