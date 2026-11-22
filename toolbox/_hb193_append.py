"""
R-NEW-V2 safe append for HB #193
Reads content from file, appends to memory/2026-07-15.md with utf-8 encoding.
"""
from pathlib import Path

target = Path(r"D:\B166ER-OpenClaw\workspace\memory\2026-07-15.md")
content_file = Path(r"D:\B166ER-OpenClaw\workspace\toolbox\_hb193_content.txt")

# Pre-stat check (R-NEW-V2: confirm target exists & non-empty before write)
size_before = target.stat().st_size
print(f"[PRE-STAT] {target.name} size before: {size_before} bytes")

if size_before < 1000:
    print(f"[ERROR] target too small, something wrong. Aborting.")
    raise SystemExit(1)

# Read content (utf-8, mode='r' default)
content = content_file.read_text(encoding='utf-8')
print(f"[CONTENT] read {len(content)} chars from temp file")

# Append (mode='a' = append-only, cannot overwrite)
with target.open('a', encoding='utf-8') as f:
    written = f.write(content)

size_after = target.stat().st_size
print(f"[POST-STAT] {target.name} size after: {size_after} bytes (delta: +{size_after - size_before})")
print(f"[OK] HB #193 appended successfully. R-NEW-V2 compliant.")
