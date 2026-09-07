# Fable-ous dashboard — design spec

**Date:** 2026-09-07 · **Branch:** `fable-ous-dashboard` · **Status:** agreed with the human

## Why

A design critique of `_system/apps/dashboard/` (Nielsen score 27/40) found: the home page
mirrors the agent's folders rather than what a product owner / requirements engineer wants
to read; the visual identity is generic (emoji icons, gradient stripes, glow wash, system
fonts, identical card grid); wayfinding is breadcrumbs only; several abbreviations and
glyphs are unexplained on a projector; and a handful of bugs (search facet counts never
update, "1 participants", ADR empty state gives the wrong next step, hard-wrapped prose
renders ragged, footer time in UTC).

## Audience and tone

- **Who:** software-engineering workshop participants, product owners, business analysts,
  requirements engineers. Read-only. Educational, not production.
- **Context:** projected in a dimmed room *and* opened on participants' own laptops/phones.
  The vault is regenerated a few times per workshop; nobody watches it live.
- **Tone:** a well-typeset requirements document that happens to be a web page. Calm,
  precise, quietly opinionated. Dark by default (projection), light as opt-in. One playful
  touch survives: nicknames on "Who's here".

## Decisions

1. **Home page in req42 reading order.** Tiles carry the req42 block number as an eyebrow.
   Order: 01 Vision & goals (double-width) · 02 Stakeholders · 03 Scope · 04 Product Backlog ·
   05 Supporting Models · 06 Quality Requirements · 07 Constraints · 08 Domain Terminology
   (Glossary) · 12 Issues · ADRs · Latest changes. The req42 and Search tiles go away.
2. **Persistent top navigation** on every page (Goals · Stakeholders · Scope · Backlog ·
   Quality · Glossary · Issues · ADRs · req42) with a search field; `/` focuses search.
   Breadcrumbs stay on sub-pages, inside the content column.
3. **Visual identity:** flat panels with hairline borders, one radius (8px), no gradients,
   no glow, no emoji, no drop-shadow hover lift. Vendored OFL fonts, offline like every
   other asset: **Bricolage Grotesque** (text + headings + numbers) and **JetBrains Mono**
   (IDs, code, eyebrows). Tinted neutrals stay navy.
4. **Maturity bar** (draft → review → accepted → deprecated) under every tile count and
   under every list-page heading; ADR / issue statuses map onto the same four steps.
5. **Open-issue flag** on each home tile: how many open issues point at pages of that type.
6. **QR "Scan to join"** in the hero and a `/join` page for full-screen projection; the URL
   is the host's LAN address (`DASH_PUBLIC_URL`, set by `dashboard.sh`).
7. **Provenance chips** on every detail page linking `sources:` to a new `/source/<stem>`
   view of `raw/sources/`; a page with no sources shows an "unsourced" chip.
8. **"Latest changes"** tile (cheap: file mtimes) and a one-line vault status strip under
   the hero. No live push; nobody watches live.
9. **Copy:** "client(s)" replaces "participant(s)" everywhere, with correct plurals.
   Abbreviations become words ("3 stories · 1 feature", "4 links", "1 epic").
10. **Bugs fixed:** live search counts, plural, ADR empty copy, empty-objectives hint,
    prose unwrapping instead of `nl2br`, footer time in the host's zone.

## Out of scope

Live push / auto-reload, editing, authentication, printing/export, Obsidian parity.
