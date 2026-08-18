# PartlyGood Editorial Workflow

The repeatable pipeline: research -> brief -> draft -> review -> publish.
Every piece moves through the same gates; every gate leaves a file in the
workspace. Nothing is published from chat.

## 1. Research

- Input: a topic (from the roadmap) or an open question (from the reader).
- Output: `research/plans/<brief-id>.md` + `research/sources/<brief-id>.sources.json`.
- Tooling: `litsearch.py` (OpenAlex), `sources.py` (annotations), the vault, vendor docs.
- Exit: every question has a source or a query; no engineering drift.

## 2. Brief

- Input: research plan + candidate sources.
- Output: `research/briefs/<brief-id>.md` (from `_template.md`).
- Exit: brief is the contract; claims to verify are numbered 1..n.

## 3. Draft

- Input: brief + sources + playbook template.
- Output: `playbooks/<field>/<slug>/draft.md` (+ `sources.json` copy).
- Produced by the `drafter.prompt` slot; template compliance is checked by
  `validate_playbook.py --mode draft`.

## 4. Review (the gate)

- A reviewer (human or agent) runs the template's Review checklist against the
  draft. Checks:
  - claims -> sources coverage (every [src:ID] resolves; every claim has one)
  - boundary: no engineering how-to content
  - reproducibility: steps are concrete, artifacts named
  - taxonomy validity (via `validate_playbook.py`)
- Output: `review.md` in the piece folder + `stage: review` in front matter.
  Publishable when checklist is all yes.

## 5. Publish

- Output: `playbooks/<field>/<topic>/<slug>.md` (final), `stage: publish`,
  canonical URL assignment (SEO) in the platform layer.
- What publishes: the playbook file + its sources.json + links to relevant
  vault notes.

## Per-piece records

Each piece folder keeps: brief (link), sources.json, draft.md, review.md,
final.md. Everything is git-committed as it moves through stages.

## The automation contract

- Prompts live in `research/prompts/` and are versioned (front matter `prompt_version`).
- Scripts in `research/scripts/` are stdlib-only, exit-code-bearing, and idempotent.
- Validation is run at every gate; nothing proceeds on a failing validator.