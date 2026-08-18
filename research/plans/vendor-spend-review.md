# Research Plan — AI-assisted vendor spend review (weekly ritual)

- brief_id: vendor-spend-review
- status: research -> brief (this plan feeds the brief)
- created: 2026-08-19

## Research questions (by importance)

1. What does a best-practice weekly vendor spend review look like for a
   mid-size company (what data, what decisions)? -> practitioner sources,
   APQC-style process guidance; vendor expense-management docs.
2. Which AI assistant capabilities apply to summarizing/spotting spend
   anomalies (chat/analysis in the office suite or an AI assistant app)?
   -> vendor docs (Microsoft 365 Copilot, ChatGPT), official.
3. What are the known failure modes of AI-generated spend summaries
   (hallucinated totals, stale data, access scope)? -> AI vendor safety/docs,
   practitioner write-ups.
4. What checks keep the output trustworthy (human review gate, cross-check
   against source tables)? -> editorial/first-party from tooling design; cite
   vendor docs on grounding.

## Candidate sources / queries

- OpenAlex: query `"spend analysis" AND procurement` (title/abstract)
- Vendor docs: Microsoft 365 Copilot overview; OpenAI ChatGPT capabilities
- Practitioner: APQC process standards; CFO/FP&A practitioner forums

## Good-enough for each

- Q1: at least one process reference + one practitioner description of the ritual
- Q2: official vendor capability page describing the feature
- Q3: vendor or practitioner description of hallucination/citation limits
- Q4: our own review-gate design + vendor grounding description

## Boundary

This is a finance/ops management ritual. No code, no API keys, no scripts to
run — the AI assistant is used as a management tool.