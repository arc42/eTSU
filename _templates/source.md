---
id: SRC-NNN
type: source
title: <Source title>
status: ingested
created: {{date}}
updated: {{date}}
tags: [source]
source-type: document   # interview | transcript | document | spec | email | ticket | diagram | observation
origin: <raw/<file> for documents, or author / system / URL>
captured: {{date}}
sha256: <body hash for drift detection (shasum -a 256); n/a if no file>
ingested-pages: []      # [[...]] wiki pages this source touched
---

# {{title}}

<!-- Slim provenance record (ADR-0006): frontmatter + ONE summary line, in raw/sources/.
     No Summary/Key-takeaways/Provenance prose — narrative lives in _system/log.md. -->
<One-line summary of what this source is. Narrative lives in `_system/log.md`.>
