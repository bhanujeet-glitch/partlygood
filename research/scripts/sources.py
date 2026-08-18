#!/usr/bin/env python3
"""sources.py -- manage PartlyGood source annotations.

A source annotation records WHY a source is trusted and WHICH claims it
supports. Every factual claim in a published piece must trace back to an
annotation here (via [src:ID] markers in the piece).

This CLI lists/validates/merges annotations across the sources/ tree.

Usage:
    python research/scripts/sources.py list [path]
    python research/scripts/sources.py validate [path]   # default: whole sources/ tree

Exit codes: 0 ok, 1 invalid, 2 usage.
"""

import argparse
import glob
import json
import os
import sys

KINDS = {"official", "peer-reviewed", "primary", "practitioner", "vendor-docs"}
CONFIDENCES = {"high", "medium", "low"}


def iter_annotations(paths):
    for path in paths:
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        for src in data.get("sources", []):
            yield path, data.get("title", os.path.basename(path)), src


def validate_path(path):
    errors = []
    try:
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
    except (OSError, ValueError) as exc:
        return ["%s: unreadable (%s)" % (path, exc)]
    if "sources" not in data:
        errors.append("%s: missing 'sources' key" % path)
    seen = set()
    for src in data.get("sources", []):
        sid = src.get("id")
        if not sid:
            errors.append("%s: source missing 'id'" % path)
        elif sid in seen:
            errors.append("%s: duplicate source id %r" % (path, sid))
        seen.add(sid)
        if not src.get("url"):
            errors.append("%s: source %r missing 'url'" % (path, sid))
        if src.get("kind") not in KINDS:
            errors.append("%s: source %r bad kind %r (allowed: %s)" % (path, sid, src.get("kind"), ", ".join(sorted(KINDS))))
        if src.get("confidence") not in CONFIDENCES:
            errors.append("%s: source %r bad confidence %r (allowed: %s)" % (path, sid, src.get("confidence"), ", ".join(sorted(CONFIDENCES))))
    return errors


def main():
    ap = argparse.ArgumentParser(description="PartlyGood source annotations manager")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("list", help="list all annotated sources")
    sub.add_parser("validate", help="lint annotation files")

    args = ap.parse_args()
    root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "sources")
    paths = sorted(glob.glob(os.path.join(root, "*.json")))
    # skip the template file
    paths = [p for p in paths if os.path.basename(p) != "_template.json"]

    if args.cmd == "list":
        n = 0
        for path, title, src in iter_annotations(paths):
            n += 1
            print("- [%s] %s | %s | %s | %s" % (src.get("id"), src.get("title"), src.get("kind"), src.get("confidence"), src.get("url")))
        print("Total: %d sources across %d files" % (n, len(paths)))
        return 0

    if args.cmd == "validate":
        all_errs = []
        for path in paths:
            all_errs.extend(validate_path(path))
        if all_errs:
            for e in all_errs:
                print("ERROR:", e)
            print("%d error(s)" % len(all_errs))
            return 1
        print("OK: %d annotation file(s) valid" % len(paths))
        return 0

    return 2


if __name__ == "__main__":
    sys.exit(main())