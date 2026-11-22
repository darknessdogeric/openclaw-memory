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
  echo "Usage: run_reference_pack.sh <plan.json> <outdir> [resolution] [aspect_ratio] [end_slide] [extra args...]"
  echo "Default behavior: generate slides 1 through 3 with max-workers=1 for sample review."
  exit 0
fi

if [[ $# -lt 2 ]]; then
  echo "Usage: run_reference_pack.sh <plan.json> <outdir> [resolution] [aspect_ratio] [end_slide] [extra args...]"
  exit 1
fi

PLAN="$1"
OUTDIR="$2"
RESOLUTION="${3:-2k}"
ASPECT_RATIO="${4:-16:9}"
END_SLIDE="${5:-3}"
EXTRA_ARGS=()
if [[ $# -gt 5 ]]; then
  EXTRA_ARGS=("${@:6}")
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GENERATOR="$SCRIPT_DIR/generate_from_plan.py"

if [[ ! -f "$GENERATOR" ]]; then
  echo "Generator script not found: $GENERATOR"
  exit 1
fi

"$PY" "$GENERATOR" \
  --plan "$PLAN" \
  --outdir "$OUTDIR" \
  --resolution "$RESOLUTION" \
  --aspect-ratio "$ASPECT_RATIO" \
  --max-workers 1 \
  --start-slide 1 \
  --end-slide "$END_SLIDE" \
  "${EXTRA_ARGS[@]}"
