# ADR-0018: Diagramme und Matrizen als Projektion typisierter Kanten

- **Status:** accepted
- **Date:** 2026-05-28

## Context
Querschnittsdarstellungen — Diagramme (Kontext, Datenmodell, Use-Case),
Coverage-Matrizen (Goals × Backlog, Stakeholder × Wert), Bäume (Story Map,
Vision-Goal) — verdichten Informationen aus mehreren Inhaltstypen zu einer
zweidimensionalen Sicht. Sie sind im Wiki bislang **ad hoc** behandelt worden:

- [[ADR-0012]] (2026-05-25) löst das für die **Story Map** — Projektion aus dem
  `FR.parent:`-Baum + `order` / `release` / `priority`.
- [[ADR-0013]] (2026-05-26) löst das für das **Kontextdiagramm** — Projektion aus
  `STK.provides:` / `receives:` + `EIF.flows`.

Beide Male wurde dasselbe Muster gewählt, ohne es zu verallgemeinern. Mit dem
neuen Inhaltstyp `goal` ([[ADR-0016]]) entsteht eine weitere Querschnittssicht
(Goal-Coverage-Matrix), und weitere sind absehbar (Datenmodell, Use-Case-Diagramm,
Vision-Goal-Baum, Quality-Tree, Traceability …). Vor dem nächsten Spezialfall
soll das Meta-Prinzip festgeschrieben werden, damit es nicht jedes Mal von Null
hergeleitet werden muss.

Drei Pfade standen prinzipiell zur Wahl:

- **A** — Jede Sicht als **eigener Inhaltstyp** (eine `coverage`-Datei pro Matrix,
  eine `diagram`-Datei pro Diagramm). Doppelte Datenhaltung, geht zwangsläufig
  stale, kein Mehrwert gegenüber einer Tabelle in Markdown.
- **B** — Sichten als **handgepflegte Markdown-Tabellen** in Übersichtsseiten.
  Skaliert nicht (jede neue Instanz verlangt Tabellen-Edit), driftet vom
  Quell-Inhalt weg, Audit-Aufwand wächst quadratisch.
- **C** — Sichten als **Projektion** aus den ohnehin schon getragenen,
  **typisierten Kanten** (Frontmatter-Felder, Wikilinks). Single Source of Truth
  bleibt der Inhaltstyp; die Sicht ist ein Generator-Output.

C ist zweimal angewandt worden (ADR-0012, ADR-0013) und funktioniert.

## Decision
**Querschnittsdarstellungen sind Projektionen aus typisierten Kanten — keine
gespeicherten Artefakte.** Single Source of Truth sind die Frontmatter-Felder
und Wikilinks der Inhaltstypen. Sichten werden bei Bedarf generiert:
Obsidian-Graph, Dashboard-Routen, LLM-Audits. **Keine eingebetteten
Mermaid-Blöcke** in Wiki-Seiten, **keine handgepflegten Übersichtstabellen**,
**keine bidirektionale Kantenpflege**.

### Aktive und geplante Projektionen

| Projektion | Quell-Kanten (single source of truth) | Verankerung | Status |
|---|---|---|---|
| Story Map | `FR.parent:` + `order` / `release` / `priority` / `lane:` | [[ADR-0012]], [[ADR-0017]] | aktiv (Anchor [[story-mapping]]) |
| Kontextdiagramm | `STK.provides:` / `receives:` + `EIF.flows` | [[ADR-0013]], [[ADR-0014]] | aktiv (Dashboard-Render) |
| **Goal-Coverage-Matrix** | `FR.goal: [[GOAL-...]]` (mehrwertig) | **dies ADR** + [[ADR-0016]] | aktiv (Backlinks); Dashboard-Render geplant |
| Vision-Goal-Baum | `GOAL.parent:` (Objective → Vision) | [[ADR-0016]] | geplant (mit erstem Goal-Ingest) |
| Datenmodell-Diagramm | `data-model.entities` + Relationship-Felder | offen | geplant (mit erstem Datenmodell-Ingest) |
| Use-Case-Diagramm | `UC.actor:` ([[STK-...]]) + `UC.parent:` ([[FR-...]]) | offen | geplant (sobald UCs entstehen — top-down aus Epics, [[ISS-009-worklist-stub-strategie]]) |
| Stakeholder-Wert-Matrix | `STK` × `GOAL.beneficiary:` (+ `FR.goal:` Indirektion) | offen | geplant |
| Quality-Tree (Utility Tree) | `QR.applies-to:` ([[FR-...]]) + `attribute:` | offen | geplant |
| Traceability-Matrix | Goal × FR × UC × QR — Komposition aus allen Kanten | offen | optional / on demand |
| Issue-Heatmap | `ISS.affects:` × Inhaltstyp / Status | offen | optional |

