# ADR-0012: Funktionale Anforderungen als ein Typ mit Stereotyp (epic|feature|story)

- **Status:** accepted
- **Date:** 2026-05-25

## Context
Wir hatten **Feature** und **User story** als getrennte Inhaltstypen. req42s
Product-Backlog (Block 04) ist aber **eine** Hierarchie funktionaler Anforderungen in
drei Granularitäten — **Epic → Feature → Story** — die man als Story Map projiziert.
Getrennte Typen zersplittern diese Familie und tragen keinen einheitlichen
Eltern-/Kind-Graphen. Der Auftraggeber will „eine funktionale Anforderung als Epic,
Story oder Feature markieren, um eine Hierarchie (oder einen Graphen) zu ermöglichen“.

## Decision
Ein Inhaltstyp **Functional requirement** (`wiki/functional-requirements/`, `FR-NNN`)
mit Feld **`stereotype: epic | feature | story`**. Die Hierarchie entsteht über
**`parent:`**-Wikilinks (mehrere erlaubt ⇒ Graph, nicht nur Baum). Für die
Story-Map-Projektion ([[story-mapping]]) tragen die Knoten zusätzlich **`order`**
(Backbone-Reihenfolge), **`priority`** ([[MoSCoW]]) und **`release`** (Swim-Lane).

Die bisherigen, **leeren** Typen Feature und User story gehen darin auf (13 → 12
Inhaltstypen). Abnahmekriterien werden per neuem Anchor **[[acceptance-criteria]]**
(Given/When/Then) erfasst — aus den abgelegten Templates geerntet. Das
Use-Case-Template wurde (Cockburn-Stil) angereichert, bleibt aber ein **eigener** Typ.
**Estimate/Owner** werden bewusst nicht im Wiki modelliert (Sache des Trackers, z. B.
JIRA); das Wiki hält Anforderungs-Fakten: Stereotyp, Hierarchie, Priorität, Release, Order.

## Consequences
Einheitlicher, graph-fähiger Backlog; die Story Map ist eine reine Projektion. Alle
Quer-Verweise heißen jetzt `[[FR-...]]` (statt `[[FEAT-...]]`/`[[US-...]]`). Aktualisiert:
`CLAUDE.md`-Typtabelle, req42-Anchor + `docs/req42/`, Index, Dashboard-App. Migration:
keine — beide Alttypen waren instanzenlos.
