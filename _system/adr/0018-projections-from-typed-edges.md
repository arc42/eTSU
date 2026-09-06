# ADR-0018: Diagrams and matrices as projections of typed edges

- **Status:** accepted
- **Date:** 2026-05-28

## Context
Cross-cutting views — diagrams (context, data model, use case), coverage
matrices (goals × backlog, stakeholder × value), trees (story map,
vision-goal) — condense information from several content types into a
two-dimensional view. So far the wiki has handled them **ad hoc**:

- [[ADR-0012]] (2026-05-25) solves this for the **story map** — projected from
  the `FR.parent:` tree plus `order` / `release` / `priority`.
- [[ADR-0013]] (2026-05-26) solves this for the **context diagram** —
  projected from `STK.provides:` / `receives:` plus `EIF.flows`.

Both times the same pattern was chosen without generalizing it. The new
`goal` content type ([[ADR-0016]]) creates another cross-cutting view (a
goal-coverage matrix), and more are foreseeable (data model, use-case
diagram, vision-goal tree, quality tree, traceability …). Before the next
special case comes up, the meta-principle should be written down so it does
not have to be re-derived from scratch every time.

Three paths were on the table in principle:

- **A** — Every view as its **own content type** (one `coverage` file per
  matrix, one `diagram` file per diagram). Duplicated data storage,
  inevitably goes stale, no advantage over a table in Markdown.
- **B** — Views as **hand-maintained Markdown tables** on overview pages.
  Doesn't scale (every new instance requires a table edit), drifts away from
  the source content, audit effort grows quadratically.
- **C** — Views as a **projection** from the already-carried, **typed edges**
  (frontmatter fields, wikilinks). The content type stays the single source of
  truth; the view is generator output.

C has already been applied twice (ADR-0012, ADR-0013) and works.

## Decision
**Cross-cutting views are projections from typed edges — never stored
artifacts.** The single source of truth is the frontmatter fields and
wikilinks of the content types. Views are generated on demand: the Obsidian
graph, dashboard routes, LLM audits. **No embedded mermaid blocks** in wiki
pages, **no hand-maintained overview tables**, **no bidirectional edge
maintenance**.

### Active and planned projections

| Projection | Source edges (single source of truth) | Anchored in | Status |
|---|---|---|---|
| Story map | `FR.parent:` + `order` / `release` / `priority` / `lane:` | [[ADR-0012]], [[ADR-0017]] | active (anchor [[story-mapping]]) |
| Context diagram | `STK.provides:` / `receives:` + `EIF.flows` | [[ADR-0013]], [[ADR-0014]] | active (dashboard render) |
| **Goal-coverage matrix** | `FR.goal: [[GOAL-...]]` (multi-valued) | **this ADR** + [[ADR-0016]] | active (backlinks); dashboard render planned |
| Vision-goal tree | `GOAL.parent:` (objective → vision) | [[ADR-0016]] | planned (with the first goal ingest) |
| Data-model diagram | `data-model.entities` + relationship fields | open | planned (with the first data-model ingest) |
| Use-case diagram | `UC.actor:` ([[STK-...]]) + `UC.parent:` ([[FR-...]]) | open | planned (once UCs exist — top-down from epics, [[ISS-009-worklist-stub-strategy]]) |
| Stakeholder-value matrix | `STK` × `GOAL.beneficiary:` (+ `FR.goal:` indirection) | open | planned |
| Quality tree (utility tree) | `QR.applies-to:` ([[FR-...]]) + `attribute:` | open | planned |
| Traceability matrix | Goal × FR × UC × QR — composed from all edges | open | optional / on demand |
| Issue heatmap | `ISS.affects:` × content type / status | open | optional |

The list is **open** — new views follow the same pattern: type the edge
first, then project.

### Conventions for every projection

1. **Edges live once**, on the **more specific side** (instance → context).
   Example: `FR.goal:` (FR → goal), **not** additionally `GOAL.realized_by:`
   (goal → FR). Obsidian backlinks supply the reverse direction automatically.
2. **"Upward" is the normal direction**: finer → coarser, instance → more
   abstract context. Consistent with the story map (`story → epic`), goal
   coverage (`FR → goal`), and the vision-goal tree (`objective → vision`).
3. **Empty values are real statements**, not "not filled in yet."
   `FR.goal: []` deliberately means an enabler (e.g. the platform lane);
   `[[ISS-...]]` marks an actual gap. Likewise `parent: []` means a root node,
   not "hierarchy unclear."
4. **Rendering is the generator's job**, not wiki-page content. Mermaid
   blocks, embedded images, or Markdown coverage tables directly in wiki
   pages are forbidden — they drift. Allowed: generated artifacts in
   `_system/apps/dashboard/` or as LLM audit output.
5. **Drift becomes visible.** During audit (the grill skill), each projection
   checks its invariants (see below); violations are flagged as `ISS-NNN`,
   never silently repaired.

### Audit invariants per projection (advisory)

- **Story map** — every backlog item carries `parent:` (except epics) and
  sits in a lane; backbone order via `order` has no gaps.
- **Context diagram** — every external actor has at least one edge
  (`provides`/`receives` or `EIF.flows`); every edge has `data`/`direction`.
- **Goal coverage** — every backlog item sets `goal:` (≥ 1 GOAL) **or** is
  explicitly `goal: []` with `lane: platform`/`display`. Every goal is served
  by ≥ 1 FR (otherwise ⇒ `[[ISS-...]]` "goal with no carrier").
- **Vision-goal tree** — exactly one GOAL root per system (`stereotype:
  vision`, `parent: []`); every objective has `parent:` pointing to the
  vision.
- **Data model, use case, quality tree** — invariants are established at
  each type's first ingest.

## Consequences

**Implemented immediately** (together with this ADR):

- `_templates/functional-requirement.md` — the `goal:` field is retyped:
  `[[GOAL-...]]` instead of `[[STK-...]]`, multi-valued, `[]` = enabler.
- `_templates/goal.md` — a "Served by" section projected from backlinks
  (explicitly documented, not to be maintained by hand).
- `FR-001..008` — `goal:` backfilled against the coverage matrix agreed in
  conversation; old stakeholder pointers (a workaround from before `goal`
  existed) implicitly move to `related:` (already present there).
- `_system/anchors/story-mapping.md` — the checklist item on the new field
  semantics was sharpened.

**Deliberately deferred:** the dashboard render route for the goal-coverage
matrix (analogous to the context render route,
[[ISS-010-context-diagram-projection-audit-loop]]); the goal ingest itself
(content of `raw/vision-draft.md` → `GOAL-001..005`); LLM audit loops per
projection.

**Risk:** the `GOAL-001..005` wikilinks pre-assigned in the FRs stay
**unresolved** (Obsidian dangling links) until the goal ingest happens.
Acceptable — the IDs are fixed, the ingest will follow; the alternative would
have been to defer the backfill until after the ingest. We accept getting
ahead of it because the coverage matrix creates value for the ongoing epic
work right now.

**Deliberately not changed:** no consolidation of ADR-0012 / ADR-0013 into
this meta-ADR. Both remain in place as special cases and are only cited here
— backward stability, not a "refactor" of accepted decisions.
