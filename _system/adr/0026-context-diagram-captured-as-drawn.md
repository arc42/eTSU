# ADR-0026: Capture the workshop context diagram as drawn — one EIF node per box

- **Status:** accepted
- **Date:** 2026-09-09

## Context

`SRC-004` (Ulrich Stürzlinger, "Context Diagram") delivers a 14-node diagram
around a **"TSU / eTSU — Gallery platform & digital marketplace"** box, arranged
in four tiers: SUPPLY, SUPPORT & ENABLEMENT, DEMAND, CORE OPERATIONS.

It is a **business ecosystem diagram, not a system context diagram.** Classified
against ADR-0013, of the fourteen boxes:

- **seven are human roles already held as stakeholders** — Artists, Museums &
  Owners, three buyer segments, and the shipper/insurer/restorer fused inside
  Logistics & Fulfillment;
- **four are TSU's own functions or eTSU's own capabilities** — Gallery
  Operations ("6 locations, staff, events"), Data & Analytics, Customer Support
  & Marketing, Business Growth & Content;
- **three bundle several distinct partners** — Logistics & Fulfillment (3),
  Technology & Infrastructure (cloud + payments + security + CDN), Regulatory &
  Compliance (tax + AML/KYC + law enforcement);
- **at most three genuine neighbouring systems are present at all** — payments,
  AML/KYC screening, and provenance verification — and every one of them is
  buried inside a bundled box, unnamed.

No arrow is labelled: solid means outbound and dashed means return, but no
payload, format or trigger is given anywhere.

ADR-0013 decided the opposite of what this diagram shows — `EIF` nodes **only**
for genuine external systems, with human actors carrying `provides:`/`receives:`
on their `[[STK-...]]`. Applying ADR-0013 strictly would have produced **zero to
three** `EIF` pages from this source and discarded the structure the workshop
actually produced.

Three options were on the table:

- **C1** — decompose: `EIF` only for the defensible neighbours, route internal
  capability boxes to `FR`/`QR`, keep human edges on stakeholders. Faithful to
  ADR-0013; loses the artefact's shape and pre-empts a boundary decision the
  group has not made.
- **C2** — capture as drawn: one `EIF` per box, all fourteen.
- **C3** — write no `EIF` at all until someone names the real systems and
  payloads. Most rigorous; leaves `wiki/external-interfaces/` empty.

## Decision

**C2 — capture the diagram as drawn, one `EIF` node per box, and carry the
correction as Issues rather than as silent reinterpretation.**

1. **Fourteen `EIF` pages, `EIF-001`…`EIF-014`**, one per box, `partner:` and
   `flows:` filled from each box's own sub-label. This **supersedes ADR-0013
   point 1** ("`EIF` nodes only for genuine external systems") *for this
   context*: nodes that are human roles, internal functions or infrastructure are
   admitted, each flagged on its own page.
2. **The `EIF` nodes own the context edges.** The seven stakeholders with `EIF`
   twins get `context_role: none` (ADR-0014) and keep `provides:`/`receives:`
   empty, so the projection renders each actor exactly once. ADR-0013's
   projection mechanism (point 3) is otherwise untouched.
3. **A `tier:` field is added to the external-interface template** —
   `supply | support | demand | core-operations` — recording which band of the
   source diagram a node came from. Without it the four tiers, which are the
   diagram's main organising idea, would be lost on ingest.
4. **The known defects are Issues, not edits.** `ISS-010` (boundary undefined),
   `ISS-011` (flows inferred, not sourced), `ISS-012` (bundled nodes hide
   distinct partners), `ISS-013` (third buyer segmentation).

## Consequences

The workshop artefact survives ingest intact and can be corrected *in the wiki*,
with every defect visible on the page that carries it rather than in a reviewer's
head. `CTX-001` renders as Ulrich drew it, which is what a workshop group needs
in front of them to argue about.

The cost is real and should not be understated: **`wiki/external-interfaces/`
no longer means "neighbouring systems".** Until `ISS-010` closes it means "boxes
someone drew outside the system". Roughly half these nodes are expected to be
reclassified or deleted when the boundary is agreed — Data & Analytics and
Gallery Operations most likely of all — and `EIF` IDs are then retired, not
reused. Any audit run before `ISS-010` closes will flag these nodes; that is
correct and expected, and `ISS-010` is the place it is tracked.

ADR-0024's principle — route new material to existing content types rather than
inventing one — is upheld: **no new content type was created.** The taxonomy
stays at thirteen (ADR-0002, ADR-0013). What changed is the *admission rule* for
one existing type, and one added field.

## Amendment (2026-09-09) — legibility of the projection

Capturing all fourteen boxes made the projected diagram unreadable, which is a
predictable consequence of the Decision above rather than a separate defect:
`build_context_diagram()` drew **one edge per direction** (28 labelled arrows)
and labelled each node with `partner:`, a full sentence by design. Fourteen
sentences and twenty-eight clauses around one box render, and cannot be read.

The projection is therefore changed — the *data* is untouched:

1. **One line per neighbour.** A neighbour with flows in both directions draws a
   single `<-->` edge, not two arrows. Edge count for `CTX-001` drops 28 → 14.
2. **One short label per line.** Each flow gains an optional `label:` (a word or
   two); the edge label is those values in the order written, deduplicated, and
   falls back to a clipped `data` when absent.
3. **`short_title:` on the interface**, mirroring the goal template's field of
   the same name. Node labels resolve `short_title` → `title` → `partner`;
   `partner` is now the last resort, not the first.
4. **`tier:` drives layout, not just provenance.** Each tier becomes a mermaid
   subgraph, and the tier decides which side of the centre a neighbour is ranked
   on — supply and support feed in from the left, demand and operations are
   served to the right. Fourteen scattered nodes become four labelled bands.
5. **A flow table beneath the diagram** (`build_context_flows()`) carries the
   detail the labels dropped: per neighbour, both directions, with `data`,
   `format` and `trigger` in full, plus the full `partner` name. Same edges, one
   projection each — the diagram for shape, the table for content.

Two latent bugs surfaced while doing this and were fixed in `_clean_label()`:
`&` was being **silently deleted** from every diagram label vault-wide
("Museums & owners" → "Museums owners") and now becomes "and"; and edge labels
were ordered inbound-then-outbound rather than in the order the author wrote the
flows.

Regression cover: `tests/test_context_projection.py`.
