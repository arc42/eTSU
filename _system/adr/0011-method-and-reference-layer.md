# ADR-0011: Method & reference layer (raw/methods → anchors + docs)

- **Status:** accepted
- **Date:** 2026-05-25

## Context
We are accumulating more RE method knowledge (templates, Jeff Patton's
story-mapping article, Dr. Hruschka's req42 chapters — all under
`raw/methods/`). Until now it was unclear where such *method/reference*
material lives permanently and how it differs from domain knowledge. Some
sources are also **copyrighted** (Patton's article, Hruschka's book chapter) —
unlike the req42 *template* (CC BY-SA 4.0).

## Decision
Method knowledge mirrors the domain layering:

- **`raw/methods/`** — method *source material* (the originals; the
  copyrighted ones in particular stay private here and are **not** republished
  verbatim).
- **`_system/anchors/`** — the *applied* standards/techniques, distilled from
  that material, citable (`[[…]]`), and carrying a checklist (advisory
  enforcement). New anchor: **[[story-mapping]]**.
- **`docs/`** — *readable, distilled* references **with attribution** (e.g.
  `docs/methods/`, `docs/req42/`). `docs/` is the preferred home for
  preserved references (books, articles) — distilled and attributed, not
  verbatim.

License line: distillation + attribution + link in `docs/`; **no** verbatim
copying of protected works. (The req42 template stays CC BY-SA 4.0; Patton's
article and Hruschka's chapter are under ordinary copyright.)

## Consequences
Clear symmetry between domain and method; references live in `docs/` as
intended; copyright is respected. Adding an anchor remains ADR-worthy
(ADR-0004). Story maps themselves do **not** become a content type — they are
a projection/report over the product backlog hierarchy (see
[[story-mapping]]).
