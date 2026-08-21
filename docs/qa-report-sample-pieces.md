---
title: "Editorial QA report — sample playbooks (PAR-12)"
type: canonical
field: cross-cutting
status: published
created: 2026-08-21
updated: 2026-08-21
slug: qa-report-sample-pieces
summary: "Quality-assurance results for the two published sample playbooks: meeting minutes and vendor spend review."
tags: [qa, editorial, samples]
quality:
  checked_at: "2026-08-21"
  checks_passed: 9
---

# Editorial QA report — published sample pieces

Corresponds to issue **PAR-12** (Editorial QA pass on published sample pieces).
Reviewed against the editorial standards in [How PartlyGood works](../about.md)
and the playbook template contract in [samples](../samples/index.md).

## Scope

Two published playbooks reviewed:

- `docs/management/drafting-meeting-minutes-with-ai.md` (management)
- `docs/operations/vendor-spend-review.md` (operations)

## What was checked

1. **AI-usage claim metering** — every playbook must meter AI work against
   human work: an explicit *AI usage* statement, at least one
   human-verification gate, and zero overreaching "AI decides/owns" claims.
2. **Sources** — every factual claim about a tool/model carries a source URL;
   every source resolves; sources are annotated in the colocated
   `sources.json`.
3. **Report metrics** — `report.json` regenerated with per-piece `ai_meter`
   and `sources_verified` records.
4. **Quality bar** — structural validation, the 9-point quality gate, and a
   strict build must all pass.

## Result per piece

| Piece | AI meter | Sources | Gate | Verdict |
|---|---|---|---|---|
| Meeting minutes | statement ✓ · 1 human gate ✓ · 0 overstated ✓ | 1/1 verified | 9/9 | **PASS** |
| Vendor spend review | statement ✓ · 1 human gate ✓ · 0 overstated ✓ | 4/4 verified | 9/9 | **PASS** |

### Meeting minutes (`drafting-meeting-minutes-with-ai.md`)

- **AI usage metered:** the blockquote at the top names what AI does
  (transcription + draft) and what the human owns (verify, correct, decide).
  Includes an explicit human-verification step (step 2 review + step 3 action
  item pass). No overstated "AI decides/owns" language.
- **Sources:** 1 URL declared; now `https://support.microsoft.com/en-us/word/transcribe-your-recordings`
  (the prior `.../office/transcribe-your-meetings-...` URL was a 404). Resolves
  200.
- **Sentence-level fixes:** none required beyond the source URL.

### Vendor spend review (`vendor-spend-review.md`)

- **AI_usage metered:** Top AI-usage statement names what AI drafts and what
  the human cross-checks; Step 4 is an explicit human verification gate
  ("You are the final reviewer. This step is not optional."). No overstated
  claims.
- **Sources:** 4 declared. One (Copilot privacy, previously
  `learn.microsoft.com/en-us/copilot/privacy-and-protected-material`) was a
  404; replaced with the canonical
  `https://learn.microsoft.com/en-us/microsoft-365-copilot/microsoft-365-copilot-privacy`
  (200). APQC resolves (200 via GET), OpenAI help center resolves. All 4
  verified reachable.
- **Sentence-level fixes:** the dead source URL was the only content change.

## Fixes published

- `docs/management/drafting-meeting-minutes-with-ai.md` — source URL fix.
- `docs/operations/vendor-spend-review.md` — source URL fix.
- `playbooks/ops/vendor-spend-review/sources.json` — corrected src4 URL/title.
- `playbooks/mgmt/meeting-agenda-outlook/sources.json` — annotated sources
  now present for the meeting-minutes piece.
- `scripts/quality_checks.py` — added the `ai_usage_meter` check (the metering
  gate).
- `scripts/quality_report.py` — report now emits per-piece `ai_meter` and
  `sources_verified` records; adds `--verify-sources` network verification.
- `report.json` — regenerated with the new metrics.

## Re-run

```bash
python scripts/quality_checks.py --all
python scripts/quality_report.py --verify-sources
python scripts/validate_content.py --strict
python -m mkdocs build --strict
```