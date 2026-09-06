# anchors

**Semantic anchors** — reusable methodological standards the wiki applies across
content types: goal frames (SMART, PAM), the user-story format, story quality
(INVEST), prioritization (MoSCoW), backlog shaping (story mapping). They are *method*,
not domain knowledge: authored and stable, never ingested from sources. They differ from `_templates/` (which
define a page's *shape*) and from `wiki/glossary/` (project-specific *vocabulary*).

**[[req42]]** is the **umbrella** among them: the requirements framework (Hruschka &
Meuten, CC BY-SA 4.0) whose 12 building blocks our content types implement, and
inside which the standards above are applied. The smaller anchors are method *within*
req42's blocks. Fuller reading copy: `docs/req42/`. See ADR-0007.

Each anchor is the single source of truth for its standard. Templates cite anchors
by wikilink rather than re-explaining them; instances may cite them too
(`> follows [[SMART]]`). Reference by alias — `[[SMART]]`, `[[INVEST]]`,
`[[MoSCoW]]` — not by a numeric ID; anchors are a small curated set, not an
enumerated collection.

**Enforcement is advisory.** During an audit (or a grilling session) the agent
checks instances against the relevant anchor's checklist and raises an `ISS-NNN`
Issue for misfits — it flags, it does not block or auto-rewrite. The human decides.

**Method & reference layer (ADR-0011).** Method *source* materials — the
copyrighted originals — are not shipped with this starter; ADR-0011 records
where they lived. What ships is the two derived layers: their *applied*
standards as anchors here, and their *readable* distilled references in `docs/`
(`docs/methods/`, `docs/req42/`) with attribution. Copyrighted originals (e.g. Patton, Hruschka) are summarised + attributed
in `docs/`, never reproduced verbatim there.
