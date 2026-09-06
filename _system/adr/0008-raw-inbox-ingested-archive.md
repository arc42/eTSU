# ADR-0008: `raw/` als Inbox, ingestierte Originale nach `raw/ingested/`

- **Status:** accepted
- **Date:** 2026-05-24

## Context
Nach ADR-0006 lagen die menschlichen Quelldateien flach in `raw/`, vermischt mit
bereits verarbeiteten und noch unverarbeiteten Quellen. Mit wachsender Quellenzahl
verliert man so den Überblick, *was noch zu ingestieren ist*. Die eigentlichen
Dateien dürfen nicht gelöscht werden (Drift-Erkennung via sha256, Re-Derivation,
Provenance), aber sie müssen die „Eingangsablage“ nicht dauerhaft belegen.

## Decision
`raw/`'s **oberste Ebene ist die Inbox**: nur *neue, noch nicht ingestierte* Quellen.
Sobald eine Quelle ingestiert ist, wird ihr Original nach **`raw/ingested/`**
verschoben, und das zugehörige `SRC-NNN` `origin:` wird auf den neuen Pfad gesetzt.

Damit ergibt sich unter `raw/`:
- **oberste Ebene** — Inbox (neue, unverarbeitete Quellen)
- **`raw/ingested/`** — archivierte Originale nach dem Ingest (menschlich, immutabel)
- **`raw/sources/`** — agent-erzeugte Provenance-Records `SRC-NNN` (ADR-0006)

Der Ingest-Workflow erhält dafür einen Abschlussschritt (Schritt 8); der
Audit-Workflow rechnet die sha256-Drift gegen die Datei am `origin:`-Pfad.

## Consequences
Die Inbox zeigt auf einen Blick die offene Ingest-Arbeit; verarbeitete Originale
bleiben erhalten und prüfbar. Da nur verschoben (nicht verändert) wird, bleiben alle
sha256-Baselines gültig. Kosten: ein zusätzlicher Move-Schritt pro Ingest und die
Pflege des `origin:`-Pfads. Trade-off der gewählten **flachen** Variante: `sources/`
(Records) und `ingested/` (Dateien) sind Geschwister mit ähnlichem Klang — bewusst
in Kauf genommen, um menschliche Originale aus dem agent-eigenen `raw/sources/`
herauszuhalten (klare Eigentümerschaft).
