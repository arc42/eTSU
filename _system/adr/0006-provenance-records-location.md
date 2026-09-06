# ADR-0006: Schlanke Provenance-Records in `raw/sources/`

- **Status:** accepted
- **Date:** 2026-05-24

## Context
Quell-/Provenance-Records (`SRC-NNN`) wurden flach in `raw/` angelegt — als
Geschwister der eigentlichen, vom Menschen kuratierten Quelldateien (z. B.
`glossary.md`). Zudem trugen sie ausführliche Prosa (`Summary`, `Key takeaways`,
`Provenance`). Das hatte zwei Nachteile:

1. **Vermischte Eigentümerschaft.** Agent-erzeugte Metadaten lagen neben den
   immutablen menschlichen Quellen — verwirrend, „warum liegen diese Dateien hier?“.
2. **Doppelung mit dem Log.** Die Prosa wiederholte die chronologische Erzählung,
   die bereits in `_system/log.md` steht.

Dabei sagte die Content-Type-Tabelle in `CLAUDE.md` ohnehin schon „frontmatter only“;
die Praxis war davon abgedriftet. Ein SRC-Record ist aber **kein** Log-Eintrag,
sondern ein Knoten im Graphen: Ziel der `sources:`-Wikilinks, Träger des `sha256`
für Drift-Erkennung und Rückwärts-Manifest (`ingested-pages` / Backlinks). Diese
Funktionen lassen sich nicht durch Log-Zeilen ersetzen.

## Decision
Provenance-Records bleiben **ein Knoten pro Quelle**, werden aber **schlank**
gehalten (Frontmatter + höchstens ein einzeiliger Summary) und liegen in einem
eigenen Ordner **`raw/sources/`**, getrennt von den menschlichen Quelldateien auf
der obersten `raw/`-Ebene.

- **Narrative** (Was-wann-Operationen) gehört ausschließlich in `_system/log.md`.
- **Provenance/Traceability** (Quelle, Hash, betroffene Seiten) in den SRC-Record.
- `_system/index.md` erhält einen Abschnitt **`## Sources`** als Registry aller
  ingestierten Quellen (analog zu allen anderen Content-Typen).

## Consequences
Klare Trennung: menschliche Rohquellen (`raw/`, immutabel) ↔ agent-erzeugte
Provenance (`raw/sources/`). Leichtgewichtige Records, eine eindeutige Stelle für
die Registry (Index) und eine für die Narrative (Log). Kosten: bestehende
`sources:`-Links wurden auf `raw/sources/…` umgestellt; `CLAUDE.md`, das
Source-Template und der Ingest-Workflow angepasst. Offene Verfeinerung: Voll-Pfad-
Links brechen bei einem erneuten Verschieben — Basename-Links (`[[SRC-001-…]]`)
wären verschiebe-robuster und könnten später eingeführt werden.
