# ADR-0017: Functional-Requirement `lane:` field for story-map lanes

Date: 2026-05-28

## Status

Accepted

## Context

We model the [req42](../anchors/req42.md) Product Backlog as one
`functional-requirement` type with `stereotype: epic | feature | story` (ADR-0012),
projected into a story map ([[story-mapping]]). The epic set, after the
grilling on 2026-05-28 ([[ISS-009-worklist-stub-strategy]]), is **not flat**: it
spans three distinct surfaces.

| Lane | Examples | Property |
|---|---|---|
| **Backbone** (chronological user activities) | FR-001 Season Preparation → FR-002 Entity Registration → … → FR-005 Result Evaluation | left-to-right narrative; `order:` = sequence |
| **Platform lane** (operational, always-on) | FR-006 System Administration · FR-008 Master Data Maintenance | parallel to backbone; supports operations |
| **Display layer** (consumer-facing, always-on) | FR-007 Public Status Board | parallel to backbone; reads from multiple backbone steps |

The `order:` field alone cannot express this — it confuses *narrative position
within the backbone* with *lane membership*. We used a provisional convention
(`order: 1–99` backbone, `order: 100–199` platform, `order: 200+` display) for
FR-007 and FR-008, but the convention is non-obvious and bakes lane semantics into
a numeric range.

## Decision

Add a new field **`lane:`** to the `functional-requirement` template with three
enumerated values:

- `backbone` — chronological user-activity step (default; left-to-right Patton backbone).
- `platform` — operational/technical capability that runs parallel to the backbone
  (e.g. user/permission admin, master-data maintenance, monitoring).
- `display` — consumer-facing read layer that consumes from backbone artifacts
  (e.g. a public status board, a personal dashboard view).

Semantics:

1. **`order:` is interpreted within the lane.** Backbone lane is sequenced
   `1, 2, 3, …`; platform lane is sequenced `1, 2, …`; display lane is sequenced
   `1, 2, …`. Order has *no* meaning across lanes.
2. **Default lane is `backbone`** when the field is missing (covers all existing
   FRs in the simplest case).
3. **Stories and features inherit the lane of their parent epic** unless
   explicitly overridden — usually the parent's lane fully determines it. Children
   only need a `lane:` if they intentionally cross-lanes (rare; should raise an ISS).
4. **Index grouping** in `_system/index.md` follows lanes; the dashboard story-map
   projection (`[[story-mapping]]`) groups by `lane` and sorts by `order` within
   each lane.

## Consequences

- Schema change: `_templates/functional-requirement.md` gets a `lane:` field with
  a one-line comment about the three values and default.
- Migration of existing FRs (one-time, no behavioral change):
  - FR-001..FR-005: `lane: backbone`, `order:` unchanged (1..5).
  - FR-008 Master Data Maintenance: `lane: platform`, `order: 1` (was 100 —
    adjusted to in-lane numbering).
  - FR-007 Public Status Board: `lane: display`, `order: 1` (was 200 — adjusted).
  - FR-006 System Administration (new): `lane: platform`, `order: 2`.
- Existing prose hints ("platform lane", "display layer") that referenced
  the order-range convention are kept as comments but the authoritative signal is
  now `lane:`.
- The story-map projection later (analogous to context-diagram projection in
  ADR-0013) groups by `lane` first, then renders `order`-sequenced bars/cards
  within each lane.

## Alternatives considered

1. **Stick with order-ranges (status quo).** Rejected — the convention is implicit
   and non-discoverable; future readers would need to know that 100+ means
   platform. Numeric overloading is the kind of "schema hack" we'd otherwise call
   out in an audit.
2. **Use `tags:` to mark lanes (e.g. `tags: [functional-requirement, platform]`).**
   Rejected — `tags:` is for cross-cutting topical labels, not for primary
   classification; querying by tag is uglier than by enum field.
3. **Split into multiple FR types (e.g. `functional-requirement-backbone`,
   `functional-requirement-platform`).** Rejected — would conflict with ADR-0012
   (one type, stereotypes) and inflate the type taxonomy.

## Related

- ADR-0012 — Functional requirement stereotypes (epic / feature / story; one type).
- ADR-0013 — Data flows as edges; context diagram as projection (same pattern:
  derive the visualization from structured fields).
- [[story-mapping]] — anchor; projection consumer of `lane:` + `order:`.
- [[ISS-009-worklist-stub-strategy]] — grilling outcome that introduced the
  three-lane decomposition.
