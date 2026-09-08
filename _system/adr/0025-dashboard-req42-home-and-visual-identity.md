# ADR-0025: The dashboard's home page follows req42's reading order, with a persistent nav and a flat vendored-font identity

- **Status:** accepted
- **Date:** 2026-09-08

## Context

A design critique of `_system/apps/dashboard/` on 2026-09-07 scored it 27/40
(Nielsen heuristics) and found five classes of problem:

- **The home page mirrored the agent's folders**, not req42's reading order —
  tiles followed `wiki/<folder>/` names rather than the sequence a product
  owner or requirements engineer reads a requirements document in (vision →
  stakeholders → scope → backlog → …).
- **A generic visual identity**: emoji as tile icons, gradient stripes, a
  glow wash on hover, system fonts, and every tile in an identical card grid
  with no hierarchy.
- **Wayfinding was breadcrumbs only** — no persistent way to jump between
  sections; the req42 and Search tiles were the only entry points, and both
  lived below the fold.
- **Unexplained glyph abbreviations** on a projector: `⤳` for "linked wiki
  pages", `NS · MF` for stories/features, a `RELATIONS` column showing a bare
  number — legible on a laptop, opaque from the back of a dimmed room.
- **Bugs**: search facet counts were static (didn't follow the query), the
  presence footer said "1 participants", the ADR empty state suggested
  running ingest (ADRs are never produced by ingesting `raw/`), hard-wrapped
  prose rendered ragged through `nl2br`, and the footer timestamp was always
  UTC regardless of the host's zone.

## Decision

Address all five classes together, since the home page redesign, the visual
identity, and the copy/bug fixes are one connected piece of work:

1. **Home tiles in req42 reading order**, each carrying its req42 block
   number as an eyebrow: 01 Vision & goals (double-width) · 02 Stakeholders ·
   03 Scope · 04 Product Backlog · 05 Supporting Models · 06 Quality
   Requirements · 07 Constraints · 08 Domain Terminology (Glossary) · 12
   Issues · Architecture decisions · Latest changes. The standalone req42 and
   Search tiles are dropped.
2. **A persistent top navigation** on every page (Goals · Stakeholders ·
   Scope · Backlog · Quality · Glossary · Issues · ADRs · req42) with a
   search field; `/` focuses it. Breadcrumbs stay on sub-pages, inside the
   content column, for local orientation.
3. **A flat visual identity**: hairline-bordered panels, one border radius,
   no gradients, no glow, no drop-shadow hover lift, no emoji anywhere.
   Vendored OFL fonts — **Bricolage Grotesque** for text/headings/numbers,
   **JetBrains Mono** for IDs/code/eyebrows — served offline like every other
   asset, replacing system fonts. Design tokens (colour, spacing, radius)
   stay the single source of styling.
4. **Maturity bars** (draft → review → accepted → deprecated) under every
   tile count and list-page heading, with ADR and issue statuses mapped onto
   the same four steps, giving a consistent "how far along" signal across
   content types.
5. **Open-issue flags** on home tiles: each tile shows how many open issues
   point at pages of that type, surfacing risk before a click.
6. **A QR "Scan to join" code** in the hero and on a dedicated `/join` page
   for full-screen projection; the encoded address is the host's LAN IP by
   default, overridable via `DASH_PUBLIC_URL` (set by `dashboard.sh`) for
   rooms with DNS or a tunnel.
7. **Provenance chips** on every detail page, resolving frontmatter
   `sources:` to a new `/source/<stem>` view over a `raw/sources/` read-only
   mount; pages with no sources show an "unsourced" chip instead of silence.
8. **Copy fixes**: "client(s)" replaces "participant(s)" everywhere with
   correct plurals; glyph abbreviations (`⤳`, `NS · MF`, a bare `RELATIONS`
   count) become words — "N links", "N stories · N features" — via one
   `plural()` macro, so there is exactly one way to pluralise a count in the
   templates.
9. **A "Latest changes" tile** (cheap: file mtimes) and a one-line vault
   status strip under the hero, since nobody watches the dashboard live — the
   vault is regenerated a few times per workshop, so freshness is reported at
   the granularity of "when did this last change", not pushed in real time.
10. **`nl2br` is replaced by prose unwrapping** that respects existing lists
    and tables instead of turning every hard-wrapped line into a `<br>`.

## Consequences

- **~120 KB of vendored fonts** (`static/vendor/fonts/`, Bricolage Grotesque
  variable + JetBrains Mono 400/600, OFL-licensed) join mermaid and cytoscape
  as offline static assets — no network call at runtime, consistent with
  every prior vendoring decision in this app.
- **A new dependency, `segno`** (pure-Python QR code generation), for the
  join code — no other new runtime dependency.
- **A third read-only mount**, `raw/sources/` (`RAW_SOURCES_DIR`, mounted at
  `/sources` in Docker), alongside the existing `wiki/` and `_system/adr/`
  mounts — needed for `/source/<stem>` and the status strip's source count.
- **The search tile's inline preview was dropped** in favour of the nav
  search field: a live, always-available search box beats a tile that only
  showed a stale snapshot below the fold.
- **Home tiles now restate `REQ42_BLOCKS` metadata** (block number, label,
  order) directly in the tile-building code rather than deriving it from a
  single source, which is a small duplication risk if the block list ever
  changes — noted here for a later refactor, not blocking this decision.
