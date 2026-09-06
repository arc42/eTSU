# ADR-0015: Backlog-Namenskonvention — epic/feature als Substantiv, story/use-case als Verb

- **Status:** accepted
- **Date:** 2026-05-27

## Context
[[ADR-0012]] führte den Typ **Functional requirement** mit `stereotype: epic | feature |
story` ein, ließ aber die **Titel-Grammatik** offen. Das Template sagte
`title: <short imperative name>` (also Verb), während die gelebte Praxis (ISS-009) Epics
als **Substantive** benannte (Saisonplanung, Stammdatenpflege …) — ein Widerspruch.

„Epic" ist kein IREB-/CPRE-Begriff (agil/SAFe), daher gibt es dafür keine verbindliche
IREB-Namensregel. Die umliegende Literatur ist aber überwiegend **verb-zentriert**:
Use Cases werden bei Cockburn als **Verb + Objekt** (aktives Ziel) benannt; Jeff Pattons
Story Map nennt Backbone-Activities und Tasks als **Verben**; die IREB/SOPHIST-Rupp-
Schablone baut den **Anforderungssatz** um ein Prozesswort (Verb) und behandelt
**Nominalisierung** als Ambiguitäts-Smell — das gilt jedoch dem *Satz*, nicht der
*Überschrift* eines Backlog-Items. Für gröbere Backlog-Knoten (Epic/Feature) ist dagegen
die **Substantiv-/Capability-Benennung** üblich (Tool-Praxis) und im Deutschen durch den
Nominalstil idiomatisch.

## Decision
**Konvention „A": Die Wortart des Titels signalisiert die Granularität.**

- **Epic + Feature** → **Substantivphrase mit klarem Outcome** (z. B. *Saisonvorbereitung,
  Wettkampfanmeldung, Wettkampfdurchführung, Ergebnisauswertung, Systemadministration*).
- **Story + Use-Case** → **Verb + Objekt** (aktives Ziel; z. B. *Wettkampf absagen,
  Versuch bewerten*).
- **Anglizismen meiden** (Domänensprache Deutsch, Stand ADR-0005 vom 2026-05-27;
  seit dessen Neufassung am 2026-09-06 ist die Domänensprache Englisch, dieser
  Punkt ist historisch) — z. B. „Reporting" → „Ergebnisauswertung".

Durchsetzung bleibt **advisory** (wie alle Anchor-Standards): beim Ingest/Audit gegen die
Namensregel prüfen, Abweichungen als `ISS-NNN` melden — nie blockieren oder still
umbenennen. Die Regel ist im [[story-mapping]]-Anchor (inkl. Grill-/Audit-Checklistenpunkt)
verankert.

## Consequences
Verfeinert [[ADR-0012]] (dort offen gelassene Titel-Grammatik). Angepasst:
`_templates/functional-requirement.md` (stereotyp-spezifischer `title:`-Hinweis +
Autoren-Notiz), `_templates/use-case.md` (`title:` = „verb + object"), und der
[[story-mapping]]-Anchor (Namensregel + Checklistenpunkt). **Keine Migration** — es gibt
noch keine `FR-…`-Instanzen; die sechs Epic-Kandidaten in `raw/Kandidaten für Epics.md`
sind bereits konform benannt (Substantive). Offen bleibt nur, die Regel beim ersten echten
Backlog-Ingest praktisch anzuwenden.
