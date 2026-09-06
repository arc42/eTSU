# ADR-0003: Issues as a first-class meta-type

- **Status:** accepted
- **Date:** {{date}}

## Context
Requirements work is mostly about resolving uncertainty: open questions,
contradictions between sources, gaps, ambiguities, untestable quality goals. If the
agent silently resolves these, the human loses sight of what's actually decided.

## Decision
We will treat **Issue** as a content type that cross-cuts all others. Every Issue
links the pages it affects via `related:`. The agent raises an Issue rather than
picking a side on any contradiction or judgment call. Issues are filed in
`wiki/issues/` like any other type — there is no standing dashboard; the current
view is produced on demand via an "open issues" report.

## Consequences
The "state of unknowns" is captured rather than lost, and an open-issues report
surfaces it on demand. Issues stay symmetric with every other content type — no
special storage or maintenance. Slightly more issues to triage, which is the point:
they represent real decisions the human owns. ("Meta" here is behavioral — issues
cross-cut and annotate the other types — not structural.)
