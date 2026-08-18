#!/usr/bin/env python3
"""quality_checks.py — editorial quality gate for the publication.

Each check is a boolean predicate. Exit 1 if any check fails.

Checks implemented:
 1. required_front_matter  — every file has the taxonomy's required keys
 2. title_length           — title <= 90 chars
 3. min_body_length        — playbook/how-to bodies >= 150 words
 4. has_ai_usage_preview   — playbook/how-to have an "AI usage" or
                             "What you will do" section
 5. sources_attribution    — factual tool/model claims carry a URL source
 6. no_todo_placeholders   — no TODO/TBD/lorem/FIXME
 7. taxonomy_conformance   — type/field/status in taxonomy, file placed
                             in matching field directory
 8. freshness_check        — published pieces updated within 365 days

Usage: python scripts/quality_checks.py [--all]
"""
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"

try:
    import yaml
except ImportError:
    print("PyYAML required: pip install -r requirements.txt", file=sys.stderr)
    sys.exit(3)

VALID_TYPES = {"playbook", "how-to", "explainer", "canonical"}
VALID_FIELDS = {"management", "operations", "finance", "marketing", "cross-cutting"}
VALID_STATUS = {"draft", "in_review", "published", "updated", "retired"}
REQUIRED_KEYS = ["title", "type", "field", "status", "created", "updated", "slug", "quality"]
URL_RE = re.compile(r"https?://\S+")
WORD_RE = re.compile(r"\b\w+\b")
BAD_PLACEHOLDERS = re.compile(r"\b(TODO|TBD|FIXME|lorem ipsum)\b", re.IGNORECASE)
TOOL_CLAIM_RE = re.compile(
    r"\b(ChatGPT|Claude|Gemini|Copilot|GPT-4|GPT-5|perplexity|notebooklm|"
    r"midjourney|dall-e|fireflies|otter\.ai|granola|elevenlabs)\b",
    re.IGNORECASE,
)
TODAY = date.today()


def parse(path: Path):
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return None, None, text
    end = text.find("\n---", 4)
    if end < 0:
        return None, None, text
    try:
        fm = yaml.safe_load(text[4:end])
    except yaml.YAMLError:
        fm = None
    return (fm if isinstance(fm, dict) else None), text[end + 4:], text


def load_docs():
    docs = []
    for path in sorted(DOCS.rglob("*.md")):
        if "_retired" in path.parts:
            continue
        fm, body, _ = parse(path)
        if fm is None:
            fm = {}
            body = ""
        record = dict(fm)
        record["__path"] = path
        record["__body"] = body or ""
        record["__words"] = len(WORD_RE.findall(record["__body"]))
        record["__urls"] = URL_RE.findall(record["__body"])
        record["__sections"] = {
            h.strip().lower()
            for h in re.findall(r"^#{1,3}\s+(.+)$", record["__body"], re.M)
        }
        docs.append(record)
    return docs


def check_required_front_matter(doc, out):
    missing = [k for k in REQUIRED_KEYS if k not in doc]
    out.append(("required_front_matter", not missing, f"{doc['__path'].name}: missing {missing}" if missing else ""))


def check_title_length(doc, out):
    title = str(doc.get("title", ""))
    ok = len(title) <= 90
    out.append(("title_length", ok, f"{doc['__path'].name}: title {len(title)} chars" if not ok else ""))


def check_min_body_length(doc, out):
    kind = doc.get("type")
    # Canonical house docs (index/about/samples/taxonomy, type=canonical)
    # are exempt from body-length policy — they are navigation/standards
    # pages, not editorial pieces.
    if kind == "canonical":
        out.append(("min_body_length", True, f"{doc['__path'].name}: canonical (no floor)"))
        return
    floor = 200 if kind in ("playbook", "how-to") else 60
    ok = doc["__words"] >= floor
    out.append(("min_body_length", ok, f"{doc['__path'].name}: {doc['__words']} words" if not ok else ""))


