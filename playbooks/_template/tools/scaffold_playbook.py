#!/usr/bin/env python3
"""scaffold_playbook.py -- create a new PartlyGood playbook folder from the template.

Usage:
    python playbooks/_template/tools/scaffold_playbook.py \
        -n meetings-outlook-agenda \
        --title "AI-prepared meeting agendas from Outlook" \
        --field mgmt --topic mgmt.meetings --pillar wf.comms

Creates playbooks/<field>/<name>/draft.md and sources.json.

Exit codes: 0 ok, 1 error (exists), 2 usage/taxonomy error.
"""

import argparse
import json
import os
import re
import sys
from datetime import date

TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.normpath(os.path.join(TOOLS_DIR, ".."))
WORKSPACE_ROOT = os.path.normpath(os.path.join(TEMPLATE_DIR, "..", ".."))

FRONT_MATTER = """---
id: {slug}
title: "{title}"
brief_id: {slug}
content_type: playbook
field: {field}
pillars: [{pillars}]
topics: [{topics}]
stage: draft
status: draft
owner: {owner}
created: {today}
updated: {today}
version: 0.0.1
prompt_versions: {{drafter: 1}}
---

# {title}

> Outline only. Fill in every section from the template:
> `playbooks/_template/playbook-template.md`

## 1. The outcome

_What the reader gets after following this playbook._

## 2. When to use this (and when not to)

- Use when:
- When not:

## 3. What you need before you start

- Prerequisites:
- Tools:
- Input artifacts:

## 4. The workflow

### Step 1 — <name>

**Inputs:** \
**Action:** \
**Prompt (if AI):** \
**Output:**

### Step 2 — <name>

...

## 5. The review gate

- [ ] Claims are all sourced `[src:ID]` and sources resolve
- [ ] No engineering how-to content
- [ ] Steps are reproducible
- [ ] Taxonomy ids valid

## 6. Failure modes and fixes

| symptom | likely cause | fix |
|---|---|---|
| | | |

## 7. What can go wrong / caveats

## 8. Sources

_Sources appear as `[src:ID]` in the body and are listed in sources.json._

## 9. Provenance

- Brief: `research/briefs/{slug}.md`
- Research plan: `research/plans/{slug}.md`
- Source annotations: `sources.json`
- Vault notes:

---

## Review checklist (filled in by reviewer)

| check | status | note |
|---|---|---|
| Outcome stated | | |
| Use-when / not-when present | | |
| Prerequisites complete | | |
| All steps concrete, artifacts named | | |
| Every claim sourced | | |
| No engineering how-to | | |
| Taxonomy valid | | |
| Checklist honest | | |

Reviewer: _name/role_ — Date: _YYYY-MM-DD_ — Verdict: _publish / revise / reject_
"""

def slugify(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def sources_payload(title, slug):
    return {
        "title": title,
        "briefId": slug,
        "content_type": "playbook",
        "sources": [],
    }


def main():
    ap = argparse.ArgumentParser(description="Scaffold a PartlyGood playbook folder")
    ap.add_argument("-n", "--name", required=True, help="playbook slug / folder name (kebab-case)")
    ap.add_argument("--title", required=True, help="human title")
    ap.add_argument("--field", required=True, help="taxonomy field id, e.g. mgmt/ops/finance")
    ap.add_argument("--topic", action="append", default=[], help="taxonomy topic id (repeatable)")
    ap.add_argument("--pillar", action="append", default=[], help="taxonomy pillar id (repeatable)")
    ap.add_argument("--owner", default="editorial-tbd", help="owner label")
    args = ap.parse_args()

    slug = slugify(args.name)
    if not slug:
        print("ERROR: name slugifies to empty", file=sys.stderr)
        return 2

    # validate taxonomy ids early
    sys.path.insert(0, os.path.join(WORKSPACE_ROOT, "research", "scripts"))
    from taxonomy import Taxonomy

    tax = Taxonomy()
    try:
        tax.validate_fields([args.field])
        if args.pillar:
            tax.validate_pillars(args.pillar)
        if args.topic:
            tax.validate_topics(args.topic)
    except ValueError as exc:
        print("ERROR: %s" % exc, file=sys.stderr)
        return 2

    folder = os.path.join(WORKSPACE_ROOT, "playbooks", args.field, slug)
    if os.path.exists(folder):
        print("ERROR: %s already exists" % folder, file=sys.stderr)
        return 1
    os.makedirs(folder)

    draft = FRONT_MATTER.format(
        slug=slug,
        title=args.title,
        field=args.field,
        pillars=", ".join(args.pillar),
        topics=", ".join(args.topic),
        owner=args.owner,
        today=date.today().isoformat(),
    )
    with open(os.path.join(folder, "draft.md"), "w", encoding="utf-8") as fh:
        fh.write(draft)

    with open(os.path.join(folder, "sources.json"), "w", encoding="utf-8") as fh:
        json.dump(sources_payload(args.title, slug), fh, indent=2)
        fh.write("\n")

    print("Created %s" % folder)
    print("  draft.md + sources.json (fill both; then run validate_playbook.py)")
    return 0


if __name__ == "__main__":
    sys.exit(main())