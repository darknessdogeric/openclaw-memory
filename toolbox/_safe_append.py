"""
safe_append.py — R-NEW-V2 compliant append tool
Forces Add-Content semantics. Rejects write-overwrite on non-empty files > 1KB.
"""
import sys
from pathlib import Path

target = Path(sys.argv[1])
content = sys.stdin.read() if not sys.stdin.isatty() else sys.argv[2] if len(sys.argv) > 2 else ""

# Pre-check: refuse write-overwrite on non-empty files > 1KB
if target.exists():
    size = target.stat().st_size
    if size > 1024:
        print(f"[SAFE_APPEND] BLOCKED: {target} exists, size={size} bytes > 1024", file=sys.stderr)
        print(f"[SAFE_APPEND] Use edit() for targeted changes, not full rewrite.", file=sys.stderr)
        sys.exit(1)

# Append
with target.open('a', encoding='utf-8') as f:
    f.write(content)

print(f"[SAFE_APPEND] OK: appended {len(content)} bytes to {target} (now {target.stat().st_size} bytes)")
