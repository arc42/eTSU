---
id: ISS-008
type: issue
title: Thomas Marti's eTSU email arrived with an empty body
status: wontfix
created: 2026-09-09
updated: 2026-09-09
sources:
  - "[[SRC-003-thomas-marti-etsu-empty]]"
related: []
tags: [issue]
severity: minor
kind: gap
raised-by: agent
resolved: 2026-09-09
---

# Thomas Marti's eTSU email arrived with an empty body

**What's unresolved.** A third workshop email was received on 2026-09-09,
subject "eTSU", from Thomas Marti. Its body is empty — nothing was ingested from
it. Either it was sent blank, or content was lost in transit or in saving it to
`raw/`. Until someone asks, we do not know which, and a missing contribution
from a workshop participant is worth chasing.

**Affects.** Nothing directly — no page derives from this source. It is recorded
so that an unexplained gap in the workshop input does not silently vanish.

**Context / evidence.** The saved file is an `.rtfd` bundle
(`raw/ingested/eTSU-ThomasMarti.rtfd`) containing a single `TXT.rtf`. That file
holds the header block (From / Subject / Date / To) and the Netcetera signature,
with nothing between them. No attachments are present in the bundle.

Since the other two emails from the same day and the same organisation both
carried substantial content (visions, goals, stakeholders), a blank third one is
more likely truncation than an intentionally empty send — but that is an
inference, not evidence.

**Options.**
1. Ask Thomas Marti to resend. Recommended — cheapest, and resolves it definitively.
2. Check whether the original mail had an attachment that was dropped when the
   `.rtfd` bundle was saved.
3. Close as `wontfix` if the email really was sent empty.

**Resolution.** **Closed `wontfix` 2026-09-09** by [[STK-001-gus-renoir]]: the
email can be ignored. Nobody will chase Thomas Marti for a resend, and no page
depends on it. [[SRC-003-thomas-marti-etsu-empty]] stays on record so the empty
source does not look like an oversight later.
