#!/usr/bin/env python3
"""Remove duplicate HB #2271 entry from HEARTBEAT.md."""
from pathlib import Path
HB = Path(r"D:\B166ER-OpenClaw\workspace\HEARTBEAT.md")

text = HB.read_text(encoding="utf-8")
marker = "## HB #2271 (2026-08-03T21:17 GMT+8 cron-event, OpenClaw heartbeat poll)"
positions = []
i = 0
while True:
    p = text.find(marker, i)
    if p < 0:
        break
    positions.append(p)
    i = p + 1
print(f"Found {len(positions)} occurrences at offsets: {positions}")

if len(positions) == 2:
    # Remove the SECOND occurrence (and the leading newline before it if any)
    second = positions[1]
    # Find what comes before second occurrence (newline)
    new_text = text[:second]
    # Ensure trailing newline kept
    if not new_text.endswith("\n"):
        new_text += "\n"
    HB.write_text(new_text, encoding="utf-8")
    size_after = HB.stat().st_size
    print(f"Removed duplicate. File size: {size_after} bytes (was {len(text.encode('utf-8'))})")
elif len(positions) == 1:
    print("Only one occurrence. No dedupe needed.")
else:
    print(f"Unexpected count: {len(positions)}. Manual review needed.")
