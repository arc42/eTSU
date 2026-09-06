# ADR-0007: req42 als Dach-Anchor und methodische Referenz

- **Status:** accepted
- **Date:** 2026-05-24

## Context
Die Inhaltstypen dieses Wikis (Glossar, Stakeholder, Use Cases, User Stories,
Features, Qualitätsanforderungen, Constraints, Issues …) sind faktisch die
Bausteine des **req42-Frameworks** (Hruschka & Meuten); die kleineren Anchors
([[SMART]], [[PAM]], [[INVEST]], [[MoSCoW]], [[user-story-format]]) sind Standards,
die req42 *innerhalb* dieser Bausteine verwendet. Bislang war diese methodische
Herkunft nirgends festgehalten. ADR-0004 hält fest: einen Anchor hinzuzufügen ist
ein bewusster, ADR-würdiger Akt.

## Decision
req42 wird als **Dach-Anchor** `_system/anchors/req42.md` aufgenommen (zitierbar als
`[[req42]]`), schlank gehalten und mit einer **Mapping-Tabelle** req42-Baustein →
Inhaltstyp/Anchor versehen. Eine ausführlichere, menschenlesbare Referenz liegt als
**Mirror** unter `docs/req42/`. req42 ist *Methode, nicht Domäne* — es wird **nicht**
über den Ingest-Workflow eingelesen und erzeugt keine `wiki/`-Seiten.

Quelle und Lizenz: req42 steht unter **CC BY-SA 4.0** (Hruschka & Meuten). Beide
Dateien nennen Autoren, Lizenz und kanonische Quelle; der Mirror ist eine adaptierte
Zusammenfassung (kein Verbatim-Abzug) und steht seinerseits unter CC BY-SA 4.0.

## Consequences
Die methodische Grundlage der Taxonomie ist jetzt explizit, zitierbar und prüfbar
(Coverage-Checkliste im Anchor). Sichtbar wird auch eine **Lücke**: req42-Baustein 03
*Scope & Abgrenzung* hat noch keinen Inhaltstyp (relevant, sobald
`raw/kontextdiagramm.md` ingestiert wird) — separat zu entscheiden. Kosten: bei
größeren req42-Updates müssen Anchor und Mirror nachgezogen werden (Drift gegenüber
Upstream); Lizenzpflichten (Attribution, Share-Alike) sind einzuhalten.
