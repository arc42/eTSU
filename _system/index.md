# Index

Content catalog, one line per page, grouped by type. The agent updates this on
every ingest (`_system/workflows/ingest.md`, step 6).

## Glossary

- [GLO-001](../wiki/glossary/GLO-001-tour.md) — Tour: a sequence of Shows, contracted and shipped as one unit.
- [GLO-002](../wiki/glossary/GLO-002-show.md) — Show: one stop of a Tour at a single gallery.

## Goals

- [GOAL-001](../wiki/goals/GOAL-001-eTSU-vision.md) — Vision: digital tour and gallery management platform for Gus Renoir's business.

## Stakeholders

- [STK-001](../wiki/stakeholders/STK-001-gus-renoir.md) — Gus Renoir, business owner / Head Office.

## Context

## External interfaces

## Data models

## Activity models

## Use cases

## Functional requirements

## Quality requirements

## Constraints

## Issues

## Sources

## Architecture Decisions (ADR)

- [0000-template](adr/0000-template.md) — ADR-0000, the Nygard template
- [0001-record-architecture-decisions](adr/0001-record-architecture-decisions.md) — ADR-0001, record every structural decision as an ADR in `_system/adr/`, using the Nygard format
- [0002-content-type-taxonomy](adr/0002-content-type-taxonomy.md) — ADR-0002, the typed wiki content types (glossary term, stakeholder, data model, activity model, use case, user story, feature, quality requirement, constraint, issue, plus source), drawing on DDD, arc42, ISO 25010 and ATAM
- [0003-issues-as-meta-type](adr/0003-issues-as-meta-type.md) — ADR-0003, Issue as a first-class content type that cross-cuts all others, raised instead of silently resolving contradictions
- [0004-semantic-anchors](adr/0004-semantic-anchors.md) — ADR-0004, reusable methodological standards (SMART, PAM, user-story-format, INVEST, MoSCoW) kept as semantic anchors in `_system/anchors/`, cited by alias
- [0005-ubiquitous-language-english](adr/0005-ubiquitous-language-english.md) — ADR-0005, the ubiquitous language of this wiki is English
- [0006-provenance-records-location](adr/0006-provenance-records-location.md) — ADR-0006, slim provenance records live in `raw/sources/`, separate from human-curated originals and from the log's narrative
- [0007-req42-as-umbrella-anchor](adr/0007-req42-as-umbrella-anchor.md) — ADR-0007, req42 is the umbrella anchor and methodological reference for the wiki's content types
- [0008-raw-inbox-ingested-archive](adr/0008-raw-inbox-ingested-archive.md) — ADR-0008, `raw/`'s top level is an inbox for new sources; ingested originals move to `raw/ingested/`
- [0009-context-and-external-interface-types](adr/0009-context-and-external-interface-types.md) — ADR-0009, introduces the Context (scope) and External interface content types for system boundary and real external systems
- [0010-stakeholder-aliases-field](adr/0010-stakeholder-aliases-field.md) — ADR-0010, adds an optional `aliases:` field to the stakeholder template for alternate names
- [0011-method-and-reference-layer](adr/0011-method-and-reference-layer.md) — ADR-0011, separates reusable method/reference knowledge from domain knowledge, split between anchors and `docs/`
- [0012-functional-requirement-stereotypes](adr/0012-functional-requirement-stereotypes.md) — ADR-0012, merges feature and user story into one Functional requirement type with stereotype `epic | feature | story`
- [0013-data-flows-as-edges-context-diagram-as-projection](adr/0013-data-flows-as-edges-context-diagram-as-projection.md) — ADR-0013, the context diagram is projected from typed data-flow edges rather than stored directly
- [0014-context-diagram-actor-roles-and-shapes](adr/0014-context-diagram-actor-roles-and-shapes.md) — ADR-0014, the context diagram distinguishes human actors from systems/organizations by shape and collapses duplicate context-level roles
- [0015-backlog-naming-convention](adr/0015-backlog-naming-convention.md) — ADR-0015, backlog naming convention: epics and features are named as nouns, stories and use cases as verb phrases
- [0016-goals-content-type](adr/0016-goals-content-type.md) — ADR-0016, introduces the Goal content type for req42 Block 01 (vision and objectives)
- [0017-functional-requirement-lane-field](adr/0017-functional-requirement-lane-field.md) — ADR-0017, adds a `lane:` field to functional requirements for story-map swimlanes when the backlog spans multiple surfaces
- [0018-projections-from-typed-edges](adr/0018-projections-from-typed-edges.md) — ADR-0018, diagrams and cross-cutting matrices are generated as projections of typed edges rather than hand-maintained
- [0019-data-model-product-and-sum-types](adr/0019-data-model-product-and-sum-types.md) — ADR-0019, data-model stereotypes distinguish product types (all fields present) from sum types (one-of variants)
- [0020-master-data-as-configuration](adr/0020-master-data-as-configuration.md) — ADR-0020, master data is loaded by file import, with runtime CRUD limited to specific owners and no soft-delete
- [0021-file-format-specs-at-boundary-owner](adr/0021-file-format-specs-at-boundary-owner.md) — ADR-0021, a data flow's file-format spec lives with whichever content type owns that boundary, not as a separate content type
- [0022-dashboard-self-shutdown-lifecycle](adr/0022-dashboard-self-shutdown-lifecycle.md) — ADR-0022, the dashboard shuts itself down when its browser tab closes (heartbeat + pagehide beacon) instead of running as a persistent background service
- [0023-glossary-term-network-force-graph](adr/0023-glossary-term-network-force-graph.md) — ADR-0023, the dashboard renders the glossary as an interactive client-side force-directed graph for viewers without Obsidian
- [0024-graphical-brand-requirements](adr/0024-graphical-brand-requirements.md) — ADR-0024, routes graphical/brand requirements to existing content types (Constraint, Functional requirement, Quality requirement, Issue) plus `raw/` for assets, rather than inventing a new type
- [0025-dashboard-req42-home-and-visual-identity](adr/0025-dashboard-req42-home-and-visual-identity.md) — ADR-0025, the dashboard's home page follows req42's reading order with a persistent nav, a flat vendored-font identity, maturity bars, issue flags, a QR join code and provenance chips
