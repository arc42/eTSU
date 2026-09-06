# ADR-0005: The ubiquitous language of this wiki is English

- **Status:** accepted
- **Date:** 2026-09-06

## Context
This vault is a content-free requirements-wiki *starter*: the schema — `CLAUDE.md`,
`_templates/`, `_system/anchors/` and the workflows — ships with no domain sources in
`raw/` and no populated `wiki/` pages. It exists to run an English-language workshop,
whose participants read the schema, fill the templates, and converse about the domain
in English. There are no domain experts attached to this vault yet whose vocabulary
could be consulted; the audience is the workshop itself.

A previous version of this ADR, written for a populated vault modelling a specific
non-English-speaking domain, decided the opposite: that vault's sources and
stakeholders used a domain vocabulary with no lossless English equivalents, so
translating it would have fractured the ubiquitous language and alienated the very
domain experts the wiki served. That reasoning does not transfer here — this starter
has no such sources or experts to alienate, and its actual audience shares English.

## Decision
The **ubiquitous language of this wiki is English**. Every requirement page —
glossary terms, stakeholders, context and external-interface pages, data and activity
models, use cases, stories, features, quality requirements, constraints, and issues —
is captured in English. The agent may converse and ask clarifying questions in **any
language** the human prefers; only the content written into `wiki/` pages is bound to
English.

The methodical `_system/anchors/` ([[SMART]], [[PAM]], [[INVEST]], [[MoSCoW]],
[[user-story-format]]) and the rest of the `_system/` machinery stay English, as they
already did under the previous decision — this ADR only fixes the language of
*domain* content, which a fresh starter otherwise leaves undefined.

## Consequences
Workshop participants read every page — schema, templates, and any worked example —
in one language, with no translation step between what is said in the room and what
lands in the wiki. The cost is symmetric with the previous decision's: any source
material or domain vocabulary that does not natively live in English must be
translated before it can be captured, and a term with no clean English equivalent
needs a glossary entry that names the gap rather than one that quietly papers over it.

## Note
This is a **per-project choice**, not a universal one — it fits this workshop's
audience today, and it will be wrong the moment a different group inherits this
starter to model a domain whose experts do not think and talk in English. That team
should **supersede this ADR on day one**, before the first real source is ingested,
with a new ADR naming their own ubiquitous language — exactly as the predecessor
decision this ADR replaces once did for a domain of its own.

A glossary is only as good as the words the people who own the domain actually use.
One written in a language the domain experts do not speak natively is worthless
twice over: once because every requirement must be translated into that language
before this wiki can capture it, and again because the moment anyone stops paying
that translation tax, the wiki's terms and the domain experts' terms quietly drift
apart. Don't let this default outlive the audience it was chosen for.
