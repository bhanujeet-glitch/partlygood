#!/usr/bin/env python3
"""new_article.py — scaffold a new PartlyGood content piece.

Usage:
    python scripts/new_article.py <type> "<Title of the piece>" [field]

Types: playbook | how-to | explainer
Fields: management | operations | finance | marketing | cross-cutting
       (default: inferred from an existing docs/<match> or 'cross-cutting')

Prints the path to the new draft. Fails (no file written) when a piece
with the same slug already exists — dedup guard for the editorial pipeline.
"""
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
TEMPLATES = ROOT / "templates"
VALID_TYPES = {"playbook", "how-to", "explainer"}
VALID_FIELDS = {"management", "operations", "finance", "marketing", "cross-cutting"}


def slugify(title: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    return slug or "untitled"


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    if len(args) < 2:
        print(__doc__)
        return 2
    kind, title = args[0].lower(), args[1]
    field = args[2].lower() if len(args) > 2 else ""

    if kind not in VALID_TYPES:
        print(f"ERROR: type '{kind}' not in {sorted(VALID_TYPES)}", file=sys.stderr)
        return 2
    if field and field not in VALID_FIELDS:
        print(f"ERROR: field '{field}' not in {sorted(VALID_FIELDS)}", file=sys.stderr)
        return 2
    if not field:
        for cand in VALID_FIELDS:
            if (DOCS / cand).exists() and any((DOCS / cand).glob("*.md")):
                field = cand
                break
        field = field or "cross-cutting"

    slug = slugify(title)
    target = DOCS / field / f"{slug}.md"
    if target.exists():
        print(f"ERROR: '{target}' already exists — duplicate slug. Not writing.",
              file=sys.stderr)
        return 1

    tmpl = TEMPLATES / f"{kind}.md"
    if not tmpl.exists():
        print(f"ERROR: template {tmpl.name} missing", file=sys.stderr)
        return 1

    today = date.today().isoformat()
    text = tmpl.read_text(encoding="utf-8")
    text = (text.replace("{{TITLE}}", title)
                .replace("{{TYPE}}", kind)
                .replace("{{FIELD}}", field)
                .replace("{{SLUG}}", slug)
                .replace("{{DATE}}", today))

    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8")
    print(f"Created {target.relative_to(ROOT)}")
    print(f"Type={kind} field={field} slug={slug}")
    return 0


if __name__ == "__main__":
    sys.exit(main())