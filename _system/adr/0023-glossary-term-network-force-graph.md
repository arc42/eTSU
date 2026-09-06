# ADR-0023: Glossary term network as an interactive force graph (cytoscape.js, client-side layout)

- **Status:** accepted
- **Date:** 2026-06-22

## Context

The dashboard (`_system/apps/dashboard/`) is not just a viewer, it is also a
**demo and persuasion artifact**: it should win stakeholders over to the wiki
idea **without Obsidian**. For the glossary — the ubiquitous language, the
heart of the domain — there is no view that brings the *network* of terms to
life at a glance. What exists is not enough:

- **The Obsidian graph** (force-directed, filterable on `path:wiki/glossary`)
  — requires Obsidian, which rules it out for the target audience.
- **`glossary.html`** (a table with a "connectivity" sort plus a relation
  count) — shows the *degree* of connectedness, not the *layout* / clusters.
- Every dashboard diagram so far (context, story map, goals) is **Mermaid**,
  rendered server-side as a deterministic string ([[ADR-0013]], [[ADR-0018]]).

Data situation (checked 2026-06-22): 27 GLO nodes; **101 GLO→GLO** edges plus
**~35 cross edges** (12 DM, 8 STK, 5 EIF, 3 GOAL, 2 CTX, 3 ISS, 1 FR, 1 CON).
`bounded-context` (all the same single domain) and `status` (26 draft, 1
deprecated) are **uniform** → unusable as a colour axis. GLO-027 has 0
glossary-internal edges (an orphan).

**Tension.** A force graph **cannot be Mermaid** — Mermaid's auto-layout is
hierarchical (dagre), not a physics layout; it would produce the familiar
boxes-and-arrows look, not the "living network" the demo needs. This forces a
**JS graph library** into the dashboard for the first time, and a
**client-side, non-deterministic layout** — a break with the "everything is
server-rendered Mermaid" rule held until now.

Options:

- **A** — Mermaid flowchart (dagre). No physics layout, no clustering effect;
  misses the demo goal.
