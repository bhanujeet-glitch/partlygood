#!/usr/bin/env python3
"""taxonomy_compat.py — prove a taxonomy version bump preserves existing topics.

Compares the two most recent taxonomy-v*.json files in research/taxonomy/
(previous version vs. latest version) and fails (exit 1) if any topic id,
field id, or pillar id that existed in the previous version is missing from
the latest one.

Usage:
    python research/scripts/taxonomy_compat.py [--prev-v1] [--json PATH]

Options:
    --prev PATH   Explicit path to the previous taxonomy file (default: the
                  second-newest taxonomy-v*.json).
    --json PATH   Explicit path to the new taxonomy file (default: the newest).
    --json        Print a machine-readable summary as JSON.

Exit codes: 0 = backward compatible, 1 = dropped ids found, 2 = usage error.
"""

import argparse
import json
import glob
import os
import sys

TAXONOMY_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "taxonomy")


def version_key(name):
    stem = os.path.basename(name)[len("taxonomy-v"):].rsplit(".", 1)[0]
    try:
        return [int(part) for part in stem.split(".")]
    except ValueError:
        return [-1]


def load(path):
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prev", help="previous taxonomy file")
    parser.add_argument("--json-path", "--json", dest="json_path", help="the new taxonomy file")
    parser.add_argument("--as-json", action="store_true", help="print machine-readable summary")
    args = parser.parse_args(argv)

    files = sorted(
        glob.glob(os.path.join(TAXONOMY_DIR, "taxonomy-v*.json")), key=version_key
    )
    if len(files) < 2:
        print(
            "taxonomy_compat: need at least two taxonomy-v*.json files to compare "
            "(found %d)" % len(files),
            file=sys.stderr,
        )
        return 2

    prev_path = args.prev or files[-2]
    new_path = args.json_path or files[-1]

    prev = load(prev_path)
    new = load(new_path)

    prev_topics = set(prev["topics"])
    new_topics = set(new["topics"])
    prev_fields = {f["id"] for f in prev["fields"]}
    new_fields = {f["id"] for f in new["fields"]}
    prev_pillars = {p["id"] for p in prev["pillars"]}
    new_pillars = {p["id"] for p in new["pillars"]}

    dropped_topics = sorted(prev_topics - new_topics)
    dropped_fields = sorted(prev_fields - new_fields)
    dropped_pillars = sorted(prev_pillars - new_pillars)
    added_topics = sorted(new_topics - prev_topics)

    ok = not (dropped_topics or dropped_fields or dropped_pillars)

    def summary():
        return {
            "prev": os.path.basename(prev_path),
            "new": os.path.basename(new_path),
            "backward_compatible": ok,
            "dropped_topics": dropped_topics,
            "dropped_fields": dropped_fields,
            "dropped_pillars": dropped_pillars,
            "added_topics": added_topics,
        }

    if args.as_json:
        print(json.dumps(summary(), indent=2))
    else:
        print("compat `%s` -> `%s`" % (os.path.basename(prev_path), os.path.basename(new_path)))
        if added_topics:
            print("  added topics  (%d): %s" % (len(added_topics), ", ".join(added_topics)))
        if ok:
            print("  OK: no existing topics/fields/pillars dropped (backward compatible)")
        else:
            if dropped_topics:
                print("  DROPPED topics (%d): %s" % (len(dropped_topics), ", ".join(dropped_topics)))
            if dropped_fields:
                print("  DROPPED fields (%d): %s" % (len(dropped_fields), ", ".join(dropped_fields)))
            if dropped_pillars:
                print("  DROPPED pillars (%d): %s" % (len(dropped_pillars), ", ".join(dropped_pillars)))
            print("  FAIL: this is a breaking taxonomy change (MAJOR bump required)")

    return 0 if ok else 1


if __name__ == "__main__":
    import sys
    sys.exit(main())