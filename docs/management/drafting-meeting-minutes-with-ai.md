---
title: "Drafting meeting minutes with AI"
type: playbook
field: management
status: published
created: 2026-08-19
updated: 2026-08-19
slug: drafting-meeting-minutes-with-ai
summary: "Turn a meeting recording into verified minutes and action items in under 30 minutes, with AI handling transcription and drafting and humans owning decisions."
tags: [meetings, minutes, transcription]
audience: "Managers, team leads, and executive assistants"
difficulty: beginner
sources:
  - https://support.microsoft.com/en-us/office/transcribe-your-meetings-4494d655-2c9c-4b2b-8f2e-9f4c1e4f3de1
quality:
  checked_at: ""
  checks_passed: 0
---

# Drafting meeting minutes with AI

> **AI usage:** AI transcribes the meeting and produces a draft of minutes
> and action items. A human (you) verifies the transcript, corrects the
> draft, and decides what is actioned. AI does not decide what anyone
> committed to; people do.

## What you will do

- Produce complete, shareable minutes within 30 minutes of a meeting
  ending.
- End up with an action-item list that names owners and due dates.
- Keep the workflow reproducible: same prompts every time, stored in your
  workflow library.

## Before you start

- A recording or live transcript of the meeting. Most meeting platforms
  (Teams, Zoom, Meet) can generate a transcript automatically once
  transcription is enabled.
- Permission to record: tell participants and honor no-record requests.
- A private workspace for the raw transcript (it is personal data).

## Steps

### 1. Get the transcript

Enable automatic transcription in your meeting tool, or upload the
recording to a transcription service. Export the transcript as plain
text when the meeting ends.

> Wait one or two minutes for processing before exporting; transcripts
> still being generated produce truncated minutes.

### 2. Draft minutes with AI

Paste the transcript into your AI assistant and run this prompt:

> You are an experienced executive assistant. From the transcript below,
> produce meeting minutes with these sections: Participants, Decisions,
> Discussion summary (no more than 3 bullet lines per topic), Action
> items (owner + due date + what), and Open questions. Do not invent
> commitments; quote only what was said. Keep the tone neutral.

Review the output against the transcript. AI will occasionally invent a
plausible owner or date — strike anything you cannot verify.

### 3. Verify action items with a human pass

The most valuable step: go through each action item and check the owner
is a real person who agreed, and the due date is what the room agreed.
Where the transcript is ambiguous (someone said "I'll do it" without a
name), mark it `UNASSIGNED` and raise it at the next meeting rather than
guessing.

### 4. Share the minutes

Paste the final minutes into the meeting notes tool you use. Link the
supporting transcript for anyone who wants the full record. Send action
items to the owners in the thread — do not rely on people reading the
notes.

### 5. Store the prompt

Save the prompt from step 2 in your team's workflow library so the next
meeting is one step: paste a transcript, edit the result. If the same
prompt produces good output twice, you have a repeatable playbook; if
not, fix the prompt before scaling it.

## Review checklist

- [ ] Transcript came from a source participants were told about
- [ ] Action items all have owners; `UNASSIGNED` items are flagged, not guessed
- [ ] Decisions match what the room decided; nothing invented
- [ ] Sensitive content (comp, personal) kept out of shared minutes

## Run it

- **Time:** 20–30 minutes for a 60-minute meeting (`5 min` AI, `10 min`
  human verification, `5 min` distribution)
- **Repeat:** after every meeting you own
- **Store:** final minutes in your meeting-notes tool; transcripts in the
  workspace; the prompt in the workflow library

## Related

- Editorial standards: [How PartlyGood works](../about.md)
- Taxonomy: [fields and content types](../taxonomy.md)