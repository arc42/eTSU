---
id: FR-005
type: functional-requirement
title: Return a Book
status: accepted
created: 2026-09-06
updated: 2026-09-06
sources: []
related: []
tags: [functional-requirement]
stereotype: story
parent:
  - "[[FR-001-lending]]"
priority: Must
release: v1
lane: backbone
order: 2
goal: []
---

# Return a Book

## Story

As a reader, I want to return a book at the front desk, so that my loan is
closed and the book becomes available again.

**Acceptance criteria.**

- **Given** an open loan, **when** the book is returned, **then** the loan is
  closed and the book's shelf record is updated.

## Hierarchy

- **Parent:** [[FR-001-lending]]
- **Children:** none (this is a story).

> [!note] Open points
> None.
