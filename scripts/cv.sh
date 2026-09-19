#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
if [[ "${1:-}" == setup ]]; then
  python3 -m venv .cache/pdf-venv
  exec .cache/pdf-venv/bin/python -m pip install -r requirements-pdf.txt
fi
if [[ -x .cache/pdf-venv/bin/python ]]; then
  exec .cache/pdf-venv/bin/python scripts/prepare_cv.py
fi
# Manual mode only needs the Python standard library.
exec python3 scripts/prepare_cv.py
