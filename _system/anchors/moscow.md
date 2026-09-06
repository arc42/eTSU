---
type: anchor
title: MoSCoW
aliases: [MoSCoW, moscow]
tags: [anchor, prioritization]
applies-to: [feature, use-case, user-story, quality-requirement]
---

# MoSCoW

The shared meaning of the `priority` field used across features, use cases, stories,
and quality requirements. One definition, cited everywhere.

- **Must** — without it the release fails; non-negotiable for this scope.
- **Should** — important and painful to omit, but the release survives without it.
- **Could** — desirable; included only if time and budget allow.
- **Won't** (this time) — explicitly out of scope now; recorded so it isn't relitigated.

## Checklist (audit / grill)
- [ ] Every `Must` is genuinely release-blocking, not a disguised `Should`.
- [ ] `Must` items are a minority — a backlog that is mostly `Must` has not been prioritized.
- [ ] Each `Won't` is recorded with a reason, so the decision is durable.
