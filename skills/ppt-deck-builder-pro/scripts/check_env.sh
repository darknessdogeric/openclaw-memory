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

"$PY" --version
"$PY" - <<'PY'
mods=[('requests','requests'),('pptx','python-pptx')]
missing=[]
for mod,pkg in mods:
    try:
        __import__(mod)
        print(f'OK {pkg}')
    except Exception:
        missing.append(pkg)
if missing:
    print('Missing packages:', ', '.join(missing))
    raise SystemExit(1)
PY

PROVIDER="${PPT_IMAGE_PROVIDER:-runninghub_g31}"
echo "PPT_IMAGE_PROVIDER=$PROVIDER"

if [[ -n "${PPT_IMAGE_PROVIDER_COMMAND:-}" ]]; then
  echo "PPT_IMAGE_PROVIDER_COMMAND is set"
else
  echo "PPT_IMAGE_PROVIDER_COMMAND is not set"
fi

case "$PROVIDER" in
  runninghub|runninghub_g31)
    if [[ -n "${RUNNINGHUB_API_KEY:-}" ]]; then
      echo "RUNNINGHUB_API_KEY is set"
    else
      echo "RUNNINGHUB_API_KEY is not set"
    fi
    ;;
  command|custom-command)
    echo "Command provider selected; verify the adapter command path is correct"
    ;;
  *)
    echo "Custom provider selected; verify provider-specific settings manually"
    ;;
esac
