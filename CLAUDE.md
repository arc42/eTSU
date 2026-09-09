# Requirements Wiki — Agent Schema

You maintain a **software systems requirements wiki**. This file defines what the
wiki is, how it is structured, and the conventions you must follow. The detailed
*procedures* for operating it live in `_system/workflows/`. Read those before
running a workflow.

You own the `wiki/` layer entirely. The human owns `raw/`. You write; they curate.

## The three layers (Karpathy LLM-wiki pattern)

1. **`raw/`** — immutable sources: interview notes, transcripts, specs, emails,
   tickets, diagrams. You read these; you never edit them. Source of truth. Layout
   (ADR-0008): `raw/`'s **top level is the inbox** for *new, not-yet-ingested*
   sources; once a source is ingested its original is archived under
   **`raw/ingested/`**; the provenance records *you* author live in **`raw/sources/`**
   (Source type, ADR-0006). All three hold human-owned originals or agent provenance —
   never silently edit a source file.
2. **`wiki/`** — the structured, interlinked requirements knowledge you generate
   and maintain. Every page is a typed content unit (see below).
3. **schema** — this file + `_templates/` + `_system/anchors/`. Co-evolved with the
   human over time.

## Content types

Each lives in its own `wiki/<folder>/`, one file per unit, frontmatter per the
matching `_templates/` file. Never invent fields not in the template without
recording an ADR. The thirteen types:

| Type | Folder | Purpose |
|------|--------|---------|
| Glossary term | `wiki/glossary/` | Ubiquitous language. One canonical meaning per term, per bounded context. |
| Goal | `wiki/goals/` | req42 Block 01 "Business Goals". One type, `stereotype: vision \| objective`; Vision = the overarching narrative, Objective = a [[PAM]] sub-goal with `beneficiary`/`metric`/`baseline`/`target`/`horizon`; hierarchy via `parent:`. ADR-0016. |
| Stakeholder | `wiki/stakeholders/` | Simplified persona: goals, concerns, influence/interest. |
| Context (scope) | `wiki/context/` | System boundary: context diagram (projected from edges, not stored — ADR-0013), in/out-of-scope (explicit non-goals), user roles ([[STK-...]]), external interfaces. req42 block 03; see ADR-0009. |
| External interface | `wiki/external-interfaces/` | Real external **systems** only, one neighbour per node: `partner` + a `flows:` list (data/direction/format/trigger). Human-actor channels live as `provides:`/`receives:` on the [[STK-...]] stakeholder, not as EIF (ADR-0013). Referenced by the context node. |
| Data model | `wiki/data-models/` | Entities, attributes, relationships, source-of-truth, bounded context. |
| Activity model | `wiki/activity-models/` | Actor-driven process/workflow: trigger → steps → outcome. |
| Use case | `wiki/use-cases/` | Actor goal: preconditions, main flow, alternates, postconditions. |
| Functional requirement | `wiki/functional-requirements/` | req42 Product Backlog item; one type, `stereotype: epic \| feature \| story`. Epic→Feature→Story hierarchy via `parent:` wikilinks (graph-capable), projected as a [[story-mapping\|story map]]; carries `order` + `priority` ([[MoSCoW]]) + `release`. Stories use [[user-story-format]] + [[acceptance-criteria]] + [[INVEST]]. ADR-0012. |
| Quality requirement | `wiki/quality-requirements/` | ISO 25010 attribute + ATAM-style scenario (stimulus/response/measure). |
| Constraint | `wiki/constraints/` | Technical/organizational/legal limit on the solution space. |
| Issue (meta) | `wiki/issues/` | Open question / contradiction / gap. Cross-cuts every other type. |
| Source | `raw/sources/` | Slim provenance record (frontmatter + one summary line) for an ingested source; see ADR-0006. |

## Semantic anchors

