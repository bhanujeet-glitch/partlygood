#!/usr/bin/env python3
"""litsearch.py -- OpenAlex literature search for PartlyGood research.

Searches the OpenAlex API (https://api.openalex.org) for scholarly literature
relevant to a research subject, and appends results to a per-subject JSON file
under research/literature/.

Why OpenAlex: it is a free, open, index-queryable catalog of scholarly works
(no API key needed for modest use). For management/practitioner topics we
triangulate with vendor docs and practitioner annotations in sources/.

Usage:
    python research/scripts/litsearch.py <subject-file.json> [--query "..."] [--limit N] [--since YYYY-MM-DD]

If --query is omitted, the subject file's default query is used; the file is
created from a template if missing.

Exit codes: 0 ok, 1 error, 2 no results.

Stdlib only. Uses urllib; no api key. Respects polite rate (0.5s between calls).
"""

import argparse
import json
import os
import sys
import time
import urllib.parse
import urllib.request
from datetime import date, datetime

BASE = "https://api.openalex.org/works"

SUBJECT_TEMPLATE = {
    "subject": "<subject-name>",
    "default_query": "<what to search>",
    "queries": [],
    "last_run_at": None,
}


def _now():
    return datetime.now().isoformat(timespec="seconds")


def load_subject(path):
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(SUBJECT_TEMPLATE, fh, indent=2)
        print("Created subject file: %s (edit its 'subject' and 'default_query')" % path)
        sys.exit(2)
    with open(path, "r", encoding="utf-8") as fh:
        data = json.load(fh)
    # backfill keys missing from older/hand-made files so they never crash
    changed = False
    for key, val in SUBJECT_TEMPLATE.items():
        if key not in data:
            data[key] = val
            changed = True
    legacy = {"defaultQuery": "default_query", "lastRun": "last_run_at"}
    for old, new in legacy.items():
        if old in data and new not in data:
            data[new] = data.pop(old)
            changed = True
    if changed:
        save_subject(path, data)
    return data


def save_subject(path, data):
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2, ensure_ascii=False)
        fh.write("\n")


def fetch(query, limit, since, mailto):
    params = {
        "search": query,
        "per-page": str(min(limit, 200)),
        "mailto": mailto or "partlygood-research@example.invalid",
    }
    if since:
        params["filter"] = "from_publication_date:%s" % since
    url = BASE + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": "PartlyGoodResearch/1.0 (research tooling)"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def main():
    ap = argparse.ArgumentParser(description="OpenAlex literature search for PartlyGood research")
    ap.add_argument("subject_file", help="JSON file in research/literature/ (created if missing)")
    ap.add_argument("--query", help="search query (default: the file's default_query)")
    ap.add_argument("--limit", type=int, default=10, help="max results (default 10)")
    ap.add_argument("--since", help="only works published on/after YYYY-MM-DD")
    ap.add_argument("--mailto", default="", help="OpenAlex polite pool contact (recommended)")
    args = ap.parse_args()

    subject = load_subject(args.subject_file)
    query = args.query or subject.get("default_query")
    if not query:
        print("No query given and no default_query in file. Edit %s first." % args.subject_file)
        return 2

    try:
        data = fetch(query, args.limit, args.since, args.mailto or "partly.example-research@example.com")
    except Exception as exc:
        print("ERROR: failed to fetch from OpenAlex: %s" % exc, file=sys.stderr)
        return 1

    works = data.get("results", [])
    run = {
        "at": _now(),
        "query": query,
        "limit": args.limit,
        "since": args.since,
        "count": len(works),
        "results": [],
    }
    for w in works:
        item = {
            "title": w.get("title"),
            "doi": w.get("doi"),
            "url": w.get("doi") or w.get("id"),
            "authors": [
                (a.get("author", {}).get("display_name") or a.get("author", {}).get("name"))
                for a in (w.get("authorships") or [])
            ][:8],
            "year": None,
            "venue": (w.get("primary_location") or {}).get("source", {}).get("display_name"),
            "type": w.get("type"),
            "cited_by": w.get("cited_by_count"),
        }
        pd = w.get("publication_date") or (w.get("publication_year") and "%d-01-01" % w["publication_year"])
        if pd:
            try:
                item["year"] = int(pd[:4])
            except (ValueError, TypeError):
                pass
        run["results"].append(item)

    subject["queries"].append(run)
    subject["lastRunAt"] = _now()
    save_subject(args.subject_file, subject)
    print("Saved %d results to %s (query: %s)" % (len(works), args.subject_file, query))
    for r in subject["queries"][-1]["results"]:
        print("  - %s | %s | %s" % (r.get("year"), r.get("title"), r.get("venue")))
    time.sleep(0.5)
    return 0


if __name__ == "__main__":
    sys.exit(main())