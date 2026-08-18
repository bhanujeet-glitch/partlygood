# Research Brief — AI-assisted weekly vendor spend review

## Brief

- id: vendor-spend-review
- title: "AI-assisted weekly vendor spend review"
- content_type: playbook
- field: ops
- pillars: [wf.analysis, wf.decision]
- topics: [ops.procurement, finance.report, ai.automation]
- status: brief
- owner: editorial-tbd
- created: 2026-08-19
- updated: 2026-08-19

## What the piece answers

Team leads and procurement managers spend 1-3 hours a week manually combining
vendor invoices, flagging odd movements, and writing a summary for leadership.
This playbook shows how to cut that to ~30 minutes with an AI assistant: feed
the assistant the week's spend data, get a vendor-by-vendor summary with flags,
review and correct it, and produce the leadership memo. The reader walks away
with a repeatable checklist, exact prompts, and a human review gate.

## Audience

Procurement lead / finance ops manager / head of a cost center at a 50-500
person company. Comfortable with spreadsheets and email, not a developer.
Wants fewer hours of grunt work and a more consistent weekly ritual.

## Key claims to verify

1. A repeatable weekly ritual can be reduced from hours to ~30 minutes with an
   assistant doing draft summarization + anomaly flagging.
2. Vendor data prepped as a plain table (vendor, invoice date, amount, cost
   center, notes) is enough input for the assistant to draft useful analysis.
3. Assistant outputs on numbers must be cross-checked against the source table
   (hallucination/citation limits).
4. A human review gate is required before the memo goes to leadership.
5. The ritual needs the same cadence and input contract every week to stay
   reliable.

## Sources / starting points

- src1: Microsoft 365 Copilot overview (official, vendor-docs) — capability
  description: drafting/summarizing grounded in company data.
- src2: ChatGPT homepage/help (official) — assistant capabilities.
- src3: APQC process guidance (practitioner) — spend/procurement process
  context.
- (OpenAlex litsearch appended under research/literature/ for literature.)

## Research notes

- Prompted output must be treated as a draft, not a final product.
- The "same input contract every week" is what makes the ritual reproducible.

## Success criteria

- Reader can run the weekly loop in ~30 minutes after one setup pass.
- Every prompt in the piece is copy-paste usable.
- Honest caveats about number accuracy and assistant limits.

## Status log

- 2026-08-19 — created; research open (example/dogfood piece for PAR-4).