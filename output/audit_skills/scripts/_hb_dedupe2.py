#!/usr/bin/env python3
"""Remove duplicate HB #2271 entry from HEARTBEAT.md (binary mode)."""
from pathlib import Path
HB = Path(r"D:\B166ER-OpenClaw\workspace\HEARTBEAT.md")

t = HB.read_bytes()
marker = b"## HB #2271 (2026-08-03T21:17"
positions = []
idx = 0
while True:
    p = t.find(marker, idx)
    if p < 0:
        break
    positions.append(p)
    idx = p + 1
print(f"Found {len(positions)} positions: {positions}")

if len(positions) == 2:
    new_t = t[:positions[1]]
    if not new_t.endswith(b"\n"):
        new_t += b"\n"
    HB.write_bytes(new_t)
    print(f"Removed duplicate. New size: {len(new_t)} bytes (was {len(t)}, delta={len(new_t)-len(t)})")
elif len(positions) == 1:
    print("Only one occurrence. No dedupe needed.")
else:
    print(f"Unexpected count: {len(positions)}. Manual review needed.")
