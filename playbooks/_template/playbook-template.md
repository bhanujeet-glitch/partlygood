# Playbook Template

Canonical PartlyGood template for **reproducible how-to AI workflows** in
management and other non-engineering fields. Every playbook in the publication
follows this structure — the reviewer checks it with
`playbooks/_template/tools/validate_playbook.py`.

Copy the `_template/` folder (or run `scaffold_playbook.py`) and fill each
section. Keep `{{...}}` placeholders replaced with real content. Front matter
below the line is authoritative.

---

## Front matter

```yaml
---
id: <kebab-case-id>            # unique; used in URLs, tags, and citations
title: "<human title>"
brief_id: <kebab-case-brief-id>
content_type: playbook
field: <field id from taxonomy>   # e.g. mgmt, ops, finance, ...
pillars: [<pillar ids>]
topics: [<topic ids>, ai.<...>]
stage: <brief | draft | review | publish>
status: <draft | review | published>
owner: <agent or person>
created: YYYY-MM-DD
updated: YYYY-MM-DD
version: 0.1.0
prompt_versions: {drafter: 1}
---
```

## 1. The outcome

What the reader gets after following this playbook. One paragraph. Answer:
"At the end of this playbook, you will have X, in about Y hours, using Z."

## 2. When to use this (and when not to)

- Use when: (specific situations)
- When not: (situations where the workflow does not fit or costs too much)

## 3. What you need before you start

- Prerequisites (roles, access, data)
- Tools (exact names, versions where it matters)
- Input artifacts (templates, data, prior outputs)

## 4. The workflow

Step-by-step. Numbered, each step ends with the artifact it produces. Where a
step is an AI prompt, the prompt text is included in a code block. Where a
step is a review/approval, name the approver and the check.

### Step 1 — <name>
Inputs → action (include the exact prompt if AI is used) → output artifact.

### Step 2 — <name>
...

## 5. The review gate

Checklist the reviewer (human or agent) runs before this playbook is
publishable. All items must be "yes":

- [ ] Claims are all sourced `[src:ID]` and sources resolve
- [ ] No engineering how-to content
- [ ] Steps are reproducible (artifacts named, prompts exact)
- [ ] Taxonomy ids valid
- [ ] Definition box answers what tool does

## 6. Failure modes and fixes

| symptom | likely cause | fix |
|---|---|---|
| ... | ... | ... |

## 7. What can go wrong / caveats

- Honest limits of the workflow
- When results degrade (data quality, tool changes)
- Red flags that the output should not be trusted

## 8. Sources

List every source used, as `[src:ID]` — URL — title — accessed date — kind
(official/peer-reviewed/primary/practitioner/vendor-docs) — confidence
(high/medium/low).

## 9. Provenance

- Brief: `research/briefs/<brief-id>.md`
- Research plan: `research/plans/<brief-id>.md`
- Source annotations: `research/sources/<brief-id>.sources.json`
- Vault notes: `[[note-ids]]`
- Generator chain and inputs used to create this file.

---

## Review checklist (filled in by reviewer)

| check | status | note |
|---|---|---|
| Outcome stated | | |
| Use-when / not-when present | | |
| Prerequisites complete | | |
| All steps concrete, artifacts named | | |
| Every claim sourced | | |
| No engineering how-to | | |
| Taxonomy valid | | |
| Checklist honest | | |

Reviewer: _name/role_ — Date: _YYYY-MM-DD_ — Verdict: _publish / revise / reject_