# ADR-0005: Fachsprache für Aquarius ist Deutsch

- **Status:** accepted
- **Date:** 2026-05-24

## Context
Aquarius modelliert die Domäne der Kinderschwimmliga. Sämtliche Quellen in `raw/`
(Glossar, Use Cases, Kontextdiagramm) sind deutsch, und die ubiquitäre Sprache
besteht aus deutschen Fachbegriffen — *Anmeldung*, *Durchgang*, *Kampfrichter*,
*Punktrichter*, *Start*, *Station* — die keine verlustfreien englischen
Entsprechungen haben. Eine Übersetzung würde die ubiquitäre Sprache zerfasern und
die Domänenexperten von ihren eigenen Anforderungen entfremden.

## Decision
Die **Fachsprache für Aquarius ist Deutsch**. Alle Anforderungs-Seiten im `wiki/`
— Glossarbegriffe, Stakeholder, Datenmodelle, Aktivitätsmodelle, Use Cases, User
Stories, Features, Qualitätsanforderungen, Constraints und Issues — werden auf
Deutsch geschrieben. Der Agent darf in Englisch **oder** Deutsch konversieren und
Rückfragen stellen (je nachdem, was dem Menschen passt), aber jeder erfasste
Anforderungsinhalt bleibt deutsch.

Die methodischen `_system/anchors/` (SMART, PAM, INVEST, MoSCoW,
user-story-format) und die übrige `_system/`-Maschinerie dürfen englisch bleiben —
sie sind Methode, nicht Domänenwissen.

## Consequences
Die ubiquitäre Sprache bleibt intakt und verlustfrei; Domänenexperten lesen
Anforderungen in ihrer eigenen Sprache. Preis: Der Agent muss auch dann auf Deutsch
erfassen, wenn er die Grilling-Session auf Englisch führt, und die Trennung von
Methoden-Sprache (EN erlaubt) und Domänen-Sprache (DE verbindlich) konsequent
einhalten.
