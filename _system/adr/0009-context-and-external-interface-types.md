# ADR-0009: Content types Context (Scope) and External Interface

- **Status:** accepted
- **Date:** 2026-05-24

## Context
ADR-0007 exposed a gap: req42 block 03 *Scope & boundaries* (arc42: Context &
Scope) had no content type. That left no typed home for the system boundary,
neighbours/external interfaces, and the deliberate boundary (what the system
*does not* do). `raw/context-diagram.md` is waiting in the inbox.

## Decision
We introduce **two** content types (templates in `_templates/`):

1. **Context** (`wiki/context/`, `CTX-NNN`) — the scope-and-context node of a
   system (`kind: business | technical`). Contains: a context diagram, **in
   scope**, **out of scope / boundaries** (explicit non-goals), a list of
   external interfaces (linking `EIF` nodes), the **user roles** (linking
   existing `[[STK-...]]` stakeholders), and an explanatory narrative.
2. **External interface** (`wiki/external-interfaces/`, `EIF-NNN`) — **each
   external interface is its own node** (a neighbouring system or a channel to
   an actor), carrying partner, direction (inbound/outbound/bidirectional),
   the data exchanged, and format.

User roles do not get their own type — they are stakeholders; the context node
references the relevant `[[STK-...]]`. This raises the number of content types
to **thirteen**.

## Consequences
req42 block 03 is covered; interfaces are nodes that can be cited from use
cases, data models, and more, and they appear in the graph. The context node
bundles diagram, boundaries, and neighbours in one place. Cost: two new
types/templates, an updated `CLAUDE.md` table, req42 anchor, and index.
Instances arise when `raw/context-diagram.md` is ingested (separately, with
the grill gate).
