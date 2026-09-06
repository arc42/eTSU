# User Story Mapping — Reference (distilled)

> **Attribution.** Distilled summary of **Jeff Patton, "The New User Story Backlog is a
> Map" (2008)**, © Jeff Patton — <https://jpattonassociates.com/the-new-backlog/>. This
> is an *adapted summary for internal use*, **not** a verbatim copy (the original is
> ordinary copyright, not CC). The verbatim article + figures are kept privately under
> `raw/methods/`. For the citable, applied version see `_system/anchors/story-mapping.md`
> (`[[story-mapping]]`).

## The problem it solves

A **flat backlog** (stories in build order) is a poor way to *explain* a system and a
poor way to *spot gaps*. Patton's image: you do all the work to understand goals →
users → capabilities → stories (a tree), then "pull all the leaves off the tree and
load them into a leaf bag" — a bag of context-free mulch. Release planning by stepping
through a flat list of 100+ stories is tedious and error-prone.

## The map

Arrange stories into a **2-D shape**:

- **Backbone** — the big stories at the top: **user activities** (e.g. "managing email").
  Arranged **left→right in narrative/time order** — the order in which you'd *explain*
  what the system does.
- **Ribs** — under each activity, the **user tasks / smaller stories** ("send message",
  "read message"), arranged **top→bottom by priority** (high = necessary).
- **Releases** — lay masking-tape **swim-lanes**; move stories up/down into a release.
  The **top row** across all activities is the **walking skeleton** (Cockburn) — the
  smallest end-to-end **MVP**. Build that first, then deepen each backbone item.

You **don't** prioritise the backbone against itself ("engine vs. transmission?"); you
prioritise *how far you build up* each backbone item.

## Why it works

- **Tells a story** — you can walk the map end-to-end with users/stakeholders.
- **Finds gaps** — walking it surfaces "you missed a couple steps here."
- **Keeps context** — the big stories (epics/activities) stay as orienting context
  instead of being decomposed and thrown away.
- **It's a pattern, not an invention** — many practitioners arrive at the same shape.

## How this vault uses it

The map is a **projection of our Epic → Feature → Story tree** (see
`[[story-mapping]]`): backbone = epics/activities (narrative order), ribs = features/
stories (priority), swim-lanes = releases. Because the tree already holds membership,
we only need **sibling order** + **priority/release** on the nodes for the map to be a
pure derived **report** — not a separate artifact.

## Source

- Jeff Patton, *"The New User Story Backlog is a Map"*, 8 Oct 2008 — <https://jpattonassociates.com/the-new-backlog/>
- Book: Jeff Patton, *User Story Mapping*, O'Reilly, 2014.
