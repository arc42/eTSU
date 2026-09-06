# ADR-0015: Backlog naming convention — epic/feature as noun, story/use-case as verb

- **Status:** accepted
- **Date:** 2026-05-27

## Context
[[ADR-0012]] introduced the **Functional requirement** type with
`stereotype: epic | feature | story`, but left the **title grammar** open. The
template said `title: <short imperative name>` (i.e. a verb), while practice
on the ground (ISS-009) named epics as **noun phrases** ("Entity Setup",
"Master Data Maintenance" …) — a contradiction.

"Epic" is not an IREB/CPRE term (it comes from agile/SAFe), so there is no
binding IREB naming rule for it. But the surrounding literature leans heavily
**verb-centric**: Cockburn names use cases as a **verb + object** (an active
goal); Jeff Patton's story map names backbone activities and tasks as
**verbs**; the IREB/SOPHIST-Rupp template builds the **requirement sentence**
around a process word (verb) and treats **nominalization** as an ambiguity
smell — but that applies to the *sentence*, not the *heading* of a backlog
item. For coarser backlog nodes (epic/feature), **noun/capability naming** is
the common tool-practice convention, and in German is idiomatic through
nominal style.

## Decision
**Convention "A": the title's part of speech signals granularity.**

- **Epic + Feature** → **a noun phrase with a clear outcome** (e.g. *Season
  Preparation, Entity Registration, Entity Processing, Result Evaluation,
  System Administration*).
- **Story + Use case** → **verb + object** (an active goal; e.g. *Cancel
  Entity, Evaluate Attempt*).
- **Avoid anglicisms** (the domain language was German as of ADR-0005 on
  2026-05-27; since its rewrite on 2026-09-06 the domain language is English,
  so this point is now historical) — e.g. "Reporting" → "Result Evaluation".

Enforcement stays **advisory** (like every anchor standard): check against the
naming rule during ingest/audit, report deviations as `ISS-NNN` — never block
or silently rename. The rule is anchored in the [[story-mapping]] anchor
(including a grill/audit checklist item).

## Consequences
Refines [[ADR-0012]] (whose title grammar was left open there). Updated:
`_templates/functional-requirement.md` (a stereotype-specific `title:` hint
plus an author note), `_templates/use-case.md` (`title:` = "verb + object"),
and the [[story-mapping]] anchor (naming rule + checklist item). **No
migration** — there are no `FR-…` instances yet; the six epic candidates in
`raw/epic-candidates.md` are already named consistently (noun phrases). What
remains open is only applying the rule in practice at the first real backlog
ingest.