Die Liste ist **offen** — neue Sichten folgen demselben Muster: erst die Kante
typisieren, dann projizieren.

### Konventionen für jede Projektion

1. **Kanten leben einmal**, auf der **spezifischeren Seite** (Instanz → Kontext).
   Beispiel: `FR.goal:` (FR → Goal), **nicht** zusätzlich `GOAL.realized_by:`
   (Goal → FR). Obsidian-Backlinks liefern die Gegenrichtung automatisch.
2. **Richtung „nach oben"** ist der Normalfall: feiner → gröber, Instanz →
   abstrakter Kontext. Konsistent mit Story Map (`story → epic`),
   Goal-Coverage (`FR → goal`), Vision-Goal-Baum (`objective → vision`).
3. **Leere Werte sind reale Aussagen**, kein „fehlt noch".
   `FR.goal: []` heißt **bewusst Enabler** (z. B. Plattform-Schiene); `[[ISS-...]]`
   bei tatsächlicher Lücke. Genauso `parent: []` = Wurzelknoten, nicht
   „Hierarchie unklar".
4. **Rendering ist Generator-Sache**, nicht Inhalt der Wiki-Seite.
   Mermaid-Blöcke, eingebettete Bilder oder Markdown-Coverage-Tabellen direkt
   in Wiki-Seiten sind verboten — sie driften. Erlaubt: Generierte Artefakte
   in `_system/apps/dashboard/` oder als LLM-Audit-Output.
5. **Drift wird sichtbar.** Beim Audit (grill-Skill) prüft jede Projektion
   ihre Invarianten (siehe unten); Verletzungen werden als `ISS-NNN` geflaggt,
   nicht stillschweigend repariert.

### Audit-Invarianten je Projektion (advisory)

- **Story Map** — jedes Backlog-Item trägt `parent:` (außer Epics) und sitzt in
  einer Lane; Backbone-Reihenfolge per `order` lückenlos.
- **Kontextdiagramm** — jeder externe Akteur hat mindestens eine Kante
  (`provides`/`receives` oder `EIF.flows`); jede Kante hat `data`/`direction`.
- **Goal-Coverage** — jedes Backlog-Item setzt `goal:` (≥ 1 GOAL) **oder** ist
  explizit `goal: []` mit `lane: platform`/`display`. Jedes Goal wird von ≥ 1
  FR bedient (sonst ⇒ `[[ISS-...]]` „Goal ohne Träger").
- **Vision-Goal-Baum** — genau eine GOAL-Wurzel pro System (`stereotype:
  vision`, `parent: []`); jedes Objective hat `parent:` auf die Vision.
- **Datenmodell, Use-Case, Quality-Tree** — Invarianten werden mit dem jeweils
  ersten Ingest festgelegt.

## Consequences

**Sofort umgesetzt** (gemeinsam mit diesem ADR):

- `_templates/functional-requirement.md` — Feld `goal:` neu typisiert:
  `[[GOAL-...]]` statt `[[STK-...]]`, mehrwertig, `[]` = Enabler.
- `_templates/goal.md` — Abschnitt „Bedient durch" projiziert aus Backlinks
  (explizit dokumentiert, nicht manuell zu pflegen).
- `FR-001..008` — `goal:`-Backfill gegen die in Konversation festgezogene
  Coverage-Matrix; alte Stakeholder-Pointer (Workaround vor Existenz von
  `goal`) wandern implizit auf `related:` (dort bereits vorhanden).
- `_system/anchors/story-mapping.md` — Checklisten-Punkt zur neuen Feld-Semantik
  geschärft.

**Bewusst aufgeschoben:** Dashboard-Render-Route für die Goal-Coverage-Matrix
(analog zur Kontext-Render-Route, [[ISS-010-kontextdiagramm-projektion-audit-loop]]);
Goal-Ingest selbst (Inhalt von `raw/vision-draft.md` → `GOAL-001..005`); LLM-Audit-Loops
je Projektion.

**Risiko:** Die vorab vergebenen `GOAL-001..005`-Wikilinks in den FRs sind bis zum
Goal-Ingest **unauflöst** (Obsidian-Dangling-Links). Vertretbar — die IDs sind
festgelegt, der Ingest folgt; alternativ wäre der Backfill nach dem Ingest
nachzuziehen gewesen. Wir akzeptieren das Vorgreifen, weil die Coverage-Matrix
für die laufende Epic-Arbeit jetzt Wert stiftet.

**Bewusst nicht geändert:** Keine Konsolidierung von ADR-0012 / ADR-0013 in
dieses Meta-ADR. Beide bleiben als Spezialfälle bestehen und werden hier nur
zitiert — Rückwärts-Stabilität, kein „Refactor" von akzeptierten Entscheidungen.
