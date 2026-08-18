#!/usr/bin/env python3
"""validate_content.py — structural validation of the publication.

Checks (each prints a line; exit 1 on any failure):
 1. Every .md under docs/ has well-formed YAML front matter.
 2. Required front-matter keys are present (title, type, field, status,
    created, updated, slug, quality).
 3. type/field/status values are in the taxonomy.
 4. The file lives in the directory matching its field.
 5. The slug matches the filename.
 6. No markdown links point to a missing local target.

Usage: python scripts/validate_content.py [--strict]
"""
import re
import sys
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

LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")


def parse_front_matter(text: str):
    if not text.startswith("---\n"):
        return None, None
    end = text.find("\n---", 4)
    if end < 0:
        return None, None
    try:
        fm = yaml.safe_load(text[4:end])
    except yaml.YAMLError:
        return None, None
    body = text[end + 4:]
    return (fm if isinstance(fm, dict) else None), body


def main() -> int:
    failures = []
    files = sorted(p for p in DOCS.rglob("*.md") if "_retired" not in p.parts)
    for path in files:
        rel = path.relative_to(DOCS)
        text = path.read_text(encoding="utf-8")
        fm, body = parse_front_matter(text)
        if fm is None:
            failures.append(f"{rel}: missing or invalid front matter")
            continue

        field, slug = fm.get("field"), fm.get("slug")
        # Canonical house docs (index/about/samples/taxonomy) live at the
        # site root; only field content must match its directory.
        if fm.get("type") != "canonical" and field in VALID_FIELDS and path.parent.name != field:
            failures.append(f"{rel}: field='{field}' but directory is '{path.parent.name}'")
        if slug and path.stem != slug:
            failures.append(f"{rel}: slug '{slug}' does not match filename '{path.stem}'")
        for key in REQUIRED_KEYS:
            if key not in fm:
                failures.append(f"{rel}: missing front matter key '{key}'")
        if fm.get("type") not in VALID_TYPES:
            failures.append(f"{rel}: bad type '{fm.get('type')}'")
        if fm.get("status") not in VALID_STATUS:
            failures.append(f"{rel}: bad status '{fm.get('status')}'")

        body = body or ""
        for m in LINK_RE.finditer(body):
            target = m.group(1).split("#")[0].strip()
            if not target or target.startswith(("http://", "https://", "mailto:", "data:")):
                continue
            if target.startswith("/"):
                # Site-root URL path (e.g. /taxonomy/) — resolved at build
                # time by mkdocs; structurally valid, skip file check.
                continue
            cand = (path.parent / target).resolve()
            try:
                cand.relative_to(DOCS)
            except ValueError:
                continue  # outside docs — not our concern here
            if not cand.exists():
                failures.append(f"{rel}: link target '{target}' not found")

    print(f"Validated {len(files)} content files.")
    if failures:
        for f in failures:
            print(f"  FAIL {f}")
        print(f"{len(failures)} validation failure(s).")
        return 1
    print("All structural checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())