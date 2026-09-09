# ADR-0027 — The data model is projected, from two carriers

- **Status:** accepted
- **Date:** 2026-09-09
- **Supersedes:** nothing. Fills the hole left open by `build_data_model_full_diagram()`,
  which returned `None` on purpose rather than show a hardcoded model.
- **Related:** [[0013-context-diagram-projected-from-edges|ADR-0013]],
  [[0019-one-file-per-entity|ADR-0019]],
  [[0023-glossary-term-network-force-graph|ADR-0023]],
  [[0026-context-diagram-captured-as-drawn|ADR-0026]]

## Context

req42 block 05 "Supporting Models" has always pointed at `wiki/data-models/`, and
the `/data-model` page has always rendered a diagram slot. The slot was empty,
with a comment saying a real projection was future work.

Two things had to be settled before it could be filled.

**Who says a thing is an entity.** A `DM-` page is one entity per file (ADR-0019)
and carries identity, attributes and a source of truth. But writing fifteen of
those is not something a workshop does between two coffees, and the room *is*
naming entities the whole time — in the glossary. The temptation is to let a
marked glossary term simply *be* an entity. That collapses two different jobs:
a glossary term is one canonical sentence about meaning, an entity is a
structure with identity and cardinality. Most terms are not entities, and an
entity's attributes have no business in a definition.

**Where relationships live.** The DM template prescribed a `Relationships.`
section of prose bullets. Nothing parsed them, and nothing could parse them
reliably: the same template already carries a hard rule that attribute names
must be in backticks, which exists precisely because prose parsing broke once.

## Decision

**A `DM-` page is the carrier of record. A marked glossary term is a stub.**

A glossary term may declare `stereotype: entity` or `stereotype: value-object`.
Such a term is promoted into the class diagram as a named, empty class annotated
`<<term>>`. It has no attributes and no relationships, because a glossary term
holds neither.

A DM page **supersedes** the stub for the same concept, so nothing is drawn
twice. It claims a term by linking it in `related:`, or by carrying the same
title — title matching is the forgiving half, because in practice the term gets
written first and the DM page forgets the back-link.

**Relationships are frontmatter, not prose.** DM pages carry a `relationships:`
list, each entry `{ verb, target, cardinality, kind }`. `kind:` is one of
association, aggregation, composition, inheritance. `cardinality:` is the
multiplicity at the **target** end only; deriving a source multiplicity from it
looked tidier and was wrong, since `0..*` would put a meaningless zero on the
owning side. A target that resolves to no page is dropped rather than drawn, so
a typo leaves a gap you notice instead of a ghost class.

The `Relationships.` body section stays, as narrative for humans. Frontmatter is
for the projection. That is the same split that makes the context diagram work
(`flows:`, ADR-0026).

**The diagram is filtered, not exhaustive.** Mermaid `classDiagram`, narrowable
by bounded context and focusable on one entity plus its direct neighbours.

## Consequences

Good: an unmodelled entity is *visible* as work outstanding rather than absent.
Marking a term costs one line during a workshop, and the model grows without
ceremony. A development team gets real attributes and cardinalities from the DM
pages, which is what they actually need, without the diagram being blocked on
those pages existing.

Good: filtering is a control, not a preference. The context diagram's one
readability regression was fourteen nodes drawn at once (ADR-0026), and a data
model gets larger than that. A projector shows one bounded context, or one
entity's neighbourhood.

Bad: two carriers means a precedence rule, and a precedence rule can surprise
someone. Renaming a glossary term so it no longer matches its DM page's title,
with no `related:` link either, resurrects the stub as a duplicate box. The
title-matching half is what makes that possible, and it is the price of not
requiring the back-link.

Bad: `stereotype:` now means something slightly different on a glossary term
(is this data at all?) than on a DM page (what kind of data?). The values
overlap deliberately, but they answer different questions.
