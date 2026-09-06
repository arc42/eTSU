---
id: FR-003
type: functional-requirement
title: Scan a Book
status: accepted
created: 2026-09-06
updated: 2026-09-06
sources: []
related:
  - "[[GLO-001-book]]"
tags: [functional-requirement]
stereotype: story
parent:
  - "[[FR-002-checkout]]"
priority: Must
release: v1
lane: backbone
order: 1
goal: []
---

# Scan a Book

## Story

As a librarian, I want to scan a book's barcode, so that its identity is
captured without typing.

**Acceptance criteria.**

- **Given** a book with a valid barcode, **when** it is scanned, **then** the
  book's record is identified within the checkout flow.

## Hierarchy

- **Parent:** [[FR-002-checkout]]
- **Children:** none (this is a story).

> [!note] Open points
> None.
