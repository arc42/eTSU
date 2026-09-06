# ADR-0009: Inhaltstypen Context (Scope) und External Interface

- **Status:** accepted
- **Date:** 2026-05-24

## Context
ADR-0007 deckte eine Lücke auf: req42-Baustein 03 *Scope & Abgrenzung* (arc42:
Context & Scope) hatte keinen Inhaltstyp. Damit ließen sich Systemgrenze,
Nachbarn/externe Schnittstellen und die bewusste Abgrenzung (was das System *nicht*
leistet) nicht typisiert ablegen. `raw/kontextdiagramm.md` wartet im Inbox.

## Decision
Wir führen **zwei** Inhaltstypen ein (Templates in `_templates/`):

1. **Context** (`wiki/context/`, `CTX-NNN`) — der Scope-&-Kontext-Knoten eines
   Systems (`kind: business | technical`). Enthält: Kontextdiagramm, **In scope**,
   **Out of scope / Abgrenzung** (explizite Nicht-Ziele), eine Liste der externen
   Schnittstellen (Verlinkung der `EIF`-Knoten), die **User-Rollen** (Verlinkung
   bestehender `[[STK-...]]`-Stakeholder) und eine erläuternde Narrative.
2. **External interface** (`wiki/external-interfaces/`, `EIF-NNN`) — **jede externe
   Schnittstelle ist ein eigener Knoten** (Nachbarsystem oder Kanal zu einem Akteur)
   mit Partner, Richtung (inbound/outbound/bidirektional), ausgetauschten Daten und
   Format.

User-Rollen bekommen **keinen** eigenen Typ — sie sind Stakeholder; der Context-Knoten
referenziert die relevanten `[[STK-...]]`. Damit steigt die Zahl der Inhaltstypen auf
**dreizehn**.

## Consequences
req42-Baustein 03 ist abgedeckt; Schnittstellen sind als Knoten aus Use Cases,
Datenmodellen u. a. zitierbar und erscheinen im Graphen. Der Context-Knoten bündelt
Diagramm, Abgrenzung und Nachbarn an einer Stelle. Kosten: zwei neue Typen/Templates,
aktualisierte `CLAUDE.md`-Tabelle, req42-Anchor und Index. Instanzen entstehen beim
Ingest von `raw/kontextdiagramm.md` (separat, mit Grill-Gate).
