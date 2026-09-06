# ADR-0002: Content-type taxonomy

- **Status:** accepted
- **Date:** {{date}}

## Context
A requirements knowledge base needs a typed vocabulary so the agent files
consistently and the graph stays navigable. We draw on established models: DDD
(ubiquitous language, bounded contexts), arc42 (constraints, quality), ISO 25010
(quality attributes), and ATAM (quality scenarios).

## Decision
We will use ten wiki content types — glossary term, stakeholder, data model,
activity model, use case, user story, feature, quality requirement, constraint,
issue — plus a `source` provenance type in `raw/`. Each has a template in
`_templates/` and a folder in `wiki/`. IDs follow `TYPE-NNN`.

## Consequences
Predictable filing and strong cross-linking. The taxonomy is opinionated; adding or
splitting a type requires a new ADR. Quality requirements carry an ATAM scenario so
they stay testable rather than vague.
