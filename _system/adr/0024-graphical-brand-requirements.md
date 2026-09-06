# ADR-0024: Grafische / Marken-Anforderungen als Constraints + Quality-Szenarien; Assets in `raw/`; Geschmack-vs-Messbar als Issue

- **Status:** accepted
- **Date:** 2026-06-24

## Context

Der Ligapräsident ([[STK-006-ligapraesident|Fritz Flosse]], `influence: high`,
Gründer/Entscheider/Sponsor) bringt **grafische Anforderungen** ins System ein — und tut
das aus einer Position, die schwer zu überstimmen ist. Konkret liegen bereits im Posteingang:

- **Acht Logo-Farbvarianten** unter `raw/drafts/logos/` (aqua-teal, classic, coral-reef,
  forest-green, marine-blue, sunset-tide, triple-blue, tropical-water) — d. h. das
  **Farbschema ist noch nicht entschieden**, es zirkulieren Kandidaten.
- Zwei Mails, die Grafik in funktionale Wünsche einbetten:
  `raw/drafts/urkunden-druck-anforderung-flosse.eml` (Urkunde mit „schönem, buntem Logo"
  **und eingescannter Präsidenten-Unterschrift") und
  `raw/drafts/ergebnistafel-anforderung-flosse.eml` (digitale Ergebnistafel, „gut sichtbar
  für alle Besucher").

Die Schema-Taxonomie ([[0002-content-type-taxonomy|ADR-0002]]) kennt 13 Inhaltstypen —
**keiner** ist ein natürliches Zuhause für „Logo / Farben / Markenauftritt". Daraus zwei
Spannungen:

1. **Grafik ist dekretiert, nicht hergeleitet.** Ein Logo oder eine Palette *emergiert*
   nicht aus Analyse — der Präsident *verfügt* sie. Das ist die Lehrbuch-Definition eines
   **Constraints** (fixe Grenze des Lösungsraums), keine aus Anforderungen abgeleitete
   Feature- oder Quality-Aussage. Würden wir Geschmack als „Requirement" behandeln, würden
   wir ihn fälschlich zur Diskussion stellen.
2. **Binär-Assets gehören nicht in `wiki/`.** Die `wiki/`-Schicht ist ein **Text-Graph**
   aus verlinkten Einheiten; PNG-Logos und gescannte Unterschriften sind menschliche
   Quellen, keine generierten Wissensseiten.

Hinzu kommt ein **Governance-Risiko**: Geschmack des Präsidenten (welches der 8 Schemata,
„bunt und schön") kann mit einem *objektiven* Bedarf kollidieren — z. B. ein hübsches, aber
kontrastarmes Schema, das auf der Ergebnistafel quer durch die Halle unlesbar ist. Die Wiki
darf hier weder den Geschmack überstimmen noch das Lesbarkeitsproblem verschweigen
(CLAUDE.md: *flag and propose, never block or silently rewrite — the human decides*).

Optionen:

- **A** — Ein **14. Inhaltstyp** „Design-/Marken-Asset". Schwergewichtig: eigenes Template,
  eigener Ordner, eigene Audit-/Index-Logik — für bislang eine Handvoll Regeln. Verstößt
  gegen das Sparsamkeitsprinzip, das schon [[0021-file-format-specs-at-boundary-owner|ADR-0021]]
  bei den Dateiformat-Specs durchgesetzt hat.
- **B** — **Ad hoc** je Mail im jeweiligen FR mitschreiben. Kein gemeinsamer Ort für die
  Markenregel; Logo-/Farbvorgaben wären über viele FRs verstreut, driften auseinander, und
  die Geschmack-vs-Messbar-Trennung ginge verloren.
- **C** — **Zerlegung auf bestehende Typen**: die Markenvorgabe als **Constraint**, ihre
  Anwendung als **Functional Requirement**, ihre messbare visuelle Güte als **Quality
  Requirement**; Assets in `raw/`; Geschmack-vs-Messbar-Konflikte als **Issue**.

## Decision

**Option C.** Grafische / Marken-Anforderungen erhalten **keinen eigenen Inhaltstyp**,
sondern werden auf die vorhandenen Typen projiziert — analog zum Reframe von
[[0021-file-format-specs-at-boundary-owner|ADR-0021]] („kein neuer Content-Type, am richtigen
Owner platzieren").

1. **Die Markenvorgabe selbst → Constraint.** Logo, Farbpalette, Typografie und die
   „Präsidenten-Unterschrift auf offiziellen Dokumenten" werden als **Constraint**
   festgehalten (`category: organizational`, Origin = [[STK-006-ligapraesident]]). Als
   Dekret ist der Constraint **per Definition nicht verhandelbar** — wir erfassen ihn treu,
   wir grillen ihn nicht klein. (Wo der Akzent klar *persönlicher* Geschmack des Präsidenten
   statt Organisationsstandard ist, ist `category: political` zulässig.)
2. **Die Anwendung der Marke → Functional Requirement.** Die *Funktion* (welche Daten,
   welcher Ablauf) lebt im FR — Urkunden-Druck, digitale Ergebnistafel — und **referenziert**
   den CI-Constraint für ihr Aussehen. Der FR trägt den fachlichen Inhalt, nicht die Pixel.
3. **Messbare visuelle Güte → Quality Requirement.** Lesbarkeit, Kontrast,
   Wiedererkennbarkeit werden als **QR** (ISO 25010 `usability` — UI-Ästhetik /
   Angemessenheit der Erkennbarkeit, plus Barrierefreiheit/Kontrast) mit einer **Zahl**
   formuliert (z. B. „aus 15 m lesbar; Kontrast ≥ WCAG AA"). **Erst das macht Farbe
   diskutierbar**, ohne über Geschmack zu streiten.
4. **Assets bleiben in `raw/`, die Wiki referenziert per Pfad.** Binär-Dateien durchlaufen
   den Quellen-Lebenszyklus ([[0008-raw-inbox-ingested-archive|ADR-0008]]): Inbox → nach
   Ingest `raw/ingested/`, mit schlankem Provenance-Record in `raw/sources/`
   ([[0006-provenance-records-location|ADR-0006]]). Der Constraint nennt **genau eine**
   kanonische Datei → **Single Source of Truth**; Varianten werden archiviert. `wiki/` hält
   die *Regel in Text*, nie das Bild.
5. **Geschmack-vs-Messbar-Konflikt → Issue, nie Überstimmung.** Kollidiert die ästhetische
   Wahl mit dem QR-Messwert, wird ein **`ISS-NNN`** angelegt
   ([[0003-issues-as-meta-type|ADR-0003]]), das Constraint und QR verlinkt, den Trade-off
   darlegt — **der Präsident entscheidet**, mit explizit gemachtem Trade-off.

**Bewusst offen gelassen:** die *konkrete* Logo-/Farbentscheidung. Fritz ist bei Details
noch unentschieden (8 Kandidaten). Diese ADR legt nur die **Strategie/Politik** fest; die
inhaltliche Wahl wird **später** beim Ingest erfasst — als Constraint plus ein **blockierendes
Issue** „Farbschema noch nicht entschieden", das der QR (Kontrast/Lesbarkeit) eingrenzt.

## Consequences

- **Schema bleibt schlank.** Wiederverwendung von Constraint + Quality + Source statt eines
  14. Typs; [[0002-content-type-taxonomy|ADR-0002]] bleibt unangetastet. Reiht sich in die
  Sparsamkeitslinie von [[0021-file-format-specs-at-boundary-owner|ADR-0021]] ein.
- **Routing-Regel für künftige grafische Wünsche:** Dekret → Constraint, Anwendung → FR,
  messbare Güte → QR, Asset → `raw/`, Geschmack-Konflikt → Issue. Jeder neue Logo-/Farb-/
  Layout-Wunsch ordnet sich damit selbst ein.
- **Assets folgen dem Quellen-Lebenszyklus** ([[0008-raw-inbox-ingested-archive|ADR-0008]],
  [[0006-provenance-records-location|ADR-0006]]); genau **ein** kanonisches File als SSoT
  entschärft die bereits sichtbare Drift (z. B. `coral-reef-redrawn.png` 628 KB vs. die
  `-flat`-Varianten).
- **Farbe wird verhandelbar gemacht, nicht erstritten.** Die objektive Schranke lebt im QR;
  der Geschmack im Constraint. Differenzen laufen über ein Issue — konsistent mit dem
  „flag and propose"-Prinzip (CLAUDE.md). Die Wiki nimmt nie selbst Partei.
- **Konkrete Logo-/Farbwahl bleibt offen** (Fritz unentschieden). Die 8 Kandidaten und die
  zwei Mails sind weiterhin **grill-gated zu ingesten** — voraussichtlich: 1 CI-Constraint,
  FRs „Urkunden-Druck" + „Digitale Ergebnistafel" (Letztere überlappt
  [[QR-001-aktualitaet-live-stand]] und das „Backoffice entlasten"-Ziel), 1–2 QRs
  (Lesbarkeit/Kontrast, Druckqualität), 1 blockierendes Issue (Farbschema), ggf. Glossar
  („Ligalogo"/„Corporate Design", „Urkunde", „Ergebnistafel") sowie SRC-Records für
  Logo-Set und Mails.
- **Reversal** hieße: einen dedizierten Inhaltstyp „Design/Brand" über eine ablösende ADR
  einführen — sinnvoll erst, wenn das Volumen an Markenregeln das Eigengewicht eines Typs
  trägt. Daher dieser Record.
