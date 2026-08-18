---
title: "PartlyGood content taxonomy"
type: canonical
field: cross-cutting
status: published
created: 2026-08-19
updated: 2026-08-19
slug: taxonomy
summary: "Fields, content types, status model, and naming conventions for the PartlyGood publication."
tags: [taxonomy, standards]
quality:
  checked_at: ""
  checks_passed: 0
---

# PartlyGood content taxonomy

Every content piece lives in `docs/<field>/<slug>.md` with YAML front
matter. This document is the single source of truth for fields, content
types, status model, and naming conventions.

## Fields (directory structure)

| Field         | Directory     | Scope |
|---------------|---------------|-------|
| Management    | `management`  | Leading teams, planning, delegation, meetings, performance, change |
| Operations    | `operations`  | Processes, workflows, vendors, analytics, project delivery |
| Finance       | `finance`     | Budgeting, FP&A, reporting, forecasting, close processes |
| Marketing     | `marketing`   | Content, campaigns, customer research, analytics |
| Cross-cutting | `cross-cutting` | AI workflows shared across fields (prompt frameworks, evaluation, tooling patterns) |

Software engineering / coding is intentionally EXCLUDED. Educational
material that happens to mention code (e.g., an AI tool suggestion) must
stay at the level a manager can use — no build instructions for software.

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
product: false            # true when the piece was produced by the pipeline itself
quality:
  checked_at: YYYY-MM-DDTHH:MM:SSZ
  checks_passed: 8        # must equal the checks that ran
```

Additional keys allowed: `summary`, `tags`, `audience`, `difficulty`
(beginner|intermediate|advanced), `reviewers`, `sources`.

## Naming conventions

- Slugs: kebab-case, ASCII, descriptive (`drafting-meeting-minutes`).
- One idea per piece. Playbooks under ~3 000 words, how-tos under ~1 500.
- Every piece must reference its sources when it makes factual claims
  about tools, pricing, or model behavior.

## Sample playbook structure (per PAR-4 template)

The canonical sample playbook lives at `docs/samples/`. All field
playbooks follow that structure so the pipeline can validate them
mechanically.