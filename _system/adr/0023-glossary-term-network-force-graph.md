# ADR-0023: Glossar-Begriffsnetz als interaktiver Force-Graph (cytoscape.js, clientseitiges Layout)

- **Status:** accepted
- **Date:** 2026-06-22

## Context

Das Dashboard (`_system/apps/dashboard/`) ist nicht nur ein Viewer, sondern auch ein
**Demo- und Überzeugungs-Artefakt**: es soll Stakeholder **ohne Obsidian** von der
Wiki-Idee überzeugen. Für das Glossar — die ubiquitäre Sprache, das Herz der Domäne —
fehlt eine Sicht, die das *Netz* der Begriffe auf einen Blick lebendig macht. Vorhanden,
aber unzureichend:

- **Obsidian-Graph** (force-directed, auf `path:wiki/glossary` filterbar) — setzt Obsidian
  voraus und fällt damit für die Zielgruppe gerade aus.
- **`glossary.html`** (Tabelle mit „Vernetzung"-Sortierung + Relationen-Zähler) — zeigt den
  *Grad* der Vernetzung, nicht die *Lage* / Cluster.
- Alle bisherigen Dashboard-Diagramme (Kontext, Story-Map, Goals) sind **Mermaid**,
  server-seitig als deterministischer String gerendert ([[ADR-0013]], [[ADR-0018]]).

Datenlage (geprüft 2026-06-22): 27 GLO-Knoten; **101 GLO→GLO**-Kanten plus **~35 Querkanten**
(12 DM, 8 STK, 5 EIF, 3 GOAL, 2 CTX, 3 ISS, 1 FR, 1 CON). `bounded-context` (alle
„Kinderschwimmliga") und `status` (26 draft, 1 deprecated) sind **uniform** → als Farbachse
untauglich. GLO-027 (Familie) hat 0 glossar-interne Kanten (Waise).

**Spannung.** Ein Force-Graph **kann kein Mermaid sein** — Mermaids Auto-Layout ist
hierarchisch (dagre), kein Physik-Layout; es käme der bekannte Kästchen-und-Pfeile-Look
heraus, nicht das „lebendige Netz", das die Demo braucht. Das zwingt erstmals eine
**JS-Graph-Bibliothek** ins Dashboard und ein **clientseitiges, nicht-deterministisches
Layout** — ein Bruch mit dem bislang durchgehaltenen „alles ist server-gerendertes Mermaid".

Optionen:

- **A** — Mermaid-Flowchart (dagre). Kein Physik-Layout, kein Cluster-Effekt; verfehlt das
  Demo-Ziel.
- **B** — Obsidian-Graph als Demo verwenden. Setzt Obsidian voraus → die Zielgruppe (ohne
  Obsidian) fällt aus.
- **C** — Clientseitiger Force-Graph (JS-Lib) über server-projizierte Graph-Daten.

## Decision

**Ein eigenständiges „Begriffsnetz" im Dashboard: ein clientseitiger Force-Graph
(cytoscape.js + fcose) über eine deterministische Server-Projektion der `related:`-Kanten.**
Option C.

Der Reframe, der die Konsistenz mit [[ADR-0018]] wahrt: **Single Source of Truth bleibt
server-deterministisch.** Eine Route `/graph/glossary` projiziert aus den typisierten
`related:`-Kanten ein Graph-JSON `{nodes, edges}` — exakt das Muster von [[ADR-0018]]
(Projektion typisierter Kanten), nur mit anderem Ausgabeformat als der Mermaid-String.
**Allein das Layout** wandert in den Browser (Physik). Es ist also keine Abkehr von
[[ADR-0018]], sondern eine weitere Projektion derselben offenen Familie — die erste mit
JS- statt Mermaid-Renderer.

1. **Renderer: cytoscape.js + fcose-Layout.** Graph-spezialisiert, deklaratives Styling
   (Selektoren), eingebaute Physik-Layouts, Klick-Handler, gut gepflegt. d3-force wäre die
   flexibelste Optik, aber am meisten Handarbeit/Wartung — gegen das Prinzip „Wartungskosten
   ≈ null". Erste JS-Graph-Lib im Dashboard neben mermaid.js.
2. **Kanten ungerichtet & dedupliziert.** `related:` ist projektweit asymmetrisch
   (Pointer-to-Context-Konvention, [[ADR-0018]] §1); für ein *semantisches Sprachnetz* ist
   ungerichtet die ehrliche Darstellung (A↔B als *eine* Kante, sonst falsche Richtungs-
   Artefakte). Kantenquelle ist **ausschließlich das `related:`-Frontmatter** — **keine**
   Body-Wikilinks (Rauschen, unkuratiert).
3. **Default = nur Glossar; Erweiterung schichtweise per Typ-Button.** Initial nur GLO-Knoten
   + GLO→GLO-Kanten. Querverbindungen zu anderen Typen werden über **Buttons** (DM, STK, EIF,
   GOAL, „Weitere") eingeblendet — je 1-Hop-Nachbarn der gezeigten GLO-Knoten, additiv,
   unabhängig schaltbar, mit inkrementell-animiertem Relayout (kein Neu-Würfeln). Die Buttons
   *sind* die Legende (farbiger Chip mit Typ + Kantenzahl, aktiv = gefüllt). Dramaturgie:
   der Demo-Präsentator blendet die Schichten nacheinander ein.
4. **Farbe = Typ; Lesbarkeit zuerst.** GLO ist der blaue Hero; die erweiterbaren Typen tragen
   je eine eigene Farbe, der Long-Tail bleibt neutral:

   | Knoten | Farbe | Form |
   |---|---|---|
   | GLO Begriff (Hero) | Blau `#2f6fb3` | abgerundetes Rechteck |
   | DM Datenmodell | Teal `#3a8f7d` | Rechteck (Entity) |
   | STK Stakeholder | Amber `#c98a2b` | Ellipse (Person) |
   | EIF Schnittstelle | Violett `#7a5ea8` | Hexagon (System) |
   | GOAL Ziel | Gold `#b8932f` | Raute |
   | CTX / FR / CON / ISS | Neutralgrau `#9aa3b2` | Raute |

   `bounded-context`/`status` sind uniform → **nicht** als Farbachse genutzt. Innerhalb GLO
   kodiert **Füllung/Rand** (nicht der Farbton) den Bestätigungsgrad: `agreed: true` voll-blau
   (weißer Text), `agreed: false` hellblau umrandet, Annahme zusätzlich ein „A"-Badge,
   `deprecated` grau/gestrichelt. Knotengröße = Vernetzungsgrad (geclamped). Labels **immer
   sichtbar** (dunkler Text, weißer Halo); Hover/Klick hebt Nachbarn hervor und dimmt den Rest
   (~15 %) — der größte Lesbarkeits-Hebel im Force-Graph. Harmoniert mit dem
   Kontextdiagramm-Blau ([[ADR-0013]], [[ADR-0014]]).
5. **Einstieg über die Glossar-Kachel — keine neue Kachel.** Der Graph ist eine *Sicht aufs
   Glossar*, kein eigener Inhaltstyp. Die Glossar-Kachel wird vom Ganz-Kachel-`<a>` zu einem
   `<div class="tile">` mit **zwei CTAs** (`Tabelle →` → `/glossary`, `Begriffsnetz →` →
   `/graph/glossary`) — Vorbild ist die bereits bestehende **Such-Kachel** (`index.html`).
   Ein zweiter `<a>` im aktuellen Ganz-Kachel-Anker wäre **verschachtelt = ungültiges HTML**,
   der Umbau ist also ohnehin nötig. Optional zusätzlich ein „Als Graph ansehen"-Umschalter
   auf der `/glossary`-Seite.

## Consequences

- Erste **clientseitige, nicht-deterministische** Sicht im Dashboard und erste **JS-Graph-
  Abhängigkeit** (cytoscape.js + fcose) neben mermaid.js. Die Server-Projektion bleibt
  deterministisch und rein (testbar wie `build_context_diagram()`); nur die Anordnung würfelt
  pro Laden — für eine Demo ein **Feature** („lebendig"), Reproduzierbarkeit per Seed bei
  Bedarf nachrüstbar.
- Reiht sich in die **offene Projektions-Familie** von [[ADR-0018]] ein (dort selbst als
  „Obsidian-Graph / Dashboard-Routen" vorgesehen). [[ADR-0018]] bleibt **unangetastet** — die
  Liste ist dort explizit offen; kein „Refactor" akzeptierter ADRs.
- **Audit-Invariante** (advisory, analog [[ADR-0018]]): jede GLO-`related:`-Kante löst auf eine
  existierende Seite auf; GLO-Begriffe ohne Kante (heute [[GLO-027-familie]]) werden als
  mögliche Fehl-Vernetzung sichtbar — der Graph deckt das visuell ab, das Audit
  (`_system/workflows/audit.md`) als Check.
- **Trade-off — Muster-Bruch:** Genau diese eine Sicht ist nicht Mermaid. Begründet durch das
  Demo-Ziel (Physik/Cluster, das Mermaid nicht liefert) und entschärft durch den
  SSoT-Reframe: server-deterministische Daten, nur Client-Layout.
- **Umsetzung offen:** Route `/graph/glossary` (JSON-Projektion aus `related:`),
  cytoscape-Einbindung, Kachel-Umbau (Such-Kachel-Muster), Typ-Buttons. Noch **kein Code** —
  als nächster Schritt zu bauen und zu tracken.
- **Reversal** hieße: Route + cytoscape entfernen, Glossar-Kachel zurück auf den
  Ganz-Kachel-Link — daher dieser Record.

## Amendment (2026-06-22, Umsetzung)

Umgesetzt auf Branch `feat/glossary-graph`. Eine Korrektur an §4/Context: Das Dashboard
hat ein **dunkles** Theme (`--bg #0e1726`); das oben genannte helle Canvas (`#f7f9fc`,
„weißer Halo") wäre ein greller Fremdkörper. Daher an Dark-Mode angepasst — **dunkles
Canvas, helle Labels mit dunklem Halo**, GLO-Bestätigung über Akzent-Blau `#3ea6ff`. Das
**semantische** Schema (Farbe = Typ, GLO-Hero-Blau, Größe = Grad, Hover-Fokus) bleibt
unverändert. cytoscape-fcose ist vendored; fehlt es, greift das eingebaute `cose`-Layout.

Nach visuellem Review zwei Präzisierungen zu §3/§4: **(a)** Der Zustand wird über die
**Randfarbe** getragen (abgestimmt = grün, Entwurf = amber, veraltet = grau/gestrichelt,
Annahme = gestrichelt), die **Füllung** bleibt für den Typ; GLO-Füllung jetzt deckend
(vorher zu blass). **(b)** Zusätzlich zur Button-Leiste gibt es eine **explizite Legende**
(Typen + Zustände) — die in §4 angedachte „Buttons *sind* die Legende"-Sparsamkeit reicht
nicht, weil die Buttons weder GLO noch die Zustände erklären.

## Amendment (2026-06-25, Layout-Engine + Begriff-Ego-Snippet)

Zwei Erweiterungen auf `feat/glossary-graph`, beide innerhalb der Projektions-Familie von
§Decision (keine neue Entscheidung, nur Verfeinerung der Umsetzung):

1. **Layout-Engine cola statt fcose (Default).** fcose (Feder-Embedder) erzwingt keine
   Überlappungsfreiheit; bei dem dichten Begriffsnetz (⌀-Grad ≈ 7,5) überlappen die
   label-großen Knoten. **cytoscape-cola** (WebCola, vendored) löst das per
   `avoidOverlap` als harte Constraint auf den Label-Boxen. cola läuft **endlich**
   (settle-and-stop), damit das Ziehen eines Knotens nur **diesen** bewegt; beim Loslassen
   rückt ein kurzer, lokal-gesperrter cola-Lauf nur die direkten Nachbarn zur Seite
   („make room", alles andere `lock()`). fcose bleibt als A/B-Umschalter erhalten, cose als
   Fallback. (Die zwischenzeitlich erprobte `infinite`-Variante — Physik dauerhaft an —
   verworfen: sie ordnet bei *jedem* Greifen das ganze Netz um.)
2. **Begriff-Ego-Snippet auf der GLO-Detailseite.** Über der textuellen Definition zeigt
   jede `glossary/`-Detailseite ein **fokussiertes 1-Hop-Netz** des Begriffs: der Term
   (ringförmig hervorgehoben) + direkte GLO-Nachbarn, mit Buttons **DM / Stakeholder /
   Ziele** zum schichtweisen Einblenden seiner 1-Hop-Nachbarn dieser Typen. Knoten-Tap
   öffnet die jeweilige Seite; „ganzes Netz →" führt zu `/graph/glossary`. Server:
   `build_glossary_ego_graph(stem)` als reine **gefilterte Projektion** von
   `build_glossary_graph()` (testbar, `tests/test_glossary_ego_graph.py`).

Styling, Layout-Engine-Registrierung und `layoutOpts` liegen jetzt **einmalig** in
`static/glossary-graph.js` (Modul `AQ_GLOSSARY_GRAPH`), das **beide** Sichten — die
Vollansicht und das Ego-Snippet — nutzen; eine Farb-/Layout-Änderung landet an *einer*
Stelle (Wartungskosten ≈ null). cola/WebCola sind in `static/vendor/` ergänzt
(siehe `static/vendor/README.md`).
