# ADR-0013: Datenflüsse als strukturierte Kanten; Kontextdiagramm als Projektion

- **Status:** accepted
- **Date:** 2026-05-26

## Context
ADR-0009 führte die Typen **Context** und **External Interface** ein, ließ aber offen,
*wie* die Datenflüsse zu menschlichen Akteuren modelliert werden — als eigene
`EIF`-Knoten pro Kanal oder an den Stakeholdern. Der Ingest von `raw/kontextdiagramm.md`
beantwortet das mit Daten: von den sieben „Partnern" im Kontextdiagramm sind sechs
bereits Stakeholder (Kind, Verein, Präsident, Offizielle, Punktrichter); nur **DRSL**
ist ein echtes Nachbarsystem. Drei Optionen standen zur Wahl:

- **B1** — `EIF` nur für Systeme, Flüsse zu Menschen nirgends strukturiert → das
  Diagramm ist nicht aus Daten projizierbar.
- **B2** — ein `EIF`-Knoten pro Kante inkl. Mensch → ~9 Knoten, die Use Cases und
  Stakeholder duplizieren und driften.
- **B3** — `EIF` nur für Systeme; menschliche Flüsse als Felder am Stakeholder.

Zudem zeigt der Quell-Knoten, dass eine einzelne `direction:` nicht reicht: *Kind* ist
**bidirektional** (Anmeldedaten rein / Startnummer raus), *Offizieller* sendet **zwei**
Nutzlasten.

## Decision
**B3 + strukturierte Flow-Listen + projiziertes Diagramm.**

1. **`EIF`-Knoten nur für echte externe Systeme** (heute genau: DRSL). Datenflüsse
   zu/von menschlichen **User-Rollen** werden als strukturierte Frontmatter-Felder am
   jeweiligen `[[STK-...]]` erfasst: `provides:` (eingehend ins System) und `receives:`
   (ausgehend an den Akteur). User-Rollen bleiben Stakeholder, kein eigener Typ
   (bestätigt ADR-0009); die Zahl der Inhaltstypen bleibt **dreizehn**.
2. **Jede `EIF` trägt eine `flows:`-Liste** statt eines einzelnen `direction:`-Feldes;
   jeder Eintrag `{ data, direction, format?, trigger? }`. Damit sind mehrere und
   bidirektionale Flüsse pro Nachbar darstellbar. `direction`/`format` als Einzelfelder
   entfallen.
3. **Das Kontextdiagramm wird nicht gepflegt, sondern projiziert.** Single Source of
   Truth sind die strukturierten Kanten (`EIF.flows` + `STK.provides`/`receives`). Eine
   Dashboard-Render-Route zeichnet das mermaid-Kontextdiagramm on-the-fly; ein
   LLM-Audit-Loop zeichnet es neu, wenn sich Schnittstellen oder Rollen ändern (Umsetzung
   in [[ISS-010-kontextdiagramm-projektion-audit-loop|ISS-010]]). Das `diagram:`-Feld des
   Context-Knotens ist `generated`, kein eingebetteter, driftender mermaid-Block.

## Consequences
`EIF` bleibt klein und bedeutsam (echte Nachbarsysteme); Stakeholder werden bzgl. ihrer
Datenflüsse maschinenlesbar; das Kontextdiagramm ist jederzeit aus den Kanten
regenerierbar. Templates `context`, `external-interface` und `stakeholder` werden
angepasst, die `CLAUDE.md`-Tabelle (EIF „direction") sinngemäß auf `flows` umgestellt.
Kosten: Render-Route und Audit-Loop sind noch zu bauen ([[ISS-010-kontextdiagramm-projektion-audit-loop|ISS-010]]).
Schärft die in ADR-0009 bewusst offen gelassene Frage „Nachbarsystem **oder** Kanal zu
einem Akteur" — Akteur-Kanäle leben jetzt am Stakeholder, nicht als `EIF`.

## Amendment (2026-06-22)
Der in der *Decision* (Punkt 3) genannte **LLM-Audit-Loop entfällt**; die Render-Route ist
gebaut. Begründung + Auflösung: [[ISS-010-kontextdiagramm-projektion-audit-loop]] (resolved).
Kanten-Konsistenz und Render-Validität deckt das reguläre Audit ab (`_system/workflows/audit.md`).
