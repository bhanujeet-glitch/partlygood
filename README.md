# PartlyGood — publication platform & editorial pipeline

PartlyGood is a publication of practical knowledge for using AI in
management workflows and other non-engineering fields: management,
operations, finance, marketing. Code and software-engineering content is
explicitly out of scope.

## What this repository contains

- `docs/` — the publication content, organized by field (see Taxonomy).
  Each doc is Markdown with YAML front matter (title, type, field, status,
  dates, quality-scan results).
- `mkdocs.yml` — MkDocs Material site configuration (navigation, taxonomy,
  SEO, analytics hooks).
- `scripts/` — the editorial pipeline: scaffold, validate, quality gate,
  build.
- `templates/` — content templates (playbook, how-to, explainer).
- `.github/workflows/ci.yml` — continuous quality + build pipeline
  (versioned, reviewable, reproducible).
- `Makefile` — the one command you need: `make check` or `make publish`.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt

make check                     # validate + quality + build (the gate)
make serve                     # local preview on http://127.0.0.1:8000
make publish                   # strict build into site/
```

## Editorial workflow (the pipeline)

New piece → scaffold → draft → quality gate → review → publish.

```bash
# 1. Scaffold a new piece (automated template, dedup check)
python scripts/new_article.py "how-to" "Drafting meeting minutes with an LLM"

# 2. Write the piece in docs/<field>/<slug>.md

# 3. Quality gate (must pass before publish)
python scripts/validate_content.py --strict   # structure, links, taxonomy
python scripts/quality_checks.py --all        # front matter, length, AI-use claims

# 4. Review & publish
make publish
```

Every step is versioned in git. The issue tracker and this repo are the
source of truth; the site build is an artifact of `docs/`.

## Taxonomy (content types & fields)

- Types: `playbook`, `how-to`, `explainer`, `playbook`-sample
- Fields: `management`, `operations`, `finance`, `marketing`, `cross-cutting`

See `docs/taxonomy.md` for the full taxonomy, status model, and
naming conventions.

## Sites / artifacts

- Built site: `site/` (generated, never committed)
- Issue tracker: company board (PAR-* issues)