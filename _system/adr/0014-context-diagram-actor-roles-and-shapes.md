# ADR-0014: Kontextdiagramm — Akteur-Rollen-Projektion und Mensch/Organisation-Form

- **Status:** accepted
- **Date:** 2026-05-27

## Context
ADR-0013 projiziert das Kontextdiagramm aus den Kanten (`EIF.flows` +
`STK.provides`/`receives`): ein Knoten je Stakeholder mit Flüssen, **alle als gleiche
Rechtecke**. Im Review fielen zwei Mängel auf:

- **Form.** Menschliche Akteure (Kind, Eltern, …) sind optisch nicht von Systemen/
  Organisationen (DRSL, Verein) zu unterscheiden — alles sind weiße Rechtecke.
- **Redundanz.** Sieben Stakeholder-Knoten, davon mehrere auf **Kontextebene** fachlich
  deckungsgleich: *Ligapräsident* und *Wettkampforganisator* sind beide planende Rollen
  (ISS-011), *Kind* und *Eltern* teilen sich den Anmelde-/Ergebnis-Kanal. Der
  *Offizielle* gehört zur Durchführung, nicht in die Außensicht des Systemkontexts.

Die **Stakeholder-Personas** sind aber bewusst getrennt (eigene Influence/Interest,
Ziele, Concerns). Ein echtes Zusammenlegen der `STK`-Seiten würde diese Information
zerstören. Gesucht ist eine **rein projektionsseitige** Vergröberung.

## Decision
Die Stakeholder-Seiten bleiben unverändert reichhaltig; das **Kontextdiagramm**
aggregiert sie zu gröberen Akteur-Rollen. Dazu zwei deklarative Frontmatter-Felder am
Stakeholder, die die Projektionsfunktion auswertet:

1. **`nature: person | organization`** (Default `person`). Steuert die Knotenform:
   - `person` → **Akteur-Symbol** (👤 + Stadion-Form, helle Füllung).
   - `organization` → graues Rechteck (wie ein System).
   - `EIF` sind immer Systeme → graues Rechteck.

2. **`context_role:`** — Label und **Merge-Schlüssel** im Kontextdiagramm.
   - Fehlt das Feld (oder leer) → der Stakeholder-Titel ist das Label (Default,
     rückwärtskompatibel).
   - Gleicher `context_role`-Wert bei mehreren Stakeholdern → **ein** Knoten; ihre
     `provides`/`receives` werden vereinigt (dedupliziert, Reihenfolge stabil).
   - Wert **`none`** → der Stakeholder erscheint **nicht** im Diagramm; seine
     `provides`/`receives` bleiben auf der Seite erhalten (kein Datenverlust).

Konkrete Projektion für Aquarius:
- *Kind* (STK-001) + *Eltern* (STK-007) → **„Kind und Eltern"**.
- *Wettkampforganisator* (STK-004) + *Ligapräsident* (STK-006) → **„Organisator:in"**.
- *Offizieller* (STK-009) → `none` (ausgeblendet; Durchführungsrolle).
- *Verein* (STK-008) → `nature: organization` (graues Rechteck).

## Consequences
Die Personas bleiben getrennt und vollständig; nur die Außensicht ist entrümpelt und
lesbar (Mensch vs. System/Organisation auf einen Blick). Verfeinert ADR-0013 (dessen
„ein Knoten je Stakeholder mit Flüssen" wird zu „ein Knoten je `context_role`").
Template `stakeholder` und die Projektionsfunktion `build_context_diagram()` werden
angepasst; der vom Audit-Loop (ISS-010) genutzte Code bleibt rein/string-basiert.
Offen: Der einzelne **Punktrichter**-Knoten (Fluss „vorläufige Punkte" während der
Durchführung) — gehört dieser Durchführungs-Datenfluss überhaupt in den *Systemkontext*
oder ebenfalls ausgeblendet? Bis zur Klärung bleibt er sichtbar.
