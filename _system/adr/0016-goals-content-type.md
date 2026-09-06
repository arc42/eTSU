# ADR-0016: Inhaltstyp **Goal** für req42-Block 01 „Zielsetzung"

- **Status:** accepted
- **Date:** 2026-05-28

## Context
req42-Block 01 **Zielsetzung** (Vision + Teilziele) hatte bislang keinen Platz im
Wiki. Der Vision-Entwurf für Aquarius (`raw/vision-draft.md`, 2026-05-27) — eine
Vision + vier [[PAM]]-Teilziele — lag deshalb außerhalb der typisierten Struktur und
konnte weder verlinkt noch im Graph projiziert werden.

Keiner der bestehenden zwölf Typen passt: `functional-requirements/` ist
Lösungsraum (Backlog), `quality-requirements/` sind ATAM-Szenarien zu ISO-25010-
Attributen, `constraints/` sind Einschränkungen, `context/` umreißt die
Systemgrenze. Ziele sind eine eigene Kategorie — der **Warum**-Raum, der den
Lösungsraum motiviert.

Sekundärfrage: **Vision vs. Teilziele — ein Typ oder zwei?** Beide sind Aussagen
über angestrebte Ergebnisse, unterscheiden sich aber in Form (Dach-Narrativ vs.
[[PAM]]-Struktur). Das Muster aus [[ADR-0012]] (ein Typ Functional requirement,
Stereotypen `epic|feature|story`) hat sich bewährt.

## Decision
**Ein neuer Inhaltstyp `goal`** (`wiki/goals/`, IDs `GOAL-NNN`) mit Feld
**`stereotype: vision | objective`**:

- **vision** — Dach-Narrativ, genau eines pro System; Format nach Geoffrey Moore
  („Für …, die …, ist <System> ein/eine …, das …. Anders als …").
- **objective** — Teilziel im **[[PAM]]**-Format (Purpose · Advantage · *eine* Metric);
  Promotion zu **[[SMART]]**, sobald `horizon` (Zeithorizont) gesetzt ist.

Hierarchie über **`parent:`**-Wikilinks (Objectives zeigen auf die Vision; Vision
hat keinen Parent). Zusätzliche frontmatter-Felder: `beneficiary:` (`[[STK-...]]`
— PAM-„Advantage"), `metric:`/`baseline:`/`target:` (genau ein Indikator),
`horizon:` (leer → PAM, gefüllt → SMART-tauglich).

Titel-Grammatik gemäß [[ADR-0015]]: **Substantivphrase mit klarem Outcome**
(Goals benennen Ergebnisse, nicht Aktivitäten). Sprache DE ([[ADR-0005]]).

Damit wächst die Typtabelle von **12 auf 13 Typen**.

## Consequences
Vision + Teilziele aus `raw/vision-draft.md` können jetzt in die Wiki überführt
werden (Folgeschritt, nicht Teil dieses ADR). Aktualisiert: `CLAUDE.md`-Typtabelle
+ Liste der Folder, `_system/index.md` (neuer Abschnitt **Goals** zwischen
Glossary und Stakeholders, entsprechend req42-Reihenfolge), neues Template
`_templates/goal.md`. **Keine Migration** — es gibt noch keine `GOAL-…`-Instanzen.

Bewusst **nicht** modelliert: getrennte Typen für Vision und Teilziel
(stattdessen Stereotyp, analog [[ADR-0012]]); Priorität (MoSCoW passt auf Backlog-
Items, nicht auf Ziele — bei wenigen Zielen genügt die Hierarchie). `beneficiary:`
ist eigenes Feld (nicht nur Prosa), damit Stakeholder-Verbindungen im Graphen und
in Reports auffindbar bleiben.
