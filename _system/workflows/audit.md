# Workflow: Audit  (the "lint" / health-check pass)

Keep the wiki consistent, current, and complete. Run periodically or on request.

## Checks

- **Contradictions** — claims that conflict across pages. Open an `ISS-NNN`
  (kind: contradiction) with both sides quoted; do not pick a winner.
- **Stale claims** — pages a newer source has superseded. Flag and propose update.
- **Orphans** — pages with no inbound wikilinks; decide link or deprecate.
- **Missing pages** — concepts referenced but with no page (glossary terms used
  but undefined, stakeholders mentioned but not profiled).
- **Broken links** — wikilinks to nonexistent IDs.
- **Anchor conformance** — check instances against `_system/anchors/` checklists:
  goals not following [[SMART]]/[[PAM]], stories failing [[INVEST]] or the
  [[user-story-format]], priorities misusing [[MoSCoW]] (e.g. a mostly-`Must`
  backlog). Raise an Issue per misfit with the proposed fix; advisory, never auto-rewrite.
- **Untestable quality requirements** — any `QR-NNN` with `testable: false` or no
  quantified measure → Issue.
- **Unsourced claims** — assertions with empty `sources:` and no `> [!assumption]`.
- **Source drift** — recompute sha256 for each `SRC-NNN` against the file at its
  `origin:` path (archived sources live in `raw/ingested/`, ADR-0008); mismatch means
  the raw file changed after ingest → re-ingest. A missing file at `origin:` is itself
  an Issue.
- **Coverage gaps** — features with no stories/use-cases; stakeholders with no
  linked use-cases; use-cases with no acceptance path.
- **Kontext-Kanten & Projektion** — die Kanten, aus denen das Kontextdiagramm
  projiziert wird (`EIF.flows`, `STK.provides`/`receives`), sind die Single Source of
  Truth (ADR-0013). Prüfe: jeder Flow nennt einen existierenden Partner/eine Rolle,
  die Flüsse sind widerspruchsfrei (vgl. ISS-011), und `build_context_diagram()`
  rendert valides mermaid. Drift gibt es konstruktionsbedingt keine (reine Projektion,
  kein persistiertes Diagramm) — daher kein Redraw-Loop, nur dieser Konsistenz-Check.
- **Relationship / graph edges** — reciprocal `related:`, concept-identity links across
  types (e.g. `GLO-` term ⇄ `DM-` entity of the same slug), entity ⇄ import-format. This
  is a structural check over the edge graph; run the dedicated **`relations.md`** (the
  graph linter) for it rather than inlining it here.

## Output
1. An **audit report** presented in chat (or filed as a wiki page if lasting).
2. New/updated `ISS-NNN` for every finding worth tracking.
3. Auto-fix only high-confidence, mechanical issues (exact-match broken link to an
   existing page). Everything judgmental → queue as an Issue for the human.
4. Append to `_system/log.md`: `## [YYYY-MM-DD] audit | <scope>` + finding counts.
