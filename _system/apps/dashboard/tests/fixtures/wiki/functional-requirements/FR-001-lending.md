---
id: FR-001
type: functional-requirement
title: Book Lending
status: accepted
created: 2026-09-06
updated: 2026-09-06
sources: []
related:
  - "[[STK-001-librarian]]"
tags: [functional-requirement]
stereotype: epic
parent: []
priority: Must
release: v1
lane: backbone
order: 1
goal:
  - "[[GOAL-002-faster-lending]]"
---

# Book Lending

## Epic: Short description

As the librarian, I want the whole lending process — from checkout to
return — to be fast and error-free, so that members spend less time at the
front desk.

**PROBLEM / GOAL**

Checking a book out or in today relies on manual bookkeeping, which is slow
and prone to mistakes.

**Success metric(s).**

Average checkout time drops and lending errors approach zero (see
[[GOAL-002-faster-lending]]).

**Scope.** in: checkout, confirmation, and return of a book · out:
reservations, fines

## Hierarchy

- **Parent:** none (this is an epic).
- **Children:** [[FR-002-checkout]] (feature), [[FR-005-return-a-book]] (story)

> [!note] Open points
> None.
