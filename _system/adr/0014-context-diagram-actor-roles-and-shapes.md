# ADR-0014: Context diagram — actor-role projection and person/organization shape

- **Status:** accepted
- **Date:** 2026-05-27

## Context
ADR-0013 projects the context diagram from the edges (`EIF.flows` +
`STK.provides`/`receives`): one node per stakeholder with its flows, **all as
identical rectangles**. Review turned up two shortcomings:

- **Shape.** Human actors (Role A, Role D, …) are visually indistinguishable
  from systems/organizations (System X, Role E) — everything is a white
  rectangle.
- **Redundancy.** Seven stakeholder nodes, several of which overlap at the
  **context level**: *Role C* and *Role B* are both planning roles (ISS-011),
  and *Role A* and *Role D* share the request/result channel. *Role F*
  belongs to execution, not to the outside view of the system context.

The **stakeholder personas** are deliberately kept separate, though (their
own influence/interest, goals, concerns). Actually merging the `STK` pages
would destroy that information. What's needed is a **projection-only**
coarsening.

## Decision
The stakeholder pages stay unchanged and detailed; the **context diagram**
aggregates them into coarser actor roles. Two declarative frontmatter fields
on the stakeholder drive this, evaluated by the projection function:

1. **`nature: person | organization`** (default `person`). Controls the node
   shape:
   - `person` → **actor symbol** (a stick figure + stadium shape, light fill).
   - `organization` → grey rectangle (like a system).
   - `EIF` nodes are always systems → grey rectangle.

2. **`context_role:`** — label and **merge key** in the context diagram.
   - Missing (or empty) → the stakeholder's title is the label (default,
     backward-compatible).
   - The same `context_role` value on several stakeholders → **one** node;
     their `provides`/`receives` are merged (deduplicated, stable order).
   - Value **`none`** → the stakeholder does **not** appear in the diagram;
     its `provides`/`receives` remain on the page (no data loss).

Concrete projection for this system:
- *Role A* (STK-001) + *Role D* (STK-007) → **"Role A and Role D"**.
- *Role B* (STK-004) + *Role C* (STK-006) → **"Organizer"**.
- *Role F* (STK-009) → `none` (hidden; an execution-time role).
- *Role E* (STK-008) → `nature: organization` (grey rectangle).

## Consequences
Personas stay separate and complete; only the outside view is decluttered and
readable (person vs. system/organization at a glance). Refines ADR-0013
(whose "one node per stakeholder with flows" becomes "one node per
`context_role`"). The `stakeholder` template and the projection function
`build_context_diagram()` are updated; the code used by the audit loop
(ISS-010) stays pure/string-based. Open question: the standalone **Role G**
node (flow "provisional score" during execution) — does this execution-time
data flow even belong in the *system context*, or should it also be hidden?
It stays visible until that is resolved.
