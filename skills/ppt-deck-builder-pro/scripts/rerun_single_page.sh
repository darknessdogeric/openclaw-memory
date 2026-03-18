#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 3 ]]; then
  echo "Usage: rerun_single_page.sh <plan.json> <outdir> <slide_number> [resolution] [aspect_ratio] [extra args...]"
  exit 1
fi

PLAN="$1"
OUTDIR="$2"
SLIDE_NUMBER="$3"
RESOLUTION="${4:-4k}"
ASPECT_RATIO="${5:-16:9}"
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

python3 "$GENERATOR" \
  --plan "$PLAN" \
  --outdir "$OUTDIR" \
  --resolution "$RESOLUTION" \
  --aspect-ratio "$ASPECT_RATIO" \
  --max-workers 1 \
  --overwrite \
  --start-slide "$SLIDE_NUMBER" \
  --end-slide "$SLIDE_NUMBER" \
  "${EXTRA_ARGS[@]}"
