# ADR-0004: Semantic anchors as shared methodological standards

- **Status:** accepted
- **Date:** 2026-05-23

## Context
We reuse methodological standards across the wiki — goal frames (SMART, PAM), the
user-story format, story quality (INVEST), prioritization (MoSCoW). Embedding these
only inside templates duplicates their definitions and makes them uncitable;
putting them in the glossary pollutes domain vocabulary with method.

## Decision
We will keep these as **semantic anchors** in `_system/anchors/`, one file each,
referenced by alias (`[[SMART]]`) rather than a numeric ID. They are method, not
ingested knowledge. Templates and instances cite anchors instead of restating them.
Each anchor carries a checklist; the agent applies it **advisorily** during ingest
and audit, raising an Issue for misfits rather than blocking or rewriting.

## Consequences
One source of truth per standard, citable and enforceable, kept out of both
`_templates/` (shape) and `wiki/glossary/` (domain vocabulary). Adding or changing
an anchor is a deliberate, ADR-worthy act. Advisory enforcement keeps the
"agent flags, human decides" principle intact.
