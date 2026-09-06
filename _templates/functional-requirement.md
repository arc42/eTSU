---
id: FR-NNN
type: functional-requirement
title: <Name>         # epic/feature: noun phrase w/ clear outcome; story: verb + object (naming convention A, ADR-0015)
status: draft         # draft | review | accepted | deprecated
created: {{date}}
updated: {{date}}
sources: []
related: []           # [[UC-...]], [[QR-...]], [[CON-...]], [[GLO-...]], [[STK-...]]
tags: [functional-requirement]
stereotype: story     # epic | feature | story  (req42 Product Backlog level)
parent: []            # [[FR-...]] coarser item(s): story→feature→epic. Multiple allowed ⇒ graph, not just tree.
priority: Should      # Must | Should | Could | Won't  ([[MoSCoW]])
release: backlog      # release/milestone tag — story-map swim-lane
lane: backbone        # backbone | platform | display  (story-map lane; default backbone; ADR-0017)
order:                # integer: narrative order WITHIN the lane (left→right within backbone; sequence within platform/display)
goal: []              # [[GOAL-...]] one or more goals this item serves; [] = explicit Enabler (e.g. Plattform-Schiene). Projection source for the Goal-Coverage matrix (ADR-0018).
---

# {{title}}

<!-- One type, three stereotypes. Page order is fixed for ALL stereotypes:
     Story first (the punchy formulation), then the body, then Hierarchy, Open points,
     and finally Historie at the very end. The Epic→Feature→Story hierarchy is wikilinks
     (`parent`), and a story map is just a projection over it ([[story-mapping]]) — hence
     order + priority + release. Title grammar (convention A, ADR-0015): epic/feature =
     noun phrase naming an outcome (e.g. „Saisonvorbereitung"); story = verb + object
     (active goal, e.g. „Wettkampf absagen"). Title language: see ADR-0005 for this
     wiki's ubiquitous-language decision. -->

## Story
<!-- HEADING is stereotype-specific: for `stereotype: epic` rename it to
     "## Epic: Kurzbeschreibung"; feature/story keep "## Story". -->

<!-- The concise formulation of this item — every stereotype gets one, up top.
     story: full user-story sentence (> follows [[user-story-format]], [[INVEST]]).
     epic/feature: the same shape at coarser altitude — who wants what, and why. -->
Als [[STK-...]] **&lt;Rolle&gt;** will ich **&lt;Ziel&gt;**, damit **&lt;Nutzen&gt;**.

**Acceptance criteria.**  — only when `stereotype: story`  <!-- follows [[acceptance-criteria]] -->

- **Given** &lt;Kontext&gt; **when** &lt;Aktion&gt; **then** &lt;beobachtbares Ergebnis&gt;.

**PROBLEM / GOAL**  — only when `stereotype: epic | feature`

<the user + business problem this addresses>

**Success metric(s).**

<how we'll know it worked — frame via [[PAM]] / [[SMART]]>

**Scope.** in: <…> · out: <…>

## Hierarchy

- **Parent:** see `parent:` (none for an epic).
- **Children:** <coarser items list finer ones here, or rely on `parent:` backlinks>

> [!note] Open points
> <ambiguities, missing children, untestable criteria → raise as [[ISS-...]]>

## Historie

<!-- Optional, always LAST: provenance / reframing notes as blockquotes, so the active
     content stays at the top. Omit the heading if there is nothing to record. -->

<!-- Estimate/owner are intentionally NOT modelled here — that's the tracker's (JIRA) job.
     The wiki keeps requirement-level facts: priority, release, order, hierarchy. -->
