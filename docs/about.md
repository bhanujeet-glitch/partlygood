---
title: "How PartlyGood works: editorial process"
type: canonical
field: cross-cutting
status: published
created: 2026-08-19
updated: 2026-08-19
slug: about
summary: "The editorial process behind PartlyGood: idea to published playbook, with gates and ownership."
tags: [editorial, process]
quality:
  checked_at: ""
  checks_passed: 0
---

# How PartlyGood works

PartlyGood is a small, fast editorial operation. The pipeline is built so
that one person (or one agent) can take a piece from idea to publication
with quality gates at every step.

## The pipeline

1. **Idea** — an editorial calendar and content pillars owned by the CEO
   shape what we write.
2. **Scaffold** — `python scripts/new_article.py <type> "<title>"` creates
   a versioned draft from a template, with front matter, slug, and dedup
   guard.
3. **Draft** — written as plain Markdown in `docs/<field>/`.
4. **Quality gate** — `make check` runs structural validation, the quality
   checks (front matter, length, AI-usage sections, sources,
   placeholder scan, taxonomy conformance, freshness), and a strict build.
5. **Review** — issue-tracker review; a human reviewer approves.
6. **Publish** — merge to main; CI rebuilds the site; the piece's front
   matter flips to `published`.

## Quality standards

- Every piece has complete front matter (title, type, field, status,
  dates, slug, quality block).
- Playbooks carry an **AI usage** statement — exactly what the AI does,
  where it does not add value, and what a human must verify.
- Factual claims about tools and models are sourced with URLs.
- Playbooks are reproducible: prompts, inputs, checks, and a run-it
  section.
- No placeholders (TODO/TBD) reach the build.

## Out of scope

Code and software-engineering how-to content is excluded by charter.
Educational material may reference tools, but never at the level of
building software.

## The team

- **CEO** — direction, editorial calendar, content pillars.
- **Founding Engineer** — publishing platform, editorial pipeline,
  infrastructure, playbook production.
- **Research & Playbook** — research tooling, the playbook template,
  and the sample playbook (see PAR-4).