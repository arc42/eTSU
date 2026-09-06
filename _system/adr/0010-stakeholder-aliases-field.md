# ADR-0010: Feld `aliases` im Stakeholder-Template

- **Status:** accepted
- **Date:** 2026-05-25

## Context
Quellen benennen dieselbe Rolle unterschiedlich. Die Story (SRC-004) spricht vom
*Backoffice* — gemeint ist die fachliche Organisator-Rolle, die wir als
[[STK-004-wettkampforganisator|Wettkampforganisator]] führen. Solche
User-Kategorie-/Synonymnamen sollen auffindbar sein, ohne den kanonischen Titel zu
ändern oder Stakeholder zu duplizieren. Das Glossar-Template hat dafür bereits
`aliases`; das Stakeholder-Template nicht.

## Decision
Das Stakeholder-Template erhält ein optionales Feld **`aliases: []`** (alternative
Namen / User-Kategorie-Labels). Obsidian löst `[[Backoffice]]` damit auf den
kanonischen Stakeholder auf. Rolle und Person bleiben getrennt: eine Mehrpersonen-
**Rolle** (z. B. Wettkampforganisator, alias *Backoffice*) kann mehrere **Instanzen**
haben (Personen-Stakeholder wie [[STK-006-ligapraesident|Fritz Flosse]] plus
Freiwillige), verlinkt über `related`.

## Consequences
Synonyme/Kategorienamen sind auffindbar, ohne Duplikate oder Titeländerungen. Kosten:
ein weiteres optionales Frontmatter-Feld; Bestandsseiten müssen es nicht nachtragen
(leer = kein Alias). Gruppen über *mehrere* Rollen (z. B. „Offizielle“, „Kinder &
Eltern“) sind **keine** Aliase eines einzelnen Stakeholders — sie werden als
User-Gruppen im Kontextknoten ([[CTX-001-systemkontext]]) geführt.
