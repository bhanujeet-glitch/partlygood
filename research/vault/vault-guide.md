# PartlyGood Research Vault Guide

The vault is PartlyGood's knowledge base: curated, versioned, cross-referenced
notes researchers and writers can build on. It is NOT a dump — everything that
lands here has passed the source bar and carries provenance.

## Directory layout

```
research/vault/
  domains/<field>/<note>.md     notes by field (mgmt, ops, finance, ...)
  working/<brief-id>/           scratch for an active piece, never published
  glossary.md                   shared terminology
  index.md                      browsable index (updated on commit)
```

## Note convention

Every note is markdown with front matter:

```yaml
---
id: <kebab-case>
title: ...
field: <field id>
topics: [<topic ids>]
created: YYYY-MM-DD
updated: YYYY-MM-DD
status: draft | reviewed
sources: [<source ids from research/sources/>]
---
```

Body rules:
- One idea per note; link related notes with `[[note-id]]`.
- Claims carry `[src:ID]` markers; no bare claims.
- Prefer tables/lists; keep notes under 400 words unless a survey note.

## Working notes

`working/<brief-id>/` holds scratch material for an active brief: search
dumps, transcripts, half-thoughts. It is exempt from the curation bar (it is
scratch) but it must not be cited in published pieces; published pieces cite
only `sources/` annotations and `domains/` notes.

## Taxonomy of notes

- `domain` notes: what we know in a field (evergreen, reviewed)
- `claim` notes: a single citable claim with provenance
- `tool` notes: how a specific AI tool behaves in management workflows
- `process` notes: how we do things (editorial, tooling)

## House rules

1. Anything claiming a fact gets a `[src:ID]`.
2. Notes get reviewed before status flips to `reviewed`.
3. Dead links (`[[missing]]`) are fixed on commit; the index is regenerated
   by `research/scripts/vault_index.py` (see below).
4. Never store secrets in the vault.

## Automation

`python research/scripts/vault_index.py` regenerates `research/vault/index.md`
from the notes' front matter and fails on missing `[[link]]` targets.
Run it before committing vault changes.