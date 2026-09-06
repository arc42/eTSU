# ADR-0001: Record architecture decisions

- **Status:** accepted
- **Date:** 2026-05-23

## Context
The structure of this wiki (content types, ID scheme, workflows) will evolve as we
learn what fits the domain. Undocumented structural changes cause agent drift and
human confusion.

## Decision
We will record every structural decision as an ADR in `_system/adr/`, using the
Nygard format (`0000-template.md`). The agent must consult ADRs before changing
conventions and write a new ADR when it does.

## Consequences
A durable rationale trail. Slightly more ceremony per structural change — accepted
as cheap insurance against incoherence.
