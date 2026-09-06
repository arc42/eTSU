# ADR-0010: `aliases` field on the stakeholder template

- **Status:** accepted
- **Date:** 2026-05-25

## Context
Sources name the same role differently. The story (SRC-004) speaks of the
*Backoffice* — meaning the operational role we track as
[[STK-004-role-b|Role B]]. Such user-category / synonym names should be
findable without changing the canonical title or duplicating stakeholders.
The glossary template already has `aliases` for this; the stakeholder
template does not.

## Decision
The stakeholder template gets an optional field **`aliases: []`** (alternative
names / user-category labels). Obsidian then resolves `[[Backoffice]]` to the
canonical stakeholder. Role and person stay separate: a multi-person **role**
(e.g. Role B, alias *Backoffice*) can have several **instances** (person
stakeholders such as [[STK-006-role-c|Role C]] plus volunteers), linked
via `related`.

## Consequences
Synonyms/category names become findable without duplicates or title changes.
Cost: one more optional frontmatter field; existing pages don't need to
backfill it (empty = no alias). Groups spanning *several* roles (e.g.
"operators", "end users") are **not** aliases of a single stakeholder — they
are tracked as user groups on the context node
([[CTX-001-system-context]]).
