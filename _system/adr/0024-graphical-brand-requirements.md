# ADR-0024: Graphical / brand requirements as Constraints + Quality scenarios; assets in `raw/`; project identity via `wiki.yaml`

- **Status:** accepted
- **Date:** 2026-06-24

## Context

A senior stakeholder with high influence — a founder, decision-maker, or
sponsor — will, sooner or later, bring **graphical requirements** into a
project: a logo, a colour palette, a required signature block on printed
documents, a "must look good and be readable from across the room" display
screen. Such requests typically arrive as decrees, not analysis, and often
arrive already embedded inside a functional wish ("print me a nice
certificate with a colourful logo", "the results board must be readable for
every visitor").

The schema taxonomy ([[0002-content-type-taxonomy|ADR-0002]]) has thirteen
content types — **none** of them is a natural home for "logo / colours /
brand". That creates two tensions:

1. **Graphics are decreed, not derived.** A logo or a palette does not
   *emerge* from analysis — a stakeholder *dictates* it. That is the textbook
   definition of a **Constraint** (a fixed boundary on the solution space),
   not a feature or quality statement derived from requirements. Treating
   taste as a "requirement" would wrongly put it up for discussion.
2. **Binary assets do not belong in `wiki/`.** The `wiki/` layer is a
   **text graph** of linked units; PNG logos and scanned signatures are
   human sources, not generated knowledge pages.

There is also a **governance risk**: a stakeholder's taste (which colour
scheme, "colourful and pretty") can collide with an *objective* need — e.g. a
pretty but low-contrast scheme that is unreadable on a results board across a
room. The wiki must neither override the stakeholder's taste nor stay silent
about the readability problem (CLAUDE.md: *flag and propose, never block or
silently rewrite — the human decides*).

Options considered:

- **A** — A **14th content type** "design/brand asset". Heavyweight: its own
  template, its own folder, its own audit/index logic — for what is so far a
  handful of rules. Violates the parsimony principle that
  [[0021-file-format-specs-at-boundary-owner|ADR-0021]] already enforced for
  file-format specs.
- **B** — Handle each request **ad hoc** inside whichever FR it touches. No
  shared home for the brand rule; logo/colour requirements would scatter
  across many FRs, drift apart, and the taste-vs-measurable distinction would
  be lost.
- **C** — **Decompose onto existing types**: the brand mandate as a
  **Constraint**, its application as a **Functional Requirement**, its
  measurable visual quality as a **Quality Requirement**; assets in `raw/`;
  taste-vs-measurable conflicts as an **Issue**.

## Decision

**Option C.** Graphical/brand requirements get **no content type of their
own**; instead they are projected onto the existing types — the same reframe
[[0021-file-format-specs-at-boundary-owner|ADR-0021]] applied ("no new
content type, place it with the right owner").

1. **The brand mandate itself → Constraint.** A logo, colour palette,
   typography, or a rule such as "requires a signature block on official
   documents" is recorded as a **Constraint** (`category: organizational`,
   with `origin:` pointing at the stakeholder who decreed it). As a decree,
   the constraint is **by definition non-negotiable** — we record it
   faithfully, we do not grill it down. (Where the emphasis is clearly a
   stakeholder's *personal* taste rather than an organizational standard,
   `category: political` is appropriate.)
2. **Applying the brand → Functional Requirement.** The *function* (which
   data, which flow) lives in the FR — e.g. "print a certificate", "show a
   live results display" — and **references** the brand constraint for its
   appearance. The FR carries the business content, not the pixels.
3. **Measurable visual quality → Quality Requirement.** Readability,
   contrast, and recognizability are captured as a **QR** (ISO 25010
   `usability` — UI aesthetics / appropriateness of recognizability, plus
   accessibility/contrast) with a **number** (e.g. "readable from 15 m;
   contrast ≥ WCAG AA"). **Only this makes colour discussable** without
   arguing about taste.
4. **Assets stay in `raw/`, the wiki references them by path.** Binary files
   go through the source lifecycle
   ([[0008-raw-inbox-ingested-archive|ADR-0008]]): inbox → after ingest
   `raw/ingested/`, with a slim provenance record in `raw/sources/`
   ([[0006-provenance-records-location|ADR-0006]]). The constraint names
   **exactly one** canonical file → a single source of truth; variants are
   archived. `wiki/` holds the *rule as text*, never the image.
5. **Taste-vs-measurable conflict → Issue, never an override.** If the
   aesthetic choice collides with the QR's measured value, an **`ISS-NNN`**
   is raised ([[0003-issues-as-meta-type|ADR-0003]]) linking the constraint
   and the QR and laying out the trade-off — **the stakeholder decides**,
   with the trade-off made explicit.

### Project identity today: text, not binary assets

The one place this repo currently carries a visual identity is the
dashboard's hero header (`_system/apps/dashboard/templates/index.html`),
which renders `system_name` and `tagline` — two plain-text fields read from
`_system/wiki.yaml` (`_system/apps/dashboard/templates/base.html` uses the
same `system_name` for the page `<title>` and footer). There is no per-project
logo, colour scheme, or header artwork: identity is carried entirely as text,
filled in once during the bootstrap workflow, and the dashboard shows neutral
defaults while it is blank. The **one fixed graphical mark** anywhere in the
dashboard is the req42 logo (`static/req42-logo-white.png`), used on the
`/req42` reference pages to identify that anchor framework — it is not a
per-project brand asset and is not affected by this ADR. Any future
per-project logo or colour request is new content, handled per the routing
rule below — it does not change this mechanism.

## Consequences

- **The schema stays lean.** Constraint + Quality + Source are reused instead
  of adding a 14th type; [[0002-content-type-taxonomy|ADR-0002]] stays
  untouched. This follows the same parsimony line as
  [[0021-file-format-specs-at-boundary-owner|ADR-0021]].
- **Routing rule for future graphical requests:** decree → Constraint,
  application → FR, measurable quality → QR, asset → `raw/`, taste conflict →
  Issue. Every new logo/colour/layout request sorts itself accordingly.
- **Assets follow the source lifecycle**
  ([[0008-raw-inbox-ingested-archive|ADR-0008]],
  [[0006-provenance-records-location|ADR-0006]]); exactly **one** canonical
  file as the single source of truth prevents the kind of drift that
  otherwise accumulates when several near-duplicate image variants circulate.
- **Colour/appearance becomes negotiable, not something to fight over.** The
  objective boundary lives in the QR; the taste lives in the constraint.
  Disagreements go through an Issue — consistent with the "flag and propose"
  principle (CLAUDE.md). The wiki never takes a side itself.
- **The dashboard's own identity mechanism is deliberately minimal** — two
  text fields in `wiki.yaml`, no binary brand assets to manage — and is
  orthogonal to this ADR's routing rule for a project's *content* about its
  own brand requirements.
- **Reversal** would mean introducing a dedicated "design/brand" content type
  via a superseding ADR — worth doing only once the volume of brand rules
  justifies the weight of its own type. Hence this record.
