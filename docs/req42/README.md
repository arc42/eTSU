# req42 — Framework Reference (Mirror)

> **Attribution & license.** This is a *distilled, adapted* reference of the **req42
> framework**, originally created by **Dr. Peter Hruschka & Markus Meuten**, licensed
> **CC BY-SA 4.0**. This page is an adaptation (summary + mapping to this vault), not a
> verbatim copy, and is shared under the same **CC BY-SA 4.0** license.
> Canonical source: <https://github.com/Hruschka/req42-framework> · <https://req42.org>
> The explanatory framing below is additionally **distilled from Dr. Peter Hruschka's
> req42 chapter** (ordinary copyright, © author) — summarised with attribution, not
> reproduced, and the verbatim chapter is not shipped with this starter.
> For the citable, condensed version used inside the wiki, see `_system/anchors/req42.md` (`[[req42]]`).

## What req42 is

req42 is *"the framework for effective, practical and pragmatic requirements
documentation and communication."* It is **agile and just-in-time**: capture a
requirement when it's needed, at the depth that aids communication — not as up-front
bureaucracy. It is the requirements counterpart to the **arc42** architecture template
and shares its toolchain.

Guiding principle: **"Never work without explicit goals or visions."**

## Structure — three groups (Hruschka)

Hruschka frames req42 as a **"Schrank" (cabinet) of ordered knowledge, not a document** —
the drawers are always open; whatever you learn about your endeavour goes in the right
drawer, in any form that lets stakeholders communicate. The 12 drawers fall into three
groups:

- **Clean Start** — 01 Business Goals · 09 Assets · 02 Stakeholder · 03 Scope. The
  Product-Owner foundation: align goals, know your means, your stakeholders and your boundary.
- **Main part** — 04 Product Backlog · 08 Domain Terminology ·
  06 Quality Requirements · 07 Constraints · 05 Supporting Models. The day-to-day RE work.
- **Management** — 11 Roadmaps · 10 Teams · 12 Risks & Assumptions.

Two principles worth keeping: **"Ziele sind Anforderungen"** (goals *are* requirements —
the ones that shouldn't keep changing within their period), and functional requirements
are a **hierarchy Epic → Feature → Story**, *not* a flat backlog — best maintained as a
**story map** (Patton; see `docs/methods/story-mapping.md`). req42 shares several drawers
with **arc42**, so if you use both, some drawers are managed jointly.

## The 12 building blocks

Each block answers a question; you fill the ones your product needs, when it needs them.

1. **Visionen & Ziele** (Business Goals) — *Why does this product exist?* Vision and
   business goals, clarified so everyone shares "what is to be achieved in which
   timeframes." Primary notation: **PAM** (Purpose · Advantage · Metric); alternatives
   include Product Canvas and Value Proposition. Goals are treated as stable
   requirements within their period.
2. **Stakeholder** — *Who is interested in or affected by the product?* The people and
   roles whose goals, concerns and influence shape it.
3. **Scope & Abgrenzung** (Scope) — *What is in vs. out, and what are the neighbours?*
   System boundary, external interfaces, and the context around the system.
4. **Product Backlog** — *What shall the product do?* The single, ranked source of
   functional requirements, organised as **Epics → Features → User Stories**, written
   user-centred (*"As [role] I want [function] so that [benefit]"*) and prioritised
   value-first.
5. **Modelle zur Unterstützung** (Supporting Models) — *How do we clarify complex
   items?* Graphical models that aid communication: flowcharts/activity diagrams, BPMN,
   state models, data/domain models, UI prototypes & wireframes. Used when they help
   (e.g. loops/conditional logic), linked bidirectionally to backlog items — not for
   their own sake.
6. **Qualitätsanforderungen** (Quality Requirements) — *How well?* Quality goals and
   measurable scenarios (the *-ilities*): performance, usability, security, etc.
7. **Randbedingungen** (Constraints) — *What limits the solution space?* Technical,
   organisational and legal constraints imposed from outside.
8. **Domänenbegriffe** (Domain Terminology) — *Do we share one language?* The glossary /
   ubiquitous language: one canonical meaning per term.
9. **Betriebsmittel & Personal** (Assets) — *What resources and people are required?*
   Operating resources and staffing.
10. **Teamstruktur** (Teams) — *Who builds it, how organised?* Team structure and
    responsibilities.
11. **Roadmaps** — *In what order, by when?* Release and roadmap planning over time.
12. **Risiken & Annahmen** (Risks & Assumptions) — *What might go wrong, what are we
    assuming?* Risks and the assumptions the requirements rest on.

## How this vault maps to req42

This requirements wiki implements req42's *requirements* blocks (01–08, 12) as typed
content units, and uses req42's recommended standards as semantic anchors. It does
**not** model the project-management blocks (09 Assets, 10 Teams, 11 Roadmaps).

| req42 building block | This vault |
|----------------------|------------|
| 01 Business Goals (Visionen & Ziele) | `wiki/goals/`, framed via `[[PAM]]` / `[[SMART]]` (ADR-0016) |
| 02 Stakeholder | `wiki/stakeholders/` |
| 03 Scope (Scope & Abgrenzung) | `wiki/context/` + `wiki/external-interfaces/` (ADR-0009) |
| 04 Product Backlog | `wiki/functional-requirements/` — one type, `stereotype: epic\|feature\|story`; hierarchy via `parent:`, story-mapped + `[[user-story-format]]`, `[[acceptance-criteria]]`, `[[INVEST]]`, `[[MoSCoW]]` |
| 05 Supporting Models (Modelle zur Unterstützung) | `wiki/use-cases/`, `wiki/activity-models/`, `wiki/data-models/` |
| 06 Quality Requirements (Qualitätsanforderungen) | `wiki/quality-requirements/` (ISO 25010 + ATAM) |
| 07 Constraints (Randbedingungen) | `wiki/constraints/` (arc42 categories) |
| 08 Domain Terminology (Domänenbegriffe) | `wiki/glossary/` |
| 09 Assets (Betriebsmittel & Personal) | *out of scope* |
| 10 Teams (Teamstruktur) | *out of scope* |
| 11 Roadmaps | *out of scope* |
| 12 Risks & Assumptions (Risiken & Annahmen) | `wiki/issues/` (`kind: risk`) + `[!assumption]` flags |

## Sources

- req42 framework repository — <https://github.com/Hruschka/req42-framework> (CC BY-SA 4.0)
- req42 website — <https://req42.org>
- Dr. Peter Hruschka, req42 explanatory chapter (© author) — distilled here with attribution; the verbatim chapter is not shipped with this starter.
- Related: arc42 architecture template — <https://arc42.org>
