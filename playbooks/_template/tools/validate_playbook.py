#!/usr/bin/env python3
"""validate_playbook.py -- validate a PartlyGood playbook folder before review/publish.

Checks, in order:
1. required files exist (draft.md or <slug>.md, sources.json)
2. front matter parses; required keys present
3. field / pillars / topics / content_type are valid taxonomy ids
4. content_type is 'playbook' (unless --allow-explainers)
5. the template's numbered sections (1..9) are present as headings
6. every [src:ID] marker in the body resolves to an entry in sources.json
7. sources.json entries are structurally sound (id, url, kind, confidence)
8. no engineering-topic heading drift (heuristic)

Usage:
    python playbooks/_template/tools/validate_playbook.py playbooks/mgmt/meetings-outlook-agenda/
    python playbooks/_template/tools/validate_playbook.py          # all playbooks

Exit codes: 0 valid, 1 invalid, 2 usage error.
"""

import argparse
import json
import os
import re
import sys

TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.normpath(os.path.join(TOOLS_DIR, ".."))
WORKSPACE_ROOT = os.path.normpath(os.path.join(TEMPLATE_DIR, "..", ".."))

REQUIRED_FM = [
    "id", "title", "brief_id", "content_type", "field", "pillars", "topics",
    "stage", "status", "owner", "created", "updated", "version",
]
SECTIONS = [
    "1. The outcome",
    "2. When to use this",
    "3. What you need before you start",
    "4. The workflow",
    "5. The review gate",
    "6. Failure modes and fixes",
    "7. What can go wrong",
    "8. Sources",
    "9. Provenance",
]
SRC_RE = re.compile(r"\[src:([A-Za-z0-9_-]+)\]")
ENG_HEADING_RE = re.compile(
    r"^#{2,3}\s.*\b(code|software engineering|programming|deploy|git clone|CI/CD|pipeline|API key setup)\b.*",
    re.IGNORECASE | re.MULTILINE,
)
KINDS = {"official", "peer-reviewed", "primary", "practitioner", "vendor-docs"}
CONF = {"high", "medium", "low"}


def parse_front(text):
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if not m:
        return None
    data = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            data[k.strip()] = v.strip().strip('"').strip("'")
    return data


def listify(raw):
    if raw is None:
        return []
    if isinstance(raw, list):
        return raw
    raw = str(raw).strip()
    if raw.startswith("[") and raw.endswith("]"):
        raw = raw[1:-1]
    return [x.strip() for x in raw.split(",") if x.strip()]


def validate_folder(folder, allow_other_types=False):
    errors = []

    # 1. required files
    slug = os.path.basename(os.path.normpath(folder))
    candidates = [os.path.join(folder, "draft.md"), os.path.join(folder, slug + ".md")]
    body_path = next((p for p in candidates if os.path.exists(p)), None)
    if not body_path:
        errors.append("missing draft.md or %s.md" % slug)
        return errors
    src_path = os.path.join(folder, "sources.json")
    if not os.path.exists(src_path):
        errors.append("missing sources.json")

    # 2. front matter
    with open(body_path, "r", encoding="utf-8") as fh:
        text = fh.read()
    fm = parse_front(text)
    if fm is None:
        errors.append("missing front matter in %s" % os.path.basename(body_path))
        return errors
    for key in REQUIRED_FM:
        if not fm.get(key):
            errors.append("front matter missing required key: %s" % key)

    # 3. taxonomy
    sys.path.insert(0, os.path.join(WORKSPACE_ROOT, "research", "scripts"))
    from taxonomy import Taxonomy

    tax = Taxonomy()
    try:
        tax.validate_fields([fm.get("field", "")])
    except ValueError as exc:
        errors.append("field: %s" % exc)
    try:
        tax.validate_pillars(listify(fm.get("pillars")))
    except ValueError as exc:
        errors.append("pillars: %s" % exc)
    try:
        tax.validate_topics(listify(fm.get("topics")))
    except ValueError as exc:
        errors.append("topics: %s" % exc)

    # 4. content type
    ctype = fm.get("content_type", "")
    if not allow_other_types and ctype and ctype != "playbook":
        errors.append("content_type must be 'playbook' (got %r); pass --allow-explainers to permit others" % ctype)
    elif not ctype:
        errors.append("front matter missing content_type")

    # 5. template sections
    for sec in SECTIONS:
        if sec not in text:
            errors.append("missing section heading: '%s'" % sec)

    # 6/7. sources resolution
    src_ids = set()
    if os.path.exists(src_path):
        with open(src_path, "r", encoding="utf-8") as fh:
            try:
                sources = json.load(fh).get("sources", [])
            except ValueError as exc:
                errors.append("sources.json unparseable: %s" % exc)
                sources = []
        for s in sources:
            sid = s.get("id")
            if not sid:
                errors.append("sources.json entry missing 'id'")
            else:
                src_ids.add(sid)
            if not s.get("url"):
                errors.append("sources.json entry %r missing 'url'" % sid)
            if s.get("kind") not in KINDS:
                errors.append("sources.json entry %r bad kind %r" % (sid, s.get("kind")))
            if s.get("confidence") not in CONF:
                errors.append("sources.json entry %r bad confidence %r" % (sid, s.get("confidence")))

    body_src = SRC_RE.findall(text)
    # 'ID' is the template's literal placeholder ([src:ID]), not a real citation
    missing = sorted({s for s in body_src if s not in src_ids and s != "ID"})
    if missing:
        errors.append("body cites undefined source id(s): %s" % ", ".join(missing))

    # 8. engineering drift (heuristic)
    hits = ENG_HEADING_RE.findall(text)
    if hits:
        errors.append("engineering-topic heading(s) detected: %s" % ", ".join(dict.fromkeys(hits[:3])))

    return errors


def collect_playbooks(root):
    found = []
    for field in sorted(os.listdir(root)):
        fpath = os.path.join(root, field)
        if not os.path.isdir(fpath) or field.startswith("_"):
            continue
        for slug in sorted(os.listdir(fpath)):
            spath = os.path.join(fpath, slug)
            if os.path.isdir(spath):
                found.append(spath)
    return found


def main():
    ap = argparse.ArgumentParser(description="Validate a PartlyGood playbook folder")
    ap.add_argument("path", nargs="?", help="playbook folder (default: all under playbooks/)")
    ap.add_argument("--allow-explainers", action="store_true",
                    help="allow content types other than 'playbook'")
    args = ap.parse_args()

    base = os.path.join(WORKSPACE_ROOT, "playbooks")
    targets = [os.path.normpath(args.path)] if args.path else collect_playbooks(base)

    n = 0
    for t in targets:
        if not os.path.isdir(t):
            print("ERROR: not a directory: %s" % t)
            n += 1
            continue
        errs = validate_folder(t, allow_other_types=args.allow_explainers)
        rel = os.path.relpath(t, WORKSPACE_ROOT)
        if errs:
            print("[INVALID] %s" % rel)
            for e in errs:
                print("   - %s" % e)
            n += len(errs)
        else:
            print("[ok] %s" % rel)

    print()
    if n:
        print("FAIL: %d issue(s)" % n)
        return 1
    print("OK: all playbooks valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())