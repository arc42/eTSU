---
id: ISS-011
type: issue
title: Every context flow was inferred from box labels — no arrow in the diagram carries a payload
status: open
created: 2026-09-09
updated: 2026-09-09
sources:
  - "[[SRC-004-ulrich-stuerzlinger-context-diagram]]"
related:
  - "[[CTX-001-etsu-system-context]]"
  - "[[EIF-001-artists]]"
  - "[[EIF-013-technology-and-infrastructure]]"
tags: [issue]
severity: major
kind: gap
raised-by: agent
resolved: null
---

# Every context flow was inferred from box labels — no arrow in the diagram carries a payload

**What's unresolved.** ADR-0013 requires each `EIF` to carry
`flows: {data, direction, format, trigger}`. The source diagram supplies
**direction only** — solid arrows are outbound, dashed are return, per its own
legend. It labels no arrow. Every `data:` value in all fourteen `EIF` pages was
therefore read off the *box* sub-label and written by the agent; every `format:`
is `unknown`; almost every `trigger:` is `unknown` or marked `unconfirmed`.

**Affects.** All of [[EIF-001-artists]] … [[EIF-014-regulatory-and-compliance]]
and the projection in [[CTX-001-etsu-system-context]].

**Context / evidence.** The diagram's legend reads in full: *"Solid arrows =
outbound flows | Dashed arrows = return flows | SUPPLY (left) | GREY support
tier (top center) | DEMAND (right) | PURPLE core ops (bottom)"*. That is the
entire flow specification.

So, for example, [[EIF-001-artists]] is recorded as carrying "artwork
submissions and tour participation" inbound and "sale notifications and
commission statements" outbound. Both are plausible from the box label
"Create & submit" and from the brief — **and neither is stated by the source.**

This matters most where the payload determines the design.
[[EIF-013-technology-and-infrastructure]] is recorded as exchanging payment
authorisations, because the box says "payments" — but whether eTSU initiates a
charge, receives a settlement webhook, or merely records a bank transfer made
elsewhere are three different systems, and the brief's deposit sequence (10%
within 24 h, balance within 14 days, half the deposit forfeited on default) is
only enforceable under some of them.

**Options.**
1. Walk the diagram with its author and label the arrows. Cheapest and highest
   value — one session converts fourteen guesses into fourteen facts. Recommended.
2. Leave `flows:` as drafted, treat every entry as a hypothesis, and let use
   cases correct them as they are written.
3. Empty the `flows:` lists back to direction-only, so the wiki asserts nothing
   it cannot source. Most honest; makes the projected diagram far less useful.

**Resolution.** *Open.*
