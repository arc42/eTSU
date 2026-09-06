---
id: GOAL-NNN
type: goal
title: <Name>           # Substantivphrase, Outcome-orientiert (z. B. „Echtzeit-Transparenz für Familien"), DE (ADR-0005)
status: draft           # draft | review | accepted | deprecated
created: {{date}}
updated: {{date}}
sources: []
related: []             # [[STK-...]], [[FR-...]], [[QR-...]], [[CON-...]]
tags: [goal]
stereotype: objective   # vision | objective  (vision = Dach-Narrativ; objective = PAM-Teilziel)
parent: []              # [[GOAL-...]] — Vision hat keinen Parent; Teilziele zeigen auf die Vision
beneficiary: []         # [[STK-...]] — wer den Vorteil hat (PAM „Advantage")
metric:                 # ein einziger Indikator (PAM); leer bei Vision
baseline:               # Ist-Wert, sobald erhoben/geschätzt — sonst leer
target:                 # Soll-Wert (z. B. „≤ 50 %", „< 15 Min")
horizon:                # Zeithorizont (z. B. „ab Saison 2027"); leer → noch PAM, gefüllt → [[SMART]]-tauglich
---

# {{title}}

<!-- Ein Typ, zwei Stereotypen — analog ADR-0012 (FR mit epic|feature|story).
     Vision = Dach (genau ein GOAL pro System); Objectives = Teilziele unter der Vision.
     Hierarchie via `parent:`-Wikilinks. Titel-Grammatik: Substantivphrase mit klarem
     Outcome (ADR-0015). DE-Fachsprache (ADR-0005). -->

## Vision  — when `stereotype: vision`   > Format nach Geoffrey Moore (Kontrast-Klausel optional)

Für **<Zielgruppe>**, die **<Bedarf/Problem>**, ist **<System>** ein/eine
**<Kategorie>**, das/die **<Schlüsselnutzen>**.

*Optional:* `Anders als <Alternative> <Differenzierung>.` — nur einsetzen, wenn
Markt-Positionierung gegen konkrete Alternativen Teil der Vision ist. Für eine
positive, einladende Vision **weglassen** (so gehandhabt in [[GOAL-001-aquarius]]).

**Teilziele.** siehe `parent:`-Backlinks (Objectives, die auf diese Vision zeigen).

## Objective  — when `stereotype: objective`   > folgt [[PAM]]; promotion zu [[SMART]] sobald `horizon` gesetzt

- **Purpose.** <Ergebnis, keine Aktivität — was angestrebt wird>
- **Advantage.** <für wen (siehe `beneficiary:`) welcher konkrete Vorteil — „so what?">
- **Metric.** <der eine Indikator (siehe `metric:` / `baseline:` / `target:`)>

**Parent.** siehe `parent:` (üblicherweise die Vision).

## Wirkung

- **Adressierte Stakeholder:** siehe `beneficiary:` (+ ggf. weitere unter `related:`).
- **Bedient durch:** projiziert aus den **FR-Backlinks** (Obsidian-Backlink-Pane bzw. Dashboard-Coverage-Matrix). Jeder `[[FR-...]]`, der dieses Ziel im `goal:`-Feld führt, erscheint hier automatisch — **nicht** manuell pflegen (Projektions-Prinzip, ADR-0018).

> [!note] Offene Punkte
> <fehlende Baseline, untestbare Metric, ungeklärter Zeithorizont → als [[ISS-...]] aufnehmen>

<!-- Goals decken req42-Block 01 „Zielsetzung" ab (ADR-0016). Sie sind der Zielraum
     (warum), nicht der Lösungsraum (wie); Letzteren tragen FR/QR/CON. -->
