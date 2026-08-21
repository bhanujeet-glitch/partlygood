# PartlyGood Taxonomy Governance

Applies to `research/taxonomy/taxonomy-v*.json` and to every piece that
references a topic id (front matter `topics:` / `field:`).

Status: active since taxonomy v1.1 (2026-08-21).

## 1. Versioning

Taxonomy files are versioned `taxonomy-v<MAJOR.MINOR>.json`. Version numbers
are SemVer-style:

- **MINOR (e.g. 1.0 → 1.1):** additive only — new topics, new metadata, new
  cross-cutting flags, new governance rules. Existing topic ids are never
  removed, renamed, or repurposed.
- **MAJOR (e.g. 1.x → 2.0):** any removal, rename, or repurposing of an
  existing topic id, or a change to the meaning of the `fields` / `pillars`
  sets.

Every change ships as a **new file**; the previous file stays on disk so that
any tool can diff versions and prove backward compatibility.

## 2. Backward compatibility

- Existing topic ids are never removed or renamed in a MINOR release.
- A new topic may be added only if no published piece already uses that id
  for a different meaning.
- When a topic id must change or merge, that is a MAJOR change and requires
  an editorial migration: re-tag affected pieces, update the changelog, and
  publish a notice before the merge lands.
- `scripts/taxonomy_compat.py` compares the new taxonomy against the previous
  one and fails the build if any existing topic id disappeared.

## 3. Roles

| Role               | Who            | Powers |
|--------------------|----------------|--------|
| Taxonomy owner     | Founding Engineer | Approves topic additions/merges, owns the loader and compat tooling. |
| Editorial intent   | CEO            | Sets direction, may veto any topic addition/merge. |
| Proposers          | Any publisher/engineer | Open an issue proposing a topic. |

## 4. Adding a topic (MINOR)

1. Open a taxonomy issue naming:
   - the topic id (`<field>.<name>`, kebab-case),
   - the field it belongs to (or `cc` for cross-cutting),
   - a one-line scope definition,
   - for cross-cutting topics, the fields it applies to.
2. The Taxonomy owner reviews; the CEO may veto for editorial intent.
3. Ship a new `taxonomy-v<minor>.json`; run `taxonomy_compat.py`.
4. Merge on green; record the change in the changelog section of the new file.

## 5. Merging / removing a topic (MAJOR)

1. Decision on the issue with a named Taxonomy owner and CEO visibility.
2. Choose the surviving id: keep the most-published id, or redirect content.
3. Re-tag published pieces, update the changelog, publish a notice.
4. Only then ship the MAJOR file and migrate the loader.

## 6. Update process checklist (for any version bump)

1. Open (or reuse) a taxonomy issue describing the change.
2. Create the new `taxonomy-v<MAJOR.MINOR>.json` (copy prior file, edit).
3. Run `python research/scripts/taxonomy_compat.py` — must pass.
4. Update `research/scripts/taxonomy.py` if the latest-file resolution changed.
5. Update `docs/taxonomy.md` and any references (prompts, templates).
6. Run `python scripts/validate_content.py --strict` and
   `python scripts/quality_checks.py --all` — must pass.
7. Merge on green. 8. Note the version in the issue and the changelog.

## 7. Fields vs cross-cutting

- `fields` are the content directories / domains (`mgmt, ops, finance,
  marketing, sales, hr-domain, strategy, cs, legal, research`).
- `cross_cutting` (`cc`) is the shared AI dimension. Cross-cutting topics
  (`ai.*`) can be attached to any piece regardless of its primary field, and
  appear in the docs `cross-cutting/` section.

Cross-cutting topics must stay general: if a topic only makes sense inside
one field, it belongs to that field.