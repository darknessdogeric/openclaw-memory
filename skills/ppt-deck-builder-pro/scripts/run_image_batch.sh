#!/usr/bin/env bash
set -euo pipefail

if [[ "${1:-}" == "--help" ]] || [[ "${1:-}" == "-h" ]]; then
  echo "Usage: run_image_batch.sh <plan.json> <outdir> [resolution] [aspect_ratio] [max_workers] [extra args...]"
  echo "Extra args commonly include: --provider, --provider-command, --max-retries, --max-poll-seconds, --overwrite, --start-slide, --end-slide"
  echo "Tip: use run_reference_pack.sh first when testing a new deck or provider."
  exit 0
fi

if [[ $# -lt 2 ]]; then
  echo "Usage: run_image_batch.sh <plan.json> <outdir> [resolution] [aspect_ratio] [max_workers] [extra args...]"
  exit 1
fi

PLAN="$1"
OUTDIR="$2"
RESOLUTION="${3:-4k}"
ASPECT_RATIO="${4:-16:9}"
MAX_WORKERS="${5:-3}"
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
  --max-workers "$MAX_WORKERS" \
  "${EXTRA_ARGS[@]}"
