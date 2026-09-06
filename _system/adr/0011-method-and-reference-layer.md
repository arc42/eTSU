# ADR-0011: Methoden- & Referenz-Schicht (raw/methods → anchors + docs)

- **Status:** accepted
- **Date:** 2026-05-25

## Context
Wir sammeln zunehmend RE-Methodenwissen an (Templates, Jeff Pattons Story-Mapping-
Artikel, Dr. Hruschkas req42-Kapitel — alles unter `raw/methods/`). Bisher war
unklar, wo solche *Methode/Referenz* dauerhaft lebt und wie sie sich von Domänen-
Wissen unterscheidet. Zudem sind manche Quellen **urheberrechtlich geschützt** (Pattons
Artikel, Hruschkas Buchkapitel) — anders als das req42-*Template* (CC BY-SA 4.0).

## Decision
Methodenwissen spiegelt die Domänen-Schichtung:

- **`raw/methods/`** — Methoden-*Quellmaterial* (die Originale; insbesondere die
  urheberrechtlich geschützten bleiben hier privat, werden **nicht** wörtlich
  republiziert).
- **`_system/anchors/`** — die *angewandten* Standards/Techniken, daraus destilliert,
  zitierbar (`[[…]]`) und mit Checkliste (advisory enforcement). Neuer Anchor:
  **[[story-mapping]]**.
- **`docs/`** — *lesbare, destillierte* Referenzen **mit Attribution** (z. B.
  `docs/methods/`, `docs/req42/`). `docs/` ist die bevorzugte Heimat für aufbewahrte
  Referenzen (Bücher, Artikel) — destilliert + attribuiert, nicht wörtlich.

Lizenzlinie: Destillat + Attribution + Link in `docs/`; **kein** wörtlicher Abzug
geschützter Werke. (Das req42-Template bleibt CC BY-SA 4.0; Pattons Artikel und
Hruschkas Kapitel sind normales Urheberrecht.)

## Consequences
Klare Symmetrie Domäne ↔ Methode; Referenzen wohnen in `docs/` wie gewünscht;
Urheberrecht gewahrt. Einen Anchor hinzuzufügen bleibt ADR-würdig (ADR-0004). Story
Maps selbst werden **nicht** zum Inhaltstyp — sie sind eine Projektion/Report über die
Product-Backlog-Hierarchie (siehe [[story-mapping]]).
