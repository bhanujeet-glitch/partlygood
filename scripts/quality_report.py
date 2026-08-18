#!/usr/bin/env python3
"""quality_report.py — produce a machine-readable quality report.

Reads the content tree and writes report/quality-report.json with the
per-file status, checks, and an overall verdict. Used by CI and by the
editorial pipeline to stamp each piece with its quality state.

Usage: python scripts/quality_report.py [--out PATH]
"""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"

sys.path.insert(0, str(Path(__file__).resolve().parent))
import quality_checks as qc  # noqa: E402


def main() -> int:
    out_path = Path(sys.argv[sys.argv.index("--out") + 1]) if "--out" in sys.argv else ROOT / "report.json"

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
        report["files"][rel] = {
            "status": doc.get("status"),
            "type": doc.get("type"),
            "field": doc.get("field"),
            "checks": checks,
            "pass": not file_failed,
            "words": doc["__words"],
        }

    report["verdict"] = "pass" if failed == 0 else "fail"
    report["failed_files"] = failed
    out_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Wrote {out_path} — verdict={report['verdict']} ({failed} file(s) failing)")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())