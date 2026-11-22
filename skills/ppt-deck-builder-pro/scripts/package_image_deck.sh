#!/usr/bin/env bash
# Portable python resolver.
# NOTE: `command -v python3` SUCCEEDS on Windows Git Bash even when it points at
# the Microsoft Store stub (WindowsApps/python3), which exits silently with code 49.
# So each candidate must be proven runnable (`--version` actually works) before use.
PY=""
for _pycand in python3 python; do
  if command -v "$_pycand" >/dev/null 2>&1 && "$_pycand" --version >/dev/null 2>&1; then
    PY="$(command -v "$_pycand")"
    break
  fi
done
if [[ -z "$PY" ]]; then
  echo "ERROR: no working python found (tried python3, python)" >&2
  exit 127
fi

set -euo pipefail

if [[ "${1:-}" == "--help" ]] || [[ "${1:-}" == "-h" ]]; then
  echo "Usage: package_image_deck.sh <images_dir> <output.pptx> [plan.json]"
  echo "If plan.json is provided, the script validates that all expected slide images exist first."
  exit 0
fi

if [[ $# -lt 2 ]]; then
  echo "Usage: package_image_deck.sh <images_dir> <output.pptx> [plan.json]"
  exit 1
fi

INDIR="$1"
OUTFILE="$2"
PLAN="${3:-}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PACKAGER="$SCRIPT_DIR/build_pptx_from_images.py"
VALIDATOR="$SCRIPT_DIR/validate_generated_deck.py"

if [[ ! -f "$PACKAGER" ]]; then
  echo "Packager script not found: $PACKAGER"
  exit 1
fi

if [[ -n "$PLAN" ]]; then
  if [[ ! -f "$VALIDATOR" ]]; then
    echo "Validator script not found: $VALIDATOR"
    exit 1
  fi
  "$PY" "$VALIDATOR" --plan "$PLAN" --indir "$INDIR"
fi

"$PY" "$PACKAGER" --indir "$INDIR" --out "$OUTFILE"
