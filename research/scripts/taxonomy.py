"""PartlyGood taxonomy loader and validator.

Resolves and validates topic ids, field ids, pillar ids, content types, and
editorial stages against the canonical taxonomy file.

Pure stdlib. Usage:
    from taxonomy import Taxonomy
    tax = Taxonomy()  # or Taxonomy(path=...)
    tax.validate_topics(["ops.procurement", "ai.automation"])   # raises ValueError
    tax.topics(), tax.fields(), tax.pillars()
"""

import json
import os

_TAXONOMY_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "taxonomy", "taxonomy-v1.json"
)


class Taxonomy:
    def __init__(self, path=None):
        self.path = path or _TAXONOMY_PATH
        with open(self.path, "r", encoding="utf-8") as fh:
            self.data = json.load(fh)
        self._fields = {f["id"]: f for f in self.data["fields"]}
        self._pillars = {p["id"]: p for p in self.data["pillars"]}
        self._topics = set(self.data["topics"])
        self._content_types = {c["id"]: c for c in self.data["content_types"]}
        self._stages = set(self.data["editorial_stages"])

    def fields(self):
        return self._fields

    def pillars(self):
        return self._pillars

    def topics(self):
        return self._topics

    def content_types(self):
        return self._content_types

    def stages(self):
        return self._stages

    def validate_topics(self, topic_ids, where="front matter"):
        bad = [t for t in topic_ids if t not in self._topics]
        if bad:
            raise ValueError(
                "Unknown topic id(s) in %s: %s (see taxonomy-v1.json)" % (where, ", ".join(sorted(bad)))
            )
        return True

    def validate_fields(self, field_ids, where="front matter"):
        bad = [f for f in field_ids if f not in self._fields]
        if bad:
            raise ValueError(
                "Unknown field id(s) in %s: %s" % (where, ", ".join(sorted(bad)))
            )
        return True

    def validate_pillars(self, pillar_ids, where="front matter"):
        bad = [p for p in pillar_ids if p not in self._pillars]
        if bad:
            raise ValueError(
                "Unknown pillar id(s) in %s: %s" % (where, ", ".join(sorted(bad)))
            )
        return True

    def validate_stage(self, stage, where="front matter"):
        if stage not in self._stages:
            raise ValueError("Unknown editorial stage %r in %s" % (stage, where))
        return True

    def validate_content_type(self, ctype, where="front matter"):
        if ctype not in self._content_types:
            raise ValueError("Unknown content type %r in %s" % (ctype, where))
        return True


if __name__ == "__main__":
    import sys

    tax = Taxonomy()
    try:
        tax.validate_topics(sys.argv[1:])
        print("OK: %d topics valid" % len(sys.argv[1:]))
    except ValueError as exc:
        print("INVALID:", exc)
        sys.exit(1)