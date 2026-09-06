---
type: anchor
title: req42
aliases: [req42, req42-framework]
tags: [anchor, framework, requirements]
applies-to: [whole-vault taxonomy, requirements coverage]
---

# req42

The pragmatic, agile, *just-in-time* framework for requirements documentation and
communication, by **Dr. Peter Hruschka & Markus Meuten** (CC BY-SA 4.0). It is the
**umbrella methodical reference for this vault**: our content types are essentially
req42's building blocks, and the smaller anchors ([[SMART]], [[PAM]], [[INVEST]],
[[MoSCoW]], [[user-story-format]]) are standards req42 uses *inside* those blocks.
Fuller reading copy: `docs/req42/`. Canonical source: <https://github.com/Hruschka/req42-framework>.

Guiding stance (Hruschka): a **"Schrank" (cabinet) of ordered knowledge, not a
document** — drawers are always open; put what you learn in the right one. Key
principles: **"Ziele sind Anforderungen"** (goals are the requirements that shouldn't
keep changing within their period); functional requirements form a **hierarchy
(Epic → Feature → Story)**, *not* a flat backlog, maintained as a [[story-mapping|story map]];
*"Never work without explicit goals or visions."*

The 12 drawers fall into three groups: **Clean Start** (01 Business Goals · 09 Assets ·
02 Stakeholders · 03 Scope), **main part** (04 Product Backlog ·
08 Domain Terminology · 06 Quality Requirements · 07 Constraints · 05 Supporting Models), and
**Management** (11 Roadmaps · 10 Teams · 12 Risks & Assumptions).

## The 12 building blocks → where they live here

req42's own block names are German in origin (Hruschka & Meuten); this vault names
them in English throughout, per its ubiquitous-language decision (ADR-0005).

| # | req42 block | Home in this vault |
|---|-------------|--------------------|
| 01 | Business Goals | Stakeholder goals ([[STK-...]]) + feature rationale; framed via [[PAM]] (req42's primary notation) or [[SMART]] |
| 02 | Stakeholders | `wiki/stakeholders/` |
| 03 | Scope | `wiki/context/` (boundary, in/out-of-scope) + `wiki/external-interfaces/` (neighbours); ADR-0009 |
| 04 | Product Backlog | `wiki/functional-requirements/` — one type, `stereotype: epic\|feature\|story`; **Epic → Feature → Story** via `parent:` links, projected as a [[story-mapping\|story map]]; [[user-story-format]], [[acceptance-criteria]], [[INVEST]], [[MoSCoW]] (ADR-0012) |
| 05 | Supporting Models | `wiki/use-cases/`, `wiki/activity-models/`, `wiki/data-models/` |
| 06 | Quality Requirements | `wiki/quality-requirements/` (ISO 25010 + ATAM) |
| 07 | Constraints | `wiki/constraints/` (arc42 categories) |
| 08 | Domain Terminology | `wiki/glossary/` (ubiquitous language) |
| 09 | Assets | *out of scope* — project resourcing |
| 10 | Teams | *out of scope* — org/team setup |
| 11 | Roadmaps | *out of scope* — release planning |
| 12 | Risks & Assumptions | `wiki/issues/` (`kind: risk`) + `> [!assumption]` flags |

Blocks 01–08 and 12 are modelled here; 09–11 are project-management concerns we
deliberately don't capture. Block 03 gained types in ADR-0009.

## Checklist (audit / grill — coverage lens)
- [ ] Goals are explicit and framed ([[PAM]]/[[SMART]]) — no silent work without goals.
- [ ] Stakeholders, glossary, constraints and quality requirements each have at least the obvious entries.
- [ ] Backlog items (stories/features) trace to a goal and a stakeholder.
- [ ] Supporting models exist where a flow/structure is non-trivial; linked both ways.
- [ ] Risks & assumptions are captured as Issues / `[!assumption]`, not left implicit.

A systematically empty block (e.g. no quality requirements at all) → raise an `ISS-NNN`.

> Cite as `[[req42]]`. Adapted under CC BY-SA 4.0 from the req42 framework
> (Hruschka & Meuten); the explanatory framing above is distilled from **Dr. Peter
> Hruschka's req42 chapter** (© author, kept in `raw/methods/`). See `docs/req42/` for
> the full attributed reference.
