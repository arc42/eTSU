# Vendored third-party assets

Served as static files so the dashboard renders diagrams **offline** (no CDN at runtime).

## mermaid.min.js
- **Library:** mermaid (diagramming) — <https://mermaid.js.org>
- **Version:** 11.15.0
- **Build:** minified UMD/IIFE; exposes `globalThis.mermaid`, loaded via a classic
  `<script>` in `templates/_mermaid.html`.
- **License:** MIT (© mermaid contributors).
- **Source:** `https://cdn.jsdelivr.net/npm/mermaid@11.15.0/dist/mermaid.min.js`
- **Used by:** the live-projected system-context diagram (ADR-0013, ISS-010) on the
  context detail page and `/req42/scope`, plus any ` ```mermaid ` block in a page body.

To update: re-download the same `dist/mermaid.min.js` for the desired pinned version and
bump the version above.

## cytoscape.min.js (+ fcose stack)
- **Library:** Cytoscape.js (graph rendering) — <https://js.cytoscape.org>
- **Version:** 3.30.3; layout plugin **cytoscape-fcose 2.2.0** (deps `cose-base` 2.2.0,
  `layout-base` 2.0.1).
- **Build:** classic `<script>`; exposes `globalThis.cytoscape`, `fcose` registers itself.
- **License:** MIT (© The Cytoscape Consortium / fcose contributors).
- **Source:** `cdnjs.cloudflare.com/ajax/libs/cytoscape/3.30.3/cytoscape.min.js`;
  `unpkg.com/{layout-base@2.0.1,cose-base@2.2.0,cytoscape-fcose@2.2.0}`.
- **Used by:** the glossary term-network force-graph (ADR-0023) on `/graph/glossary`.
  Load order matters: cytoscape → layout-base → cose-base → cytoscape-fcose. If the
  fcose plugin is absent, the page falls back to cytoscape's built-in `cose` layout.

## cola.min.js + cytoscape-cola.js (constraint layout)
- **Library:** WebCola (`cola.min.js`) — <https://ialab.it.monash.edu/webcola/> — plus the
  Cytoscape binding **cytoscape-cola** (`cytoscape-cola.js`).
- **Version:** webcola 3.4.0; cytoscape-cola 2.5.1.
- **Build:** classic `<script>`. webcola exposes `globalThis.cola`; cytoscape-cola is a
  webpack UMD that reads `globalThis.webcola` at load and **auto-registers** the `cola`
  layout on the global `cytoscape`.
- **License:** MIT (© Tim Dwyer / Monash IALab; cytoscape-cola: The Cytoscape Consortium).
- **Source:** `unpkg.com/webcola@3.4.0/WebCola/cola.min.js`;
  `unpkg.com/cytoscape-cola@2.5.1/cytoscape-cola.js`.
- **Used by:** the glossary term-network graph (ADR-0023 cola amendment) as the **default**
  layout — constraint-based with `avoidOverlap: true` (hard non-overlap on label-sized
  boxes), with fcose kept as an A/B toggle. Load order: cytoscape → cola → (bridge)
  → cytoscape-cola. **Name bridge:** webcola sets `window.cola` but cytoscape-cola's UMD
  expects `window.webcola`; `graph.html` runs `window.webcola = window.cola` between the two
  `<script>` tags so the plugin gets the real module. If cola is absent, fcose/cose apply.
