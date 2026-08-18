#!/usr/bin/env python3
"""vault_index.py -- regenerate the PartlyGood vault index and check links.

Scans research/vault/domains/**/*.md (domain notes), reads front matter,
rebuilds research/vault/index.md, and fails if any [[wikilink]] targets a
note id that does not exist anywhere in the vault.

Usage:
    python research/scripts/vault_index.py [--vault research/vault] [--check]

Exit codes: 0 ok, 1 broken links / missing vault.
"""

import argparse
import os
import re
import sys
from datetime import datetime

FRONT_MATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
WIKILINK_RE = re.compile(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]")


def parse_front(text):
    """Parse the YAML-ish front matter block of a note."""
    data = {}
    for line in text.splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            data[k.strip()] = v.strip()
    return data


def load_notes(vault):
    """Return {note_id: (path, frontmatter)} for every .md with front matter."""
    notes = {}
    for root, _dirs, files in os.walk(vault):
        for fn in sorted(files):
            if not fn.endswith(".md"):
                continue
            path = os.path.join(root, fn)
            with open(path, "r", encoding="utf-8") as fh:
                text = fh.read()
            m = FRONT_MATTER_RE.match(text)
            if not m:
                continue
            fm = parse_front(m.group(1))
            nid = fm.get("id") or os.path.splitext(fn)[0]
            notes[nid] = (path, fm)
    return notes


def main():
    ap = argparse.ArgumentParser(description="Rebuild the vault index and check wikilinks")
    ap.add_argument("--vault", default=None, help="path to research/vault")
    ap.add_argument("--check", action="store_true", help="only check links, don't rewrite index")
    args = ap.parse_args()

    vault = args.vault or os.path.normpath(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "vault")
    )
    if not os.path.isdir(vault):
        print("ERROR: vault dir not found: %s" % vault, file=sys.stderr)
        return 1

    notes = load_notes(vault)

    # 1) check wikilinks
    problems = []
    for nid, (path, _fm) in notes.items():
        with open(path, "r", encoding="utf-8") as fh:
            text = fh.read()
        for target in WIKILINK_RE.findall(text):
            if target not in notes:
                problems.append(
                    "%s: [[%s]] has no note" % (os.path.relpath(path, vault), target)
                )
    if problems:
        print("ERROR: %d broken wikilink(s)" % len(problems))
        for p in problems:
            print("  " + p)
        return 1
    if args.check:
        print("OK: %d notes, no broken links" % len(notes))
        return 0

    # 2. rebuild index.md from domain notes
    by_field = {}
    for nid, (path, fm) in notes.items():
        if "domains" not in path:
            continue
        parts = os.path.relpath(path, vault).split(os.sep)
        field = parts[1] if len(parts) > 1 and parts[0] == "domains" else "?"
        by_field.setdefault(field, []).append((nid, fm))

    lines = [
        "# Vault Index",
        "",
        "_Regenerated %s; see vault-guide.md._" % datetime.now().strftime("%Y-%m-%d %H:%M"),
        "",
    ]
    for field in sorted(by_field):
        lines.append("## %s" % field)
        lines.append("")
        for nid, fm in sorted(by_field[field]):
            lines.append("- %s: %s" % (nid, fm.get("title", nid)))
        lines.append("")

    idx_path = os.path.join(vault, "index.md")
    with open(idx_path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))
    print("index.md updated (%d notes, %d domains)" % (len(notes), len(by_field)))
    return 0


if __name__ == "__main__":
    sys.exit(main())