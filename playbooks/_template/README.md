# README — the _template folder

This folder is the canonical AI-workflow playbook template and its tooling.

- `playbook-template.md` — the template itself (what every playbook must contain)
- `tools/scaffold_playbook.py` — scaffolds a new playbook folder from the template
- `tools/validate_playbook.py` — validates an existing playbook folder (front
  matter, taxonomy, template sections, sources)
- `sources-template.json` — source annotation skeleton for a piece

## How to create a new playbook

```bash
python playbooks/_template/tools/scaffold_playbook.py \
  -n meetings-outlook-agenda \
  --title "AI-prepared meeting agendas from Outlook" \
  --field mgmt --topic mgmt.meetings --pillar wf.comms
```

This creates `playbooks/mgmt/meetings-outlook-agenda/` with
`draft.md` and `sources.json` ready to fill. Then write the piece, add
sources, and validate:

```bash
python playbooks/_template/tools/validate_playbook.py playbooks/mgmt/meetings-outlook-agenda/
```

Validation checks (all must pass before review):
1. front matter present with required keys
2. field/pillars/topics resolve against the latest taxonomy
   (`research/taxonomy/taxonomy-v*.json`); run `research/scripts/taxonomy_compat.py`
   when bumping a version.
3. content_type is `playbook` (or explicit override)
4. the template's numbered sections 1.-9. are present
5. every `[src:ID]` marker in the body resolves to an entry in `sources.json`
6. `sources.json` is structurally valid
7. no engineering-topic heading drift

## How to publish

1. Fill `draft.md` fully (all sections).
2. Fill `sources.json` with real annotations.
3. Run the validator; fix issues.
4. Get a review (checklist in the template); flip `stage`/`status`.
5. Rename `draft.md` to `<slug>.md`; commit.