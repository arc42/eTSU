# Gefilterte Graph-Ansichten (Obsidian Workspaces)

Der Obsidian-Graph speichert global nur **eine** Konfiguration
(`.obsidian/graph.json`). **Groups** färben Knoten nur ein – sie entfernen keine.
Wer den Graphen auf bestimmte Knoten **reduzieren** will, nutzt das Suchfeld im
Abschnitt **Filters** der Graph-Einstellungen (oben).

Um mehrere solcher Filter wiederzuverwenden, speichern wir sie als benannte
**Workspaces** (Core-Plugin „Workspaces"). Ein Workspace sichert das gesamte
Layout inklusive der Graph-Filter. Die gespeicherten Layouts liegen in
`.obsidian/workspaces.json`.

## Vorhandene Graph-Workspaces

| Workspace | Filter (`search`) | Zeigt |
|---|---|---|
| **Graph: Glossar + Goals** | `["type":"glossary"] OR ["type":"goal"]` | GLO- und GOAL-Knoten (grün / gold) |
| **Graph: Epics + FRs** | `["type":"functional-requirement"]` | alle FRs, eingefärbt nach Stereotyp epic/feature/story |
| **Graph: Kind (alles dazu)** | `GLO-006-kind` | den Begriff *Kind* + jede Seite, die darauf verlinkt |
| **Graph: Data Models** | `["type":"data-model"]` | alle DM-Knoten |

## Laden

1. `Cmd+P` → **Workspaces: Load workspace** (oder Ribbon-Icon) → einen der vier wählen.
2. Zurück zum normalen Layout: einen regulären Workspace laden/speichern.

> Wurde `workspaces.json` extern (z. B. von einem Agenten) geschrieben, während
> Obsidian läuft, muss Obsidian die Datei erst neu einlesen:
> `Cmd+P` → **Reload app without saving**. **Vorher keinen Workspace speichern**,
> sonst überschreibt Obsidian die neue Datei mit dem alten Speicherstand.

## Filter-Syntax (Spickzettel)

Das Filter-Feld nutzt dieselbe Such-Syntax wie die globale Suche.

- `path:wiki/glossary` — nur ein Ordner
- `["type":"goal"]` — nach Frontmatter-**Property** (robust, auch wenn Dateien umziehen)
- `["status":"accepted"]` — nach Status
- `tag:#data-model` — nach Tag (mit `#`)
- `A OR B` — Vereinigung (**`OR` muss groß geschrieben sein**; `or` ist ein Wort)
- `-["status":"deprecated"]` — Ausschluss
- `GLO-006-kind` — der Knoten selbst **plus** alle Seiten, deren Text diesen
  Wikilink enthält (nutzt die Konvention „jede Referenz ist ein echter Link")

## Neuen Graph-Workspace anlegen

1. Graph öffnen, gewünschten Ausdruck ins **Filters**-Feld eintragen, ggf. Farben
   unter **Groups** setzen.
2. `Cmd+P` → **Workspaces: Save workspace as…** → sprechenden Namen vergeben
   (Konvention hier: Präfix `Graph: …`).

> Hinweis: Ein Workspace sichert das **gesamte** Layout, nicht nur den Graphen.
> Die vier Graph-Workspaces oben übernehmen die seitlichen Panels aus dem
> Standard-Layout. Beim Laden wird die Pane-Anordnung also umgestellt.
