# Workflow: Report

Produce a view over the wiki for a specific audience or question. Reports are
*derived* — but a good one can be filed back as a wiki page so it compounds.

## Common reports

- **Open issues** — current `ISS-NNN` by severity/status, read from `wiki/issues/`.
  Generated on demand; no standing file.
- **Requirements coverage** — features → use-cases → stories → acceptance criteria;
  highlight gaps.
- **Stakeholder matrix** — influence × interest grid, with linked goals/concerns.
- **Quality scenarios** — all `QR-NNN` as an ATAM-style table; flag untestable ones.
- **Glossary** — the agreed ubiquitous language, alphabetized, contested terms marked.
- **Traceability** — from a source or stakeholder goal down to the stories that serve it.

## Steps
1. Read `_system/index.md`, then drill into the relevant pages.
2. Synthesize with citations (link the `TYPE-NNN` pages and `SRC-NNN` sources).
3. Choose the form: markdown page, comparison table, or chat response.
4. If the report has lasting value, file it as a page and link it from `_system/index.md`.
5. Append to `_system/log.md`: `## [YYYY-MM-DD] report | <title>`.