- **B** — Use the Obsidian graph as the demo. Requires Obsidian → rules out
  the target audience (who don't have Obsidian).
- **C** — A client-side force graph (JS library) over server-projected graph
  data.

## Decision

**A standalone "term network" in the dashboard: a client-side force graph
(cytoscape.js + fcose) over a deterministic server projection of the
`related:` edges.** Option C.

The reframe that keeps this consistent with [[ADR-0018]]: **the single
source of truth stays server-deterministic.** A route `/graph/glossary`
projects a graph JSON `{nodes, edges}` from the typed `related:` edges —
exactly the pattern from [[ADR-0018]] (projection of typed edges), just with
a different output format than the Mermaid string. **Only the layout** moves
into the browser (physics). So this is not a departure from [[ADR-0018]] but
another projection within the same open family — the first one with a JS
renderer instead of Mermaid.

1. **Renderer: cytoscape.js + fcose layout.** Graph-specialised, declarative
   styling (selectors), built-in physics layouts, click handlers, well
   maintained. d3-force would be the most flexible visually, but the most
   hand-rolled/high-maintenance — against the "maintenance cost ≈ zero"
   principle. The first JS graph library in the dashboard alongside
   mermaid.js.
2. **Edges undirected & deduplicated.** `related:` is asymmetric project-wide
   (the pointer-to-context convention, [[ADR-0018]] §1); for a *semantic
   language network*, undirected is the honest representation (A↔B as *one*
   edge, otherwise you get false direction artifacts). The edge source is
   **exclusively the `related:` frontmatter** — **not** body wikilinks (noisy,
   uncurated).
3. **Default = glossary only; expansion layered per type button.** Initially
   only GLO nodes + GLO→GLO edges. Cross-connections to other types are
   revealed via **buttons** (DM, STK, EIF, GOAL, "more") — each showing the
   1-hop neighbours of the displayed GLO nodes, additive, independently
   toggled, with an incrementally animated relayout (no re-randomizing). The
   buttons *are* the legend (a coloured chip with type + edge count, filled
   when active). Dramaturgy: the demo presenter reveals the layers one at a
   time.
4. **Colour = type; readability first.** GLO is the blue hero; the
   expandable types each get their own colour, the long tail stays neutral:

   | Node | Colour | Shape |
   |---|---|---|
   | GLO glossary term (hero) | Blue `#2f6fb3` | rounded rectangle |
   | DM data model | Teal `#3a8f7d` | rectangle (entity) |
   | STK stakeholder | Amber `#c98a2b` | ellipse (person) |
   | EIF interface | Violet `#7a5ea8` | hexagon (system) |
   | GOAL goal | Gold `#b8932f` | diamond |
   | CTX / FR / CON / ISS | Neutral grey `#9aa3b2` | diamond |

   `bounded-context`/`status` are uniform → **not** used as a colour axis.
   Within GLO, **fill/border** (not hue) encodes the confirmation level:
   `agreed: true` solid blue (white text), `agreed: false` light-blue
   outline, an assumption additionally gets an "A" badge, `deprecated` is
   grey/dashed. Node size = connectivity degree (clamped). Labels are
   **always visible** (dark text, white halo); hover/click highlights
   neighbours and dims the rest (~15%) — the biggest readability lever in a
   force graph. Harmonises with the context-diagram blue ([[ADR-0013]],
   [[ADR-0014]]).
5. **Entry point via the glossary tile — no new tile.** The graph is a *view
   onto the glossary*, not its own content type. The glossary tile changes
   from a whole-tile `<a>` to a `<div class="tile">` with **two CTAs**
   (`Table →` → `/glossary`, `Term network →` → `/graph/glossary`) — modelled
   on the already-existing **search tile** (`index.html`). A second `<a>`
   inside the current whole-tile anchor would be **nested = invalid HTML**,
   so the change is needed anyway. Optionally, also a "view as graph" toggle
   on the `/glossary` page.

## Consequences

- The first **client-side, non-deterministic** view in the dashboard, and
  the first **JS graph dependency** (cytoscape.js + fcose) alongside
  mermaid.js. The server projection stays deterministic and pure (testable
  like `build_context_diagram()`); only the arrangement is randomized per
  load — for a demo, that's a **feature** ("alive"), and reproducibility via
  a seed can be retrofitted if needed.
- Joins the **open projection family** from [[ADR-0018]] (itself already
  anticipated there as "Obsidian graph / dashboard routes"). [[ADR-0018]]
  stays **untouched** — the list there is explicitly open; this is not a
  "refactor" of an accepted ADR.
- **Audit invariant** (advisory, analogous to [[ADR-0018]]): every GLO
  `related:` edge resolves to an existing page; GLO terms with no edge
  (today, [[GLO-027-example-term]]) become visible as a possible mis-linking
  — the graph covers this visually, the audit (`_system/workflows/audit.md`)
  as a check.
- **Trade-off — pattern break:** this one view alone is not Mermaid.
  Justified by the demo goal (physics/clustering, which Mermaid can't
  deliver) and softened by the SSoT reframe: server-deterministic data, only
  client-side layout.
- **Implementation open:** route `/graph/glossary` (JSON projection from
  `related:`), cytoscape integration, tile rework (search-tile pattern), type
  buttons. **No code yet** — to be built and tracked as the next step.
- **Reversal** would mean: remove the route + cytoscape, revert the glossary
  tile to the whole-tile link — hence this record.

## Amendment (2026-06-22, implementation)

Implemented on branch `feat/glossary-graph`. One correction to §4/Context:
the dashboard has a **dark** theme (`--bg #0e1726`); the light canvas
mentioned above (`#f7f9fc`, "white halo") would be a jarring outlier.
Adapted for dark mode accordingly — **dark canvas, light labels with a dark
halo**, GLO confirmation via accent blue `#3ea6ff`. The **semantic** scheme
(colour = type, GLO hero blue, size = degree, hover focus) stays unchanged.
cytoscape-fcose is vendored; if it's missing, the built-in `cose` layout
takes over.

After visual review, two refinements to §3/§4: **(a)** State is now carried
via **border colour** (agreed = green, draft = amber, deprecated =
grey/dashed, assumption = dashed), while **fill** stays for type; GLO fill is
now opaque (previously too pale). **(b)** In addition to the button bar there
is now an **explicit legend** (types + states) — the "the buttons *are* the
legend" economy considered in §4 wasn't enough, because the buttons explain
neither GLO nor the states.

## Amendment (2026-06-25, layout engine + term ego snippet)

Two extensions on `feat/glossary-graph`, both within the projection family
from §Decision (no new decision, just a refinement of the implementation):

1. **Layout engine: cola instead of fcose (default).** fcose (a spring
   embedder) does not enforce overlap-freedom; with the dense term network
   (average degree ≈ 7.5), the label-sized nodes overlap. **cytoscape-cola**
   (WebCola, vendored) resolves this via `avoidOverlap` as a hard constraint
   on the label boxes. cola runs to **completion** (settle-and-stop), so
   dragging a node moves only **that** node; on release, a brief,
   locally-locked cola run nudges only the direct neighbours aside ("make
   room", everything else `lock()`ed). fcose remains available as an A/B
   toggle, cose as a fallback. (An `infinite` variant tried in the meantime
   — physics permanently on — was dropped: it rearranges the whole network on
   *every* grab.)
2. **Term ego snippet on the GLO detail page.** Above the textual
   definition, every `glossary/` detail page now shows a **focused 1-hop
   network** of the term: the term itself (highlighted with a ring) plus its
   direct GLO neighbours, with **DM / Stakeholder / Goals** buttons to reveal
   its 1-hop neighbours of those types layer by layer. Tapping a node opens
   its page; "full network →" leads to `/graph/glossary`. Server side:
   `build_glossary_ego_graph(stem)` as a pure **filtered projection** of
   `build_glossary_graph()` (testable, `tests/test_glossary_ego_graph.py`).

Styling, layout-engine registration, and `layoutOpts` now live **once** in
`static/glossary-graph.js` (module `AQ_GLOSSARY_GRAPH`), used by **both**
views — the full view and the ego snippet — so a colour/layout change lands
in *one* place (maintenance cost ≈ zero). cola/WebCola were added under
`static/vendor/` (see `static/vendor/README.md`).
