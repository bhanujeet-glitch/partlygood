---
title: "AI-assisted weekly vendor spend review"
type: playbook
field: operations
status: published
created: 2026-08-19
updated: 2026-08-20
slug: vendor-spend-review
summary: "Run a weekly vendor-spend review in ~30 minutes instead of 1-3 hours, with AI drafting the summary and anomaly flags and humans owning the numbers."
tags: [vendor, procurement, spend-analysis, finance]
audience: "Operations managers, procurement leads, finance analysts"
difficulty: beginner
sources:
  - https://support.microsoft.com/en-us/copilot
  - https://help.openai.com/en/articles/6825453-chatgpt-release-notes
  - https://www.apqc.org/
  - https://learn.microsoft.com/en-us/copilot/privacy-and-protected-material
quality:
  checked_at: "2026-08-20"
  checks_passed: 0
---

# AI-assisted weekly vendor spend review

> **AI usage:** AI drafts the vendor-by-vendor summary, flags anomalies, and
> produces a leadership-ready memo. A human (you) cross-checks every number,
> verifies the source data, and signs the final memo. AI does not decide
> what is material; people do.

## What you will do

- Run a weekly vendor-spend review in about 30 minutes instead of 1-3 hours.
- Produce a vendor-by-vendor summary with anomalies flagged.
- Produce a leadership-ready memo reviewed by a human.
- Keep the workflow repeatable: the same inputs, prompts, and output template
  every week.

## Before you start

- A weekly spend export (vendor, invoice date, amount, cost center, notes).
- Access to an AI assistant you are allowed to use with company data
  (check your org's data policy first).
- Last week's summary for comparison.
- A stable output template for the memo.

## Steps

### 1. Prepare the input table (5 min)

Export the week's spend to a flat table with columns: `vendor, invoice date,
amount, cost center, notes`. Remove duplicates and obvious errors. Keep the
same column contract every week — it is what makes the assistant's output
comparable week to week.

### 2. Set the assistant's context (2 min)

Start a fresh session for the week. Paste a short context block:

> You are my vendor-spend analyst. I give you a table of this week's vendor
> spend. You will respond with (1) a vendor-by-vendor summary in a table,
> (2) anomalies or changes vs last week, and (3) a draft memo for leadership.
> Do not invent numbers: if a number is not in the table you give me, say so.

### 3. Have the assistant draft (5 min)

Attach/paste the input table and last week's summary, then run:

> Here is this week's vendor spend table and last week's summary. Draft the
> three-part analysis. For each vendor with a change over 15% week-over-week,
> call it out. Round totals to whole dollars. Mark anything you are unsure
> about as [UNSURE] instead of guessing.

### 4. Cross-check the numbers (10 min)

You are the final reviewer. This step is not optional. Verify:

- The total row in the draft equals a sum you independently compute.
- Every flagged anomaly exists in the source table.
- [UNSURE] flags have a correct name.

If the assistant reports a total that does not match the table, correct it
and note the discrepancy in the memo. A total mismatch means the memo must
not ship until resolved.

### 5. Publish the memo (5 min)

Copy the reviewed summary into the leadership memo template: headline, table,
flags, and the one thing you are doing about it next week. Sign it. Archive
the assistant exchange and the data table alongside the memo for audit.

## Review checklist

- [ ] Numbers independently summed and verified against source table
- [ ] Every flagged anomaly exists in the source data
- [ ] [UNSURE] items are flagged, not guessed
- [ ] Data policy: assistant access is permitted for this data
- [ ] Date range covers the full week

## Failure modes and fixes

| Symptom | Likely cause | Fix |
|---|---|---|
| Assistant totals never match | Pasted table formatting / hidden rows | Re-export the table; sum in the sheet first |
| No vendor flagged, ever | Assistant too conservative | Tighten the prompt threshold to 10% |
| Memo reads like boilerplate | Context block too weak | Add 2 lines about what this week matters for |
| Data policy reluctance | Sharing concern | Run assistant with local-only mode, or redact vendor names |

## What can go wrong

- **Numbers can be wrong.** Assistants are not calculators; always
  independently sum the table before trusting any total.
- **Stale data.** If the export is cut before the week closes, the review is
  silently incomplete; check the date range each week.
- **Context bleed.** Pasted notes from other weeks can leak into the draft;
  start each week with a fresh session.
- **Tooling changes.** Assistant behaviors change between releases; re-verify
  the workflow after major assistant updates.

## Run it

- **Time:** ~30 minutes per week (`10 min` prep, `5 min` AI drafting,
  `10 min` cross-check, `5 min` publish)
- **Repeat:** every week
- **Store:** final memo in your reporting tool; assistant exchange and data
  table archived alongside

## Related

- Editorial standards: [How PartlyGood works](../about.md)
- Taxonomy: [fields and content types](../taxonomy.md)
- Management playbook: [Drafting meeting minutes with AI](../management/drafting-meeting-minutes-with-ai.md)