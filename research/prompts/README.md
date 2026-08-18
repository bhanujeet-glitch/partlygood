# PartlyGood Prompt Library

Reusable prompts for the AI editorial pipeline. Each prompt is a *slot* with
placeholders (`{{...}}`); the pipeline fills them from the brief, sources, and
draft. Prompts are versioned by filename: `<slot>.prompt.md` carrying a
front-matter `prompt_version`.

Rules:
- Prompts are assets, not chat. Edit them here, review them, commit them.
- Keep every prompt self-contained: include the role, the task, the input
  contract (what `{{...}}` values are), constraints, and the output contract
  (file to produce + exit criteria).
- Boundary reminder: for any draft prompt, the line "This is a management /
  non-engineering workflow" belongs in the role definition.

## Files

- `brief-writer.prompt.md` -- turn research notes into a brief
- `drafter.prompt.md` -- turn brief + sources into a playbook draft
- `researcher.prompt.md` -- turn a brief into a research plan + source list

## The three stages in practice

1. researcher: brief -> research plan, queries, candidate sources
2. brief-writer: research notes -> structured brief
3. drafter: brief + sources -> template-compliant draft

Each stage emits a document into the workspace (research/…, briefs/…,
playbooks/…) and the next stage consumes files, not chat. That keeps the
pipeline reproducible and auditable.