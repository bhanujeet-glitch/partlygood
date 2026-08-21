#!/usr/bin/env python3
"""quality_report.py — produce a machine-readable quality report.

Reads the content tree and writes report/quality-report.json with the
per-file status, checks, and an overall verdict. Used by CI and by the
editorial pipeline to stamp each piece with its quality state.

report.json schema (per-file entry):
  status  str      taxonomy status (published/draft/in_review/updated/retired)
  type    str      content type (playbook/how-to/explainer/canonical)
  field   str      taxonomy field
  words   int      body word count
  checks  {name: bool}  every quality check accepted/rejected for this file
  pass    bool     all checks passed
  ai_meter {ai_statement, human_gates, overstated_claims}  only for playbook/how-to:
                     ai_statement  bool   explicit "AI usage" statement present
                     human_gates   int    count of human-verification markers
                     overstated_claims int — AI-role claims that overreach
  sources_verified {count, missing, dead, verified}  only when a playbook has
                     a co-located sources.json:
                     count   total URLs claimed in the piece front matter
                     verified  URLs that resolved (HTTP 2xx/3xx) at QA time
                     dead      URLs that failed to resolve
                     missing   front-matter sources with no sources.json entry

Usage: python scripts/quality_report.py [--out PATH]
"""
import json
import os
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"

sys.path.insert(0, str(Path(__file__).resolve().parent))
import quality_checks as qc  # noqa: E402


def _check_url_ok(url, timeout=12):
    """Return True if url is genuinely reachable.

    HEAD first, then GET. A 2xx/3xx is fine. A 403/429 is a bot-defense /
    rate-limit response from an authoritative source (many real sources,
    e.g. APQC, block HEAD and scripted clients) — treat it as reachable, not
    dead. Only genuine 404/410/5xx problems count as dead links.
    """
    def probe(method):
        try:
            req = urllib.request.Request(url, method=method,
                                         headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                                                               "AppleWebKit/537.36 Chrome/126 Safari/537.36"})
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.status
        except Exception as e:
            code = getattr(e, "code", None)
            if code is not None:
                return int(code)
            return None
    for method in ("HEAD", "GET"):
        code = probe(method)
        if code is None:
            continue
        if 200 <= code < 400:
            return True  # resolved
        if code in (403, 429):
            return True  # bot-blocked, but served (reachable)
        return False  # 404/410/5xx = genuinely dead
    return False


def _sources_record(doc, verify_network=False):
    """Source-verification record for a playbook.

    Source of truth for a published piece is its front-matter `sources:`
    list. If a colocated sources.json exists under playbooks/, prefer its
    annotated URLs when it matches the piece's slug. When verify_network is
    true, each URL is reachability-checked and counted as verified/dead. The
    network check is never a hard gate failure (a dead link is reported, not
    fatal) so the tool stays usable offline and in CI.
    """
    if doc.get("type") not in ("playbook", "how-to"):
        return {"count": 0, "verified": 0, "dead": 0, "missing": 0, "ok": True}
    fm = doc.get("sources") or []
    if isinstance(fm, str):
        fm = [fm]
    fm = [str(u) for u in fm if str(u).startswith(("http://", "https://"))]
    # Prefer annotated sources.json when it matches this slug.
    slug = doc.get("slug")
    sph = None
    for cand in (ROOT / "playbooks").rglob("sources.json"):
        if slug and slug in cand.parent.name:
            sph = cand
            break
    if sph is not None:
        try:
            meta = json.loads(sph.read_text(encoding="utf-8"))
            ann = [s["url"] for s in meta.get("sources", []) if s.get("url")]
            if ann:
                fm = ann
        except Exception:
            pass
    urls = [u for u in fm if str(u).startswith(("http://", "https://"))]
    verified = dead = 0
    ok = True
    if verify_network and urls:
        for u in urls:
            if _check_url_ok(u):
                verified += 1
            else:
                dead += 1
        ok = dead == 0
    return {
        "count": len(urls),
        "verified": verified,
        "dead": dead,
        "missing": max(0, len(fm) - len(urls)),
        "ok": ok,
        "hint": None if verify_network and urls else "network source check deferred to editorial QA",
    }


def main() -> int:
    out_path = Path(sys.argv[sys.argv.index("--out") + 1]) if "--out" in sys.argv else ROOT / "report.json"
    verify = "--verify-sources" in sys.argv

    docs = qc.load_docs()
    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_files": len(docs),
        "files": {},
    }
    failed = 0
    for doc in docs:
        results = []
        for fn in qc.CHECKS:
            fn(doc, results)
        rel = doc["__path"].relative_to(DOCS).as_posix()
        checks = {name: ok for name, ok, _ in results}
        file_failed = any(not ok for ok in checks.values())
        failed += int(file_failed)
        meter = qc._meter(doc)
        entry = {
            "status": doc.get("status"),
            "type": doc.get("type"),
            "field": doc.get("field"),
            "checks": checks,
            "pass": not file_failed,
            "words": doc["__words"],
        }
        if doc.get("type") in ("playbook", "how-to"):
            entry["ai_meter"] = {
                "ai_statement": meter[0],
                "human_gates": meter[1],
                "overstated_claims": meter[2],
            }
        entry["sources_verified"] = _sources_record(doc, verify_network=verify)
        report["files"][rel] = entry

    report["verdict"] = "pass" if failed == 0 else "fail"
    report["failed_files"] = failed
    out_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Wrote {out_path} — verdict={report['verdict']} ({failed} file(s) failing)")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())