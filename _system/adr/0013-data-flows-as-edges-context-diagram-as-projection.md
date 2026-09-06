# ADR-0013: Data flows as structured edges; context diagram as a projection

- **Status:** accepted
- **Date:** 2026-05-26

## Context
ADR-0009 introduced the **Context** and **External Interface** types, but left
open *how* data flows to human actors should be modelled — as their own `EIF`
node per channel, or on the stakeholders. Ingesting `raw/context-diagram.md`
answers this with data: of the seven "partners" in the context diagram, six
are already stakeholders (Role A, Role E, Role C, Role F, Role G); only
**System X** is a genuine neighbouring system. Three options were on the
table:

- **B1** — `EIF` only for systems, flows to humans structured nowhere → the
  diagram cannot be projected from data.
- **B2** — one `EIF` node per edge, humans included → roughly 9 nodes that
  duplicate use cases and stakeholders, and drift.
- **B3** — `EIF` only for systems; human flows as fields on the stakeholder.

The source node also shows that a single `direction:` isn't enough: *Role A*
is **bidirectional** (request data in / confirmation out), while *Role F*
sends **two** payloads.

## Decision
**B3 plus structured flow lists plus a projected diagram.**

1. **`EIF` nodes only for genuine external systems** (today, exactly: System
   X). Data flows to/from human **user roles** are captured as structured
   frontmatter fields on the relevant `[[STK-...]]`: `provides:` (inbound to
   the system) and `receives:` (outbound to the actor). User roles remain
   stakeholders, not their own type (confirming ADR-0009); the number of
   content types stays at **thirteen**.
2. **Every `EIF` carries a `flows:` list** instead of a single `direction:`
   field; each entry is `{ data, direction, format?, trigger? }`. This lets
   multiple and bidirectional flows per neighbour be represented.
   `direction`/`format` as standalone fields are dropped.
3. **The context diagram is not maintained by hand, it is projected.** The
   single source of truth is the structured edges (`EIF.flows` +
   `STK.provides`/`receives`). A dashboard render route draws the mermaid
   context diagram on the fly; an LLM audit loop redraws it whenever
   interfaces or roles change (implementation in
   [[ISS-010-context-diagram-projection-audit-loop|ISS-010]]). The context
   node's `diagram:` field is `generated`, not an embedded, drifting mermaid
   block.

## Consequences
`EIF` stays small and meaningful (genuine neighbouring systems); stakeholders
become machine-readable with respect to their data flows; the context diagram
can be regenerated from the edges at any time. Templates `context`,
`external-interface`, and `stakeholder` are updated, and the `CLAUDE.md` table
(EIF "direction") is changed accordingly to `flows`. Cost: the render route
and audit loop still need to be built
([[ISS-010-context-diagram-projection-audit-loop|ISS-010]]). This sharpens
the question ADR-0009 deliberately left open — "neighbouring system **or**
channel to an actor" — actor channels now live on the stakeholder, not as
`EIF`.

## Amendment (2026-06-22)
The **LLM audit loop** named in the *Decision* (point 3) is dropped; the
render route has been built. Rationale and resolution:
[[ISS-010-context-diagram-projection-audit-loop]] (resolved). Edge consistency
and render validity are covered by the regular audit
(`_system/workflows/audit.md`).
