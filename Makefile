# PartlyGood publication — editorial pipeline entry points
.PHONY: check validate quality build publish serve clean report

VENV ?= .venv
PY := $(VENV)/Scripts/python.exe
ifeq ($(OS),Windows_NT)
PY := $(VENV)/Scripts/python.exe
else
PY := $(VENV)/bin/python
endif

# Full gate: validate + quality + strict build (what CI runs)
check: validate quality build

validate:
	$(PY) scripts/validate_content.py --strict

quality:
	$(PY) scripts/quality_checks.py --all

report:
	$(PY) scripts/quality_report.py --out report.json

# Strict production build; fails on any warning.
build:
	$(PY) -m mkdocs build --strict

publish: check
	@echo "Publish gate passed. Deploy target not configured yet — see issue PAR-3."

# Local preview
serve:
	$(PY) -m mkdocs serve

clean:
	rm -rf site report.json