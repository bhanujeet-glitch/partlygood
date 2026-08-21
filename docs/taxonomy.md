---
title: "PartlyGood content taxonomy"
type: canonical
field: cross-cutting
status: published
created: 2026-08-19
updated: 2026-08-21
slug: taxonomy
summary: "Fields, content types, status model, naming conventions, cross-cutting topics, and governance for the PartlyGood publication."
tags: [taxonomy, standards, governance]
version: 1.1
quality:
  checked_at: ""
  checks_passed: 0
---

# PartlyGood content taxonomy

Every content piece lives in `docs/<field>/<slug>.md` with YAML front
matter. This document is the single source of truth for fields, content
types, status model, naming conventions, cross-cutting topics, and topic
governance.

Machine-readable taxonomy and change history live at
`research/taxonomy/taxonomy-v<version>.json` (currently **v1.1**).

## Fields (directory structure)

| Field         | Directory     | Scope |
|---------------|---------------|-------|
| Management    | `management`  | Leading teams, planning, delegation, meetings, performance, change |
| Operations    | `operations`  | Processes, workflows, vendors, analytics, project delivery |
| Finance       | `finance`     | Budgeting, FP&A, reporting, forecasting, close processes |
| Marketing     | `marketing`   | Content, campaigns, customer research, analytics |
| Cross-cutting | `cross-cutting` | AI workflows shared across fields (prompt frameworks, evaluation, data, vendors, security, tooling patterns) |

Software engineering / coding is intentionally EXCLUDED. Educational
material that happens to mention code (e.g., an AI tool suggestion) must
stay at the level a manager can use — no build instructions for software.

## Cross-cutting dimension (v1.1)

The `ai.*` topics are a **cross-cutting dimension**: they apply to every
field and can be tagged on any piece regardless of its primary field.
The canonical list lives in the `cross_cutting.topics` section of the
taxonomy file. They are exposed on the
[Cross-cutting index](cross-cutting/index.md).

| Cross-cutting topic   | Scope |
|-----------------------|-------|
| `ai.prompting`        | Framing prompts for business tasks |
| `ai.agents`           | Using agents / multi-step AI workflows |
| `ai.automation`       | Automating recurring workflows |
| `ai.evaluation`       | Verifying and evaluating AI output |
| `ai.safety`           | Safe defaults, failure handling, human review |
| `ai.adoption`         | Getting teams to adopt AI |
| `ai.data`             | Data preparation & hygiene (new in v1.1) |
| `ai.documents`        | Document drafting & operations (new) |
| `ai.reporting`        | Reporting & dashboards (new) |
| `ai.vendors`          | AI tool & vendor selection (new) |
| `ai.security`         | Privacy, permissions & data handling (new) |

## Content types

- **playbook** — a reproducible step-by-step procedure for a recurring
  workflow, with inputs, outputs, quality checks, and a "run it" section.
- **how-to** — a focused single-workflow guide (shorter than a playbook).
- **explainer** — foundation knowledge about using AI in a field
  (concepts, options, evaluation).
- **canonical** — house documents (taxonomy, editorial standards) rather
  than field content.

## Status model

`draft` → `in_review` → `published` → `updated` → `retired`

Retired pieces move under `docs/_retired/` and keep their slug to avoid
link rot; the front matter `status: retired` is set.

## Front matter (required for every piece)

```yaml
title: <Human title>
type: playbook | how-to | explainer | canonical
field: management | operations | finance | marketing | cross-cutting
status: draft | in_review | published | updated | retired
created: YYYY-MM-DD
updated: YYYY-MM-DD
slug: <kebab-case>
product: false            # true when produced by the pipeline itself
quality:
  checked_at: YYYY-MM-DDTHH:MM:SSZ
  checks_passed: 8        # must equal the checks that ran
```

Additional keys allowed: `summary`, `tags`, `audience`, `difficulty`
(beginner|intermediate|advanced), `reviewers`, `sources`, and `topics`
(array of topic ids) for pieces that want to declare granular topics.

## Topic governance

Who adds/merges topics, versioning, and the update process are documented in
`research/taxonomy/GOVERNANCE.md`. Summary:

- **Additive only in MINOR releases.** New topics may be proposed by any
  publisher/engineer via an issue; the Taxonomy owner (Founding Engineer)
  approves; the CEO owns editorial intent and may veto.
- **Breaking changes (remove/rename/merge) are MAJOR releases** that require
  re-tagging published pieces and a published notice first.
- **Versioning** is SemVer-style: each change ships as a new
  `taxonomy-v<MAJOR.MINOR>.json`, and the previous file stays on disk.
- **Backward compatibility** is enforced by
  `research/scripts/taxonomy_compat.py`, which fails the build if any
  existing topic id is dropped.

## Sample playbook structure (per PAR-4 template)

The canonical sample playbook lives at `docs/samples/`. All field
playbooks follow that structure so the pipeline can validate them mechanically.