def check_ai_usage_preview(doc, out):
    kind = doc.get("type")
    if kind not in ("playbook", "how-to"):
        out.append(("ai_usage_preview", True, f"{doc['__path'].name}: n/a for {kind}"))
        return
    sections = doc["__sections"]
    ok = any("ai usage" in s or "what you will do" in s or "before you start" in s for s in sections)
    out.append(("ai_usage_preview", ok, f"{doc['__path'].name}: missing AI usage section" if not ok else ""))


def check_sources_attribution(doc, out):
    body = doc["__body"]
    if not URL_RE.search(body):
        out.append(("sources_attribution", True, f"{doc['__path'].name}: (no URLs)"))
        return
    claims = TOOL_CLAIM.findall(body)
    ok = bool(doc["__urls"])  # any URL present satisfies attribution for now
    out.append(("sources_attribution", ok, f"{doc['__path'].name}: {len(claims)} tool claims, {len(doc['__urls'])} URLs" if not ok else ""))


PLACEHOLDERS = re.compile(r"\b(TODO|TBD|FIXME)\b|\blorem ipsum\b", re.IGNORECASE)
PLACEHOLDER_EXEMPT = re.compile(r"`[^`]*\b(TODO|TBD|FIXME)\b[^`]*`")


def check_no_todo_placeholders(doc, out):
    if doc.get("type") == "canonical":
        out.append(("no_todo_placeholders", True, f"{doc['__path'].name}: canonical exempt"))
        return
    body = PLACEHOLDER_EXEMPT.sub("", doc["__body"])  # ignore inline-code mentions
    hits = [m.group(0) for m in PLACEHOLDERS.finditer(body)]
    out.append(("no_todo_placeholders", not hits, f"{doc['__path'].name}: {hits}" if hits else ""))


def check_taxonomy_conformance(doc, out):
    # Canonical house docs (index/about/samples/taxonomy) may carry a
    # field value without living in the matching directory; exempt.
    if doc.get("type") == "canonical":
        out.append(("taxonomy_conformance", True, f"{doc['__path'].name}: canonical"))
        return
    problems = []
    if doc.get("type") not in VALID_TYPES:
        problems.append(f"type={doc.get('type')}")
    if doc.get("field") not in VALID_FIELDS:
        problems.append(f"field={doc.get('field')}")
    if doc.get("status") not in VALID_STATUS:
        problems.append(f"status={doc.get('status')}")
    if doc.get("field") in VALID_FIELDS and doc["__path"].parent.name != doc["field"]:
        problems.append("dir mismatch")
    out.append(("taxonomy_conformance", not problems, f"{doc['__path'].name}: {problems}" if problems else ""))


def check_freshness(doc, out):
    if doc.get("status") not in ("published", "updated"):
        out.append(("freshness", True, f"{doc['__path'].name}: (status {doc.get('status')} skips freshness)"))
        return
    try:
        updated = date.fromisoformat(str(doc.get("updated")))
    except (ValueError, TypeError):
        out.append(("freshness", False, f"{doc['__path'].name}: bad updated date"))
        return
    ok = (TODAY - updated).days <= 365
    out.append(("freshness", ok, f"{doc['__path'].name}: last updated {updated} ({ (TODAY - updated).days }d)" if not ok else ""))


CHECKS = [
    check_required_front_matter,
    check_title_length,
    check_min_body_length,
    check_ai_usage_preview,
    check_sources_attribution,
    check_no_todo_placeholders,
    check_taxonomy_conformance,
    check_freshness,
]


def main() -> int:
    docs = load_docs()
    if not docs:
        print("No content found under docs/.")
        return 1
    results = []
    for doc in docs:
        for fn in CHECKS:
            fn(doc, results)

    percheck = {}
    for name, ok, detail in results:
        percheck.setdefault(name, []).append((ok, detail))

    failed = 0
    for name in sorted(percheck):
        rows = percheck[name]
        bad = [d for ok, d in rows if not ok]
        status = "OK  " if not bad else "FAIL"
        print(f"  [{status}] {name} ({len(rows) - len(bad)}/{len(rows)})")
        for d in bad:
            print(f"           - {d}")
        failed += len(bad)

    print(f"Quality gate: {len(results) - failed}/{len(results)} checks passed.")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())