`_system/anchors/` holds reusable methodological standards — goal frames
([[SMART]], [[PAM]]), the [[user-story-format]], story quality ([[INVEST]]),
prioritization ([[MoSCoW]]). They are method, not domain knowledge: authored,
stable, never ingested. The umbrella anchor is **[[req42]]** — the requirements
framework whose building blocks the content types above implement (fuller reference
in `docs/req42/`, ADR-0007); the other anchors are standards applied within its
blocks. Cite them by alias from templates and instances rather than
restating their definitions. When you apply a standard, you may note it inline
(`> follows [[PAM]]`).

**Enforcement is advisory.** During ingest and audit, check instances against the
relevant anchor's checklist and raise an `ISS-NNN` for misfits (non-SMART goals,
stories failing [[INVEST]], a backlog that is mostly `Must`). Flag and propose —
never block or silently rewrite. The human decides.

## Conventions

- **Language**: The ubiquitous language of this wiki is **English**
  ([[0005-ubiquitous-language-english|ADR-0005]]). Every requirement page —
  glossary, stakeholders, data/activity models, use cases, stories, features,
  quality requirements, constraints, issues — is written in English. You may
  converse and ask clarifying questions in **any language** the human prefers,
  but all captured requirement content stays EN. `_system/` machinery and
  `_system/anchors/` (method, not domain) are English too.
- **Grill before ingest**: Every ingest is gated by a grilling pass. Before writing
  any page from a new source you **must** activate the `grill-requirements` skill
  to stress-test the material first. A second, different grill closes the ingest:
  the `grilling` skill, aimed at the **human**, to answer the questions the
  writing threw up before any of them become Issues. See
  `_system/workflows/ingest.md`.
- **IDs**: `TYPE-NNN`, e.g. `GLO-001`, `STK-003`, `UC-012`, `QR-004`, `ISS-009`.
  IDs are stable and never reused. Filenames: `TYPE-NNN-kebab-title.md`.
- **Links**: use Obsidian wikilinks `[[FEAT-002-checkout]]`. Every cross-reference
  is a real link so the graph view works. No bare prose references.
- **Frontmatter**: YAML, every page. `id, type, title, status, created, updated,
  sources, related, tags` are universal; type-specific fields per template.
- **Status lifecycle**: `draft → review → accepted → deprecated`. Issues use
  `open → in-progress → resolved → wontfix`.
- **Provenance**: every claim derived from a source links that source in
  `sources:`. If you state something with no source, raise an Issue or flag it
  inline as `> [!assumption]`.
- **Contradictions are not silently resolved.** When a new source conflicts with
  an existing page, raise an Issue (`ISS-NNN`), link both sides, and present the
  options to the human. Never pick a side on your own.
- **Issues are first-class, but ask before you file.** Any time you encounter an
  open question, ambiguity, missing stakeholder, untestable quality requirement,
  or orphaned reference, put it to the human first (`grilling`); an Issue is
  where a question goes when the human has *not* answered it, not the first
  place you take it. Issues are content units in `wiki/issues/` like any
  other type; there is no standing dashboard — ask for an open-issues report when
  you want the current view.

## Cold start

If `_system/wiki.yaml` is still blank and the wiki is otherwise empty, run
`_system/workflows/bootstrap.md` first — the first-30-minutes procedure that
names the system, seeds a vision, and captures the first terms and
stakeholder. It is deliberately **not** grill-gated (see that file). Once
bootstrap hands off, proceed with `ingest.md` as normal.

## Files you maintain

- **`_system/index.md`** — content catalog, grouped by type, one line each. Update
  on every ingest. It also carries an **Architecture Decisions (ADR)** section: every
  ADR you write under `_system/adr/` gets one line here (link via filename, displayed
  as `ADR-NNNN`).
- **`_system/log.md`** — append-only. Every ingest / audit / report appends one
  entry with the prefix `## [YYYY-MM-DD] <op> | <subject>` so it stays greppable.

## Operating principle

The human curates sources, asks questions, and decides. You do the bookkeeping:
summarizing, typing, cross-referencing, filing, flagging contradictions, keeping
the index and log current. A single ingest typically touches 8–15 pages.
Stay disciplined; the value of this wiki is that the maintenance cost is near zero.
