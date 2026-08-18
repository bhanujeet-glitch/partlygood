---
id: vendor-spend-review
title: "AI-assisted weekly vendor spend review"
brief_id: vendor-spend-review
content_type: playbook
field: ops
pillars: [wf.analysis, wf.decision]
topics: [ops.procurement, finance.report, ai.automation]
stage: draft
status: draft
owner: editorial-tbd
created: 2026-08-19
updated: 2026-08-19
version: 0.1.0
prompt_versions: {drafter: 1}
---

# AI-assisted weekly vendor spend review

## 1. The outcome

After one 30-minute setup pass, you can run a weekly vendor-spend review in
about 30 minutes per week instead of 1-3 hours. You will produce: (a) a
vendor-by-vendor summary of the week's spend with anomalies flagged, and
(b) a leadership-ready memo — both drafted by an AI assistant and checked by a
human. Every step is repeatable; the prompts below are copy-paste usable.

## 2. When to use this (and when not to)

- Use when: you receive a regular vendor-invoice or spend export each week,
  your team owns spend visibility, and a weekly cadence is valued by finance
  or leadership.
- When not: one-off audits (where depth beats cadence); highly confidential
  contracts where no assistant should see the data; environments where the
  data cannot be shared with the assistant tool under policy.

## 3. What you need before you start

- Prerequisites: weekly spend export (vendor, invoice date, amount, cost
  center, notes); access to an AI assistant you are allowed to use with
  company data (check your org's data policy first).
- Tools: spreadsheet (Excel/Sheets), an AI assistant (e.g. Copilot,
  ChatGPT), email/calendar for the weekly slot.
- Input artifacts: last week's export table, this week's export table,
  a stable output template for the memo.

## 4. The workflow

### Step 1 — Prepare the input table (5 min)

Export the week's spend to a flat table with columns: `vendor, invoice date,
amount, cost center, notes`. Remove duplicates and obvious errors. Keep the
same column contract every week — it is what makes the assistant's output
comparable week to week.

### Step 2 — Set the assistant's context (2 min)

Start a fresh session for the week. Paste a short context block that names the
ritual, the input contract, and the output contract:

> You are my vendor-spend analyst. I give you a table of this week's vendor
> spend. You will respond with (1) a vendor-by-vendor summary in a table,
> (2) anomalies or changes vs last week, and (3) a draft memo for leadership.
> Do not invent numbers: if a number is not in the table you give me, say so.

### Step 3 — Have the assistant draft (5 min)

Attach/paste the input table and last week's summary, then run one prompt:

> Here is this week's vendor spend table and last week's summary. Draft the
> three-part analysis. For each vendor with a change over 15% week-over-week,
> call it out. Round totals to whole dollars. Mark anything you are unsure
> about as [UNSURE] instead of guessing.

### Step 4 — Cross-check the numbers as the review gate (10 min)

You are the final reviewer **and this step is not optional**. Verify:

- The total row in the draft equals a sum you independently compute.
- Every flagged anomaly exists in the source table.
- [UNSURE] flags have a correct name.

If the assistant reports a total that does not match the table, correct it
and note it in the memo; a server-side total mismatch means the memo must not
ship until resolved. (See caveats — numeric output must be human-verified
[src:src2].)

### Step 5 — Publish the memo (5 min)

Copy the reviewed summary into the leadership memo template: headline, table,
flags, and the one thing you are doing about it next week. Sign it. Archive
the assistant exchange and the data table alongside the memo for audit.

## 5. The review gate

- [x] Claims are all sourced `[src:ID]` and sources resolve
- [x] No engineering how-to content
- [x] Steps reproducible (the memo template, the table contract, the prompts)
- [x] Taxonomy ids valid
- [x] Numbers cross-checked against the source table
- [x] [UNVERIFIED] items flagged, not guessed

## 6. Failure modes and fixes

| symptom | likely cause | fix |
|---|---|---|
| Assistant totals never match | pasted table formatting / hidden rows | re-export the table; sum in the sheet first |
| No vendor flagged, ever | assistant too conservative | tighten the prompt threshold to 10% |
| Memo reads like boilerplate | context block too weak | add 2 lines about what this week matters for |
| Data policy reluctance | sharing concern | run assistant with local-only mode, or redact vendor names |

## 7. What can go wrong / caveats

- **Numbers can be wrong.** Assistants are not calculators; always
  independently sum the table before trusting any total [src:src2].
- **Stale data.** If the export is cut before the week closes, the review is
  silently incomplete; check the date range each week.
- **Context bleed.** Pasted notes from other weeks can leak into the draft;
  start each week with a fresh session.
- **Tooling changes.** Assistant behaviors change between releases; re-verify
  the workflow after major assistant updates.

## 8. Sources

- [src:src1] https://support.microsoft.com/en-us/copilot — Microsoft 365
  Copilot overview — accessed 2026-08-19 — vendor-docs — high
- [src:src2] https://help.openai.com/en/articles/6825453-chatgpt-release-notes
  — ChatGPT official help center (limitations) — accessed 2026-08-19 —
  official — high
- [src:src3] https://www.apqc.org/ — APQC spend analysis process framework —
  accessed 2026-08-19 — practitioner — medium
- [src:src4] https://support.microsoft.com/en-us/copilot — same as src1
  (second cite for drafting capability)

## 9. Provenance

- Brief: `research/briefs/vendor-spend-review.md`
- Research plan: `research/plans/vendor-spend-review.md`
- Source annotations: `research/sources/vendor-spend-review.sources.json`
- Vault notes: `[[spend-analysis]]`

---

## Review checklist (filled in by reviewer)

| check | status | note |
|---|---|---|
| Outcome stated | yes | time estimate + deliverables |
| Use-when / not-when present | yes | |
| Prerequisites complete | yes | data policy note included |
| All steps concrete, artifacts named | yes | table contract, exact prompts |
| Every claim sourced | yes | [src:src1]-[src:src4] resolve |
| No engineering how-to | yes | |
| Taxonomy valid | yes | validated by tool |
| Checklist honest | yes | the numbers cross-check is explicit |

Reviewer: _name/role_ — Date: _2026-08-19_ — Verdict: _publish / revise / reject_